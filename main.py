import pandas as pd
import geopandas as gpd
import momepy

import matplotlib.pyplot as plt

def geodata_process(csv_file, category):
    df = pd.read_csv(csv_file, sep=';')
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
    )
    gdf['category'] = category
    return gdf

if __name__ == "__main__":
    
    SEA_DATASET = "UPPLY-SEAPORTS.csv"
    AIR_DATASET = "UPPLY-AIRPORTS.csv"

    # Geoseries processing
    sea_port = geodata_process(SEA_DATASET, "Sea")
    air_port = geodata_process(AIR_DATASET, "Air")

    complete_dataset = pd.concat([sea_port, air_port], ignore_index=True)

    # print(complete_dataset.head())
    # print(complete_dataset.columns)
    # print(complete_dataset.shape)

    start_point = input("Please input start port name: ")
    end_point = input("Please input destination port name: ")

    

    