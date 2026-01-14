import pandas as pd
import geopandas as gpd

from sklearn.neighbors import BallTree

import networkx as nx
import numpy as np


def geodata_process(csv_file, category):
    df = pd.read_csv(csv_file, sep=';')
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
    )
    gdf['category'] = category
    return gdf


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