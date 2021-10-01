#-----------------------------------------------------------------------------------------------------#
# Name:        Calc node skims
# Purpose:     Node to node travel times within given distance for maz to maz distance for DaySim
# Note:        The logger is for Visum 17 - this should be changed to Visum.WriteToTrace if Visum 16
# Author:      Chetan Joshi, Portland OR
# Created:     06/19/2018
# Updates:     09/17/18 Ben Stabler, ben.stabler@rsginc.com, Write additional DaySim format files
#              W?T - wtf is this two space indent JS bullshit for the run_daysim_files?
#-----------------------------------------------------------------------------------------------------#

import numpy
import scipy.sparse
import time
import struct
import csv
import pandas as pd
import os

csv.field_size_limit(1000000000)
PRIO = 20480
#-----------------------user input--------------------------------------------------------------------#
poi_lookup = dict(Visum.Net.POICategories.GetMultipleAttributes(['name','no']))
if poi_lookup.has_key('MAZ'):
    POICatNo = poi_lookup['MAZ']
elif poi_lookup.has_key('maz'):
    POICatNo = poi_lookup['maz']
else:
    Visum.Log(PRIO, 'MAZ key not found!')

node_skimfname1 = r"node_distance_dvrpc_tst1.csv"
node_skimfname2 = r"node_distance_dvrpc_tst2.bin"
maz_map_fname = r"maz_to_node.csv"

ParcelNode_fname = r"corr_mznode.dat"
NodeDistances_fname = r"nodeskims_visum_text.dat"
NodeIndex_fname = r"nodeskims_visum_index.dat"

#------------------------functions--------------------------------------------------------------------#

def get_network_visum(cost_attr, scale = 5280, tsysset = ''):
    '''
    Returns a sparse matrix where the rows are the origin nodes, the columns are the destination nodes, and the entries are the length in feet
    '''
    numnodes = Visum.Net.Nodes.Count
    nodeids = numpy.array(Visum.Net.Nodes.GetMultiAttValues("NO", False))[:,1]
    nodeix = dict(zip(nodeids, range(numnodes)))
    linkdata = Visum.Net.Links.GetMultipleAttributes(["FromNodeNo","ToNodeNo","TSysSet",cost_attr])
    i = []
    j = []
    data = []
    for fnode, tnode, tsys, cost in linkdata:
        if tsysset == '':
            i.append(long(nodeix[fnode]))
            j.append(long(nodeix[tnode]))
            data.append(long(cost*scale))
        else:
            if tsys.find(tsysset) >= 0:
                i.append(long(nodeix[fnode]))
                j.append(long(nodeix[tnode]))
                data.append(long(cost*scale))

    network = scipy.sparse.csr_matrix((data, (i,j)), shape=(numnodes, numnodes), dtype='int')
    return network

def run_graph_search(poi_catno, maz_map_fname, node_skimfname, exportfmt = 1, cutoff = 15840, tsysset = ''):
    Visum.Log(PRIO, 'start...')
    tstart = time.time()
    Visum.Log(PRIO, 'init filters...')
    Visum.Filters.InitAll()
    nodefilter = Visum.Filters.NodeFilter()
    nodefilter.Init()
    nodefilter.UseFilter = True
    nodefilter.AddCondition("OP_NONE", False, "Count:POIs_"+str(int(poi_catno)), "GreaterEqualVal", 1) #Filters out any node that isn't attached to a MAZ

    Visum.Log(PRIO, 'getting network...')
    network = get_network_visum("length", tsysset = '')
    Visum.Log(PRIO, 'done!')

    origins = numpy.array(Visum.Net.Nodes.GetMultiAttValues("NO", True), dtype='int')
    dests = numpy.array(Visum.Net.Nodes.GetMultiAttValues("NO", False), dtype='int')[:,1]
    fo = open(node_skimfname, 'wb')
    if exportfmt == 1:
        writer = csv.writer(fo, delimiter = ',')

    cnt = 1
    Visum.Log(PRIO, 'running search...')
    for i, o in origins:
        result = scipy.sparse.csgraph.dijkstra(network, indices=i-1, limit=cutoff) #Perform's Djikstra's algorithm to get the shortest path to each d node from o
        valid_dests = dests[result <> numpy.inf] #Filter out paths that have infinite length
        result = result[result <> numpy.inf]
        if exportfmt == 1:
            writer.writerows(zip(numpy.repeat(o, len(result)), valid_dests, result))
        else:
            for d, v in zip(valid_dests, result):
                data = struct.pack('iii', o, d, v)
                fo.write(data)
        cnt+=1
        if cnt%10000 == 0:
            Visum.Log(PRIO, 'finished: ' + str(cnt) + ' origins')

    fo.close()
    Visum.Log(PRIO, 'clear temp data and export maz to node mapping...')
    POILayer = Visum.Net.POICategories.ItemByKey(poi_catno).POIs
    fo = open(maz_map_fname, 'wb')
    writer = csv.writer(fo, delimiter = ',')
    writer.writerows(POILayer.GetMultipleAttributes(["No", "Max:Nodes\\No"]))
    fo.close()
    del result, network, origins, dests, POILayer
    Visum.Log(PRIO, 'end. time taken: ' +str(time.time()-tstart))

