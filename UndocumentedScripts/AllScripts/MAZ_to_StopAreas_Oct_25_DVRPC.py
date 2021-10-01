import os
import numpy
import time
import csv
import pandas
csv.field_size_limit(1000000000)

# maz to stop area access functions | Chetan Joshi, Portland OR 6/19/2018
# Ben.Stabler@rsginc.com, 10/18/19

#-----------------------------------------------------INPUTS-----------------------------------------------------------#
PRIO = 20480
POICatNo = 10
Tsys = 'Bik' #maz to sa access network mode
Get_CutOff = {('Bus',1): 0.25,
    ('Bus',2): 0.25,
    ('Bus',3): 0.50,
    ('Bus',4): 0.75,
    ('Bus',5): 1.50,
    ('Bus',6): 1.50,
    ('Trl',1): 0.25,
    ('Trl',2): 0.25,
    ('Trl',3): 0.50,
    ('Trl',4): 0.75,
    ('Trl',5): 1.50,
    ('Trl',6): 1.50,
    ('Rail',1): 1.00,
    ('Rail',2): 1.00,
    ('Rail',3): 1.50,
    ('Rail',4): 1.50,
    ('Rail',5): 1.50,
    ('Rail',6): 1.50,
    ('Pat',1): 1.00,
    ('Pat',2): 1.00,
    ('Pat',3): 1.50,
    ('Pat',4): 1.50,
    ('Pat',5): 1.50,
    ('Pat',6): 1.50,
    ('Sub',1): 1.00,
    ('Sub',2): 1.00,
    ('Sub',3): 1.00,
    ('Sub',4): 1.50, # NHSL, BSL express, spur, end of line stops
    ('Sub',5): 1.50,
    ('Sub',6): 1.50,
    ('LRT',1): 1.00,
    ('LRT',2): 1.00,
    ('LRT',3): 1.00, # Riverline, 101/102 in urban area/two ends
    ('LRT',4): 1.50, # Riverline, 101/102 in suburban
    ('LRT',5): 1.50,
    ('LRT',6): 1.50}

#-----------------------------------------------------------------------------------------------------------------------

ver_dir = os.path.dirname(Visum.UserPreferences.DocumentName) # for Visum 12.5, Visum.Options.DocumentName

def maz_to_node(POICatNo, fn):
    Visum.Log(PRIO,'Joining MAZ to Node...')
    POILayer = Visum.Net.POICategories.ItemByKey(POICatNo).POIs
    Visum.Filters.InitAll()
    linkfilter = Visum.Filters.LinkFilter()
    linkfilter.AddCondition("OP_NONE", False, "TSysSet", "ContainsOneOf", "Bik")
    nodefilter = Visum.Filters.NodeFilter()
    nodefilter.AddCondition("OP_NONE", False, "CountActive:OutLinks", "GreaterEqualVal", 1)
    nodefilter.AddCondition("OP_OR", False, "CountActive:InLinks", "GreaterEqualVal", 1)

    NodeNoXY = numpy.array(Visum.Net.Nodes.GetMultipleAttributes(["NO","XCOORD","YCOORD"], True))

    outf = open(fn, 'wb')
    writer = csv.writer(outf, delimiter = ';')
    writer.writerows([['$VISION'],
                      ['$VERSION:VERSNR','FILETYPE','LANGUAGE','UNIT'],
                      [9.000000,'Net','ENG','MI'],
                      ['$POITONODE:POICATNO','POINO','NODENO','TSYSSET']])
    cnt = 1
    for POI in POILayer:
        dis = numpy.argmin(numpy.power(POI.AttValue("XCOORD") - NodeNoXY[:,1], 2) + numpy.power(POI.AttValue("YCOORD") - NodeNoXY[:,2], 2))
        writer.writerow([POICatNo,POI.AttValue("NO"),NodeNoXY[dis][0],'Ped,Bik'])
        cnt+=1
        if cnt%1000 == 0:
            Visum.Log(PRIO,'Processed: '+str(cnt) + ' mazs')
    outf.close()
    netAddPara = Visum.CreateAddNetReadController
    netAddPara.SetWhatToDo("POITONODE", 4)
    Visum.LoadNet(fn, 1, None, netAddPara)
    Visum.Log(PRIO,'Finished joining MAZ to Node')

