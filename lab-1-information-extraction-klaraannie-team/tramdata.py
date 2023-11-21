import sys
import json
from haversine import haversine


# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = './tramnetwork.json'

def build_tram_stops(jsonobject):
    tram_stops = {}
    for stop_name, stop_info in jsonobject.items():
        lat = float(stop_info["position"][0])
        lon = float(stop_info["position"][1])
        tram_stops[stop_name] = {"lat": lat, "lon": lon}

    return tram_stops


with open("data/tramstops.json", 'r') as infile:
    tram_stop_data = json.load(infile)
    result = build_tram_stops(tram_stop_data)

def build_tram_lines(lines):
    tram_lines = {}
    tram_number = None
    for line in lines:
        line = line.strip()

        if line and line[0].isdigit():
            tram_number = int(line.split(":")[0])
            tram_lines[tram_number] = []

        elif tram_number is not None:
            names_and_times = line.split()
            if line and line[0].isalpha():
                names = " ".join(names_and_times[:-1])
                tram_lines[tram_number].append(names)
    return tram_lines

with open("data/tramlines.txt", 'r') as file:

    build_tram_lines(file)

def time_dictionary(file = "data/tramlines.txt"):
    prev_stop = None
    prev_time = None
    time_dict = {}

    with open(file, 'r') as file:
        file = file.readlines()

        for n, line in enumerate(file):
            line = line.strip()
            n += 1
            if len(line) == 0:
                continue
            elif line[0].isdigit():
                pass

            if file[n-1][0].isalpha() and file[n][0].isalpha():

                current_stop = " ".join(file[n].split()[:-1])
                prev_stop = " ".join(file[n-1].split()[:-1])

                c_time = file[n].strip()
                current_time = c_time[-2:]
                p_time = file[n-1].strip()
                prev_time = p_time[-2:]

                time_diff = abs(int(prev_time) - int(current_time))

                if prev_stop not in time_dict.keys():
                    time_dict[prev_stop] = time_dict.get(prev_stop, {})
                    time_dict[prev_stop][current_stop] = time_diff

                else:
                    time_dict[prev_stop][current_stop] = time_diff

    return time_dict

time_dictionary()


def build_tram_network(stopfile = "data/tramstops.json", linefile= "data/tramlines.txt"):

    with open(stopfile, 'r') as infile:
        data = json.load(infile)
    with open(linefile, 'r') as file:
        tram_network = {}
        tram_network["stops"] = build_tram_stops(data)
        tram_network["lines"]  = build_tram_lines(file)
        tram_network["times"] = time_dictionary(linefile)
        with open(TRAM_FILE, "w") as outfile:
            json.dump(tram_network, outfile, ensure_ascii=False, indent=4)

build_tram_network()

def lines_via_stop(linedict, stop):
    lines_trough_stop = []
    for tram_number, stops in sorted(linedict.items(), key= lambda  item:int(item[0])):
        if stop in stops:
            lines_trough_stop.append(str(tram_number))
    return lines_trough_stop

def lines_between_stops(linedict, stop1, stop2):
    lines_trough_2stop = []
    for tram_number, stops in sorted(linedict.items(), key=lambda item: int(item[0])):
        if stop1 in stops and stop2 in stops:
            lines_trough_2stop.append(str(tram_number))
    return lines_trough_2stop

def time_between_stops(linedict, timedict, line, stop1, stop2):

    if line in linedict:
        list_of_stops = linedict[line]

        if stop1 not in list_of_stops and stop2 not in list_of_stops or stop1 not in list_of_stops or stop2 not in list_of_stops:
            return "No such line exists"
        index1 = list_of_stops.index(stop1)
        index2 = list_of_stops.index(stop2)
        sum = 0

        if index1 < index2:
            for s in range(index1, index2):
                sum += int(timedict[list_of_stops[s]][list_of_stops[s+1]])

        elif index1 > index2:
            for i in range(index1,index2,-1):
                sum += int(timedict[list_of_stops[i-1]][list_of_stops[i]])

        return sum


def distance_between_stops(stopdict, stop1, stop2):

    pos1 = (stopdict[stop1]["lat"],stopdict[stop1]["lon"])
    pos2 = (stopdict[stop2]["lat"],stopdict[stop2]["lon"])
    distance = haversine(pos1,pos2)
    return distance

def answer_query(tramdict, user_input):
    with open("tramnetwork.json") as trams:
        tramdict = json.loads(trams.read())
        stopdict = tramdict['stops']
        linedict = tramdict['lines']
        timedict = tramdict['times']


        if user_input.startswith("via "):
            via_stop = user_input[4:]
            if via_stop in stopdict:
                return lines_via_stop(linedict, via_stop)
            else:
                return "unknown arguments"


        elif user_input.startswith("between "):
            stop_names = user_input[8:].split(" and ")
            stop1, stop2 = stop_names[0], stop_names[1]
            if stop1 in stopdict and stop2 in stopdict:
                return lines_between_stops(linedict, stop1, stop2)
            else:
                return "unknown arguments"

        elif user_input.startswith("time with "):
            line_and_stops = user_input[10:].split(" from ")
            line_nr = line_and_stops[0]
            stops = line_and_stops[1].split(" to ")
            stop1 = stops[0]
            stop2 = stops[1]
            if not line_nr.isdigit() or line_nr not in linedict:
                return "unknown line"
            elif stop1 not in stopdict or stop2 not in stopdict:
                return "unknown stop or stops"
            else:
                return time_between_stops(linedict, timedict, line_nr, stop1, stop2)

        elif user_input.startswith("distance from "):
            stop_names = user_input[14:].split(" to ")
            stop1 = stop_names[0]
            stop2 = stop_names[1]
            if stop1 in stopdict and stop2 in stopdict:
                return distance_between_stops(stopdict, stop1, stop2)
            else:
                return "unknown stop or unknown stops"

        else:
            return "sorry, try again"

def dialogue(tramfile=TRAM_FILE):
        while True:
            user_input = input("> ")
            if user_input == "quit":
                break
            else:
                answer = answer_query(tramfile,user_input)
                print(answer)


if __name__ == '__main__':
        if sys.argv[1:] == ['init']:
            build_tram_network("tramlines.txt", "tramstops.json")
        else:
            dialogue("tramnetwork.json")
