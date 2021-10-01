import VisumPy.helpers as h
import numpy

ActPairs = [ap.AttValue("CODE") for ap in Visum.Net.ActPairs.GetAll]
for ActPair in ActPairs:
    productions = numpy.array(h.GetMulti(Visum.Net.Zones, 'Production(' + ActPair + '_NT)'))
    attractions = numpy.array(h.GetMulti(Visum.Net.Zones, 'Attraction(' + ActPair + '_NT)'))
    h.SetMulti(Visum.Net.Zones, 'Production(' + ActPair + '_EV)', 0.5*productions)
    h.SetMulti(Visum.Net.Zones, 'Production(' + ActPair + '_NT)', 0.5*productions)
    h.SetMulti(Visum.Net.Zones, 'Attraction(' + ActPair + '_EV)', 0.5*attractions)
    h.SetMulti(Visum.Net.Zones, 'Attraction(' + ActPair + '_NT)', 0.5*attractions)