def sa_to_node(sx, sy):
    Visum.Filters.InitAll()
    linkfilter = Visum.Filters.LinkFilter()
    linkfilter.AddCondition("OP_NONE", False, "TSysSet", "ContainsOneOf", "Bik")
    nodefilter = Visum.Filters.NodeFilter()
    nodefilter.AddCondition("OP_NONE", False, "CountActive:OutLinks", "GreaterEqualVal", 1)
    nodefilter.AddCondition("OP_OR", False, "CountActive:InLinks", "GreaterEqualVal", 1)
    NodeNoXY = numpy.array(Visum.Net.Nodes.GetMultipleAttributes(["NO","XCOORD","YCOORD"], True))
    dis = numpy.argmin(numpy.power(sx - NodeNoXY[:,1], 2) + numpy.power(sy - NodeNoXY[:,2], 2))
    Visum.Filters.InitAll()
    return(NodeNoXY[dis][0])


def remove_poi_alloc(POICatNo):
    POILayer = Visum.Net.POICategories.ItemByKey(POICatNo).POIs
    Visum.Graphic.StopDrawing = True
    for POI in POILayer:
        POI.POIToNodeItems.RemoveAll()
    Visum.Graphic.StopDrawing = False
    Visum.Graphic.Redraw()


def update_sa_index(fn):
    sadata = Visum.Net.StopAreas.GetMultipleAttributes(["NO", "XCOORD", "YCOORD"])
    outf = open(fn, 'wb')
    writer = csv.writer(outf, delimiter = '\t')
    writer.writerow(['Zone_id','Zone_ordinal','Dest_eligible','External','xcoord','ycoord'])
    ix = 1
    for no, x, y in sadata:
        writer.writerow([int(no), ix, 1, 0, round(x,3), round(y,3)])
        ix+=1
    outf.close()

