from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime,timedelta
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
from django.utils.safestring import mark_safe
import  json
import socket
import pathlib
import glob


# Create your views here.
# request -> response
# requset handler
# action



def path(request):
    point_dic={"station_lat0":[],"station_lat1":[],"station_lat2":[],"station_lng0":[],"station_lng1":[],
                                "station_lng2":[],"waypoint_lat0":[],"waypoint_lat1":[],"waypoint_lat2":[],"waypoint_lng0":[],
                                "waypoint_lng1":[],"waypoint_lng2":[],"path_duration":[],"start_end":[],"station_time0":[],"station_time1":[],"station_time2":[],
                                "arrive_station_time0":[],"arrive_station_time1":[],"arrive_station_time2":[],
                                "arrive_station_time_text0":[],"arrive_station_time_text1":[],"arrive_station_time_text2":[],"score":[],"weather0":[],"weather1":[],"weather2":[],
                                "alert_lat0":[],"alert_lng0":[],"alert_lat1":[],"alert_lng1":[],"alert_lat2":[],"alert_lng2":[],
                                "alert_path0":[],"alert_path1":[],"alert_path2":[],"one_hour_lat":[],"one_hour_lng":[],"AI_cardName0":[],"AI_cardName1":[],"AI_cardName2":[]}
    print("path got")
    data = request.POST.get("data");
    #print("data=",data)
    data=json.loads(data)
    # print("json_data",data)
    #print("data type=",type(data))
    point_dic["start_end"].append(data["path_lat0"][0])
    point_dic["start_end"].append(data["path_lng0"][0])
    point_dic["start_end"].append(data["path_lat0"][len(data["path_lat0"])-1])
    point_dic["start_end"].append(data["path_lng0"][len(data["path_lng0"])-1])
    print("totally have %d routes"%len(data["path_duration"]))
    for i in range(len(data["path_duration"])):
        point_dic["path_duration"].append(data["path_duration"][i])
        # 找一個小時候的點
        if data["path_duration"][i]<=3600:
            point_dic["one_hour_lat"].append(data["path_lat"+str(i)][-1])
            point_dic["one_hour_lng"].append(data["path_lng"+str(i)][-1])
        else :
            one_hour_later=int(len(data["path_lat"+str(i)])*3600/data["path_duration"][i])
            point_dic["one_hour_lat"].append(data["path_lat"+str(i)][one_hour_later])
            point_dic["one_hour_lng"].append(data["path_lng"+str(i)][one_hour_later])           
            
        # 建立測站
        if len(data["path_lat"+str(i)])<=101: #若起點與終點距離太近 只抓起點與終點
            point_dic["station_lat"+str(i)].append(data["path_lat"+str(i)][0])
            point_dic["station_lng"+str(i)].append(data["path_lng"+str(i)][0])
            point_dic["station_lat"+str(i)].append(data["path_lat"+str(i)][-1])
            point_dic["station_lng"+str(i)].append(data["path_lng"+str(i)][-1])
        else :
            for k in range(0,len(data["path_lat"+str(i)]),100): #每隔100個點 建立個測站
                point_dic["station_lat"+str(i)].append(data["path_lat"+str(i)][k])
                point_dic["station_lng"+str(i)].append(data["path_lng"+str(i)][k])
        # 建立中繼站 20個
        for j in range(int(len(data["path_lat"+str(i)])/20),int(len(data["path_lat"+str(i)])*19/20),int(len(data["path_lat"+str(i)])/20)):
            point_dic["waypoint_lat"+str(i)].append(data["path_lat"+str(i)][j])
            point_dic["waypoint_lng"+str(i)].append(data["path_lng"+str(i)][j])
        #print('station=',len(point_dic["station_lat"+str(i)]))
        #print('waypoint=',len(point_dic["waypoint_lng"+str(i)]))
        #print("duration=",point_dic["path_duration"])
        #print("start&end=",point_dic["start_end"])
        #print(len(data["path_lat"+str(i)]))
        #print(len(data["path_lng"+str(i)]))
    user_ip=socket.gethostbyname(socket.gethostname())
    upload_dic('path/'+user_ip,str(point_dic),'star-of-commuter.appspot.com')
    return JsonResponse({'message': "success","duration":point_dic["path_duration"]})
