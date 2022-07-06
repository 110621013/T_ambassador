import time
from key import google_key, Client_Id, Client_Secret
import os
import matplotlib.pyplot as plt


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
'''
def get_VDID():
    import requests
    
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
    
    # get api (建立台北所有VDs id文件)
    api_url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/Taipei?%24format=JSON'
    api_return = requests.get(api_url, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_dict = api_return.json()
    #print(type(api_return_dict))
    #for name, obj in api_return_dict.items():
    #    if name != 'VDs':
    #        print('->', name, obj)
    VDs_dict = api_return_dict['VDs']
    '''
    with open(os.path.join('.', 'project', 'VDID_list.txt'), 'w') as f:
        for obj in VDs_dict:
            print('-->', obj)
            f.write(obj['VDID']+'\n')
    '''
    
    # 用經緯度找離天險最近的VDs
    '''
    my_lon, my_lat = 121.540466, 25.052012 #天險座標
    plt.plot(my_lon, my_lat, 'o', color='red')
    min_location_diff = 99999
    min_VD_dict = {}
    for VD_dict in VDs_dict:
        plt.plot(VD_dict['PositionLon'], VD_dict['PositionLat'], 'o', color='black')
        location_diff = ((my_lon-VD_dict['PositionLon'])**2 + (my_lat-VD_dict['PositionLat'])**2)**0.5
        if location_diff < min_location_diff:
            min_VD_dict = VD_dict
            min_location_diff = location_diff
    print(min_VD_dict)
    plt.plot(min_VD_dict['PositionLon'], min_VD_dict['PositionLat'], 'o', color='blue')
    plt.show()
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
    
if __name__ == '__main__':
    #test1()
    #test2()
    get_VDID()