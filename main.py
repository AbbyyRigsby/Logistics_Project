import pandas as pd

import networkx as nx
import json

from dataprocess import geodata_process, add_edges

if __name__ == "__main__":
    
    SEA_DATASET = "datasets/UPPLY-SEAPORTS.csv"
    AIR_DATASET = "datasets/UPPLY-AIRPORTS.csv"

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