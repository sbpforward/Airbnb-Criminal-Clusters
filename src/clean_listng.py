import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

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

##### WHERE HOT-ENCODE/STANDARDIZE STARTS 

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
    return df

def NaN_to_zero(df):
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
    df['review_scores_rating'].fillna(value=0, inplace=True)
    df['bedrooms'].fillna(value=0, inplace=True)
    df['bathrooms'].fillna(value=0, inplace=True)  
    df['beds'].fillna(value=0, inplace=True)     
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

def true_false_hot_enconde(df):
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

def drop_cols(df):
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
    df.drop(columns=['host_location', 'host_is_superhost', 'city', 'requires_license', 'license'], axis=1, inplace=True)
    return df

def add_violation_col(df):
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
    df['is_violating'] = df['listing_url'].map(lambda x: 1.0 if x in violater else 0.0) 
    return df

def standardize_pricing(df,cols):
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
    features = df[cols]
    scaler = StandardScaler().fit(features.values)
    features = scaler.transform(features.values)
    df[cols] = features
    return df

def save(df):
     df.to_pickle('../data/pickled_listings_df')

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

    ### HOT-ENCODE/STANDARDIZE START

    text_cols = ['summary', 'space', 'description', 'notes', 'access', 'interaction', 'house_rules', 'host_about']
    violater = ['https://www.airbnb.com/rooms/2086', 'https://www.airbnb.com/rooms/36026536',
                'https://www.airbnb.com/rooms/30991941', 'https://www.airbnb.com/rooms/36110171', 
                'https://www.airbnb.com/rooms/283162', 'https://www.airbnb.com/rooms/21281617', 
                'https://www.airbnb.com/rooms/27987428', 'https://www.airbnb.com/rooms/2139342',
                'https://www.airbnb.com/rooms/1488774', 'https://www.airbnb.com/rooms/1153002',
                'https://www.airbnb.com/rooms/2599115', 'https://www.airbnb.com/rooms/2827887',
                'https://www.airbnb.com/rooms/3495498', 'https://www.airbnb.com/rooms/4137490',
                'https://www.airbnb.com/rooms/4556950', 'https://www.airbnb.com/rooms/4671735',
                'https://www.airbnb.com/rooms/19214092', 'https://www.airbnb.com/rooms/4753876',
                'https://www.airbnb.com/rooms/4896381', 'https://www.airbnb.com/rooms/5070640',
                'https://www.airbnb.com/rooms/5402378', 'https://www.airbnb.com/rooms/35678320',
                'https://www.airbnb.com/rooms/35683218', 'https://www.airbnb.com/rooms/35828919',
                'https://www.airbnb.com/rooms/21753893', 'https://www.airbnb.com/rooms/5696654',
                'https://www.airbnb.com/rooms/8797683', 'https://www.airbnb.com/rooms/37746342',
                'https://www.airbnb.com/rooms/6288460', 'https://www.airbnb.com/rooms/6370140',
                'https://www.airbnb.com/rooms/7475742', 'https://www.airbnb.com/rooms/7859145',
                'https://www.airbnb.com/rooms/8211278', 'https://www.airbnb.com/rooms/8366762',
                'https://www.airbnb.com/rooms/8555795', 'https://www.airbnb.com/rooms/8739814',
                'https://www.airbnb.com/rooms/8829680', 'https://www.airbnb.com/rooms/8884899',
                'https://www.airbnb.com/rooms/8951180', 'https://www.airbnb.com/rooms/8989473',
                'https://www.airbnb.com/rooms/9165337', 'https://www.airbnb.com/rooms/20419783',
                'https://www.airbnb.com/rooms/9372481', 'https://www.airbnb.com/rooms/9591731',
                'https://www.airbnb.com/rooms/9169634', 'https://www.airbnb.com/rooms/10426535',
                'https://www.airbnb.com/rooms/10088031', 'https://www.airbnb.com/rooms/9237825',
                'https://www.airbnb.com/rooms/9330036', 'https://www.airbnb.com/rooms/9409334',
                'https://www.airbnb.com/rooms/9532575', 'https://www.airbnb.com/rooms/12172692',
                'https://www.airbnb.com/rooms/11377981', 'https://www.airbnb.com/rooms/21899331',
                'https://www.airbnb.com/rooms/11358422', 'https://www.airbnb.com/rooms/11240044',
                'https://www.airbnb.com/rooms/11191271', 'https://www.airbnb.com/rooms/11148272',
                'https://www.airbnb.com/rooms/11070296', 'https://www.airbnb.com/rooms/10995273',
                'https://www.airbnb.com/rooms/15743145', 'https://www.airbnb.com/rooms/10706175',
                'https://www.airbnb.com/rooms/10392285', 'https://www.airbnb.com/rooms/18000300',
                'https://www.airbnb.com/rooms/10190798', 'https://www.airbnb.com/rooms/9856869',
                'https://www.airbnb.com/rooms/9796646', 'https://www.airbnb.com/rooms/9795040',
                'https://www.airbnb.com/rooms/22307026', 'https://www.airbnb.com/rooms/9734548',
                'https://www.airbnb.com/rooms/9633450', 'https://www.airbnb.com/rooms/12711245',
                'https://www.airbnb.com/rooms/12681403', 'https://www.airbnb.com/rooms/12791280',
                'https://www.airbnb.com/rooms/13550337', 'https://www.airbnb.com/rooms/13377190',
                'https://www.airbnb.com/rooms/13140326', 'https://www.airbnb.com/rooms/12874653',
                'https://www.airbnb.com/rooms/13688138', 'https://www.airbnb.com/rooms/13656290',
                'https://www.airbnb.com/rooms/13877553', 'https://www.airbnb.com/rooms/14654146',
                'https://www.airbnb.com/rooms/14902544', 'https://www.airbnb.com/rooms/15097005',
                'https://www.airbnb.com/rooms/15237689', 'https://www.airbnb.com/rooms/38982793',
                'https://www.airbnb.com/rooms/19141160', 'https://www.airbnb.com/rooms/15583685',
                'https://www.airbnb.com/rooms/15585225', 'https://www.airbnb.com/rooms/15641776',
                'https://www.airbnb.com/rooms/15680276', 'https://www.airbnb.com/rooms/15745694',
                'https://www.airbnb.com/rooms/15807599', 'https://www.airbnb.com/rooms/27545807',
                'https://www.airbnb.com/rooms/14125469', 'https://www.airbnb.com/rooms/16497996',
                'https://www.airbnb.com/rooms/16443175', 'https://www.airbnb.com/rooms/16392236',
                'https://www.airbnb.com/rooms/16299372']
    standardize_cols = ['price', 'weekly_price', 'monthly_price']

    df = NaN_to_None(df, text_cols)
    df = host_in_Denver(df)
    df = true_false_hot_enconde(df)
    df = in_top_10_neighbourhood(df)
    df = listing_location(df)
    df = fill_NaN_pricing(df)
    df = NaN_to_zero(df)
    df = room_type_dummies(df)
    df = current_license(df)
    df = drop_cols(df)
    df = add_violation_col(df)
    df = standardize_pricing(df,standardize_cols)

    ### HOT-ENCODE/STANDARDIZE END
    save(df)