def product(request):

    dic={"晴朗":1,
         "晴時多雲":2,
         "多雲時晴":3,
         "多雲時陰":4,
         "多雲":5,
         "陰時多雲":6,
         "陰":7,
         "細雨":8,
         "小雨":9,
         "中雨":10,
         "大雨":11}

    if 'endpoint' in request.GET:

        user_ip=socket.gethostbyname(socket.gethostname())
        dic_product=download_dic('path/'+user_ip,'star-of-commuter.appspot.com')
        #print(dic_product,type(dic_product))
        # 從使用者介面取得資料
        time=request.GET['time']
        date=request.GET['date']
        para_date=date.split("-") # 整理資料 YY MM DD
        para_time=time.split(":") # 整理資料 hour min
        YY=int(para_date[0]) # 年
        MM=int(para_date[1]) # 月
        DD=int(para_date[2]) # 天
        hours=int(para_time[0]) # 時
        mins=int(para_time[1]) # 分
        departure_time=datetime(YY,MM,DD,hours,mins)
        user_time=datetime.now()


        # 各監測站預計抵達時間(花費秒數)
        for i in range(len(dic_product["path_duration"])):
            for k in range(len(dic_product["station_lat"+str(i)])):
                dic_product["station_time"+str(i)].append(int(dic_product["path_duration"][i]/(len(dic_product["station_lat"+str(i)])-1)*k))
                timer=timedelta(seconds=dic_product["station_time"+str(i)][k])
                dic_product["arrive_station_time"+str(i)].append(timer+departure_time)
                dic_product["arrive_station_time_text"+str(i)].append(dic_product["arrive_station_time"+str(i)][k].strftime('%Y-%m-%d %H:%M:%S.%f')[:-7])
                #print("arrive_sation_time",dic_product["arrive_station_time"+str(i)])
                #print("arrive_sation_time_text",dic_product["arrive_station_time_text"+str(i)])
        # print(pathlib.Path(__file__).parent.absolute())
        # rain_yes_or_not=rain_pre_dnn(departure_time,dic_product["station_lng0"][-1],dic_product["station_lat0"][-1])
        # print("rainging or shining ???",rain_yes_or_not)
        # 評分系統&緊抱上線

        download_data(['weather_dbz.npy',
                'weather_forcast_dict.npy',
                'weather_obs_aqi_dict.npy',
                'weather_obs_rain_dict.npy',
                'weather_obs_temp_dict.npy',
                'weather_obs_weather_dict.npy',
                'traffic_dict.npy'])

        for line in range(len(dic_product["path_duration"])):
            
            app_temp=[]
            temp=[]
            wdsd=[]
            aqi=[]
            rain=[]
            app_temp_score=[]
            wdsd_score=[]
            aqi_score=[]
            rain_score=[]
            aqi_station=len(dic_product["station_lat"+str(line)])
            geo=[]
            geo_score=[]
            traffic_score=[]
            #溫度警示
            font_type = 'playground/data/TaipeiSansTCBeta-Regular.ttf'
            warning1_1 = '高溫黃燈警報：\n溫度達攝氏36度，請注意防曬\n'
            warning1_2 = '高溫紅燈警報：\n溫度達攝氏38度，請注意防曬，\n 並留意水分攝取。\n'
            warning1_3 = '低溫黃燈警報：\n溫度低於攝氏10度，請注意保暖\n'
            warning1_4 = '低溫紅燈警報：\n溫度低於攝氏6度，請注意保暖\n'      
            #其他警示
            warning2 = '強風警報：\n行經此路段請注意行車安全\n'
            warning3 = '大雨警報：\n行經此路段請注意行車安全，\n或等雨勢暫歇再上路\n'
            warning4 = '淹水警報：\n行經此路段請注意路面積水\n'
            warning5 = '砂石車警報：\n行經此路段請注意大車動向\n'    
            
   
            # 天氣部分
                # 抓取資料
            for i in range (len(dic_product["station_lat"+str(line)])):
                weatherdata=get_weather_data(user_time,dic_product["arrive_station_time_text"+str(line)][i], dic_product["station_lng"+str(line)][i], dic_product["station_lat"+str(line)][i])
                dic_product["weather"+str(line)].append(dic[weatherdata["weather"]])
                app_temp.append(weatherdata["app_temp"])
                temp.append(weatherdata["temp"])
                wdsd.append(weatherdata["wdsd"])
                if weatherdata["aqi"]==None:
                    aqi.append(-1)
                    aqi_station=aqi_station-1
                else :
                    aqi.append(weatherdata["aqi"])
                rain.append(weatherdata["rain"])
             
            #print("weaher in route",line,":",dic_product["weather"+str(line)])
                    # 計算分數
            for i in range (len(dic_product["station_lat"+str(line)])):
                        # 體感溫度
                if app_temp[i]>37 or app_temp[i]<10:
                    app_temp_score.append(1)
                elif app_temp[i]>34 or app_temp[i]<15:
                    app_temp_score.append(2)
                elif app_temp[i]>30 or app_temp[i]<18:
                    app_temp_score.append(3)
                elif app_temp[i]>26 or app_temp[i]<21:
                    app_temp_score.append(4)
                else :
                    app_temp_score.append(5)
                        # 風速
                if wdsd[i]>10.8:
                    wdsd_score.append(1)
                else :
                    wdsd_score.append(5)
                        # AQI
                if aqi[i]>=161:
                    aqi_score.append(1)
                elif aqi[i]>=121:
                    aqi_score.append(2)
                elif aqi[i]>=81:
                    aqi_score.append(3)
                elif aqi[i]>=41:
                    aqi_score.append(4)
                elif aqi[i]>=0:
                    aqi_score.append(5)
                else :
                    aqi_score.append(0)
                        # 降雨量
                if rain[i]>=31:
                    rain_score.append(1)
                elif rain[i]>=21:
                    rain_score.append(2)
                elif rain[i]>=11:
                    rain_score.append(3)
                elif rain[i]>0:
                    rain_score.append(4)
                else :
                    rain_score.append(5)
            # 地理部分
                # 抓取資料
            for i in range (len(dic_product["station_lat"+str(line)])):
                geodata=get_geo_data(dic_product["station_lng"+str(line)][i], dic_product["station_lat"+str(line)][i], rain[i])
                geo.append(geodata)
                # 計算分數
            for i in range (len(dic_product["station_lat"+str(line)])):
                if geo[i]==True:
                    geo_score.append(1)
                else :
                    geo_score.append((5))
            # 交通部分
                # 邊抓取資料邊計算分數
            traffic_station=len(dic_product["station_lat"+str(line)])
            big_car_score=[]
            big_car_staion=len(dic_product["station_lat"+str(line)])
            for i in range (len(dic_product["station_lat"+str(line)])):
                count=0
                sum_speed=0
                min_VD_dict = get_traffic_data(dic_product["station_lng"+str(line)][i], dic_product["station_lat"+str(line)][i])
                # 砂石車分數
                if min_VD_dict:
                    if min_VD_dict["Volume"][2]+min_VD_dict["Volume"][3]>0:
                        big_car_score.append(1)
                    else :
                        big_car_score.append((5))
                else:
                    big_car_score.append(0)
                    big_car_staion=big_car_staion-1
                # 車流量分數
                if min_VD_dict:
                    for j in range(4):
                        sum_speed=sum_speed+min_VD_dict["Speed"][j]*min_VD_dict["Volume"][j]
                        count=count+min_VD_dict["Volume"][j]
                    # print("count=",count)
                    if  count ==0:
                        traffic_score.append(5)
                    else :        
                        totalspeeds=sum_speed/count
                    traffic_score.append(get_congestion_score(min_VD_dict["RoadClass"],totalspeeds))
                else:
                    traffic_score.append(0)
                    traffic_station=traffic_station-1
            # 時間分數
            
            if dic_product["path_duration"][line]/max(dic_product["path_duration"])==1:
                time_score=1
            elif dic_product["path_duration"][line]/max(dic_product["path_duration"])>=0.95:
                time_score=2
            elif dic_product["path_duration"][line]/max(dic_product["path_duration"])>=0.9:
                time_score=3
            elif dic_product["path_duration"][line]/max(dic_product["path_duration"])>=0.85:
                time_score=4
            else :
                time_score=5
            
                time_score=5
            a=len(dic_product["station_lat"+str(line)])
            b=traffic_station
            c=big_car_staion
            if aqi_station==0:
                aqi_station=1
            if a==0:
                a=1
            if b==0:
                b=1
            if c==0:
                c=1
            #print("division=",len(dic_product["station_lat"+str(line)]))
            #print(traffic_station)
            #print(big_car_staion)
            if (dic_product["arrive_station_time"+str(line)][-1]-user_time).total_seconds()<=3600: # 抵達時間離現在超過1小時，不使用交通資料
                scores=(sum(app_temp_score)/a+sum(wdsd_score)/a+sum(aqi_score)/aqi_station+sum(rain_score)/a \
                    +sum(geo_score)/a+sum(traffic_score)/b+sum(big_car_score)/c+time_score)/40*10
                scores=round(scores, 2)
            else :
                scores=(sum(app_temp_score)/a+sum(wdsd_score)/a+sum(aqi_score)/aqi_station+sum(rain_score)/a \
                    +sum(geo_score)/a+time_score)/30*10
                scores=round(scores, 2)
            dic_product["score"].append(scores)
            # 天氣緊抱
            for i in range (len(dic_product["station_lat"+str(line)])):
                save_name=""
                warning_show =''
                #判斷天氣狀況
                #晴
                if dic_product["weather"+str(line)][i] == 1:
                     save_name += 'sun'
                #雨
                elif dic_product["weather"+str(line)][i]== 8 or 9 or 10 or 11:
                    save_name += 'rain'
                else:
                    save_name += 'other'
           
                #判斷溫度
                if temp[i]>=38:
                    save_name += '1b'
                    warning_show += '1b'
                elif (temp[i]>=36 and temp[i]<38):
                    save_name += '1a'
                    warning_show += '1a'
                elif (temp[i]<=10 and temp[i]>6):
                    save_name += '1c'
                    warning_show += '1c'
                elif (temp[i]<=6):
                    save_name += '1d'
                    warning_show += '1d'
                #判斷風速
                if wdsd[i]>= 10.8:
                    save_name += '2'
                    warning_show += '2'
                #判斷雨勢
                if rain[i]>= 31:
                   save_name += '3'
                   warning_show += '3'
                #判斷淹水
                if geo[i] == True:
                    save_name += '4'
                    warning_show += '4'

                #判斷砂石車
                if big_car_score[i] ==1:
                    save_name += '5'
                    warning_show += '5'
                # 紀錄有警報的經緯度
                # print("warning_show=",warning_show)
                if warning_show=="":
                    pass
                else:
                    dic_product["alert_lat"+str(line)].append(dic_product["station_lat"+str(line)][i])
                    dic_product["alert_lng"+str(line)].append(dic_product["station_lng"+str(line)][i])
                    dic_product["alert_path"+str(line)].append(save_name)
            # 判斷一小時候的降雨狀況
            rain_yes_or_not=rain_pre_dnn(departure_time,dic_product["one_hour_lng"][line],dic_product["one_hour_lat"][line])

            AI_cardName =""

            if dic_product["path_duration"][line]>=3600:
                AI_cardName += 'onehour_'
            else:
                AI_cardName += 'destination_' 

            if rain_yes_or_not == True:    #假設1是下雨
                AI_cardName += 'rain.png'
            else:
                AI_cardName += 'sun.png'
            dic_product["AI_cardName"+str(line)].append(AI_cardName)
            print("rain or not",rain_yes_or_not)
        print("AI cardname", dic_product["AI_cardName0"],dic_product["AI_cardName1"],dic_product["AI_cardName2"])
        del dic_product["arrive_station_time0"]
        del dic_product["arrive_station_time1"]
        del dic_product["arrive_station_time2"]
        upload_dic('path2/'+user_ip,str(dic_product),'star-of-commuter.appspot.com')
        score_dic={}
        for i in range(len(dic_product["path_duration"])):
            score_dic["score{}".format(i)]=dic_product["score"][i]
        return render(request,'secondpage_practice.html',score_dic)
    else:
        min_time=(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[11:-10])
        min_date=(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-15])
        delta = timedelta(days=3)
        max_date=((datetime.now()+delta).strftime('%Y-%m-%d %H:%M:%S.%f')[:-15])
        time_dic={
                    "min_time":min_time,
                    "min_date":min_date,
                    "max_date":max_date
                 }
        print('error')
        return render(request,'homepage.html',time_dic)

