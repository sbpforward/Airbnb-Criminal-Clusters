import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_top_10_neighbourhoods(df):
    '''
    Passes through the cleaned DataFrame and groups by neighbourhood and room types.
    Then the number of room types per neighbourhood are counted and the sum total of
    airbnb listings per neighbourhood are added to a new column called 'count'. 
    The DataFrame is then placed in descending order and sliced to show only the top 
    10 neighbourhoods with the most total listings on Airbnb.

    The room type options are:
    ============= 
    Entire home/apt
    Private room
    Shared room
    =============

    Parameters
    ----------
    df: pandas.DataFrame
        'pickled_listings_df' cleaned DataFrame from clean_listing.py

    Returns
    ----------
    df: pandas.DataFrame
        A new DataFrame (df_top_10_neighbourhood) storing the top 10 neighbourhoods
        and sum total listings per neighbourhood.
    '''
    df_top_10_neighbourhood = pd.DataFrame()

    temp = df.groupby(['neighbourhood_cleansed','room_type']).size().to_frame('count').reset_index()
    temp = temp.groupby(['neighbourhood_cleansed'])['count'].sum().sort_values(ascending=False)
    df_top_10_neighbourhood = temp.iloc[0:10].reset_index()

    return df_top_10_neighbourhood

def get_top_10_neighbourhoods_list(df_top_10_neighbourhood):
    '''
    Creates and stores a list of strings of the top 10 neighbourhoods.  

    Parameters
    ----------
    df: pandas.DataFrame
        Calls the df_top_10_neighbourhood DataFrame as it's already sorted in the order 
        needed. 

    Returns
    ----------
    list
        Saves and stores the names of top 10 neighbourhoods as a list of strings called 
        'top_10_neighbourhood_lst'.
    '''
    top_10_neighbourhood_lst = df_top_10_neighbourhood['neighbourhood_cleansed'].tolist()

    return top_10_neighbourhood_lst

def plot_top_10_neighbourhoods(df_top_10_neighbourhood, city):
    '''
    Plots and saves bar chart jpeg of the city's top 10 neighbourhood with the most 
    Airbnb listings using the df_top_10_neighbourhood DataFrame.

    Parameters
    ----------
    df: pandas.DataFrame
        'df_top_10_neighbourhood' DataFrame
    city: str 
        Enter the name of the city of which the data is representing. It will title and save 
        the image appropriately.

    Returns
    ----------
    image: jpeg
        Visual representation of the top 10 neighbourhoods in the desired city.
    '''
    ax = df_top_10_neighbourhood.plot.bar(x='neighbourhood_cleansed', y='count', rot=45, figsize=(10, 6), legend=False)
    ax.set_xlabel("Neighbourhood", fontsize=14)
    ax.set_ylabel("# of Total Listings", fontsize=14)
    plt.title(f'Top 10 {city} Neighbourhood with Most Available Airbnb Listings', fontsize=20)
    plt.tight_layout()
    # plt.savefig(f'top-10-neighbourhoods-in-{city}-with-most-airbnb-listings.jpeg')
    # plt.show()

def get_top_10_neighbourhoods_and_room_type(df, top_10_neighbourhood_lst):
    '''
    Groups the original DataFrame by neighbourhood and room types, then counts the number of 
    room types and adds it to a new column called "count". The saved list of only the names of top
    10 neighbourhoods (top_10_neighbourhood_lst) is called and loops through the original DataFrame
    creating a new DataFrame consisting of only the neighbourhoods in the called list. The DataFrame
    is in the same descending order and lists each room type count invidually.

    The room type options are:
    =============
    Entire home/apt
    Private room
    Shared room
    =============

    Parameters
    ----------
    df: pandas.DataFrame
        Original DataFrame
    list: list of strings
        The 'top_10_neighbourhood_lst' consisting of only the names of the top 10 neighbourhoods with 
        the largest sum total of Airbnb listings per neighbourhood.

    Returns
    ----------
    df: pandas.DataFrame
    '''
    df_top_10_neighbourhoods_and_room_type = pd.DataFrame()
    
    df = df.groupby(['neighbourhood_cleansed','room_type']).size().to_frame('count').reset_index()

    for neighbourhood in top_10_neighbourhood_lst:
        temp = df[df.neighbourhood_cleansed == neighbourhood]
        df_top_10_neighbourhoods_and_room_type = df_top_10_neighbourhoods_and_room_type.append(temp)

    return df_top_10_neighbourhoods_and_room_type

