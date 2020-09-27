# TransectTools
Transect tools for GPS, analysis and fieldwork

Transects are usually straight lines along which observations or samples are taken. The tools here are meant to set up transects for a given geographic sample area and create route files for usage on GPS units for field navigation.

General conventions:
* Transect geometry: for now, all transects are 2-node lines (one start point, one end, nothing in the middle).
* Transect name: each transect should have a unique ID or name, ideally sortable. 
  * 01, 02, 03 ... 99 - numbers padded with 0s.
  * A01, A02, A03 ... - stratum code and padded number.
  * A, B, C, D ... - alphanumeric code.
* Transect endpoints: each transect should have unique endpoints named by the transect ID and the position relative to the centroid, i.e. A01E and A01W for the east and west points of transect A01. The 'position' signifier should be 1-character from E, W, N, S.

## points2route

    usage: surveyWaypoints.py [-h] -i INFILE [-o OUTFILE] [-r ROUTE] [-w SWAP]
                          [-s SORT]
    
    optional arguments:
    -h, --help            show this help message and exit
    -i INFILE, --infile INFILE
                          path to input GPX file
    -o OUTFILE, --outfile OUTFILE
                          path to output GPX file with route
    -r ROUTE, --route ROUTE
                          Route name.
    -w SWAP, --swap SWAP  Swap the starting side
    -s SORT, --sort SORT  Sort the waypoints by name before routing. Default 0
                          (do nothing), 1 to sort alphabetically by name, -1 to
                          sort in reverse.

 

| Input: a GPX file with transect endpoints (2 per transect) following the [ID][Position] format above.    | Output: a GPX file with added route providing a 'snake' pattern.     |
| ---- | ---- |
| <a href="url"><img src="_media/points2route_WPTS.png"  width="300" ></a> | <a href="url"><img src="_media/points2route_RTE.png" width="400" ></a> |