def map0(request):
    user_ip=socket.gethostbyname(socket.gethostname())
    print(user_ip)
    dic_product2=download_dic('path2/'+user_ip,'star-of-commuter.appspot.com')    
    dic0={}
    subkey=["station_lat0","station_lng0","waypoint_lat0","waypoint_lng0","start_end","arrive_station_time_text0","weather0","alert_path0","alert_lat0","alert_lng0","AI_cardName0"]
    dic0=dict([(key, dic_product2[key]) for key in subkey])
    dic0["station_lat"]=dic0.pop("station_lat0")
    dic0["station_lng"]=dic0.pop("station_lng0")
    dic0["waypoint_lat"]=dic0.pop("waypoint_lat0")
    dic0["waypoint_lng"]=dic0.pop("waypoint_lng0")
    dic0["arrive_station_time"]=dic0.pop("arrive_station_time_text0")
    dic0["weather_icon"]=dic0.pop("weather0")
    dic0["alert_path"]=dic0.pop("alert_path0")
    dic0["alert_path"]=mark_safe(json.dumps(dic0["alert_path"]))
    dic0["alert_lat"]=dic0.pop("alert_lat0")
    dic0["alert_lng"]=dic0.pop("alert_lng0")
    dic0["AI_cardName"]=dic0.pop("AI_cardName0")
    dic0["AI_cardName"]=mark_safe(json.dumps(dic0["AI_cardName"]))
    #print(dic0)    
    return render(request,"route.html",context=dic0)

