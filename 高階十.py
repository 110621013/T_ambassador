'''
有一天，臺灣的火車路線從各站靠停變成兩地直達的類型了， 為了要抵達你心中的目的地，你可能會需要轉搭很多次車。
例：
你在車站看見這樣的火車行程表 [('臺北', '新竹'),('彰化','臺北'),('高雄','彰化'),('新竹','臺南')] 
如果今天你的出發點在'高雄'的話，應返回串列['高雄','彰化','臺北','新竹','臺南']

但如果給定行程[('臺北','臺中'),('臺中','臺南')]而出發點設為'臺中'的話， 返回值應為 null

注意：
如給定行程[('臺北','臺中'),('臺北','臺南'),('臺中','臺南'),('臺南','臺北')] 應返回串列[('臺北','臺中','臺南','臺北','臺南')] 
就算有另一答案為[('臺北','臺南','臺北','臺中','臺南')]也正確， 但串列的排序方式應由北到南優先排序
'''
# county(node) base假設是給定一個出發站，得到要走遍所有縣市的路線(最簡且從北到南)
# path base假設是給定一出發站，得到可走遍所有路徑且只走一次的路線

lat_str_of_county = {
    '臺北':'25N01’00”',
    '台北':'25N01’00”',
    '新北':'25N01’00”',
    '桃園':'24N59’00”',
    '新竹':'24N48’00”',
    '苗栗':'24N37’00”',
    '臺中':'24N11’00”',
    '台中':'24N11’00”',
    '彰化':'24N04’00”',
    '南投':'23N58’00”',
    '雲林':'23N45’00”',
    '嘉義':'23N29’00”',
    '臺南':'23N02’00”',
    '台南':'23N02’00”',
    '高雄':'22N38’00”',
    '屏東':'22N00’00”',
    '臺東':'22N45’00”',
    '台東':'22N45’00”',
    '花蓮':'23N59’00”',
    '宜蘭':'24N46’00”',
}

# county(node) base
class County():
    def __init__(self, name, lat_str):
        self.name = name
        self.lat = int(lat_str[0:2]) + int(lat_str[3:5])//60 + int(lat_str[6:8])//3600
        self.go_list = []
        self.dfs_pointer = -1
    def append_go_list(self, county):
        self.go_list.append(county)
    def renew_northernmost_go_list(self):
        import operator
        #print(self.name, 'before', [county.name for county in self.go_list])
        self.go_list = sorted(self.go_list, key=operator.attrgetter('lat'), reverse=True)
        #print(self.name, 'after ', [county.name for county in self.go_list])


# 單向圖，dict實作，DFS
class Graph():
    def __init__(self, travel_list):
        self.county_record = {}
        for i in range(len(travel_list)):
            begin_name, arrive_name = travel_list[i][0], travel_list[i][1]
            # for begin part
            if begin_name not in self.county_record.keys():
                new_county = County(name=begin_name, lat_str=lat_str_of_county[begin_name])
                self.county_record[begin_name] = new_county
            # for arrive part
            if arrive_name not in self.county_record.keys():
                new_county = County(name=arrive_name, lat_str=lat_str_of_county[arrive_name])
                self.county_record[arrive_name] = new_county
            self.county_record[begin_name].append_go_list( self.county_record[arrive_name] )
        # all renew
        for county in self.county_record.values():
            county.renew_northernmost_go_list()
    def get_start_walk_path(self, start_county_name):
        # init walk_county
        walk_county = []
        num_of_county = len(self.county_record.keys())
        if start_county_name not in self.county_record.keys():
            return None
        self.county_record[start_county_name].dfs_pointer += 1
        walk_county.append(self.county_record[start_county_name])
        # util done (DFS)
        while len(walk_county) != num_of_county:
            #print('->', [county.name for county in walk_county])
            if walk_county[-1].dfs_pointer < len(walk_county[-1].go_list): # 
                walk_county.append(walk_county[-1].go_list[ walk_county[-1].dfs_pointer ])
                walk_county[-1].dfs_pointer += 1
            else:
                poped_county = walk_county.pop()
                poped_county.dfs_pointer = -1
                if walk_county == []:
                    return None
                walk_county[-1].dfs_pointer += 1
        # reset dfs_pointer
        for county in walk_county:
            county.dfs_pointer = -1
        # return
        walk_path = []
        for county in walk_county:
            walk_path.append(county.name)
        return [tuple(walk_path)]


if __name__ == '__main__':
    # county(node) base
    travel_list_0 = [('臺北', '新竹'),('彰化','臺北'),('高雄','彰化'),('新竹','臺南')]
    graph_0 = Graph(travel_list_0)
    start_county_name = '高雄'
    walk_path = graph_0.get_start_walk_path(start_county_name)
    print(walk_path) #['高雄','彰化','臺北','新竹','臺南']
    
    # 多餘縣市測試
    travel_list_1 = [('臺北', '新竹'),('彰化','臺北'),('高雄','彰化'),('新竹','臺南')  ,('高雄','臺南'),('高雄','臺北')]
    graph_1 = Graph(travel_list_1)
    start_county_name = '高雄'
    walk_path = graph_1.get_start_walk_path(start_county_name)
    print(walk_path) #['高雄','彰化','臺北','新竹','臺南']
    
    # 不完整測試
    travel_list_2 = [('臺北', '新竹'),('彰化','臺北'),('新竹','臺南'),('高雄','臺南'),('高雄','臺北')]
    graph_2 = Graph(travel_list_2)
    start_county_name = '高雄'
    walk_path = graph_2.get_start_walk_path(start_county_name)
    print(walk_path) #應該None
    
    # 不完整測試
    travel_list_3 = [('臺北','臺中'),('臺中','臺南')]
    graph_3 = Graph(travel_list_3)
    start_county_name = '臺中'
    walk_path = graph_3.get_start_walk_path(start_county_name)
    print(walk_path) #應該None

    travel_list_4 = [('臺北','臺中'),('臺北','臺南'),('臺中','臺南'),('臺南','臺北')]
    graph_4 = Graph(travel_list_4)
    start_county_name = '臺北'
    walk_path = graph_4.get_start_walk_path(start_county_name)
    print(walk_path) #應該[('臺北','臺中','臺南','臺北','臺南')]
    # 這邊的問題是實際上[('臺北', '臺中', '臺南')]就可以走完全部了，不需要[('臺北','臺中','臺南','臺北','臺南')]
