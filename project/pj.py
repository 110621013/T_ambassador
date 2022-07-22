import time
from key import google_key, Client_Id, Client_Secret
import os
import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np
#import threading
from concurrent.futures.thread import ThreadPoolExecutor


'''
def test1():
    import googlemaps
    from datetime import datetime
    gmaps = googlemaps.Client(key=google_key)

    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    print(type(geocode_result), len(geocode_result))
    for i in range(len(geocode_result)):
        print(geocode_result[i])

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                        "Parramatta, NSW",
                                        mode="transit",
                                        departure_time=now)
    
def test2():
    import googlemaps  
    import pprint  
    import time  
    gmaps = googlemaps.Client(key=google_key)
    
    places_result = gmaps.places_nearby(location='25.114842, 121.516219',radius=1000,open_now=False,type='convenience_store')
    pprint.pprint(places_result)
    time.sleep(3)

def google_map_api_test():
    import requests
    data = {
        #"homeMobileCountryCode": 310,
        #"homeMobileNetworkCode": 410,
        #"radioType": "gsm",
        #"carrier": "Vodafone",
        #"cellTowers": [],
        'considerIp': False,
        'wifiAccessPoints': [
            {
                #'macAddress': '80:B6:55:54:3D:5F', #電腦
                'macAddress': '58:24:29:65:41:55', #手機
                #"signalStrength": -43,
                #"signalToNoiseRatio": 0,
                #"channel": 11,
                #"age": 0
            }
        ]
    }
    geolocate_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key={}'.format(google_key)
    geolocate_post_return = requests.post(geolocate_url, data=data)
    geolocate_post_return_dict = geolocate_post_return.json()
    # 以下多行註解用來在'considerIp': False時檢查是否看wifi
    try:
        print(geolocate_post_return_dict['location'], geolocate_post_return_dict['accuracy'])
    except KeyError:
        print('--no considerIp--')
    print(geolocate_post_return_dict['location'], geolocate_post_return_dict['accuracy'])
'''