def map1(request):
    user_ip=socket.gethostbyname(socket.gethostname())
    print(user_ip)
    dic_product2=download_dic('path2/'+user_ip,'star-of-commuter.appspot.com')  
    dic1={}
    subkey=["station_lat1","station_lng1","waypoint_lat1","waypoint_lng1","start_end","arrive_station_time_text1","weather1","alert_path1","alert_lat1","alert_lng1","AI_cardName1"]
    dic1=dict([(key, dic_product2[key]) for key in subkey])
    dic1["station_lat"]=dic1.pop("station_lat1")
    dic1["station_lng"]=dic1.pop("station_lng1")
    dic1["waypoint_lat"]=dic1.pop("waypoint_lat1")
    dic1["waypoint_lng"]=dic1.pop("waypoint_lng1")
    dic1["arrive_station_time"]=dic1.pop("arrive_station_time_text1")
    dic1["weather_icon"]=dic1.pop("weather1")
    dic1["alert_path"]=dic1.pop("alert_path1")
    dic1["alert_path"]=mark_safe(json.dumps(dic1["alert_path"]))
    dic1["alert_lat"]=dic1.pop("alert_lat1")
    dic1["alert_lng"]=dic1.pop("alert_lng1") 
    dic1["AI_cardName"]=dic1.pop("AI_cardName1")
    dic1["AI_cardName"]=mark_safe(json.dumps(dic1["AI_cardName"]))

    #print(dic1) 
    return render(request,"route.html",context=dic1)