def sa_node_isoc(fn, Tsys, Get_CutOff, POICatNo):
    t0 = time.time()
    Visum.Log(PRIO,"Isoschrone calculation started: "+str(t0))
    Visum.Filters.InitAll() #Clear all filters
    poicat = Visum.Net.POICategories.ItemByKey(POICatNo)
    external_zones_start_at = 50000 #external nodes are TAZ_P > 50000
    maznodes = numpy.array(poicat.POIs.GetMultipleAttributes(['Max:Nodes\\No', 'XCoord', 'YCoord', 'TAZ_P', "NO"]))
    for i in range(len(maznodes)):
        maznodes[i][3] = (maznodes[i][3] >= external_zones_start_at)

    nodefilter = Visum.Filters.NodeFilter() #Init filters on nodes
    nodefilter.Init()
    nodefilter.UseFilter = True #Set node filter: only nodes with IsocTimePrT <= maxdistance and connected to maz are active
    nodefilter.AddCondition("OP_NONE", False, "Count:POIs_"+str(POICatNo), "GreaterEqualVal", 1)

    #every stop area needs an access mode network node
    #for rail, pat, sub, use stop's bus node instead
    #assign nearest network node when stop area node is the same as network node
    stop_area_data = numpy.array(Visum.Net.StopAreas.GetMultipleAttributes(["NO","NODENO","XCOORD","YCOORD", "AREATYPE","MODE","STOP\CONCATENATE:STOPAREAS\MODE","STOP\CONCATENATE:STOPAREAS\NODENO","ADDVAL3"]))
    for i in range(len(stop_area_data)):
        mode = stop_area_data[i][5]
        stop_modes = stop_area_data[i][6]
        stop_nodes = stop_area_data[i][7]
        
        # if mode in ["Rail","Pat","Sub","LRT"] and "Bus" in stop_modes:
            # stop_area_data[i][1] = stop_nodes.split(",")[stop_modes.split(',').index("Bus")]
            # Visum.Log(PRIO,"Set stop area node: "+str(stop_area_data[i][0])+" : " +stop_area_data[i][1])
            
        if mode in ["Rail","Pat","Sub","LRT"]:
            stop_area_data[i][1] = sa_to_node(float(stop_area_data[i][2]), float(stop_area_data[i][3]))
            Visum.Log(PRIO,"Set stop area node: "+str(stop_area_data[i][0])+" : " +stop_area_data[i][1])
            
        sano = int(float(stop_area_data[i][0]))        
        node = int(float(stop_area_data[i][1]))
        
        # if sano == node:
            # stop_area_data[i][1] = sa_to_node(float(stop_area_data[i][2]), float(stop_area_data[i][3]))
            # Visum.Log(PRIO,"Set stop area node: "+str(stop_area_data[i][0])+" : " +stop_area_data[i][1])

        # node = int(float(stop_area_data[i][1]))
                
        if node == 0:
            stop_area_data[i][1] = sa_to_node(float(stop_area_data[i][2]), float(stop_area_data[i][3]))
            Visum.Log(PRIO,"Set stop area node: "+str(stop_area_data[i][0])+" : " +stop_area_data[i][1])
        
        node = int(float(stop_area_data[i][1]))

        #add stop area to node distance 
        sx = float(stop_area_data[i][2])
        sy = float(stop_area_data[i][3])
        nx = Visum.Net.Nodes.ItemByKey(stop_area_data[i][1]).AttValue("XCOORD")
        ny = Visum.Net.Nodes.ItemByKey(stop_area_data[i][1]).AttValue("YCOORD")
        dis = numpy.sqrt(numpy.power(sx - nx, 2) + numpy.power(sy - ny, 2))
        stop_area_data[i][8] = dis

    Visum.Graphic.StopDrawing = True
    csvfile = open(fn, 'wb')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['StopAreaID','NodeID','Distance'])
    Visum.Analysis.Isochrones.Clear() #Clear any existing isochrones
    SearchCrit = 3 #Search criterion (1 = time, 3 = distance)
    i = 0
    Visum.Log(PRIO,Get_CutOff)
    
    #loop through stop areas
    for sano, node, sx, sy, atype, mode, stop_modes, stop_nodes, dist in stop_area_data:
        i+=1
        sano = int(float(sano))
        node = int(float(node))
        sx = float(sx)
        sy = float(sy)
        atype = int(float(atype))
        dist = float(dist)
        Visum.Log(PRIO,"Isoschrone calculation stop area and node: "+str(sano)+" "+str(node))

        MaxCost = Get_CutOff[(mode, atype)] * 1602 #Isoc cutoff in meters
        Node = Visum.Net.Nodes.ItemByKey(node)
        IsocNodes = Visum.CreateNetElements()
        IsocNodes.Add(Node)
        Visum.Analysis.Isochrones.ExecutePrT(IsocNodes, Tsys, SearchCrit, MaxCost)
        IsocVal = numpy.array(Visum.Net.Nodes.GetMultiAttValues("IsocTimePrT", True)).astype('int')[:,1]
        DestID  = numpy.array(Visum.Net.Nodes.GetMultiAttValues("No", True)).astype('int')[:,1]
        DestID = numpy.compress(IsocVal < MaxCost, DestID) #, axis = 0)
        IsocVal = numpy.compress(IsocVal < MaxCost, IsocVal)
        IsocVal = IsocVal * 3.28084 #convert meter to ft
        IsocVal = IsocVal + dist #add stop area to network node distance 
        OrigID = numpy.zeros(len(DestID)).astype('int')+int(sano)
        writer.writerows(zip(OrigID,DestID,IsocVal))
        csvfile.flush()
        Visum.Analysis.Isochrones.Clear()

    csvfile.close()
    Visum.Graphic.StopDrawing = False
    Visum.Graphic.Redraw()
    Visum.Log(PRIO,"Finished calculating: "+str(i)+" isochrones")
    Visum.Log(PRIO,"Time taken: "+str(int(time.time()-t0)))