def get_VDID_and_plot():
    # get access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type':'client_credentials',
        'client_id':'cs35711361999-b12305ce-7553-4663',
        'client_secret':'628e9b98-b288-441c-a85d-4bc60cdf32f3',
    }
    post_return = requests.post('https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token', headers=headers, data=data)
    #print(post_return.json())
    access_token = post_return.json()['access_token']
    #print(access_token)
    
    #if os.path.isfile(os.path.join('.', 'project', 'VDID_list.txt')):
    #    os.remove(os.path.join('.', 'project', 'VDID_list.txt'))
    
    # get api (建立台北所有VDs id文件)
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Taipei?%24format=JSON'
    api_return_taipei = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_taipei_dict = api_return_taipei.json()
    #print(type(api_return_taipei_dict))
    #for name, obj in api_return_taipei_dict.items():
    #    if name != 'VDs':
    #        print('->', name, obj)
    VDs_dict_taipei = api_return_taipei_dict['VDs']
    '''
    with open(os.path.join('.', 'project', 'VDID_list.txt'), 'a') as f:
        print('---Taipei---')
        f.write('---Taipei---')
        for VD_dict_taipei in VDs_dict_taipei:
            #print('-->', VD_dict_taipei)
            f.write('{}_{}({})\n'.format(VD_dict_taipei['VDID'], VD_dict_taipei['RoadName'], len(VD_dict_taipei['DetectionLinks'])))
    '''
    
    # get api (建立新北/桃園/基隆所有VDs id文件)
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/NewTaipei?%24format=JSON'
    api_return_NewTaipei = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_NewTaipei_dict = api_return_NewTaipei.json()
    VDs_dict_NewTaipei = api_return_NewTaipei_dict['VDs']
    
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Taoyuan?%24format=JSON'
    api_return_Taoyuan = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_Taoyuan_dict = api_return_Taoyuan.json()
    VDs_dict_Taoyuan = api_return_Taoyuan_dict['VDs']
    
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Keelung?%24format=JSON'
    api_return_Keelung = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_Keelung_dict = api_return_Keelung.json()
    VDs_dict_Keelung = api_return_Keelung_dict['VDs']
    
    # get api (建立高速公路所有VDs id文件)
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/Freeway?%24format=JSON'
    api_return_freeway = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_freeway_dict = api_return_freeway.json()
    VDs_dict_freeway = api_return_freeway_dict['VDs']
    '''
    with open(os.path.join('.', 'project', 'VDID_list.txt'), 'a') as f:
        print('---freeway---')
        f.write('---freeway---')
        for VD_dict_freeway in VDs_dict_freeway:
            #print('-->', VD_dict_freeway)
            try:
                f.write('{}_{}({}~{})({})\n'.format(VD_dict_freeway['VDID'], VD_dict_freeway['RoadName'], VD_dict_freeway['RoadSection']['Start'], VD_dict_freeway['RoadSection']['End'], len(VD_dict_freeway['DetectionLinks'])))
            except KeyError:
                print('這個在搞= =:', VD_dict_freeway['VDID'])
                f.write('{}_!!沒路名!!({}~{})({})\n'.format(VD_dict_freeway['VDID'], VD_dict_freeway['RoadSection']['Start'], VD_dict_freeway['RoadSection']['End'], len(VD_dict_freeway['DetectionLinks'])))
    '''
    
    # get api (建立省道所有VDs id文件)
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/Highway?%24format=JSON'
    api_return_highway = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_highway_dict = api_return_highway.json()
    VDs_dict_highway = api_return_highway_dict['VDs']
    '''
    with open(os.path.join('.', 'project', 'VDID_list.txt'), 'a') as f:
        print('---freeway---')
        f.write('---freeway---')
        for VD_dict_highway in VDs_dict_highway:
            #print('-->', VD_dict_highway)
            f.write('{}_{}({})\n'.format(VD_dict_highway['VDID'], VD_dict_highway['RoadName'], len(VD_dict_highway['DetectionLinks'])))
    '''
    
    # 繪圖所有種類VDs
    for VD_dict_highway in VDs_dict_highway:
        plt.plot(VD_dict_highway['PositionLon'], VD_dict_highway['PositionLat'], 'o', color='green', markersize=2)
    plt.plot(VD_dict_highway['PositionLon'], VD_dict_highway['PositionLat'], 'o', color='green', label='green highway', markersize=2)
    
    for VD_dict_freeway in VDs_dict_freeway:
        plt.plot(VD_dict_freeway['PositionLon'], VD_dict_freeway['PositionLat'], 'o', color='blue', markersize=2)
    plt.plot(VD_dict_freeway['PositionLon'], VD_dict_freeway['PositionLat'], 'o', color='blue', label='blue freeway', markersize=2)
    
    for VD_dict_taipei in VDs_dict_taipei:
        plt.plot(VD_dict_taipei['PositionLon'], VD_dict_taipei['PositionLat'], 'o', color='red', markersize=2)
    plt.plot(VD_dict_taipei['PositionLon'], VD_dict_taipei['PositionLat'], 'o', color='red', label='red taipei', markersize=2)
    
    for VD_dict_NewTaipei in VDs_dict_NewTaipei:
        plt.plot(VD_dict_NewTaipei['PositionLon'], VD_dict_NewTaipei['PositionLat'], 'o', color='purple', markersize=2)
    plt.plot(VD_dict_NewTaipei['PositionLon'], VD_dict_NewTaipei['PositionLat'], 'o', color='purple', label='purple newtaipei', markersize=2)
    for VD_dict_Taoyuan in VDs_dict_Taoyuan:
        plt.plot(VD_dict_Taoyuan['PositionLon'], VD_dict_Taoyuan['PositionLat'], 'o', color='orange', markersize=2)
    plt.plot(VD_dict_Taoyuan['PositionLon'], VD_dict_Taoyuan['PositionLat'], 'o', color='orange', label='orange Taoyuan', markersize=2)
    for VD_dict_Keelung in VDs_dict_Keelung:
        plt.plot(VD_dict_Keelung['PositionLon'], VD_dict_Keelung['PositionLat'], 'o', color='pink', markersize=2)
    plt.plot(VD_dict_Keelung['PositionLon'], VD_dict_Keelung['PositionLat'], 'o', color='pink', label='pink Keelung', markersize=2)
    
    # 用給定經緯度找最近的taipei VDs
    my_lon, my_lat = 121.540466, 25.052012 #天險座標
    plt.plot(my_lon, my_lat, '*', color='black', markersize=3)
    min_location_diff = 99999
    min_VD_dict = {}
    for VD_dict_taipei in VDs_dict_taipei:
        location_diff = ((my_lon-VD_dict_taipei['PositionLon'])**2 + (my_lat-VD_dict_taipei['PositionLat'])**2)**0.5
        if location_diff < min_location_diff:
            min_VD_dict = VD_dict_taipei
            min_location_diff = location_diff
    print(min_VD_dict)
    plt.plot(min_VD_dict['PositionLon'], min_VD_dict['PositionLat'], 'o', color='black', markersize=2)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.legend()
    
    plt.xlim(119, 123)
    plt.ylim(21.5, 25.5)
    plt.savefig(os.path.join('.', 'project', 'vd_plot_taiwan_add_otherCity'))
    
    plt.xlim(121.4, 121.7)
    plt.ylim(24.9, 25.2)
    plt.savefig(os.path.join('.', 'project', 'vd_plot_taipei_add_otherCity'))
    
    plt.close()
    #plt.show()
    
    #for VDs_dict in [VDs_dict_taipei, VDs_dict_NewTaipei, VDs_dict_Taoyuan, VDs_dict_highway]:
    #    for VD_dict in VDs_dict:
    #        pass
    
    '''
    # get api (5秒跑一次)
    old_Lanes_list = []
    while True:
        api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/City/Taipei/VLQLI40?%24format=JSON'
        api_return = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
        api_return_dict = api_return.json()
        
        Lanes_list = api_return_dict['VDLives'][0]['LinkFlows'][0]['Lanes']
        if old_Lanes_list != Lanes_list:
            old_Lanes_list = Lanes_list
            for lane in Lanes_list:
                print('=>', lane)
        print('--pass--')
        time.sleep(5)
    '''
    
    #print(type(api_return_dict), api_return_dict)
    '''
    for name, obj in api_return_dict.items():
        if name == 'VDLives': #api_return_dict['VDLives'][0] is dict
            for name, obj in api_return_dict['VDLives'][0].items():
                if name == 'LinkFlows':
                    for name_2, obj_2 in obj[0].items():
                        print('---->', name_2, obj_2)
                else:
                    print('-->', name, obj)
        else:
            print('->', name, obj)'''

