import requests
import numpy as np
import os
import time
from key import Client_Id, Client_Secret

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
#下載一次[台北 桃園 基隆]的VD資料 //新北 
def get_DataCollectTime_traffic_flow_county(access_token, county, VDimfo_list, traffic_dict):
    print('--> getting', county)
    # 執行抓資料
    for i in range(len(VDimfo_list)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/City/{}/{}?%24format=JSON'.format(county, VDimfo_list[i]['id'])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        VDLives = VDid_return_dict['VDLives'][0]
        mslt, mslt_v = [0,0,0,0], [0.0,0.0,0.0,0.0]
        for j in range(len(VDLives["LinkFlows"])): #對每個LinkFlows
            for lane_dict in VDLives["LinkFlows"][j]["Lanes"]: #對每個Lane
                for k in range(4): #對每個車種
                    mslt[k] += lane_dict['Vehicles'][k]['Volume']
                    mslt_v[k] += lane_dict['Vehicles'][k]['Speed']*lane_dict['Vehicles'][k]['Volume']
        
        # check if neg/gogo
        gogo_flag = True
        for k in range(4):
            if mslt[k]<0 or mslt_v[k]<0.0:
                gogo_flag = False
                break
            elif mslt[k] == 0:
                continue
            else:
                mslt_v[k] /= mslt[k]
        
        if gogo_flag:
            #print('ok', county, VDLives["VDID"], mslt, mslt_v)
            traffic_dict[VDLives["VDID"]] = {}
            traffic_dict[VDLives["VDID"]]['lon'] = VDimfo_list[i]['lon']
            traffic_dict[VDLives["VDID"]]['lat'] = VDimfo_list[i]['lat']
            traffic_dict[VDLives["VDID"]]['RoadName'] = VDimfo_list[i]['RoadName']
            traffic_dict[VDLives["VDID"]]['RoadClass'] = VDimfo_list[i]['RoadClass']
            traffic_dict[VDLives["VDID"]]['LaneNum'] = VDimfo_list[i]['LaneNum']
            
            traffic_dict[VDLives["VDID"]]['Volume'] = mslt
            traffic_dict[VDLives["VDID"]]['Speed'] = mslt_v
            traffic_dict[VDLives["VDID"]]["DataCollectTime"] = VDLives["DataCollectTime"]
        #else:
        #    print('not ok', county, VDLives["VDID"], mslt, mslt_v)
    return traffic_dict

#下載一次省道的VD資料
def get_traffic_api_data_highway(access_token, VDimfo_list_highway, traffic_dict):
    print('--> getting highway')
    # 執行抓資料
            
    for i in range(len(VDimfo_list_highway)):
        url = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/Live/VD/Highway/{}?%24format=JSON'.format(VDimfo_list_highway[i]['id'])
        VDid_return_dict = requests.get(url, headers={'authorization': 'Bearer {}'.format(access_token)}).json() #網站所見之json
        #if i%100 == 0:
        #    print('i', i)
        
        # 有可能有VDid_return_dict['VDLives']沒東西的問題
        if VDid_return_dict['VDLives']:
            VDLives = VDid_return_dict['VDLives'][0]
            mslt, mslt_v = [0,0,0,0], [0.0,0.0,0.0,0.0]
            for j in range(len(VDLives["LinkFlows"])): #對每個LinkFlows
                for lane_dict in VDLives["LinkFlows"][j]["Lanes"]: #對每個Lane
                    for k in range(len(lane_dict['Vehicles'])): #對每個車種
                        try:
                            mslt[k] += lane_dict['Vehicles'][k]['Volume']
                            mslt_v[k] += lane_dict['Vehicles'][k]['Speed']*lane_dict['Vehicles'][k]['Volume']
                        except KeyError: #沒車速
                            mslt[k] += lane_dict['Vehicles'][k]['Volume']
                            mslt_v[k] = -1.0
            
            # check if neg/gogo
            gogo_flag = True
            for k in range(4):
                if mslt[k]<0 or mslt_v[k]<0.0:
                    gogo_flag = False
                    break
                elif mslt[k] == 0:
                    continue
                else:
                    mslt_v[k] /= mslt[k]
                
            if gogo_flag:
                #print('ok', VDLives["VDID"], mslt, mslt_v)
                traffic_dict[VDLives["VDID"]] = {}
                traffic_dict[VDLives["VDID"]]['lon'] = VDimfo_list_highway[i]['lon']
                traffic_dict[VDLives["VDID"]]['lat'] = VDimfo_list_highway[i]['lat']
                traffic_dict[VDLives["VDID"]]['RoadName'] = VDimfo_list_highway[i]['RoadName']
                traffic_dict[VDLives["VDID"]]['RoadClass'] = VDimfo_list_highway[i]['RoadClass']
                traffic_dict[VDLives["VDID"]]['LaneNum'] = VDimfo_list_highway[i]['LaneNum']
                
                traffic_dict[VDLives["VDID"]]['Volume'] = mslt
                traffic_dict[VDLives["VDID"]]['Speed'] = mslt_v
                traffic_dict[VDLives["VDID"]]["DataCollectTime"] = VDLives["DataCollectTime"]
            #else:
            #    print('not ok', VDLives["VDID"], mslt, mslt_v)
        #else:
        #    print('==> no', VDimfo_list_highway[i]['id'])
    return traffic_dict

#回傳：無，每五分鐘儲存一套各VD的經緯度跟車流資料
def save_traffic_data(get_gap=600):
    county_list = ['Taipei','Taoyuan','Keelung'] #,'NewTaipei'
    
    # get IDX access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type':'client_credentials',
        'client_id':Client_Id,
        'client_secret':Client_Secret,
    }
    post_return = requests.post('https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token', headers=headers, data=data)
    access_token = post_return.json()['access_token']
    
    # get all county VDimfo_list(所有應該對的VD列表靜態資料)
    county_dict = {}
    for county in county_list:
        VDimfo_list = []
        api_url_county = 'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/City/{}?%24format=JSON'.format(county)
        api_return_county = requests.get(api_url_county, headers={'authorization': 'Bearer {}'.format(access_token)})
        api_return_county_dict = api_return_county.json()
        VDs_list_county = api_return_county_dict['VDs']
        for VD_dict_county in VDs_list_county:
            VDimfo = {}
            VDimfo['id'] = VD_dict_county['VDID']
            VDimfo['lon'] = VD_dict_county['PositionLon']
            VDimfo['lat'] = VD_dict_county['PositionLat']
            VDimfo['RoadName'] = VD_dict_county['RoadName']
            VDimfo['RoadClass'] = VD_dict_county['RoadClass']
            total_LaneNum = 0
            for DetectionLinks_dict in VD_dict_county['DetectionLinks']:
                total_LaneNum += DetectionLinks_dict['LaneNum']
            VDimfo['LaneNum'] = total_LaneNum
            VDimfo_list.append(VDimfo)
            
        county_dict[county] = VDimfo_list
        print(county, len(VDimfo_list))
        
    # get highway VDimfo_list(所有應該對的VD列表靜態資料)
    VDimfo_list_highway = []
    api_url_highway =   'https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/VD/Highway?%24format=JSON'
    api_return_highway = requests.get(api_url_highway, headers={'authorization': 'Bearer {}'.format(access_token)})
    api_return_dict_highway = api_return_highway.json()
    VDs_list_highway = api_return_dict_highway['VDs']
    # 緯度過24.5
    for VD_dict_highway in VDs_list_highway:
        if VD_dict_highway['PositionLat'] > lat_limit:
            VDimfo = {}
            VDimfo['id'] = VD_dict_highway['VDID']
            VDimfo['lon'] = VD_dict_highway['PositionLon']
            VDimfo['lat'] = VD_dict_highway['PositionLat']
            VDimfo['RoadName'] = VD_dict_highway['RoadName']
            VDimfo['RoadClass'] = VD_dict_highway['RoadClass']
            total_LaneNum = 0
            for DetectionLinks_dict in VD_dict_highway['DetectionLinks']:
                total_LaneNum += DetectionLinks_dict['LaneNum']
            VDimfo['LaneNum'] = total_LaneNum
            VDimfo_list_highway.append(VDimfo)
    print('highway', len(VDimfo_list_highway))

    #print('gogo:')
    last_time = 0.0
    while True:
        now_time = time.time() # float
        #now_time_str = time.strftime('%Y_%m_%d-%H:%M', time.localtime(now_time))
        #print(now_time_str)
        if now_time - last_time > get_gap: # 執行抓資料
            traffic_dict = {}
            start_time = time.time()
            
            # county data county_dict[county] = VDimfo_list
            for county, VDimfo_list in county_dict.items():
                traffic_dict = get_DataCollectTime_traffic_flow_county(access_token, county, VDimfo_list, traffic_dict)
            # highway data
            traffic_dict = get_traffic_api_data_highway(access_token, VDimfo_list_highway, traffic_dict)
            #print('---> traffic_dict len:', len(traffic_dict.values()))
            upload_data(['traffic_dict.npy'])
            last_time = now_time
            print('抓資料上傳資料執行ㄌ：', time.time()-start_time)
            #print('traffic_dict', traffic_dict)
            np.save(os.path.join('.', 'traffic_dict.npy'), traffic_dict)
            #np.save(os.path.join('.', 'data', 'traffic_dict.npy'), traffic_dict)
            
            traffic_dict = np.load(os.path.join('.', 'traffic_dict.npy'), allow_pickle=True).item()
            print('len(traffic_dict.keys())', len(traffic_dict.keys()))
            #直接算分數
            traffic_score = {}
            for vdid, vdlive in traffic_dict.items():
                traffic_score[vdid] = {}
                # lon, lat
                traffic_score[vdid]['lon'] = vdlive['lon']
                traffic_score[vdid]['lat'] = vdlive['lat']
                # avgspeed_score
                avgspeed = 0.0
                Volume_sum = 0
                for i in range(4):
                    avgspeed += vdlive['Volume'][i]*vdlive['Speed'][i]
                    Volume_sum += vdlive['Volume'][i]
                
                if Volume_sum == 0:
                    traffic_score[vdid]['avgspeed_score'] = 5
                else:
                    avgspeed /= Volume_sum
                    traffic_score[vdid]['avgspeed_score'] = get_congestion_score(vdlive['RoadClass'], avgspeed)
                
                # if_large_car_score
                if vdlive['Volume'][2] != 0 or vdlive['Volume'][3] != 0:
                    traffic_score[vdid]['if_large_car_score'] = 1
                else:
                    traffic_score[vdid]['if_large_car_score'] = 5
            np.save(os.path.join('.', 'traffic_score.npy'), traffic_score)
            print('np.save traffic_score')
        else:
            time.sleep(10)
            #print('--sleep--')

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
    save_traffic_data()