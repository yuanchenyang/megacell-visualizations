'''
This script extracts route geometry
'''

import json
from pdb import set_trace as T

from utils import FeatureCollection, gyr_cmap
from extract_links import get_flows, get_links

routes_sql = '''
SELECT flow_count, ST_AsGeoJSON(geom)
FROM experiment2_routes
WHERE orig_taz=%s and od_route_index < %s;
'''

od_routes_sql = '''
SELECT flow_count, ST_AsGeoJSON(geom)
FROM experiment2_routes
WHERE orig_taz=%s and dest_taz=%s and od_route_index < %s;
'''

routes_links_sql = '''
SELECT flow_count, links
FROM experiment2_routes
WHERE orig_taz=%s and dest_taz=%s and od_route_index < %s;
'''

OD_sql = '''
SELECT ST_AsGeoJSON(ST_ConvexHull(ST_Collect({0}_point)))
FROM experiment2_routes
WHERE {1}_taz=%s;
'''
orig_sql = OD_sql.format('start','orig')
dest_sql = OD_sql.format('end','dest')

ORIG_ID = 22113000 # 21107000 #
DEST_ID = 22307000 #22091000
DEST = True

NUM_ROUTES = 30

def execute(conn, outfile):

    cur = conn.cursor()
    fc = FeatureCollection()
    cmap = gyr_cmap(20)

    links = get_links()
    flows = get_flows()

    if True:
        if DEST:
            cur.execute(od_routes_sql, (ORIG_ID, DEST_ID, NUM_ROUTES))
        else:
            cur.execute(routes_sql, (ORIG_ID, NUM_ROUTES))
        all_data = sorted(cur.fetchall())
        for flow_count, geom in all_data:
            fc.add(json.loads(geom), {'weight': flow_count})
        cur.execute(orig_sql, (ORIG_ID,))
        fc.add(json.loads(cur.fetchone()[0]), {})
        if DEST:
            cur.execute(dest_sql, (DEST_ID,))
            fc.add(json.loads(cur.fetchone()[0]), {})
    elif True:
        pass
    fc.dump(open(outfile, 'w'))

if __name__ == "__main__":
    main()