def map2(request):
    user_ip=socket.gethostbyname(socket.gethostname())
    dic_product2=download_dic('path2/'+user_ip,'star-of-commuter.appspot.com')  
    dic2={}
    subkey=["station_lat2","station_lng2","waypoint_lat2","waypoint_lng2","start_end","arrive_station_time_text2","weather2","alert_path2","alert_lat2","alert_lng2","AI_cardName2"]
    dic2=dict([(key, dic_product2[key]) for key in subkey])
    dic2["station_lat"]=dic2.pop("station_lat2")
    dic2["station_lng"]=dic2.pop("station_lng2")
    dic2["waypoint_lat"]=dic2.pop("waypoint_lat2")
    dic2["waypoint_lng"]=dic2.pop("waypoint_lng2")
    dic2["arrive_station_time"]=dic2.pop("arrive_station_time_text2")
    dic2["weather_icon"]=dic2.pop("weather2")
    dic2["alert_path"]=dic2.pop("alert_path2")
    dic2["alert_path"]=mark_safe(json.dumps(dic2["alert_path"]))    
    dic2["alert_lat"]=dic2.pop("alert_lat2")
    dic2["alert_lng"]=dic2.pop("alert_lng2")
    dic2["AI_cardName"]=dic2.pop("AI_cardName2")
    dic2["AI_cardName"]=mark_safe(json.dumps(dic2["AI_cardName"]))    

    #print(dic2)  
    return render(request,"route.html",context=dic2)
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
    from keras.models import load_model
    model = load_model(os.path.join('.','playground','data','dnn_oversampling_8.h5')) #yes_thr=0.918
    
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
    dbz_arr = np.load(os.path.join('.', 'playground','data','weather_dbz.npy'))
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
    var_range_dict = np.load( os.path.join('.','playground','data','var_range_dict.npy'), allow_pickle=True).item()
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(os.getcwd(), 'playground', 'star-of-commuter-00086cd89516.json')
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