def run_daysim_files(node_skimfname1, maz_map_fname, ParcelNode_fname, NodeDistances_fname, NodeIndex_fname):
    '''
    DaySim input files renumbered to be sequential since DaySim assumes 1toN numbering

    ParcelNode - ParcelNode_fname - corr_mznode.dat - id node_id
    id - The parcel ID number.  This file must have the same number of records as the raw parcel file, with the parcel IDs in the same order.
    node_id - The id of the nearest all-streets network node. This is an integer that does not need to be unique in this file. (Two or more parcels may share the same nearest node.)

    NodeDistances - NodeDistances_fname - nodeskims_visum_text.dat - onode dnode feet
    onode - The ANode ID, from the all-streets network. For efficiency, should be a node present in the ParcelNode file.
    dnode - The BNode ID, from the all-streets network. For efficiency, should be a node present in the ParcelNode file.  The file must be sorted first by ANodeID and then by BNodeID within ANodeID.
    feet - The node-node shortest path distance, in length units (typically feet)

    NodeIndex - NodeIndex_fname - nodeskims_visum_index.dat - node_Id firstrec lastrec
    node_Id - The ANode ID, from the all-streets network. For efficiency, should be a node present in the ParcelNode file.
    firstrec - The position in the NodeDistances file for the first record with ANodeID as the A node
    lastrec - The position in the NodeDistances file for the last record with ANodeID as the A node (LastRecord >= FirstRecord)
    '''

    #read maz to node and add seq id
    maz2node = pd.read_csv(maz_map_fname, header=None)
    maz2node.columns = ["id","visum_node_id"]
    maz2node["id"] = maz2node["id"].astype('int64')
    uniq_visum_nodes = maz2node["visum_node_id"].unique()
    uniq_visum_nodes_seq_ids = range(1, len(uniq_visum_nodes)+1)

    uniq_visum_nodes = pd.DataFrame({"id":uniq_visum_nodes_seq_ids,"visum_node_id":uniq_visum_nodes})
    uniq_visum_nodes["id"] = uniq_visum_nodes["id"].astype('int64')
    uniq_visum_nodes["visum_node_id"] = uniq_visum_nodes["visum_node_id"].astype('int64')
    nodeLookup = uniq_visum_nodes.set_index("visum_node_id", drop=False)
    nodeLookup['onode'] = nodeLookup['id']
    nodeLookup['dnode'] = nodeLookup['id']

    #get new ids
    maz2node["node_id"] = nodeLookup["id"].loc[maz2node["visum_node_id"]].tolist()

    #read distances file and remove records where dest=maz (as opposed to joining node)
    dists = pd.read_csv(node_skimfname1)
    dists.columns = ["visum_onode","visum_dnode","feet"]
    dists = dists[dists["visum_dnode"].isin(maz2node["visum_node_id"])]

    #get seq ids and sort distances
    dists = dists.set_index("visum_onode", drop=False)
    dists = dists.join(nodeLookup['onode'])
    dists = dists.set_index("visum_dnode", drop=False)
    dists = dists.join(nodeLookup['dnode'])
    dists = dists.reset_index()
    dists = dists[["onode","dnode","feet"]]
    dists = dists.sort_values(by=['onode', 'dnode'])
    dists = dists[dists["onode"] != dists["dnode"]]
    dists = dists[dists["onode"].notnull()]
    dists["onode"] = dists["onode"].astype('int64')
    dists["feet"] = dists["feet"].astype('int64')
    dists['seq'] = range(1,len(dists)+1)

    #create node index file
    nodeIndex = pd.DataFrame({"node_Id":nodeLookup["id"]})
    nodeIndex = nodeIndex.set_index("node_Id", drop=False)
    nodeIndex['firstrec'] = dists.groupby("onode").first()["seq"]
    nodeIndex['firstrec'][nodeIndex['firstrec'].isnull()] = 0
    nodeIndex['firstrec'] = nodeIndex['firstrec'].astype('int64')
    nodeIndex['lastrec'] = dists.groupby("onode").last()["seq"]
    nodeIndex['lastrec'][nodeIndex['lastrec'].isnull()] = 0
    nodeIndex['lastrec'] = nodeIndex['lastrec'].astype('int64')

    #write files
    maz2node = maz2node[["id","node_id"]]
    maz2node.to_csv(ParcelNode_fname, sep=" ", index=False)
    dists.to_csv(NodeDistances_fname, sep=" ", index=False)
    nodeIndex.to_csv(NodeIndex_fname, sep=" ", index=False)

#------------------------steps------------------------------------------------------------------------#

#switch to version file location for writing outputs
ver_dir = os.path.dirname(Visum.UserPreferences.DocumentName)
os.chdir(ver_dir)

#exports csv file and includes only links with tsys bik in the search graph
run_graph_search(POICatNo, maz_map_fname, node_skimfname1, exportfmt = 1, cutoff = 15840, tsysset = 'Bik')

#exports binary file and includes only links with tsys bik in the search graph
#run_graph_search(POICatNo, maz_map_fname, node_skimfname2, exportfmt = 2, cutoff = 15840, tsysset = 'Bik')

#exports daysim input files
run_daysim_files(node_skimfname1, maz_map_fname, ParcelNode_fname, NodeDistances_fname, NodeIndex_fname)