#下載一次[新北 台北 桃園 基隆]的VD資料
def save_traffic_api_data_county(access_token, county, now_time, VDid_list, save_path):
    print('--> getting', county)
    # 執行抓資料
    now_time_dict = {} # need pd.DataFrame()
    now_time_str = time.strftime('%Y/%m/%d_%H:%M', time.localtime(now_time))
    now_time_dict[now_time_str] = []
            
    for i in range(len(VDid_list)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/City/{}/{}?%24format=JSON'.format(county, VDid_list[i])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        VDLives = VDid_return_dict['VDLives'][0]
        now_time_dict[now_time_str].append(VDLives)
            
    #now_time_df = pd.DataFrame(now_time_dict)
    now_time_df = pd.concat([pd.DataFrame(v) for k,v in now_time_dict.items()], keys=now_time_dict)
    now_time_df.to_csv(os.path.join(save_path, 'now_time_df.csv'), mode='a')

#下載一次省道的VD資料
def save_traffic_api_data_highway(access_token, now_time, VDid_list_highway, save_path):
    print('--> getting highway')
    # 執行抓資料
    now_time_dict = {} # need pd.DataFrame()
    now_time_str = time.strftime('%Y/%m/%d_%H:%M', time.localtime(now_time))
    now_time_dict[now_time_str] = []
            
    for i in range(len(VDid_list_highway)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/Highway/{}?%24format=JSON'.format(VDid_list_highway[i])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        
        # 有可能有VDid_return_dict['VDLives']沒東西的問題
        if VDid_return_dict['VDLives']:
            VDLives = VDid_return_dict['VDLives'][0]
            now_time_dict[now_time_str].append(VDLives)
        else:
            print('==> no', VDid_list_highway[i])
            
    #now_time_df = pd.DataFrame(now_time_dict)
    now_time_df = pd.concat([pd.DataFrame(v) for k,v in now_time_dict.items()], keys=now_time_dict)
    now_time_df.to_csv(os.path.join(save_path, 'now_time_df.csv'), mode='a')
    

def auto_get_traffic_api_and_save(get_gap=300): #預設間隔5分鐘抓一次
    save_path = os.path.join('..', '..', 'data2', '3T')
    #save_path = os.path.join('.')
    county_list = ['Taipei','NewTaipei','Taoyuan','Keelung']
    
    # get IDX access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type':'client_credentials',
        'client_id':Client_Id,
        'client_secret':Client_Secret,
    }
    post_return = requests.post('https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token', headers=headers, data=data)
    access_token = post_return.json()['access_token']
    
    # get all county VDid_list
    county_dict = {}
    for county in county_list:
        VDid_list = []
        api_url_county = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/{}?%24format=JSON'.format(county)
        api_return_county = requests.get(api_url_county, headers={'authorization': 'Bearer {}'.format(access_token)})
        api_return_county_dict = api_return_county.json()
        VDs_list_county = api_return_county_dict['VDs']
        for VD_dict_county in VDs_list_county:
            VDid_list.append(VD_dict_county['VDID'])
        county_dict[county] = VDid_list
        print(county, len(VDid_list))
    # get highway VDid_list
    VDid_list_highway = []
    api_url_highway =   'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/Highway?%24format=JSON'
    api_return_highway = requests.get(api_url_highway, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_dict_highway = api_return_highway.json()
    VDs_list_highway = api_return_dict_highway['VDs']
    # 緯度過24.5
    for VD_dict_highway in VDs_list_highway:
        if VD_dict_highway['PositionLat'] > 24.5:
            VDid_list_highway.append(VD_dict_highway['VDID'])
    print('highway', len(VDid_list_highway))

    #print('gogo:')
    last_time = 0.0
    while True:
        now_time = time.time() # float
        now_time_str = time.strftime('%Y/%m/%d_%H:%M', time.localtime(now_time))
        print(now_time_str)
        if now_time - last_time > get_gap: # 執行抓資料
            start_time = time.time()
            # county data
            for county, VDid_list in county_dict.items():
                save_traffic_api_data_county(access_token, county, now_time, VDid_list, save_path)
            # highway data
            save_traffic_api_data_highway(access_token, now_time, VDid_list_highway, save_path)
            last_time = now_time
            print('抓資料執行ㄌ：', time.time()-start_time)
        else:
            time.sleep(10)
            #print('--sleep--')



#回傳：最近一個VD的車流資訊(ID、路線方向、幾線道、路名、各車種(MSLT)數量)
def get_traffic_data(lon, lat):
    pass


def xml_analysis():
    import xml.etree.ElementTree as ET
    tree = ET.parse(os.path.join(os.path.join('.', 'project', '202207031700compref_mosaic.xml')))
    root = tree.getroot()
    #print(root.tag, root.attrib)
    #print(len(root[8]), root[8][1][1].text)
    content = root[8][1][1].text # cwbopendata = root /dataset/contents/content
    print(type(content), len(content))
    content_list = content.split(',')
    assert len(content_list)==921*881
    
    xn, yn = 921, 881
    dbz = np.full((yn, xn), -99.0, dtype=np.float)
    for y in range(yn):
        for x in range(xn):
            dbz[y, x] = float(content_list[x+y*xn])
    plt.contourf(dbz)
    plt.colorbar()
    plt.show()

def get_cwb_station_lonlat():
    # 局屬
    api_url = 'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/DIV3/C-B0074-001.json'
    api_return_dict = requests.get(api_url).json()
    #print(api_return_dict)
    station_list = api_return_dict['cwbdata']['resources']['resource']['data']['stationsStatus']['station']
    assert type(station_list) == type([])
    
    with open(os.path.join('.', 'project', 'stationID.txt'), 'a' ,encoding='UTF-8') as f:
        print('---局屬---')
        f.write('---局屬---')
        for station in station_list:
            #print('-->', VD_dict_taipei)
            if station['status'] == '現存測站':
                if station['note']:
                    f.write('{}_{} lon={} lat={}, {}\n'.format(station['stationID'], station['stationName'], station['longitude'], station['latitude'], station['note']))
                else:
                    f.write('{}_{} lon={} lat={}\n'.format(station['stationID'], station['stationName'], station['longitude'], station['latitude']))
    
    # 無人
    api_url = 'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/DIV3/C-B0074-002.json'
    api_return_dict = requests.get(api_url).json()
    #print(api_return_dict)
    station_list = api_return_dict['cwbdata']['resources']['resource']['data']['stationsStatus']['station']
    assert type(station_list) == type([])
    
    with open(os.path.join('.', 'project', 'stationID.txt'), 'a', encoding='UTF-8') as f:
        print('---無人---')
        f.write('---無人---')
        for station in station_list:
            #print('-->', VD_dict_taipei)
            if station['status'] == '現存測站':
                if station['note']:
                    f.write('{}_{} lon={} lat={}, {}\n'.format(station['stationID'], station['stationName'], station['longitude'], station['latitude'], station['note']))
                else:
                    f.write('{}_{} lon={} lat={}\n'.format(station['stationID'], station['stationName'], station['longitude'], station['latitude']))
    

# 丹宇ㄉ地理資訊
def get_geo_data(lon, lat, hourly_rainfall):
    import geopandas
    from geopandas import GeoDataFrame
    import shapely
    from shapely.geometry import Point 

    if 25 <= hourly_rainfall < 41.6 :
        df = geopandas.GeoDataFrame.from_file('.shp檔案名')
    elif 41.6 <= hourly_rainfall < 58.3 :
        df = geopandas.GeoDataFrame.from_file('.shp檔案名')
    elif 58.3< hourly_rainfall :
        df = geopandas.GeoDataFrame.from_file('.shp檔案名')
    
    df = df.to_crs(4326)  
    df = df.dropna(axis=0) 
    
    point = Point(lon,lat)
    s = df['geometry'] 
    output = s.contains(point) 
    return output

# 對車禍發生做天氣變數(下雨、風強、氣溫、陽光角度)的統計分析
def a1_with_weather():
    project_path = os.path.join(os.path.dirname(__file__))
    for filename in os.listdir(project_path):
        if '交通事故資料' in filename:
            print('->', filename)
            df = pd.read_csv(os.path.join(os.path.dirname(__file__), filename))
            print(df.shape, len(df))
            
            #去掉最後兩行廢物:)
            for _ in range(2):
                df = df.drop(df.shape[0]-1, axis=0)
            #改民國為西元
            for i in range(len(df)):
                df['發生時間'].iloc[i] = df['發生時間'].iloc[i].replace(df['發生時間'].iloc[i][0:3], str(int(df['發生時間'].iloc[i][0:3]) + 1911))
            
            #for row in df.itertuples(): #要iteration用這樣
            #    print('-->', row[1], row[5], row[6]) #0idx 1發生時間	2發生地點	3死亡受傷人數	4車種	5經度	6緯度
            #print(df['發生時間']) #, df['經度'], df['緯度']
            
            '''
            for time_string in df['發生時間']:
                #print(time_string)
                result = time.strptime(time_string, "%Y年%m月%d日 %H時%M分%S秒")
                print(result)
            '''
            plt.scatter(df['經度'], df['緯度'], s=2, marker='o', label=filename)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.legend()
    
    plt.xlim(119, 123)
    plt.ylim(21.5, 25.5)
    
    plt.show()
    
#多執行緒測試
def mt_test_1():
    print("start1")
    time.sleep(10)
    print("sleep done1")
def mt_test_2():
    print("start2")
    time.sleep(5)
    print("sleep done2")
    

if __name__ == '__main__':
    #test1()
    #test2()
    
    # google map
    #google_map_api_test()
    # get_google_map_path(begin, end)

    # 交通
    #get_VDID_and_plot()
    auto_get_traffic_api_and_save()
        
    #get_traffic_data(lon, lat)
    
    # 天氣
    #xml_analysis() #雷達資料處裡
    #get_cwb_station_lonlat()
    
    # 地理
    #lon, lat = 121.540672, 25.052168
    #hourly_rainfall = 30
    #get_geo_data(lon, lat, hourly_rainfall)
    
    # A1事故跟天氣關係
    #a1_with_weather()
    
    #多執行緒測試
    '''
    t1 = threading.Thread(target=mt_test_1)  #建立執行緒
    t2 = threading.Thread(target=mt_test_2)  #建立執行緒
    t1.start()  #執行
    t2.start()  #執行
    print("end")'''
    '''
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(mt_test_1)
        executor.submit(mt_test_2)'''