def plot_top_10_neighbourhoods_and_room_type(df_top_10_neighbourhoods_and_room_type, city):
    '''
    Plots and saves bar chart jpeg of the city's top 10 neighbourhood with the most 
    Airbnb listings and room type using the df_top_10_neighbourhood DataFrame.

    The room type options are:
    =============
    Entire home/apt
    Private room
    Shared room
    =============

    Parameters
    ----------
    df: pandas.DataFrame
        'df_top_10_neighbourhood' DataFrame
    city: str 
        Enter the name of the city of which the data is representing. It will title and save 
        the image appropriately.

    Returns
    ----------
    image: jpeg
        Visual representation of the top 10 neighbourhoods in the desired city.
    '''
    plt.figure(figsize=(12, 6))

    ax = sns.barplot(x="neighbourhood_cleansed", y="count", hue="room_type", palette='YlOrRd', data=df_top_10_neighbourhoods_and_room_type)
    ax.set_xlabel("Neighbourhood", fontsize=14)
    ax.set_ylabel("Number of Listings", fontsize=14)
    ax.set_title(f'Most Available Neighbourhood on Airbnb in {city} by Room Type', fontsize=20)
    plt.gca().legend().set_title('Room Type')
    plt.legend(loc=1, prop={'size': 14})

    plt.tight_layout()
    # plt.savefig('most-available-airbnb-listings-in-{city}-by-room-type.jpeg')
    # plt.show()

def get_single_neighbourhood_with_most_listings_entire_home_apt(df, df_top_10_neighbourhood, room_type='Entire home/apt'):
    '''
    Creates a new DataFrame consisting of all the of information about the number one neighbourhood with the largest sum 
    total of Airbnb listings. A temporary variable (neighbourhood_with_most_listings) stores the number one neighbourhood. It
    is used later to mask through the original DataFrame also pulling only those listings that offer the "Entire home/apt".

    Parameters
    ----------
    df: pandas.DataFrame
        Original DataFrame
    df: pandas.DataFrame
        df_top_10_neighbourhood
    room_type = string (required)
        'Entire home/apt'

    Returns
    ----------
    df: pandas.DataFrame
        A df_number_one_neighbourhood_entire_home_apt consisting of the all the information about the number one neighbourhood
        with the largest sum total of Airbnb listings that offer the "Entire home/apt".
    '''
    df_number_one_neighbourhood_entire_home_apt = pd.DataFrame()
    neighbourhood_with_most_listings = df_top_10_neighbourhood.loc[0,'neighbourhood_cleansed']
    df_number_one_neighbourhood_entire_home_apt = df[(df['neighbourhood_cleansed'] == neighbourhood_with_most_listings) & 
                                                        (df['room_type'] == room_type)]

    return df_number_one_neighbourhood_entire_home_apt

def get_single_neighbourhood_with_most_listings_to_list(df_number_one_neighbourhood_entire_home_apt):
    '''
    Creates a list of integers of the listing ID of the number one neighbourhood that rents out the entire home/apt using the
    'df_number_one_neighbourhood_entire_home_apt' DataFrame. This will be used when merging the 'pickled_cal_df' later.

    Parameters
    ----------
    df: pandas.DataFrame
        df_number_one_neighbourhood_entire_home_apt

    Returns
    ----------
    list: list of integers
        The 'single_neighbourhood_with_most_listings_lst' consisting of listing ID's for the number one neighbourhood with the 
        largest sum total of Airbnb listings per neighbourhood.   
    '''
    single_neighbourhood_with_most_listings_lst = df_number_one_neighbourhood_entire_home_apt['id'].tolist()

    return single_neighbourhood_with_most_listings_lst


if __name__ == '__main__':
    df = pd.read_pickle('../data/pickled_listings_df')

    get_top_10_neighbourhoods(df)

    # Counts and pulls the top 10 neighbourhoods with the most total Airbnb listings
    df_top_10_neighbourhood = get_top_10_neighbourhoods(df)

    # Creates list of top 10 neighbourhoods
    top_10_neighbourhood_lst = get_top_10_neighbourhoods_list(df_top_10_neighbourhood)

    # Plots and saves the top 10 neighbourhoods
    plot_top_10_neighbourhoods(df_top_10_neighbourhood, 'Denver')

    # Creates df of the top 10 neighbourhood and room type
    df_top_10_neighbourhoods_and_room_type = get_top_10_neighbourhoods_and_room_type(df, top_10_neighbourhood_lst)
    
    # Plots and saves the top 10 neighbourhood and room type
    plot_top_10_neighbourhoods_and_room_type(df_top_10_neighbourhoods_and_room_type, 'Denver')

    # Creates df of the number 1, most listed neighbourhood on Airbnb that lists the entire home
    df_number_one_neighbourhood_entire_home_apt = get_single_neighbourhood_with_most_listings_entire_home_apt(df,df_top_10_neighbourhood,room_type='Entire home/apt')

    # Creates list of the number one neighbourhood with most listings that offer the entire home
    single_neighbourhood_with_most_listings_lst = get_single_neighbourhood_with_most_listings_to_list(df_number_one_neighbourhood_entire_home_apt)
    
