import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import webcolors as wc

def plot_color_trends_from_csv(file_path):
    # Read data from CSV file
    df = pd.read_csv(file_path)
    #print(df.columns)
    
    # Get top 10 most used colors across all eras
    top_colors = df.groupby('Color').sum().nlargest(10, 'Number of Paintings').index
    df = df[df['Color'].isin(top_colors)]
    
    #print(df)
    
    color_rgb_value = []
    for x in df['Color Family']:
        color_rgb_value = wc.name_to_rgb(x)
    '''for x in df['Color']:
        color_rgb_value = wc.name_to_rgb(x)'''
            
    '''for x in df['Color']:
        color_rgb_value += mcolors.to_rgb(x)'''
        
    print(color_rgb_value)
    '''
    # Pivot the data for stacked bar chart
    pivot_df = df.pivot_table(index='Era', columns='Color', values='Number of Paintings', aggfunc='sum', fill_value=0)
    
    # Plot
    pivot_df.plot(kind='bar', stacked=True, colormap='rainbow', figsize=(12, 6))
    plt.title("Top 10 Colors Used in Paintings by Era")
    plt.xlabel("Era of Painting")
    plt.ylabel("Number of Paintings")
    plt.legend(title="Color", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
    '''


file_path = 'paintingColors.csv'  
plot_color_trends_from_csv(file_path)
