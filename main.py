import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def iqr_filter(data, col):
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    return data[(data[col] >= Q1 - 2.2 * IQR) & (data[col] <= Q3 + 2.2 * IQR)]

def plot_graph(df, graph, x_column, y_column=None, title_suffix=""):
    plt.figure(figsize=(10, 6))
    if graph == 'histogram':
        sns.histplot(df[x_column], kde=True, bins=50, color='blue')
        plt.title(f'Distribution of {x_column}{title_suffix}')
        plt.xlabel(f'{x_column} ({units.get(x_column, "")})')
        plt.ylabel('Frequency')
    elif graph == 'scatter' and y_column:
        sns.scatterplot(x=df[x_column], y=df[y_column], color='red')
        plt.title(f'Scatter Plot of {y_column} vs {x_column}{title_suffix}')
        plt.xlabel(f'{x_column} ({units.get(x_column, "")})')
        plt.ylabel(f'{y_column} ({units.get(y_column, "")})')
    elif graph == 'line' and y_column:
        sns.lineplot(x=df[x_column], y=df[y_column], color='green')
        plt.title(f'Line Plot of {y_column} vs {x_column}{title_suffix}')
        plt.xlabel(f'{x_column} ({units.get(x_column, "")})')
        plt.ylabel(f'{y_column} ({units.get(y_column, "")})')

components = ['px1', 'py1', 'pz1', 'px2', 'py2', 'pz2']
units = {
    'E1': 'GeV',
    'E2': 'GeV',
    'pt1': 'GeV',
    'pt2': 'GeV',
    'phi1': 'rad',
    'phi2': 'rad',
    'M': 'GeV'
}
units.update({key: 'GeV/c' for key in components})

def main():
    df = pd.read_csv('dielectron.csv')

    parser = argparse.ArgumentParser(
        prog='CERN Data Visualization',
        description='Visualize CERN electron collision data'
    )
    parser.add_argument('Graph_Type', choices=['histogram', 'scatter', 'line'], help='Type of graph to plot')
    parser.add_argument('x_column', help='Name of the x column to plot')
    parser.add_argument('y_column', nargs='?', help='Name of the y column to plot')
    args = parser.parse_args()
    graph = args.Graph_Type
    x_column = args.x_column
    y_column = args.y_column

    # Raw Data Graph
    plot_graph(df, graph, x_column, y_column)

    # IQR Filtered Data Graph
    filtered_df = iqr_filter(df, x_column)
    if y_column:
        filtered_df = iqr_filter(filtered_df, y_column)
    plot_graph(filtered_df, graph, x_column, y_column, title_suffix=" (IQR Filtered)")

    plt.show()

if __name__ == "__main__":
    main()