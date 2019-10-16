import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### Functions




if __name__ == '__main__':
    df = pd.read_pickle('../data/pickled_listings_df')
    print(df.head())











    # get_top_10_neighbourhoods(df)

    # # Counts and pulls the top 10 neighbourhoods with the most total Airbnb listings
    # df_top_10_neighbourhood = get_top_10_neighbourhoods(df)

    # # Creates list of top 10 neighbourhoods
    # top_10_neighbourhood_lst = get_top_10_neighbourhoods_list(df_top_10_neighbourhood)

    # # Plots and saves the top 10 neighbourhoods
    # plot_top_10_neighbourhoods(df_top_10_neighbourhood, 'Denver')

    # # Creates df of the top 10 neighbourhood and room type
    # df_top_10_neighbourhoods_and_room_type = get_top_10_neighbourhoods_and_room_type(df, top_10_neighbourhood_lst)
    
    # # Plots and saves the top 10 neighbourhood and room type
    # plot_top_10_neighbourhoods_and_room_type(df_top_10_neighbourhoods_and_room_type, 'Denver')

    # # Creates df of the number 1, most listed neighbourhood on Airbnb that lists the entire home
    # df_number_one_neighbourhood_entire_home_apt = get_single_neighbourhood_with_most_listings_entire_home_apt(df,df_top_10_neighbourhood,room_type='Entire home/apt')

    # # Creates list of the number one neighbourhood with most listings that offer the entire home
    # single_neighbourhood_with_most_listings_lst = get_single_neighbourhood_with_most_listings_to_list(df_number_one_neighbourhood_entire_home_apt)
    
