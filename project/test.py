import os
import numpy as np
from datetime import datetime
from datetime import timedelta


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
    if -0.001 <= delta_hour < 6 :   #觀測預報線性加權              
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
# 必須先跑save_weather_data至少一次、有dnn_oversampling_8.h5跟var_range_dict.npy，在/data2/3T執行
def rain_pre_dnn(user_time, lon, lat):
    '''
    -> dnn_no_8 thr0.500 ets:0.372241
    -> dnn_no_4 thr0.500 ets:0.279723
    -> dnn_oversampling_8 thr0.918 ets:0.491323
    -> dnn_oversampling_4 thr0.918 ets:0.436868
    
    -> dnn_no_8 thr0.500 F1:0.570635
    -> dnn_no_4 thr0.500 F1:0.464559
    -> dnn_oversampling_8 thr0.918 F1:0.803666
    -> dnn_oversampling_4 thr0.918 F1:0.766626
    '''
    from tensorflow.keras.models import load_model #2.4.0
    model = load_model(os.path.join('.', 'rain_pre_dnn', 'dnn_oversampling_8.h5')) #yes_thr=0.918
    
    # 抓各種資料
    var_name_list = ['lat','lon','time','temp','rh','ws','rainfall','dbz']
    predict_input_arr = np.zeros((1, 8))
    
    ## lat, lon, time_hour
    gogo_time = user_time + timedelta(hours=1)
    time_hour = gogo_time.hour
    #print(type(time_hour), time_hour)
    predict_input_arr[0,0] = lat
    predict_input_arr[0,1] = lon
    predict_input_arr[0,2] = time_hour
    
    ## temp rh ws rainfall
    weather_dict = get_weather_data(user_time, gogo_time.strftime('%Y-%m-%d %H:%M:%S'), lon, lat)
    predict_input_arr[0,3] = weather_dict['temp']
    predict_input_arr[0,4] = weather_dict['humd']
    predict_input_arr[0,5] = weather_dict['wdsd']
    predict_input_arr[0,6] = weather_dict['rain']
    
    ## dbz
    lat_begin, lon_begin, reso = 18.0, 115.0, 0.0125
    dbz_arr = np.load(os.path.join('.', 'weather_dbz.npy'))
    #print(dbz_arr.shape)
    
    # lat_inx, lon_inx
    lat_inx = round((lat-lat_begin)/reso)
    lon_inx = round((lon-lon_begin)/reso)
    #print(lat_inx, lon_inx)
    #print(dbz_arr[lat_inx, lon_inx])
    if dbz_arr[lat_inx, lon_inx] < 0.0:
        predict_input_arr[0,7] = 0.0
    else:
        predict_input_arr[0,7] = dbz_arr[lat_inx, lon_inx]
    
    #print(predict_input_arr, predict_input_arr.shape)
    # 尺度縮放
    var_range_dict = np.load(os.path.join('.', 'rain_pre_dnn', 'var_range_dict.npy'), allow_pickle=True).item()
    for i in range(predict_input_arr.shape[1]):
        var_range = var_range_dict[var_name_list[i]]
        predict_input_arr[0, i] = (predict_input_arr[0, i]-var_range[0]) / (var_range[1]-var_range[0])
    #print(predict_input_arr)
    
    yes_thr = 0.918
    output = model.predict(predict_input_arr)
    #print(output.shape, output)
    if output[0,1]>=yes_thr:
        return True
    else:
        return False
    
def download_data(download_data_name_list=[]):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/data2/3T/star-of-commuter-00086cd89516.json"
    from google.cloud import storage 
    bucket_name = 'star-of-commuter.appspot.com' #資料夾/專案名
    
    try:
        my_storage_client = storage.Client()
        my_bucket = my_storage_client.get_bucket(bucket_name)
        for data_name in download_data_name_list:
            blob_name = 'data/{}'.format(data_name)
            blob = my_bucket.blob(blob_name)
            blob.download_to_filename(filename=data_name)

        return True
    except Exception as e :
        print(e)
        return False
    


if __name__ == '__main__':
    #user_time = datetime.now()
    #lon, lat = 121.540672, 25.052168
    #if_rain = rain_pre_dnn(user_time, lon, lat)
    #print(if_rain)
    a=[
                'weather_dbz.npy',
                'weather_forcast_dict.npy',
                'weather_obs_aqi_dict.npy',
                'weather_obs_rain_dict.npy',
                'weather_obs_temp_dict.npy',
                'weather_obs_weather_dict.npy',
                'traffic_dict.npy'
    ]
    download_data(download_data_name_list=a)