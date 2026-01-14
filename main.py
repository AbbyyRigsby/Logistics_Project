import pandas as pd
import geopandas as gpd

import networkx as nx
import numpy as np

from sklearn.neighbors import BallTree
import json

def geodata_process(csv_file, category):
    df = pd.read_csv(csv_file, sep=';')
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
    )
    gdf['category'] = category
    return gdf

def gather_point_data(gdf, port_name):
    points = []

    port_data = gdf.loc[gdf['name'] == port_name, 'geometry'].iloc[0]

    lon = port_data.x
    lat = port_data.y

    points.append(lat)
    points.append(lon)
    return points

def add_edges(dataframe, graph, k_neighbors=10):
    #k-neighbors to give default amount of connections
    
    coords = np.radians(dataframe[['latitude', 'longitude']].values)
    tree = BallTree(coords, metric='haversine') 

    #graph = nx.Graph()
    EARTH_RADIUS_MILES = 3958.8

    distances, indices = tree.query(coords, k=k_neighbors + 1)

    for i, neighbor_indices in enumerate(indices):
        start_node = dataframe.iloc[i]['name']
        #print(f"Processing edges for: {start_node}...")
        
        for j, neighbor_idx in enumerate(neighbor_indices):
            if i == neighbor_idx:
                continue  # Skip self-connection
            
            end_node = dataframe.iloc[neighbor_idx]['name']
            
            # Convert distance from radians to miles
            dist_miles = distances[i][j] * EARTH_RADIUS_MILES
            
            # Add weighted edge
            graph.add_edge(start_node, 
                           end_node, 
                           weight=round(dist_miles, 2),
                           travel_type=dataframe.iloc[neighbor_idx]['category'])

    return graph

if __name__ == "__main__":
    
    SEA_DATASET = "UPPLY-SEAPORTS.csv"
    AIR_DATASET = "UPPLY-AIRPORTS.csv"

    # Geoseries processing
    sea_port = geodata_process(SEA_DATASET, "sea")
    air_port = geodata_process(AIR_DATASET, "air")

    complete_dataset = pd.concat([sea_port, air_port], ignore_index=True)

    print(f"Creating graph...")
    
    graph = nx.Graph()

    graph = add_edges(complete_dataset, graph)

    start_point = input("Please input start port name: ")
    end_point = input("Please input destination port name: ")

    try:
        shortest_path = nx.dijkstra_path(graph, start_point, end_point, weight='weight')
        distance = nx.dijkstra_path_length(graph, start_point, end_point, weight='weight')
        
        output_data = {
            "start_point": start_point,
            "end_point": end_point,
            "shortest_path": shortest_path,
            "distance_miles": distance
        }

        with open('output.json', 'w') as f:
            f.write(json.dumps(output_data, indent=4))

        print(shortest_path)
        print(distance)

    except nx.NetworkXNoPath:
        print(f"No path found between {start_point} and {end_point}.")