def skim_maz_sa(POICatNo, fn_sa_to_maznode, fn_maz_to_sa_skim):
    #Load sa -> maz_node lookup table
    #sa to maz_node isochrone
    csvfile = open(fn_sa_to_maznode, 'rb')
    reader = csv.reader(csvfile, delimiter=',')
    print reader.next()
    Visum.Log(PRIO,'Building maz to sa lookup.')
    maz_to_sa = {}
    for row in reader:
        dat = map(float, row)
        if maz_to_sa.has_key(dat[1]):
            maz_to_sa[dat[1]].append([dat[0] ,dat[2]])
        else:
            maz_to_sa[dat[1]] = [[dat[0],dat[2]]]
    csvfile.close()
    Visum.Log(PRIO,'Finished building lookup.')
    Visum.Log(PRIO,"Skim calculation started...")
    Visum.Log(PRIO,'Add MAZ to node distance as well')
    Visum.Filters.InitAll() #Clear all filters
    poicat = Visum.Net.POICategories.ItemByKey(POICatNo)
    maznodes = poicat.POIs.GetMultipleAttributes(['ID','Max:Nodes\\No', 'XCoord', 'YCoord', "MAX:NODES\XCOORD", "MAX:NODES\YCOORD"])
    Visum.Graphic.StopDrawing = True
    outf = open(fn_maz_to_sa_skim, 'wb')
    writer = csv.writer(outf, delimiter = ' ')
    writer.writerow(['zoneid', 'stopareaid', 'distance'])
    for mazid, nodeno, mazx, mazy, nodex, nodey in maznodes:
        if nodeno > 0 and maz_to_sa.has_key(nodeno):
            stop_areas = maz_to_sa[nodeno]
            #add maz to node distance
            maz_to_node_dist = numpy.sqrt(numpy.power(mazx - nodex, 2) + numpy.power(mazy - nodey, 2))
            for sano, dis in stop_areas:
                total_dis = dis + maz_to_node_dist
                writer.writerow([int(mazid), int(sano), total_dis])
    outf.close()
    Visum.Log(PRIO,"Skim calculation finished!")
    Visum.Graphic.StopDrawing = False
    Visum.Graphic.Redraw()

def sort_maz_sa(fn_maz_to_sa_skim):
    Visum.Log(PRIO,"Sort by distance for DaySim")
    maz_sa = pandas.read_csv(fn_maz_to_sa_skim, sep=" ")
    maz_sa = maz_sa.sort_values(["zoneid","distance"])
    maz_sa["distance"] = maz_sa["distance"].round(5)
    maz_sa.to_csv(fn_maz_to_sa_skim, sep=" ", index=False, float_format='%.5f')



#Joins poi - maz to node | run only if nodes are not allocated to pois
#fn_poi_to_node =  os.path.join(ver_dir,r'dvrpc_poi_to_node.net')
#maz_to_node(POICatNo, fn_poi_to_node)

#Updates the stop area index file for Daysim
#fn_sa_ix = os.path.join(ver_dir,r'_DVRPC_stoparea_indexes_withxy.dat')
#update_sa_index(fn_sa_ix)

#sa to maz_node isochrone
fn_sa_to_maznode = os.path.join(ver_dir, r'StopArea_To_Node_11k_test.csv')
#sa_node_isoc(fn_sa_to_maznode, Tsys, Get_CutOff, POICatNo)

#Runs the maz to stop area skim, add maz to node distance, and write a space delimited file sorted by zone and distance 
fn_maz_to_sa_skim = r'D:\TIM3\maz2sa.dat' #os.path.join(ver_dir,r'microzonetostopareadistance.dat')
skim_maz_sa(POICatNo, fn_sa_to_maznode, fn_maz_to_sa_skim)
sort_maz_sa(fn_maz_to_sa_skim)
