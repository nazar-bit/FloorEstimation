from lxml import etree
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point


NAME_COLUMN = "MKN"     

NS = {
    "bldg": "http://www.opengis.net/citygml/building/2.0",
    "gml": "http://www.opengis.net/gml",
}
GML_ID = "{http://www.opengis.net/gml}id"




# get geometry of one building according to kind (Walls/Roofs)
def surfaces(building, kind):
    """kind: 'WallSurface', 'RoofSurface' or 'GroundSurface'.
    Returns a list of polygons, each a list of (x, y, z) points."""
    polys = []
    for surf in building.iterfind(f".//bldg:{kind}", NS):
        for pl in surf.iterfind(".//gml:exterior//gml:posList", NS):
            v = [float(n) for n in pl.text.split()]

            polys.append( to_four_points( [tuple(v[i:i + 3]) for i in range(0, len(v), 3)] ) )
    return polys


#Transform n-shaped surface into 4-shaped
def to_four_points(points):
    pts = [np.array(p) for p in points]

    # drop the closing point 
    if np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]

    # only 3 corners:
    if len(pts) == 3:
        lengths = [np.linalg.norm(pts[(i + 1) % 3] - pts[i]) for i in range(3)]
        i = int(np.argmax(lengths))
        pts.insert(i + 1, (pts[i] + pts[(i + 1) % 3]) / 2)

    # more than 4 corners: 
    while len(pts) > 4:
        n = len(pts)
        importance = []
        for i in range(n):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            importance.append(np.linalg.norm(np.cross(b - a, c - a)) / 2)
        del pts[int(np.argmin(importance))]

    return [tuple(p) for p in pts]


# Find facade's normal vector
def facade_normal(wall_pts):
    pts = np.array(wall_pts)
    pts = pts - pts.mean(axis=0)              
    n = np.zeros(3)
    for i in range(len(pts)):
        n += np.cross(pts[i], pts[(i + 1) % len(pts)])
    n_xy = n[:2]
    return n_xy / np.linalg.norm(n_xy)


def bottom_midpoint(wall_pts):
    pts = np.array(wall_pts)
    two_lowest = pts[np.argsort(pts[:, 2])[:2]]   
    return two_lowest.mean(axis=0)[:2]            


def distance_to_street(wall_pts, building_center, street, max_dist=2000):
    start = bottom_midpoint(wall_pts)             
    normal = facade_normal(wall_pts)

    if np.dot(normal, start - building_center) < 0:
        normal = -normal

    ray = LineString([start, start + normal * max_dist])
    hit = ray.intersection(street)
    if hit.is_empty:
        return None
    return Point(start).distance(hit)


#Testing
if __name__ == "__main__":
    STREET_NAME = "Nad Kostelem"      

    street_file = r"D:\FloorEstimation\DOP_CUR_DOP_TSK_ULICUSPAKOM_L\DOP_TSK_UlicUsPAKOM_l.shp"
    streets = gpd.read_file(street_file)  
    found = streets[streets[NAME_COLUMN].str.contains(STREET_NAME, case=False, na=False)]
    print(len(found), "street pieces found")
    street = found.geometry.union_all()

    model_file = r"D:\FloorEstimation\Budovy_3D\Prah_7-4.gml"
    target_id = "_165873"

    tree = etree.parse(model_file)

    building = tree.xpath("//bldg:Building[@gml:id=$id]", namespaces=NS, id=target_id)[0]
    walls = surfaces(building, "WallSurface")
    roofs = surfaces(building, "RoofSurface")

    all_points = np.array([p for wall in walls for p in wall])
    building_center = all_points.mean(axis=0)[:2]

    for wall in walls:
        dist = distance_to_street(wall, building_center, street)
        if dist:
            print(wall, dist)