import io
import urllib, base64
import os
from google.cloud import storage
from PIL import Image, ImageDraw, ImageFont
os.environ['GOOGLE_APPLICATION_CREDENTTALS']='star-of-commuter-00086cd89516.json'

storage_client=storage.Client()

my_bucket = storage_client.get_bucket('star-of-commuter.appspot.com')

def upload(blob,file,bucket):
    try:
        bucket = storage_client.get_bucket(bucket)
        blob = bucket.blob(blob)
        blob.upload_from_string(file, content_type='png')
        return True
    except Exception as e :
        print(e)
        return False
def upload_dic(blob,contents,bucket):
    try:
        bucket = storage_client.get_bucket(bucket)
        blob = bucket.blob(blob)
        blob.upload_from_string(contents)

        return True
    except Exception as e :
        print(e)
        return False
def download_dic(blob,bucket):
    try:
        bucket = storage_client.get_bucket(bucket)
        blob = bucket.blob(blob)
        contents = blob.download_as_string()
        contents=contents.decode("utf-8") 
        dic=eval(contents)
        #print(dic,type(dic))

        return dic
    except Exception as e :
        print(e)
        return False
import time
import os
import requests
import pandas as pd
import numpy as np
#import threading


lat_limit = 24.5

#回傳：最近一個VD的車流資訊(ID、路線方向、幾線道、路名、各車種(MSLT)數量)
def get_traffic_data(lon, lat):
    traffic_dict = np.load(os.path.join('.', 'traffic_dict.npy'), allow_pickle=True).item()
    #traffic_dict = np.load(os.path.join('.', 'data', 'traffic_dict.npy'), allow_pickle=True).item()
    max_limit_range = 0.01
    
    min_location_diff = 99999
    min_VD_dict = {}
    for _, VD_dict in traffic_dict.items():
        location_diff = ((lon-VD_dict['lon'])**2 + (lat-VD_dict['lat'])**2)**0.5
        if location_diff < min_location_diff:
            min_VD_dict = VD_dict
            min_location_diff = location_diff
    #print(min_VD_dict)
    if min_location_diff > max_limit_range:
        return None
    return min_VD_dict

def look_all_vd():
    traffic_dict = np.load(os.path.join('.','playground','data','traffic_dict.npy'), allow_pickle=True).item()
    for VD_id, VD_dict in traffic_dict.items():
        #print(VD_id, VD_dict['Volume'])
        if VD_dict['Volume']:
            if VD_dict['Volume'][3] > 0:
                print(VD_id, VD_dict, VD_dict['RoadName'], VD_dict['Volume'])



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
    if -99 <= delta_hour < 6 :   #觀測預報線性加權              
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


    
