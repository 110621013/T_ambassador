import time
from datetime import datetime
from datetime import timedelta
from key import Client_Id, Client_Secret
import os
import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np
#import threading
from concurrent.futures.thread import ThreadPoolExecutor

lat_limit = 24.5

'''
def test1():
    import googlemaps
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
    '''
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/NewTaipei?%24format=JSON'
    api_return_NewTaipei = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_NewTaipei_dict = api_return_NewTaipei.json()
    VDs_dict_NewTaipei = api_return_NewTaipei_dict['VDs']
    '''
    
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
    #for VD_dict_highway in VDs_dict_highway:
    #    plt.plot(VD_dict_highway['PositionLon'], VD_dict_highway['PositionLat'], 'o', color='green', markersize=2)
    #plt.plot(VD_dict_highway['PositionLon'], VD_dict_highway['PositionLat'], 'o', color='green', label='green highway', markersize=2)
    
    for VD_dict_freeway in VDs_dict_freeway:
        plt.plot(VD_dict_freeway['PositionLon'], VD_dict_freeway['PositionLat'], 'o', color='blue', markersize=2)
    plt.plot(VD_dict_freeway['PositionLon'], VD_dict_freeway['PositionLat'], 'o', color='blue', label='blue freeway', markersize=2)
    
    for VD_dict_taipei in VDs_dict_taipei:
        plt.plot(VD_dict_taipei['PositionLon'], VD_dict_taipei['PositionLat'], 'o', color='red', markersize=2)
    plt.plot(VD_dict_taipei['PositionLon'], VD_dict_taipei['PositionLat'], 'o', color='red', label='red taipei', markersize=2)
    '''
    for VD_dict_NewTaipei in VDs_dict_NewTaipei:
        plt.plot(VD_dict_NewTaipei['PositionLon'], VD_dict_NewTaipei['PositionLat'], 'o', color='purple', markersize=2)
    plt.plot(VD_dict_NewTaipei['PositionLon'], VD_dict_NewTaipei['PositionLat'], 'o', color='purple', label='purple newtaipei', markersize=2)
    '''
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
    plt.savefig(os.path.join('.', 'project', 'vd_plot_taiwan_add_otherCity_2'))
    
    plt.xlim(121.4, 121.7)
    plt.ylim(24.9, 25.2)
    plt.savefig(os.path.join('.', 'project', 'vd_plot_taipei_add_otherCity_2'))
    
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
    now_time_df.to_csv(os.path.join(save_path, 'traffic_{}.csv'.format(county)), mode='a')

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
        
        # 中文VDID就不要ㄌ
        china = False
        for c in VDid_list_highway[i]:
            if '\u4e00' <= c <= '\u9fa5':
                china = True
        
        # 有可能有VDid_return_dict['VDLives']沒東西的問題
        if not china:
            if VDid_return_dict['VDLives']:
                VDLives = VDid_return_dict['VDLives'][0]
                now_time_dict[now_time_str].append(VDLives)
            else:
                print('==> no', VDid_list_highway[i])
        else:
            print('==> have_china', VDid_list_highway[i])
            
    #now_time_df = pd.DataFrame(now_time_dict)
    now_time_df = pd.concat([pd.DataFrame(v) for k,v in now_time_dict.items()], keys=now_time_dict)
    now_time_df.to_csv(os.path.join(save_path, 'traffic_highway.csv'), mode='a')
    

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
        if VD_dict_highway['PositionLat'] > lat_limit:
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

def plot_traffic_data():
    pass
    
    #my_data = np.genfromtxt(os.path.join('.', 'project', 'now_time_df.csv'), delimiter=',', encoding='utf-8', dtype=str)
    #print(my_data.shape, type(my_data))
    #my_data_arr = np.array(my_data)
    
    #now_time_df = pd.read_csv(os.path.join('.', 'project', 'now_time_df.csv'))
    #print(now_time_df.head)


#下載一次[新北 台北 桃園 基隆]的VD資料
def get_DataCollectTime_traffic_flow_county(access_token, county, VDid_list, traffic_dict):
    print('--> getting', county)
    # 執行抓資料
    for i in range(len(VDid_list)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/City/{}/{}?%24format=JSON'.format(county, VDid_list[i])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        VDLives = VDid_return_dict['VDLives'][0]
        traffic_dict[VDLives["VDID"]]["DataCollectTime"] = VDLives["DataCollectTime"]
        mslt = [0, 0, 0, 0]
        mslt_v = [0.0, 0.0, 0.0, 0.0]
        for j in range(len(VDLives["LinkFlows"])): #對每個LinkFlows
            for lane_dict in VDLives["LinkFlows"][j]["Lanes"]: #對每個Lane
                for k in range(4): #對每個車種
                    mslt[k] += lane_dict['Vehicles'][k]['Volume']
                    mslt_v[k] += lane_dict['Vehicles'][k]['Speed'] * lane_dict['Vehicles'][k]['Volume']
        for k in range(4): #算加權平均車速
            if mslt[k] == 0:
                continue
            else:
                mslt_v[k] /= mslt[k]
        # check no neg
        neg_flag = False
        for k in range(4):
            if mslt[k]<0 or mslt_v[k]<0.0:
                neg_flag = True
        if neg_flag:
            continue
        traffic_dict[VDLives["VDID"]]['Volume'] = mslt
        traffic_dict[VDLives["VDID"]]['Speed'] = mslt_v
    return traffic_dict

#下載一次省道的VD資料
def get_traffic_api_data_highway(access_token, VDid_list_highway, traffic_dict):
    print('--> getting highway')
    # 執行抓資料
            
    for i in range(len(VDid_list_highway)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/Highway/{}?%24format=JSON'.format(VDid_list_highway[i])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        
        # 有可能有VDid_return_dict['VDLives']沒東西的問題
        if VDid_return_dict['VDLives']:
            VDLives = VDid_return_dict['VDLives'][0]
            
            traffic_dict[VDLives["VDID"]]["DataCollectTime"] = VDLives["DataCollectTime"]
            mslt = [0, 0, 0, 0]
            mslt_v = [0.0, 0.0, 0.0, 0.0]
            for j in range(len(VDLives["LinkFlows"])): #對每個LinkFlows
                for lane_dict in VDLives["LinkFlows"][j]["Lanes"]: #對每個Lane
                    for k in range(len(lane_dict['Vehicles'])): #對每個車種
                        try:
                            mslt[k] += lane_dict['Vehicles'][k]['Volume']
                            mslt_v[k] += lane_dict['Vehicles'][k]['Speed'] * lane_dict['Vehicles'][k]['Volume']
                        except KeyError: #沒車速
                            mslt[k] += lane_dict['Vehicles'][k]['Volume']
                            mslt_v = [-1.0, -1.0, -1.0, -1.0]
            # check no neg
            neg_flag = False
            for k in range(4):
                if mslt[k]<0 or mslt_v[k]<0.0:
                    neg_flag = True
            if neg_flag:
                continue

            for k in range(4): #算加權平均車速
                if mslt[k] != 0:
                    mslt_v[k] /= mslt[k]
            traffic_dict[VDLives["VDID"]]['Volume'] = mslt
            traffic_dict[VDLives["VDID"]]['Speed'] = mslt_v
        else:
            print('==> no', VDid_list_highway[i])
    return traffic_dict


#回傳：無，每五分鐘儲存一套各VD的經緯度跟車流資料
def save_traffic_data(get_gap=300):
    county_list = ['Taipei','Taoyuan','Keelung'] #,'NewTaipei'
    traffic_dict = {}
    
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
            
            traffic_dict[VD_dict_county['VDID']] = {}
            
            traffic_dict[VD_dict_county['VDID']]['lon'] = VD_dict_county['PositionLon']
            traffic_dict[VD_dict_county['VDID']]['lat'] = VD_dict_county['PositionLat']
            traffic_dict[VD_dict_county['VDID']]['RoadName'] = VD_dict_county['RoadName']
            traffic_dict[VD_dict_county['VDID']]['RoadClass'] = VD_dict_county['RoadClass']
            total_LaneNum = 0
            for DetectionLinks_dict in VD_dict_county['DetectionLinks']:
                total_LaneNum += DetectionLinks_dict['LaneNum']
            traffic_dict[VD_dict_county['VDID']]['LaneNum'] = total_LaneNum
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
        if VD_dict_highway['PositionLat'] > lat_limit:
            VDid_list_highway.append(VD_dict_highway['VDID'])
            
            traffic_dict[VD_dict_highway['VDID']] = {}
            
            traffic_dict[VD_dict_highway['VDID']]['lon'] = VD_dict_highway['PositionLon']
            traffic_dict[VD_dict_highway['VDID']]['lat'] = VD_dict_highway['PositionLat']
            traffic_dict[VD_dict_highway['VDID']]['RoadName'] = VD_dict_highway['RoadName']
            traffic_dict[VD_dict_highway['VDID']]['RoadClass'] = VD_dict_highway['RoadClass']
            total_LaneNum = 0
            for DetectionLinks_dict in VD_dict_highway['DetectionLinks']:
                total_LaneNum += DetectionLinks_dict['LaneNum']
            traffic_dict[VD_dict_highway['VDID']]['LaneNum'] = total_LaneNum
    print('highway', len(VDid_list_highway))

    print('len(traffic_dict.keys())', len(traffic_dict.keys()))

    #print('gogo:')
    last_time = 0.0
    while True:
        now_time = time.time() # float
        now_time_str = time.strftime('%Y_%m_%d-%H:%M', time.localtime(now_time))
        print(now_time_str)
        if now_time - last_time > get_gap: # 執行抓資料
            start_time = time.time()
            # county data
            for county, VDid_list in county_dict.items():
                traffic_dict = get_DataCollectTime_traffic_flow_county(access_token, county, VDid_list, traffic_dict)
            # highway data
            traffic_dict = get_traffic_api_data_highway(access_token, VDid_list_highway, traffic_dict)
            last_time = now_time
            print('抓資料執行ㄌ：', time.time()-start_time)
            #print('traffic_dict', traffic_dict)
            np.save(os.path.join('.', 'traffic_dict.npy'), traffic_dict)
        else:
            time.sleep(10)
            #print('--sleep--')

#回傳：最近一個VD的車流資訊(ID、路線方向、幾線道、路名、各車種(MSLT)數量)
def get_traffic_data(lon, lat):
    traffic_dict = np.load(os.path.join('.', 'traffic_dict.npy'), allow_pickle=True).item()
    
    min_location_diff = 99999
    min_VD_dict = {}
    for _, VD_dict in traffic_dict.items():
        location_diff = ((lon-VD_dict['lon'])**2 + (lat-VD_dict['lat'])**2)**0.5
        if location_diff < min_location_diff:
            min_VD_dict = VD_dict
            min_location_diff = location_diff
    #print(min_VD_dict)
    return min_VD_dict

def look_all_vd():
    traffic_dict = np.load(os.path.join('.', 'traffic_dict.npy'), allow_pickle=True).item()
    for VD_id, VD_dict in traffic_dict.items():
        #print(VD_id, VD_dict['Volume'])
        if VD_dict['Volume']:
            if VD_dict['Volume'][3] > 0:
                print(VD_id, VD_dict, VD_dict['RoadName'], VD_dict['Volume'])

def traffic_test():
    lat_list = [
        24.9686378,
        24.9632276,
        24.972769833333334,
        24.982312066666665,
        24.9918543,
        24.996770050000002,
        25.0016858,
        25.0162001,
        25.0417015,
        25.043151366666667,
        25.04460123333333,
        25.0460511,
        25.0527949,
    ]
    lon_list = [
        121.1948768,
        121.2297378,
        121.25351696666667,
        121.27729613333332,
        121.3010753,
        121.331499,
        121.3619227,
        121.3991162,
        121.4307448,
        121.4597472,
        121.4887496,
        121.517752,
        121.5420693,
    ]
    
    for i in range(len(lon_list)):
        min_VD_id, min_VD_dict = get_traffic_data(lon_list[i], lat_list[i])
        plt.plot(lon_list[i], lat_list[i], 'o', color='purple', markersize=4)
        plt.plot(min_VD_dict['lon'], min_VD_dict['lat'], 'o', color='red', markersize=4)
    plt.show()
def plot_vd_time():
    pass

#台北標準，其他縣市標準超爛= =
def get_congestion_score(roadclass, totalspeed):
    assert 0<=roadclass<=7
    assert type(roadclass) == type(int(2))
    assert totalspeed>=0.0
    
    congestion_standard = [
        [40, 35, 30, 25],
        [70, 65, 60, 50],
        [40, 35, 30, 25],
        [45, 40, 35, 30],
        [70, 65, 60, 50],
        [60, 58, 55, 50],
        [35, 30, 25, 20],
        [60, 35, 30, 25],
    ]
    congestion_score = 5
    compared_thr_idx = 0
    while totalspeed < congestion_standard[roadclass][compared_thr_idx]:
        congestion_score -= 1
        compared_thr_idx += 1
        if compared_thr_idx == 4:
            return congestion_score
    return congestion_score
    

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

def plot():
    #x = np.linspace(0, 360, 361)
    x = np.linspace(0, 6, 7)
    y = 100*np.exp(-0.5*x)
    print(y)
    plt.plot(x, y)
    plt.show()

"""抓取obs與for資料存為.npy檔(obs_temp_data.npy/obs_rain_data.npy/obs_weatherVIS_data.npy/ obs_aqi_data.npy/obs_forcast_data.npy)"""
def save_obs_temp_data(): #局屬跟無人
    url_cwb = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-800E53EB-AF03-4977-99E7-0C1F2AE8BFB7&format=JSON&stationId=466850,466880,466900,466910,466920,466930,466940,467050&elementName=WDSD,TEMP,HUMD,VIS,Weather&parameterName='
    url_auto = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-800E53EB-AF03-4977-99E7-0C1F2AE8BFB7&format=JSON&stationId=C0A520,C0A530,C0A540,C0A550,C0A560,C0A570,C0A640,C0A650,C0A660,C0A770,C0A860,C0A870,C0A880,C0A890,C0A920,C0A931,C0A940,C0A950,C0A970,C0A980,C0A9C0,C0A9F0,C0AC40,C0AC60,C0AC70,C0AC80,C0ACA0,C0AD00,C0AD10,C0AD30,C0AD40,C0AD50,C0AG80,C0AH00,C0AH10,C0AH30,C0AH40,C0AH50,C0AH70,C0AH80,C0AH90,C0AI00,C0AI10,C0AI20,C0AI30,C0AI40,C0AJ10,C0AJ20,C0AJ30,C0AJ40,C0AJ50,C0B010,C0B040,C0B050,C0C460,C0C480,C0C490,C0C590,C0C620,C0C630,C0C650,C0C660,C0C670,C0C680,C0C700,C0C710,C0C720,C0C730,C0C740,C1A630,C1A750,C1A760,C1A9N0,C1AC50,C1AI50,C1AI60,C1C510&elementName=WDSD,TEMP,HUMD&parameterName='
    url_list = [url_cwb,url_auto]
    weather_obs_temp_dict = {}
    
    for url in url_list:
        location = requests.get(url).json()['records']['location']
        for i in location:
            lat = float(i['lat'])
            lon = float(i['lon'])
            wdsd = float(i['weatherElement'][0]['elementValue'])
            temp = float(i['weatherElement'][1]['elementValue'])
            humd = float(str(round(float(i['weatherElement'][2]['elementValue'])*100 ,1)))
            app_temp = 1.07*float(temp)+(0.2*float(humd)/100*6.105*np.exp(17.27*float(temp)/(237.7+float(temp))))-0.65*float(wdsd)-2.7
            
            if wdsd >=0.0 and temp>=-98 and humd>=0.0:
                weather_obs_temp_dict[i['stationId']] = {
                    'lat':lat,
                    'lon':lon,
                    'wdsd':wdsd,
                    'temp':temp,
                    'humd':humd,
                    'app_temp':app_temp,
                }
    np.save('weather_obs_temp_dict.npy',weather_obs_temp_dict)
    print('save_obs_temp_data done')
    #weather_obs_temp_dict = np.load('weather_obs_temp_dict.npy', allow_pickle=True).item()
def save_obs_rain_data(): #雨量
    url_rain = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-800E53EB-AF03-4977-99E7-0C1F2AE8BFB7&format=JSON&stationId=C0A520,C0A530,C0A540,C0A550,C0A560,C0A570,C0A640,C0A650,C0A660,C0A770,C0A860,C0A870,C0A880,C0A890,C0A920,C0A931,C0A940,C0A950,C0A970,C0A980,C0A9C0,C0A9F0,C0AC40,C0AC60,C0AC70,C0AC80,C0ACA0,C0AD00,C0AD10,C0AD30,C0AD40,C0AD50,C0AG80,C0AH00,C0AH10,C0AH30,C0AH40,C0AH50,C0AH70,C0AH80,C0AH90,C0AI00,C0AI10,C0AI20,C0AI30,C0AI40,C0AJ10,C0AJ20,C0AJ30,C0AJ40,C0AJ50,C0B010,C0B040,C0B050,C0C460,C0C480,C0C490,C0C590,C0C620,C0C630,C0C650,C0C660,C0C670,C0C680,C0C700,C0C710,C0C720,C0C730,C0C740,C1A630,C1A750,C1A760,C1A9N0,C1AC50,C1AI50,C1AI60,C1C510&elementName=RAIN&parameterName='
    location = requests.get(url_rain).json()['records']['location']
    weather_obs_rain_dict = {}
    
    for i in location:
        lat = float(i['lat'])
        lon = float(i['lon'])
        rain = float(i['weatherElement'][0]['elementValue'])
        if rain == -998.0:
            rain = 0.0
        
        if rain>=0.0:
            weather_obs_rain_dict[i['stationId']] = {
                'lat':lat,
                'lon':lon,
                'rain':rain,
            }
    np.save('weather_obs_rain_dict.npy',weather_obs_rain_dict)
    print('save_obs_rain_data done')
    #weather_obs_rain_dict = np.load('weather_obs_rain_dict.npy', allow_pickle=True).item()
def save_obs_weather_data(): #局屬
    url_weather = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-800E53EB-AF03-4977-99E7-0C1F2AE8BFB7&format=JSON&stationId=466850,466880,466900,466910,466920,466930,466940,467050&elementName=WDSD,TEMP,HUMD,VIS,Weather&parameterName='
    location = requests.get(url_weather).json()['records']['location']
    weather_obs_weather_dict = {}

    for i in location:
        if float(i['lat']) > lat_limit:
            lat = float(i['lat'])
            lon = float(i['lon'])
            weather = i['weatherElement'][4]['elementValue']  
            
            if weather != '':
                weather_obs_weather_dict[i['stationId']] = {
                    'lat':lat,
                    'lon':lon,
                    'weather':weather,
                }
      
    np.save('weather_obs_weather_dict.npy',weather_obs_weather_dict)
    print('save_obs_weather_data done')
    #weather_obs_weather_dict = np.load('weather_obs_weather_dict.npy', allow_pickle=True).item()
def save_obs_aqi_data():
    url_aqi = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=668a6684-c173-483e-a05c-03b993655ce4'
    records = requests.get(url_aqi).json()['records']
    weather_obs_aqi_dict = {}

    for i in records:
        lat = float(i['latitude'])
        lon = float(i['longitude'])
        if i['aqi'] == '':
            continue
        aqi = float(i['aqi'])
        
        if aqi >= 0.0:
            weather_obs_aqi_dict[i['siteid']] = {
                'lat':lat,
                'lon':lon,
                'aqi':aqi,
            }
    np.save('weather_obs_aqi_dict.npy',weather_obs_aqi_dict)
    print('save_obs_aqi_data done')
    #weather_obs_aqi_dict = np.load('weather_obs_aqi_dict.npy', allow_pickle=True).item()
"""抓取forcast存為.npy檔"""
def save_forcast_data():
    forcast_lon_lat_list = [
        [121.781205,25.071182],[121.442017,24.997647],[121.448906,25.164889],[121.529731,25.182586],[121.514853,25.037658],[121.544547,25.162078],[121.740475,25.133314],[121.613275,23.975128],[121.047486,25.006744],
        [121.402008,24.974944],[121.709750,24.938183],[121.745736,24.892600],[121.823711,24.971197],[121.502811,24.776203],[121.597992,24.848222],[121.662917,24.993969],[121.742892,25.002719],[121.801147,25.113169],
        [121.516507,25.096356],[121.632969,25.165914],[121.608692,25.132153],[121.942083,25.017842],[121.864242,25.036003],[121.565258,25.263783],[121.595236,25.233153],[121.643967,25.223628],[121.923372,25.129036],
        [122.002058,25.007606],[121.469681,25.109508],[121.537169,25.117494],[121.575450,25.079422],[121.522408,25.175675],[121.369728,24.939025],[121.564597,25.037822],[121.575728,25.002350],[121.446756,25.051478],
        [121.501917,25.258131],[121.403947,25.150211],[121.472331,25.086594],[121.445169,24.973208],[121.346294,24.951533],[121.491792,24.991622],[121.658778,25.066881],[121.508111,25.011250],[121.780794,25.071250],
        [121.577086,25.129142],[121.577086,25.129142],[121.550420,25.048710],[121.628328,25.002703],[121.581350,24.760717],[121.427280,25.074450],[121.544750,24.921840],[121.519058,25.283128],[121.500629,25.057328],
        [121.513139,25.115597],[121.927272,25.057107],[121.690021,25.207030],[121.408616,25.184591],[121.601198,25.273672],[121.862238,25.123695],[121.717130,25.094819],[121.783910,25.191410],[121.706993,25.166676],
        [121.791670,25.144754],[121.352281,24.820208],[121.323172,24.992425],[121.283289,24.928708],[121.153317,25.027072],[121.265767,25.084275],[121.265547,24.882853],[121.214636,24.897503],[121.143047,24.912375],
        [121.221389,24.870056],[121.386560,25.028460],[121.256375,24.977661],[121.324975,24.892936],[121.239824,25.112692],[121.008581,24.966126],[121.114856,25.064764],[121.538622,24.771003],[121.646242,25.008720],
        [121.713442,24.942840],[121.593283,24.934158],[121.469331,25.133486],[121.619664,25.034164],[121.383836,25.064361],[121.087161,24.940081]
    ]
    weather_forcast_dict = {}
    for i in range(len(forcast_lon_lat_list)):#測站87
        url_for = 'https://premium-weather-api.weatherrisk.com/future-3t/168hr-3km-model-forecast/{},{}'.format(str(forcast_lon_lat_list[i][1]), str(forcast_lon_lat_list[i][0]))
        requests_json = requests.get(url_for).json()
        data = requests_json['data']
        for idx in range(192): #權抓啦幹
            start_time = data[idx]['forecast_time']['start']  #預報的時間(一小時的開頭)
            rain = data[idx]['pcpn']                          #降雨量
            humd = data[idx]['rh']                            #濕度int
            temp = data[idx]['tempture']                      #溫度int
            weather = data[idx]['weather_condition']          #天氣狀態(晴朗、晴時多雲、多雲時晴...)
            wdsd = data[idx]['wind_speed']                    #風速
            app_temp = 1.07*float(temp)+(0.2*float(humd)/100*6.105*np.exp(17.27*float(temp)/(237.7+float(temp))))-0.65*float(wdsd)-2.7
            
            weather_forcast_dict[str(i)+'_'+str(idx)] = {
                'lat':requests_json['location'][1],
                'lon':requests_json['location'][0],
                'start_time':start_time,
                'rain':rain,
                'humd':humd,
                'temp':temp,
                'weather':weather,
                'wdsd':wdsd,
                'app_temp':app_temp,
            }
    np.save('weather_forcast_dict.npy',weather_forcast_dict)
    print('save_forcast_data done')
    #weather_forcast_dict = np.load('weather_forcast_dict.npy', allow_pickle=True).item()

"""執行迴圈 *每10分鐘執行一次*"""
def save_weather_data(gap_time=600.0):
    start_time = 0.0

    while True:
        now_time = time.time() # float
        now_time_str = time.strftime('%Y/%m/%d_%H:%M', time.localtime(now_time))
        if now_time - start_time > gap_time :
            save_obs_temp_data()
            save_obs_rain_data()
            save_obs_weather_data()
            save_obs_aqi_data()
            save_forcast_data()
            print('抓資料執行ㄌ：', time.time()-start_time)
            start_time = now_time
        else:
            time.sleep(10)
            print(now_time_str)

def get_weather_data(user_time, gogo_time, lon, lat):  
    #到達站點時間 +0UTC
    gogo_time_UTC = datetime.strptime(gogo_time,'%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    gogo_time_new = str(gogo_time_UTC)[0:10]+ 'T' +str(gogo_time_UTC)[11:13]+ ':00:00+00:00'
    user_time_UTC = user_time - timedelta(hours=8)
    #現實世界時間 +0UTC
    #now_time_UTC = datetime.now() - timedelta(hours=8)

    #選擇 觀測預報要用的比例 
    delta_hour = (gogo_time_UTC - user_time_UTC).total_seconds() / 3600
    print('delta_hour', delta_hour)
    if 0 <= delta_hour < 6 :   #觀測預報線性加權              
        nowcast_ratio = np.exp(-0.5*delta_hour)
        obs_dict = {}
        
        # get wdsd temp humd app_temp
        obs_data_dict = np.load('weather_obs_temp_dict.npy', allow_pickle=True).item()
        min_station_diff = 999999
        min_id_data = {}
        for _, id_data in obs_data_dict.items():
            i_lat = id_data['lat']
            i_lon = id_data['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = id_data
        obs_dict['wdsd'] = min_id_data['wdsd']
        obs_dict['temp'] = min_id_data['temp']
        obs_dict['humd'] = min_id_data['humd']
        obs_dict['app_temp'] = min_id_data['app_temp']
                
        # get rain
        obs_data_dict = np.load('weather_obs_rain_dict.npy', allow_pickle=True).item()
        min_station_diff = 999999
        min_id_data = {}
        for _, id_data in obs_data_dict.items():
            i_lat = id_data['lat']
            i_lon = id_data['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = id_data
        obs_dict['rain'] = min_id_data['rain']
        
        # get weather
        obs_data_dict = np.load('weather_obs_weather_dict.npy', allow_pickle=True).item()
        min_station_diff = 999999
        min_id_data = {}
        for _, id_data in obs_data_dict.items():
            i_lat = id_data['lat']
            i_lon = id_data['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = id_data
        obs_dict['weather'] = min_id_data['weather']
        
        # get aqi
        obs_data_dict = np.load('weather_obs_aqi_dict.npy', allow_pickle=True).item()
        min_station_diff = 999999
        min_id_data = {}
        for _, id_data in obs_data_dict.items():
            i_lat = id_data['lat']
            i_lon = id_data['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = id_data
        obs_dict['aqi'] = min_id_data['aqi']

        # get weather_forcast_dict
        for_dict = {}
        weather_forcast_dict = np.load('weather_forcast_dict.npy', allow_pickle=True).item()
        #來找時間
        time_idx = -1
        for id, id_data in weather_forcast_dict.items():
            if id_data['start_time'] == gogo_time_new:
                time_idx = id.split('_')[-1]
                break
        assert time_idx != -1
        
        #來找空間        
        min_station_diff = 999999
        min_id_data = {}
        for i in range(87):
            name = '{}_{}'.format(str(i), str(time_idx))
            i_lat = weather_forcast_dict[name]['lat']
            i_lon = weather_forcast_dict[name]['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = weather_forcast_dict[name]
        for_dict['rain'] = min_id_data['rain']
        for_dict['humd'] = min_id_data['humd']
        for_dict['temp'] = min_id_data['temp']
        for_dict['weather'] = min_id_data['weather']
        for_dict['wdsd'] = min_id_data['wdsd']
        for_dict['app_temp'] = min_id_data['app_temp']
        for_dict['aqi'] = None
        
        #print('---hybrid check---')
        #for key, value in obs_dict.items():
        #    print('obs_dict', key, value, type(value))
        #for key, value in for_dict.items():
        #    print('for_dict', key, value, type(value))
        
        # 混合
        hybrid_dict = {}
        hybrid_dict['rain'] = float(obs_dict['rain'])*nowcast_ratio + float(for_dict['rain'])*(1-nowcast_ratio)
        hybrid_dict['humd'] = float(obs_dict['humd'])*nowcast_ratio + float(for_dict['humd'])*(1-nowcast_ratio)
        hybrid_dict['temp'] = float(obs_dict['temp'])*nowcast_ratio + float(for_dict['temp'])*(1-nowcast_ratio)
        hybrid_dict['weather'] = obs_dict['weather'] if nowcast_ratio>=0.5 else for_dict['weather']
        hybrid_dict['wdsd'] = float(obs_dict['wdsd'])*nowcast_ratio + float(for_dict['wdsd'])*(1-nowcast_ratio)
        hybrid_dict['app_temp'] = float(obs_dict['app_temp'])*nowcast_ratio + float(for_dict['app_temp'])*(1-nowcast_ratio)
        hybrid_dict['aqi'] = obs_dict['aqi'] if nowcast_ratio>=0.5 else None
        
        return hybrid_dict
    elif 6 <= delta_hour < 72 :  #全預報
        # get weather_forcast_dict
        weather_forcast_dict = np.load('weather_forcast_dict.npy', allow_pickle=True).item()
        #來找時間
        time_idx = -1
        for id, id_data in weather_forcast_dict.items():
            if id_data['start_time'] == gogo_time_new:
                time_idx = id.split('_')[-1]
                break
        assert time_idx != -1
        
        #來找空間        
        min_station_diff = 999999
        min_id_data = {}
        for i in range(87):
            name = '{}_{}'.format(str(i), str(time_idx))
            i_lat = weather_forcast_dict[name]['lat']
            i_lon = weather_forcast_dict[name]['lon']
            station_diff = np.sqrt( np.square(float(i_lon)-float(lon)) + np.square(float(i_lat)-float(lat)) )
            if station_diff < min_station_diff:
                min_station_diff = station_diff
                min_id_data = weather_forcast_dict[name]
        
        forcast_dict={}
        forcast_dict['rain'] = float(min_id_data['rain'])
        forcast_dict['humd'] = float(min_id_data['humd'])
        forcast_dict['temp'] = float(min_id_data['temp'])
        forcast_dict['weather'] = min_id_data['weather']
        forcast_dict['wdsd'] = float(min_id_data['wdsd'])
        forcast_dict['app_temp'] = float(min_id_data['app_temp'])
        forcast_dict['aqi'] = None
        
        return forcast_dict
    else:
        raise ValueError('delta_hour not in 0~72')


# 丹宇ㄉ地理資訊
def get_geo_data(lon, lat, hourly_rainfall):
    import geopandas
    from geopandas import GeoDataFrame
    import shapely
    from shapely.geometry import Point
    
    point = Point(lon,lat)

    #台北就是麻煩= =
    rainfall_thr_list = []
    if (25 <= hourly_rainfall):
        rainfall_thr_list.append('25')
    if (41.6 <= hourly_rainfall):
        rainfall_thr_list.append('41.6')
    if (58.3 <= hourly_rainfall):
        rainfall_thr_list.append('58.3')
    #print(rainfall_thr_list)

    tp_df = False
    for rainfall_thr in rainfall_thr_list:
        tp_single_df = geopandas.read_file('tp_{}mm.shp'.format(rainfall_thr))
        tp_single_df = tp_single_df.to_crs(4326)
        #print('->, rainfall_thr', list(tp_single_df.contains(point)), rainfall_thr)
        if type(tp_df) != type(False):
            tp_df = pd.concat([tp_df, tp_single_df['geometry']], axis=0)
        else:
            tp_df = tp_single_df['geometry']
        #print('tp_df', type(tp_df))
    
    #其他縣市
    rainfall_thr = False
    if (25 <= hourly_rainfall < 41.6):
        rainfall_thr = '25'
    elif (41.6 <= hourly_rainfall < 58.3):
        rainfall_thr = '41.6'
    elif (58.3 <= hourly_rainfall):
        rainfall_thr = '58.3'
    
    if rainfall_thr:
        ty_single_df = geopandas.read_file('ty_{}mm.shp'.format(rainfall_thr))
        sp_single_df = geopandas.read_file('sp_{}mm.shp'.format(rainfall_thr))
        KL_single_df = geopandas.read_file('KL_{}mm.shp'.format(rainfall_thr))
        #print('->', list(ty_single_df.contains(point)))
        #print('->', list(sp_single_df.contains(point)))
        #print('->', list(KL_single_df.contains(point)))
        other_county_df = pd.concat([ty_single_df['geometry'],sp_single_df['geometry'],KL_single_df['geometry']],axis=0)
    
    #
    if (type(tp_df) != type(False)) and rainfall_thr:
        inp = list(tp_df.contains(point)) + list(other_county_df.contains(point))
    elif type(tp_df) != type(False):
        inp = list(tp_df.contains(point))
    elif rainfall_thr:
        inp = list(other_county_df.contains(point))
    else:
        return False
    #print('-->', inp, len(inp))
    if True in inp:
        return True
    else:
        return False



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

    # 交通
    #get_VDID_and_plot()
    #auto_get_traffic_api_and_save()
    #plot_traffic_data()
    #save_traffic_data()
    #lon, lat = 121.540672, 25.052168
    #min_VD_dict = get_traffic_data(lon, lat)
    #traffic_test()
    '''
    VLQLI40 {'lon': 121.54058, 'lat': 25.05369, 'RoadName': '龍江路', 'RoadClass': 6, 'LaneNum': 2, 'DataCollectTime': '2022-08-03T10:13:00+08:00', 'Volume': [4, 5, 2, 0], 'Speed': [12.25, 8.0, 16.5, 0.0]}
    VLQLI40 {'lon': 121.54058, 'lat': 25.05369, 'RoadName': '龍江路', 'RoadClass': 6, 'LaneNum': 2, 'DataCollectTime': '2022-08-03T10:24:00+08:00', 'Volume': [4, 2, 0, 0], 'Speed': [6.5, 19.0, 0.0, 0.0]}
    '''
    roadclass, totalspeed = 1, 75
    congestion_score = get_congestion_score(roadclass, totalspeed)
    print(congestion_score)

    # 天氣
    #xml_analysis() #雷達資料處裡
    #get_cwb_station_lonlat()
    #plot()
    #save_weather_data()
    '''
    lon, lat = 121.540672, 25.052168
    user_time = datetime.now()
    gogo_time = user_time + timedelta(hours=1)
    weather_dict = get_weather_data(user_time, gogo_time.strftime('%Y-%m-%d %H:%M:%S'), lon, lat)
    for key, value in weather_dict.items():
        print('weather_dict', key, value, type(value))
    '''
    #look_all_vd()
    
    # 地理
    #lon, lat = 121.540672, 25.052168
    #hourly_rainfall = 30
    #get_geo_data(lon, lat, hourly_rainfall) -> done
    
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