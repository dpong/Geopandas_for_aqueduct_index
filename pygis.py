import shapefile
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import pickle,os

def let_data_union():
    county = gpd.read_file('mapdata201907311006/COUNTY_MOI_1080726.shp',encoding='utf-8')
    basin = gpd.read_file('Taiwan_basin_shapefile/Taiwan_Basin.shp',encoding='utf-8')
    county.crs = {'init' :'epsg:4326'}
    union = gpd.overlay(county, basin, how='intersection')
    if not os.path.exists('data/'):
        os.makedirs('data/')
    with open('data/intersection.pickle','wb') as f:
        pickle.dump(union,f)

def load_df():
    if os.path.exists('data/intersection.pickle'):
        with open('data/intersection.pickle','rb') as f:
            df = pickle.load(f)
            return df
    else:
        pass
def load_csv_data():
    fold_path = '../PDF_reader/99/station'
    dataset =[]
    files = os.listdir(fold_path)
    files.remove('.DS_Store')
    for t in files:
        df = pd.read_csv(fold_path+'/'+t+'/測站資料.csv')
        name = df.iloc[0,2]
        if not name.find('\n') == -1:
            name = name.split('\n')
            name = name[0]
        area = df.iloc[0,5]
        if type(area) is str:
            area = area.split('\n')
            area = float(area[0])
        area = area * 1000000  #流域面積km2換算成m2
        df = pd.read_csv(fold_path+'/'+t+'/年度統計.csv')
        if type(df.iloc[0,1]) is str:
            discharge = None
        else:
            total_discharge = int(df.iloc[0,1]) * 86400 #CMS-day 換算成 m/m2/year
            discharge = total_discharge / area

        dataset.append([name[:3],discharge]) 
    return dataset

#把流量資料丟進df
def combine_df(df,dataset):
    df['discharge'] = 0
    for data in dataset:
        for i in range(len(df)):
            if df.at[i,'Name'] in data:
                df.at[i,'discharge'] = data[1]
    return df

def visualization(df):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    df.plot(ax=ax,edgecolor='black')
    df[df.discharge == 0 ].plot(ax=ax,edgecolor='black',color='white')
    #basin.plot(ax=ax,edgecolor='black',color='blue')
    plt.xlim(119,122.5)
    plt.ylim(21.7,25.5)
    plt.show()

if __name__=='__main__':
    #let_data_union()
    df = load_df()
    dataset = load_csv_data()
    df = combine_df(df,dataset)
    visualization(df)
    