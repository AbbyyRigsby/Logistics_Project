import pandas as pd
import geopandas

import matplotlib.pyplot as plt

def geoseries_process(csv_file):
    df = pd.read_csv(csv_file, sep=';')
    points = geopandas.points_from_xy(df.longitude, df.latitude)
    gdf = geopandas.GeoSeries(points)
    
    return gdf


if __name__ == "__main__":
    
    SEA_DATASET = "UPPLY-SEAPORTS.csv"
    AIR_DATASET = "UPPLY-AIRPORTS.csv"

    # Geoseries processing
    sea_df = geoseries_process(SEA_DATASET)
    air_df = geoseries_process(AIR_DATASET)

    fig, ax = plt.subplots()
    sea_df.plot(ax=ax, color='blue', markersize=2)
    air_df.plot(ax=ax, color='red', markersize=2)
    ax.set_title("Port GeoData")
    #plt.show()

