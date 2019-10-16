import numpy as np
import pandas as pd

def select_cols(df, columns_to_keep):
    '''
    Returns pandas DataFrame with desired columns.
    
    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame produced by the listings.csv file.
    cols: list

    Returns
    ----------
    df: pandas.DataFrame
        DataFrame that consists only of the columns passed through.

    '''
    columns_to_drop = []
    for x in df.columns:
        if x not in columns_to_keep:
            columns_to_drop.append(x)
    df.drop(columns_to_drop, inplace=True, axis=1)
    return df


def to_float(df, cols):
    '''
    Converts specifified column to float type.

    Parameters
    ----------
    df: pandas.DataFrame
        Passes the DataFrame that was recently updated to have the
        desired columns.

    cols: list
        List of strings of the column names that need to be 
        converted to float.
        =============
        price
        weekly_price
        monthly_price
        =============

    Returns
    ----------
    df: pandas.DataFrame
        Updated DataFrame that updates the 'price' column datatype from a
        string to a float datatype.
    '''
    for c in cols:
        df[c] = df[c].replace({'\$':'', ',':''}, regex = True).astype(float)
    return df

##### WHERE STANDARDIZING STARTS 

def NaN_to_None(df, cols):
    '''
    Covert NaN's to 'none'.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    for col in cols:
        df[col].fillna('none', inplace=True)
        df.head()
    return df

def host_in_Denver(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df['host_loc_denver'] = df['host_location'].map(lambda x: 1.0 if x == 'Denver, Colorado, United States' else 0.0)
    return df

def true_false_standardize(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df['is_superhost'] = df['host_is_superhost'].map(lambda x: 1.0 if x == 't' else 0.0) 
    df['needs_license'] = df['requires_license'].map(lambda x: 1.0 if x == 't' else 0.0) 
    return df 

def in_top_10_neighbourhood(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df_prop_type_per_hood = df.groupby(['neighbourhood_cleansed','room_type']).size().to_frame('count').reset_index()
    df_hoodtop10 = df_prop_type_per_hood.groupby(['neighbourhood_cleansed'])['count'].sum().sort_values(ascending=False)
    df_hoodtop10 = df_hoodtop10.iloc[0:10].reset_index()
    top10neighborhoods = df_hoodtop10['neighbourhood_cleansed'].tolist()
    df['in_top_10_neighbourhood'] = df['neighbourhood_cleansed'].map(lambda x: 1.0 if x in top10neighborhoods else 0.0) 
    return df

def listing_location(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df['list_loc_denver'] = df['city'].map(lambda x: 1.0 if x == 'Denver' else 0.0) 
    return df

def fill_NaN_pricing(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df['weekly_price'].fillna(value=df['price']*7, inplace=True)
    df['monthly_price'].fillna(value=df['price']*30, inplace=True)
    return df

def room_type_dummies(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df = pd.get_dummies(df, columns=['room_type'])
    return df

def current_license(df):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df['license'].fillna(0, inplace=True)
    searchString = "2019"
    find_current_df = df.loc[df['license'].str.contains(searchString, regex=False, na=False)]
    current_lst = find_current_df['license'].tolist()
    df['current_license'] = df['license'].map(lambda x: 1.0 if x in current_lst else 0.0) 
    return df

def drop_cols(df, cols):
    '''
    Desc.
    
    Parameters
    ----------
    df: 
    cols: 

    Returns
    ----------
    df: 
    '''
    df.drop(columns=['host_location', 'host_is_superhost', 'city', 'requires_license', 'license'])


# def save(df):
#      df.to_pickle('../data/pickled_listings_df')

if __name__ == '__main__':
    df = pd.read_csv('../data/listings.csv')

    ### CLEAN START
    columns_to_keep = ['id', 'listing_url', 'summary', 'space', 'description', 'notes', 'access', 'interaction', 
                       'house_rules', 'host_id', 'host_url','host_location', 
                       'host_about', 'host_is_superhost', 'neighbourhood_cleansed', 'city',
                       'price','weekly_price','monthly_price', 'room_type','accommodates','bathrooms', 
                       'bedrooms', 'beds', 'minimum_nights', 'maximum_nights','review_scores_rating', 
                       'requires_license','license', 'calculated_host_listings_count_entire_homes', 
                       'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms']

    float_cols = ['price','weekly_price','monthly_price']
    
    df = select_cols(df, columns_to_keep)
    df = to_float(df, float_cols)
    
    ### CLEAN END

    ### STANDARDIZING START

    text_cols = ['summary', 'space', 'description', 'notes', 'access', 'interaction', 'house_rules', 'host_about']
    drop_cols = ['host_location', 'host_is_superhost', 'city', 'requires_license', 'license']

    df = NaN_to_None(df, text_cols)
    df = host_in_Denver(df)
    df = true_false_standardize(df)
    df = in_top_10_neighbourhood(df)
    df = listing_location(df)
    df = fill_NaN_pricing(df)
    df = room_type_dummies(df)
    df = current_license(df)
    df = drop_cols(df, drop_cols)

    ### STANDARDIZING END




    # save(df)



