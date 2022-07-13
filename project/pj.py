import time
from key import google_key, Client_Id, Client_Secret
import os
import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np

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
'''
def kivy_test():
    from kivy.app import App
    from kivy.uix.screenmanager import Screen,SlideTransition
    #from kivy.core.text import LabelBase
    from kivy.uix.button import ButtonBehavior
    from kivy.uix.image import Image
    from kivy.clock import Clock
    import time
    
    #LabelBase.register(
    #    name='SiyuanHeiti',
    #    fn_regular='./font/SourceHanSansCN-Normal.ttf'
    #)
    
    # 影象按鈕
    class ImageButton(ButtonBehavior,Image):
        pass
    # 秒錶螢幕
    class StopwatchScreen(Screen):
        pass
    # 時鐘螢幕
    class ClockScreen(Screen):
        pass
    
    class MainApp(App):
        def __init__(self):
            sw_started = False # 秒錶啟動狀態
            sw_seconds = 0 # 當前秒錶秒數
        def update(self,n):
            # 如果秒錶已啟動，更新當前秒數
            if self.sw_started:
                self.sw_seconds += n
            # 更新當前時間
            self.root.ids['clock_screen'].ids['time'].text = time.strftime("[b]%H[/b]:%M:%S")
            # 更新秒錶
            m,s = divmod(self.sw_seconds,60) # 返回一個包含商和餘數的元組
            self.root.ids['stopwatch_screen'].ids['stopwatch'].text = ("%02d: %02d.[size=40]%02d[/size]" % (int(m),int(s),int(s*100%100)))
        # 重寫程式啟動的事件
        def on_start(self):
            Clock.schedule_interval(self.update,0)
        # 開始/停止
        def start_stop(self):
            self.root.ids['stopwatch_screen'].ids['start_stop'].text = 'start!' if self.sw_started else 'stop!'
            self.sw_started = not self.sw_started
        # 重置秒錶
        def reset(self):
            if self.sw_started:
                self.root.ids['stopwatch_screen'].ids['start_stop'].text = 'start!'
                self.sw_started = False
                self.sw_seconds = 0
        def go_forward(self):
            screen_manager = self.root.ids['screen_manager']
            screen_manager.transition = SlideTransition(direction="right")
            screen_manager.current = "stopwatch_screen"
        def go_back(self):
            screen_manager = self.root.ids['screen_manager']
            screen_manager.transition = SlideTransition(direction="left")
            screen_manager.current = "clock_screen"
    
    if __name__ == '__main__':
        app = MainApp()
        app.run()
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

def auto_get_traffic_api_and_save():
    get_gap = 60.0 #間隔多久抓一次
    
    # get IDX access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type':'client_credentials',
        'client_id':Client_Id,
        'client_secret':Client_Secret,
    }
    post_return = requests.post('https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token', headers=headers, data=data)
    #print(post_return.json())
    access_token = post_return.json()['access_token']
    
    # get all Taipei VDid_list
    VDid_list = []
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Taipei?%24format=JSON'
    api_return_taipei = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_taipei_dict = api_return_taipei.json()
    VDs_dict_taipei = api_return_taipei_dict['VDs']
    for VD_dict_taipei in VDs_dict_taipei:
        VDid_list.append(VD_dict_taipei['VDID'])

    print('gogo:')
    last_time = 0.0
    while True:
        now_time = time.time() # float
        if now_time - last_time > get_gap:
            # 執行抓資料
            start_time = time.time()
            # 時間項
            now_time_dict = {} # need pd.DataFrame()
            now_time_str = time.strftime('%Y/%m/%d_%H:%M', time.localtime(now_time))
            now_time_dict[now_time_str] = []
            
            for i in range(len(VDid_list)):
                #single_VDid_dict = {}
                url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Taipei/{}?%24format=JSON'.format(VDid_list[i])
                VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
                if i%100 == 0:
                    print('i', i)
                VDs = VDid_return_dict['VDs'][0]
                now_time_dict[now_time_str].append(VDs)
            
            #now_time_df = pd.DataFrame(now_time_dict)
            now_time_df = pd.concat([pd.DataFrame(v) for k,v in now_time_dict.items()], keys=now_time_dict)
            now_time_df.to_csv('now_time_df_v2.csv', mode='a')
            
            last_time = now_time
            print('抓資料執行ㄌ：', time.time()-start_time, now_time_str)
        else:
            time.sleep(10)
            print('--sleep--')

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
    
    
    


if __name__ == '__main__':
    #test1()
    #test2()
    #google_map_api_test()
    #kivy_test() #有夠麻煩還要另外做UX設計
    
    
    #get_VDID_and_plot()
    #auto_get_traffic_api_and_save()
    
    xml_analysis()