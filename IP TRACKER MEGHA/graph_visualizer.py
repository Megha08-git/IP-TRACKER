# graph_visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import fetch_all_data

def generate_graph():
    """
    Generate a bar plot based on stored IP data.
    """
    data = fetch_all_data()
    if not data:
        print("No data to visualize.")
        return

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=["ID", "IP Address", "Details"])
    plt.figure(figsize=(10, 6))
    sns.barplot(x="ID", y="IP Address", data=df)
    plt.title("IP Tracker Data Visualization")
    plt.xlabel("Record ID")
    plt.ylabel("IP Address")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
