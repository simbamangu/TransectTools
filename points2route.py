#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# ToDo:
#   - Appify?
 
import gpxpy
import math
import argparse

# Parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--infile", required=True,
    help="path to input GPX file")
ap.add_argument("-o", "--outfile", required=False,
    help="path to output GPX file with route")
ap.add_argument("-r", "--route", required=False, default = 'A',
    help="Route name.")
ap.add_argument("-w", "--swap", required=False, default = '0',
               help = "Swap the starting side")
ap.add_argument("-s", "--sort", required = False, default = '1',
               help = 'Sort the waypoints by name before routing. Default 0 (do nothing), 1 to sort alphabetically by name, -1 to sort in reverse.')
args = vars(ap.parse_args())
print(args)

# Read initial file and get list of waypoints
infile = args['infile']
gpx_file = open(infile, "r")
gpx = gpxpy.parse(gpx_file)

gpx_wpts = gpx.waypoints
gpx_wpts = [ t for t in gpx.waypoints if t.name[-1:] in ('N', 'S', 'E', 'W')]

# Sort the waypoints (often necessary)
if args['sort'] == '1':
    gpx_wpts = sorted(gpx_wpts, key = lambda gpx_wpts: gpx_wpts.name)

# Create the route
gpx_route = gpxpy.gpx.GPXRoute(name = args["route"])

# Create routepoint order
# 'alt' (alternating) list added to normal order gives new 'snake' pattern order
# 'swap' changes the side on which one starts transects
print(args['swap'])
if args['swap'] == '1':
    alt = [1, -1, 0, 0]
    print("Order swapped")
else:
    alt = [0, 0, 1, -1]

ord = alt * int(math.ceil(len(gpx_wpts) / 4))
ord = ord[0:len(gpx_wpts)]
or2 = range(0, len(ord))
or3 = [ord[i] + or2[i] for i in range(0, len(ord))]

# Create routes
for i in or3:
    gpx_route.points.append(gpx_wpts[i])

gpx.routes.append(gpx_route)

# Write new GPX file
if args["outfile"] == None:
    outfile = args["infile"]
else:
    outfile = args["outfile"]

with open(outfile,'w') as fl:
    fl.write(gpx.to_xml())

# Some results text
print("Start: ", gpx_route.points[0])
print("End: ", gpx_route.points[-1])
