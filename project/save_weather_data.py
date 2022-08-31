import requests
import numpy as np
import os
import time


def change_obs_weather(weather):
    sunny = ['晴','晴有霾','晴有靄','晴有霧','晴朗']
    cloudy = ['多雲','多雲有霾','多雲有靄','多雲有霧','多雲有雷','多雲有閃電','多雲雷聲','多雲']
    overcast = ['陰','陰有雷','陰有閃電','陰有雷聲','陰']
    rainy_1 = ['多雲有雨','陰有雨','細雨']
    rainy_2 = ['多雲有陣雨','陰有陣雨','小雨']
    rainy_3 = ['多雲有雷雨','陰有雷雨','中雨']
    rainy_4 = ['多雲大雷雨','陰大雷雨','大雨']
    hail = ['陰有雹','陰有雷雹','陰大雷雹','有冰雹']
    weather_list=[sunny,cloudy,overcast,rainy_1,rainy_2,rainy_3,rainy_4,hail]

    for weather_type in weather_list:
        for weather_type2 in weather_type:
            if weather_type2 == weather :
                weather = weather_type[-1]
                return(weather)

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
    #np.save('weather_obs_temp_dict.npy',weather_obs_temp_dict)
    np.save(os.path.join('.', 'weather_obs_temp_dict.npy'),weather_obs_temp_dict)
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
    #np.save('weather_obs_rain_dict.npy',weather_obs_rain_dict)
    np.save(os.path.join('.', 'weather_obs_rain_dict.npy'),weather_obs_rain_dict)
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
            
            weather = change_obs_weather(weather)
            
            if weather != '':
                weather_obs_weather_dict[i['stationId']] = {
                    'lat':lat,
                    'lon':lon,
                    'weather':weather,
                }
      
    #np.save('weather_obs_weather_dict.npy',weather_obs_weather_dict)
    np.save(os.path.join('.', 'weather_obs_weather_dict.npy'),weather_obs_weather_dict)
    
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
    #np.save('weather_obs_aqi_dict.npy',weather_obs_aqi_dict)
    np.save(os.path.join('.', 'weather_obs_aqi_dict.npy'),weather_obs_aqi_dict)
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
    #np.save('weather_forcast_dict.npy',weather_forcast_dict)
    np.save(os.path.join('.', 'weather_forcast_dict.npy'),weather_forcast_dict)
    print('save_forcast_data done')
    #weather_forcast_dict = np.load('weather_forcast_dict.npy', allow_pickle=True).item()
def save_radar_data():
    api_url = 'https://opendata.cwb.gov.tw/historyapi/v1/getMetadata/O-A0059-001?Authorization=CWB-800E53EB-AF03-4977-99E7-0C1F2AE8BFB7&format=JSON'
    api_return_taipei = requests.get(api_url)
    api_return_taipei_dict = api_return_taipei.json()
    last_release_url = api_return_taipei_dict['dataset']['resources']['resource']['data']['time'][-1]['url']
    #print(last_release_url)
    
    content = requests.get(last_release_url).text
    content = content[content.find('<content>')+9 : content.find('</content>')]
    #print(content)
    content_list = content.split(',')
    assert len(content_list)==921*881
    
    xn, yn = 921, 881
    dbz = np.full((yn, xn), -99.0, dtype=np.float)
    for y in range(yn):
        for x in range(xn):
            dbz[y, x] = float(content_list[x+y*xn])
    np.save(os.path.join('.', 'weather_dbz.npy'), dbz)

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
            save_radar_data()
            upload_data([
                'weather_dbz.npy',
                'weather_forcast_dict.npy',
                'weather_obs_aqi_dict.npy',
                'weather_obs_rain_dict.npy',
                'weather_obs_temp_dict.npy',
                'weather_obs_weather_dict.npy'
            ])
            print('抓資料上傳資料執行ㄌ：', time.time()-start_time)
            start_time = now_time
        else:
            time.sleep(10)
            #print(now_time_str)

def upload_data(upload_data_name_list=[]):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/data2/3T/star-of-commuter-00086cd89516.json"
    from google.cloud import storage 
    bucket_name = 'star-of-commuter.appspot.com' #資料夾/專案名
    
    try:
        my_storage_client = storage.Client()
        my_bucket = my_storage_client.get_bucket(bucket_name)
        for data_name in upload_data_name_list:
            blob_name = 'data/{}'.format(data_name)
            blob = my_bucket.blob(blob_name)
            #with open(data_name, "rb") as my_file:
            #    blob.upload_from_file(my_file)
            blob.upload_from_filename(os.path.join(os.path.abspath("."),data_name))
            print('--->', data_name, 'upload')
    except Exception as e :
        print(e)
        return False
            
if __name__ == '__main__':
    lat_limit = 24.5
    save_weather_data()