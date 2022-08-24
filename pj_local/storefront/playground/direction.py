import googlemaps
from pprint import pprint
from datetime import datetime
import gmplot
import math
API_KEY='AIzaSyB5WPfBV6n-qOjuJiYmKG8qCG3JbcONopY'
gmaps = googlemaps.Client(key=API_KEY)

def product(start,end,YY,MM,DD,hours,mins):
    origins=gmaps.geocode(start,components={"country": "Taiwan"}) # 出發點
    destinations=gmaps.geocode(end,components={"country": "Taiwan"}) #終點
    # gooogle導航
    directions= gmaps.directions(origins[0]['formatted_address'], # 出發點
                                          destinations[0]["formatted_address"], #終點
                                          avoid=["highways", "tolls", "ferries"], #避開
                                          mode="driving", #模式
                                          alternatives=True, #是否多條選擇路線
                                          language='zh-TW', #繁體中文
                                          departure_time=datetime(YY,MM,DD,hours,mins)) #出發時間

    for line in range(len(directions)): # 路線 1 2 3 4....
        save_location="/Users/chenkeyi/storefront/playground/templates/map{}.html".format(line) #存檔路徑
        latitude_list = [] #緯度list
        longitude_list = [] #經度list
        station_lat=[]
        station_lng=[]
        station_judge=1
        marker_points = [] #經緯度
        waypoints=() #中繼站
        tupleA=() #小小工具
        title=[] #導航文字
        duration_time=directions[line]['legs'][0]['duration_in_traffic']['value'] #預測行車時間
        road_numbers=len(directions[line]['legs'][0]['steps']) #路段數量
        print('路段數量:%d'%road_numbers)
        
        for i in range(road_numbers): #路段 1 2 3 4...
            # 導航文字整理   
            print('路段%d'%i)
            text=directions[line]['legs'][0]['steps'][i]['html_instructions']
            text=text.replace('<wbr>','')
            text=text.replace('<wbr/>','')
            text=text.replace('/','')
            text=text.replace('<b>','')
            text=text.replace('<div>','')
            text=text.replace('<div style="font-size:0.9em">','')
            text=text.replace('&nbsp;','')
            pprint(text)
            title.append(text) #導航文字匯入title list
            if i == 0 : #第0個路段 點0 & 點1 經緯度
                marker_points.append(f'({directions[line]["legs"][0]["steps"][i]["start_location"]["lat"]},{directions[line]["legs"][0]["steps"][i]["start_location"]["lng"]})')
                marker_points.append(f'({directions[line]["legs"][0]["steps"][i]["end_location"]["lat"]},{directions[line]["legs"][0]["steps"][i]["end_location"]["lng"]})')
                latitude_list.append(directions[line]['legs'][0]['steps'][i]['start_location']['lat'])
                longitude_list.append(directions[line]['legs'][0]['steps'][i]['start_location']['lng'])
                latitude_list.append(directions[line]['legs'][0]['steps'][i]['end_location']['lat'])
                longitude_list.append(directions[line]['legs'][0]['steps'][i]['end_location']['lng'])
                # 建立測站
                station_lat.append(directions[0]['legs'][0]['steps'][i]['start_location']['lat'])
                station_lng.append(directions[0]['legs'][0]['steps'][i]['start_location']['lng'])
                
            else: #其餘路段 點2 點3 點4... 經緯度
                marker_points.append(f'({directions[line]["legs"][0]["steps"][i]["end_location"]["lat"]},{directions[line]["legs"][0]["steps"][i]["end_location"]["lng"]})')
                latitude_list.append(directions[line]['legs'][0]['steps'][i]['end_location']['lat'])
                longitude_list.append(directions[line]['legs'][0]['steps'][i]['end_location']['lng'])
                # 建立測站
                station_distance=math.sqrt((latitude_list[i]-latitude_list[i-station_judge])**2+(longitude_list[i]-longitude_list[i-station_judge])**2)
                print("station_distance=",station_distance)
                if station_distance<0.025:
                    station_judge=station_judge+1
                    print("station_judge+")
                else:
                    station_space=int(station_distance/0.025)
                    for s in range(station_space):
                        station_lat.append(latitude_list[i-station_judge]+((latitude_list[i]-latitude_list[i-station_judge])/station_space)*(s+1))
                        station_lat.append(latitude_list[i]) 
                        station_lng.append(longitude_list[i-station_judge]+((longitude_list[i]-longitude_list[i-station_judge])/station_space)*(s+1))
                        station_lng.append(longitude_list[i])  
                    station_judge=1
        
        print('It totally takes %d minutes in prediction'%(duration_time/60))   
        
        route = gmplot.GoogleMapPlotter(latitude_list[0],longitude_list[0],18)  # 設定googlemaps視覺化 使用gmplot作圖
        
        # 中繼站設定
        waypoints_space=int((len(latitude_list)-7)/10) # 中繼站間隔 (中繼站不能太多!!)
        if ((len(latitude_list)-7)/10)-waypoints_space>=0.5 and waypoints_space>=2: # 中繼站間隔四捨五入
            waypoints_space=waypoints_space+1
        if waypoints_space<2: #中繼站間隔最少為2
            waypoints_space=2
        start=3 # 中繼站從第4個轉折點開始 (前面的點設為中繼站沒有意義!!)
        if len(latitude_list)<=4: # 避免轉折點太少 start變成負數
            start=1
        end=len(latitude_list)-3 # 接近終點設中繼站沒有意義!!
        if end <1:
            end=1
            
        for i in range(start,end,waypoints_space): #中繼站經緯度
        
            tupleA=(latitude_list[i],longitude_list[i]),(latitude_list[i+1],longitude_list[i+1])
            waypoints=waypoints+tupleA
        # 繪出測站點
        for i in range(len(station_lat)):
            route.marker(station_lat[i],station_lng[i], color='purple')
            
       # 用gmplot 將路徑可視化(gmplot無法選擇避免國道 因此透過中繼站 盡量避開國道)    
        route.directions(
            (origins[0]['geometry']['location']['lat'],origins[0]['geometry']['location']['lng']),
            (destinations[0]['geometry']['location']['lat'],destinations[0]['geometry']['location']['lng']),
            waypoints=waypoints)
        route.apikey = API_KEY #輸入金鑰
        route.draw( save_location ) #存檔


