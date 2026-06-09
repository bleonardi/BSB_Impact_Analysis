import duckdb
import pandas as pd
import json

# ZIP centroids from research
ZIP_CENTROIDS = """
ZIP,City,State,Latitude,Longitude
45202,Cincinnati,OH,39.1027,-84.5095
45203,Cincinnati,OH,39.1055,-84.5313
45204,Cincinnati,OH,39.0985,-84.5583
45205,Cincinnati,OH,39.1141,-84.5765
45206,Cincinnati,OH,39.1265,-84.4885
45207,Cincinnati,OH,39.1445,-84.4745
45208,Cincinnati,OH,39.1365,-84.4395
45209,Cincinnati,OH,39.1545,-84.4345
45211,Cincinnati,OH,39.1515,-84.6015
45212,Cincinnati,OH,39.1645,-84.4545
45213,Cincinnati,OH,39.1785,-84.4245
45214,Cincinnati,OH,39.1245,-84.5395
45215,Cincinnati,OH,39.2285,-84.4545
45216,Cincinnati,OH,39.2015,-84.4845
45217,Cincinnati,OH,39.1685,-84.4945
45219,Cincinnati,OH,39.1295,-84.5095
45220,Cincinnati,OH,39.1445,-84.5245
45223,Cincinnati,OH,39.1615,-84.5445
45224,Cincinnati,OH,39.2015,-84.5445
45225,Cincinnati,OH,39.1445,-84.5495
45226,Cincinnati,OH,39.1185,-84.4345
45227,Cincinnati,OH,39.1445,-84.4045
45229,Cincinnati,OH,39.1485,-84.4945
45230,Cincinnati,OH,39.0845,-84.3945
45233,Cincinnati,OH,39.1145,-84.6745
45237,Cincinnati,OH,39.1915,-84.4545
45238,Cincinnati,OH,39.1145,-84.6145
45239,Cincinnati,OH,39.2115,-84.5845
41011,Covington,KY,39.0745,-84.5145
41014,Covington,KY,39.0645,-84.5245
41015,Covington,KY,39.0145,-84.5045
41016,Covington,KY,39.0845,-84.5445
41017,Covington,KY,39.0245,-84.5745
41018,Covington,KY,39.0045,-84.5945
"""

# 1. Prepare ZIP Points
import io
zip_df = pd.read_csv(io.StringIO(ZIP_CENTROIDS))

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")

# 2. Get BSB Corridor Geometry (I-75)
con.execute("""
    CREATE TABLE segments AS 
    SELECT geometry 
    FROM read_parquet('Transportation_ROI_Analysis/data/oki_transportation_segments.parquet') 
    WHERE len(list_filter(routes, x -> x.ref = '75' AND x.network = 'US:I')) > 0
""")

# 3. Calculate Distances
results = []
for idx, row in zip_df.iterrows():
    zip_code = row['ZIP']
    lat = row['Latitude']
    lon = row['Longitude']
    
    # Simple distance query
    query = f"""
    SELECT ST_Distance(
        ST_Point({lon}, {lat}), 
        (SELECT ST_Collect(list(geometry)) FROM segments)
    ) * 111319.5 as dist_meters
    """
    dist = con.execute(query).fetchone()[0]
    results.append({"ZIP": zip_code, "dist_meters": dist})

dist_df = pd.DataFrame(results)
dist_df.to_csv("BSB_Impact_Analysis/data/zip_bsb_distances.csv", index=False)
print(dist_df.sort_values('dist_meters').head(15))
