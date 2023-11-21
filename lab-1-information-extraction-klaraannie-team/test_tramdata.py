import unittest
from tramdata import *
from haversine import haversine

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_line_exist(self):
        with open("data/tramlines.txt", 'r') as lines:
            for line in lines:
                line = line.strip()

                if line and line[0].isdigit():
                    tram_number = line.split(":")[0]

                    self.assertIn(tram_number,self.linedict, msg= line + 'not in linedict')

    def test_stop_same(self):

        with open("data/tramlines.txt", 'r') as lines:
            for line in lines:
                line = line.strip()

                if line and line[0].isalpha():
                    tram_names = " ".join(line.split(" ")[:-1]).strip()

                    self.assertIn(tram_names, self.stopdict, msg= line + 'not in linedict')

    def test_same_time(self):
        stop1 = "Chalmers"
        stop2 = "Kapellplatsen"
        line = "1"
        distance1 = time_between_stops(self.linedict,self.timedict,line,stop1,stop2)
        distance2 = time_between_stops(self.linedict, self.timedict,line,stop2,stop1)

        self.assertEqual(distance1,distance2, msg="is equal")
        # have done different tests with different stops

    def test_distance(self):
        stop1 = "Östra Sjukhuset"
        stop2 = "Saltholmen"
        #have done different tests with different stops
        distance = float(distance_between_stops(self.stopdict,stop1,stop2))
        self.assertGreater(20.0, distance)



if __name__ == '__main__':
    unittest.main()