import os
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense, Flatten
import matplotlib.pyplot as plt

#在/data2/3T/rain_pre_dnn執行

def dnn_8_v1(var_num):
    model = Sequential()
    model.add(tf.keras.Input(shape=(var_num), batch_size=None))
    model.add(Flatten())
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    return model
def dnn_4_v1(var_num):
    model = Sequential()
    model.add(tf.keras.Input(shape=(var_num), batch_size=None))
    model.add(Flatten())
    model.add(Dense(4, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    return model
def summarize_diagnostics(history, model_name, save_path):
    # plot loss
    plt.subplot(211)
    plt.title(model_name+' Cross Entropy Loss')
    plt.plot(history.history['loss'], color='blue', label='train')
    plt.plot(history.history['val_loss'], color='orange', label='test')
    plt.legend()
    # plot accuracy
    plt.subplot(212)
    plt.title(model_name+' Classification accuracy')
    plt.plot(history.history['accuracy'], color='blue', label='train')
    plt.legend()
    # save plot to file
    plt.savefig(os.path.join(save_path, model_name))
    plt.close()
def cal_ETS_F1(model_name, model, x_test, y_test, yes_thr=0.5):
    print('=== cal_ETS_F1 ===', model_name)
    output = model.predict(x_test)
    a,b,c,d=0,0,0,0
    for i in range(y_test.shape[0]):
        if y_test[i,1]==1.0 and output[i,1]>=yes_thr:
            a += 1
        elif y_test[i,1]==0.0 and output[i,1]>=yes_thr:
            b += 1
        elif y_test[i,1]==1.0 and output[i,1]<yes_thr:
            c += 1
        elif y_test[i,1]==0.0 and output[i,1]<yes_thr:
            d += 1
        else:
            print('??? cal_ETS_F1 wtf ???')
            return
    # ETS
    ar = (a+b)*(a+c)/(a+b+c+d)
    if ar == 0:
        ets = 0
    else:
        ets = (a-ar)/(a+b+c-ar)
    print('-> {} thr{:.3f} ets:{:.6f}\n'.format(model_name, yes_thr, ets))
    with open(os.path.join('.', 'ETS.txt'), 'a') as f:
        f.write('-> {} thr{:.3f} ets:{:.6f}\n'.format(model_name, yes_thr, ets))
    # F1
    F1 = 2*(a/(a+b))*(a/(a+c)) / (a/(a+b) + a/(a+c))
    print('-> {} thr{:.3f} F1:{:.6f}\n'.format(model_name, yes_thr, F1))
    with open(os.path.join('.', 'F1.txt'), 'a') as f:
        f.write('-> {} thr{:.3f} F1:{:.6f}\n'.format(model_name, yes_thr, F1))
            
## !!還沒做完!!
def SHAP():
    #平均將預測的絕對概率改變了???個百分點
    import shap
    shap_path = os.path.join('.', 'shap')
    
    # create name_list
    datadeal_type_list = ['no', 'oversampling']
        
    # plot
    for datadeal_type in datadeal_type_list:
        for dnn_num in ['4', '8']:
            name = 'dnn_{}_{}'.format(datadeal_type, dnn_num)
            model = load_model(os.path.join('.', name+'.h5'))
            x_train, _ = get_data_x_y('train', datadeal_type)
            x_test, _ = get_data_x_y('test', datadeal_type)
            
            for random_choice_i in range(5):
                print('random_choice_i', random_choice_i)
                x_train_picked = x_train[np.random.choice(x_train.shape[0], 1000, replace=False)]
                x_test_picked = x_test[np.random.choice(x_test.shape[0], 1000, replace=False)]
                    
                explainer = shap.DeepExplainer(model, x_train_picked) 
                shap_values = explainer.shap_values(x_test_picked) #shap_values is list(len=2) / shap_values[0].shape = (1000, 114)
                    
                # summary_plot
                shap.summary_plot(shap_values[0], plot_type='bar', feature_names=['lat','lon','time','temp','rh','ws','rainfall','dbz'], show=False)
                plt.savefig(os.path.join(shap_path, 'shap_summary_plot_{}_{}'.format(name, str(random_choice_i)) ))
                plt.close()
                    
                # waterfall_plot (only 0)
                #shap.waterfall_plot(shap_values[0], max_display=20, show=False)
                #shap.plots._waterfall.waterfall_legacy(explainer.expected_value[0], shap_values[0][0], show=False)
                #plt.savefig(os.path.join(shap_path, 'shap_waterfall_plot_{}_{}'.format(name, str(random_choice_i)) ))
                #plt.close()


def make_var_arr():
    import pandas as pd
    num_list=[466880,466900,466920,466940,466950,466990,467050,467060,467080,467110,467270,467300,467350,467410,467420,467440,467441,467480,467490,467540,467571,467590,467610,467620,467660]
    #---觀測氣象要素---
    #測站經緯度擷取
    '''
    with open(os.path.join('.', 'stationID.txt')) as id_f:
        id_data_list=[]
        for line in id_f.readlines():
            for num in num_list:
                if line[0:6] == str(num):
                    a = line.find('lon=')
                    b = line.find('lat=')
                    if b == -1:
                        break
                    else: 
                        lon = line[(a+4):(a+14)]
                        lat = line[(b+4):(b+13)]
                        data=[num,lat,lon]
                        id_data_list.append(data)
    id_data_array = pd.DataFrame(id_data_list)
    id_data_array.columns = ['sta_id','lat','lon']

    #CSV
    var_arr = np.full((13104*24, 8), np.nan, dtype=np.float64)
    obs_path = os.path.join('..', 'obs')

    counter = 0
    all_file_list = os.listdir(obs_path)
    all_file_list.sort()
    for filename in all_file_list:
        if int(filename[:6]) not in num_list or '2021' not in filename:
            continue
        df = pd.read_csv(os.path.join(obs_path, filename))
        columns = df[['hour','TX01','RH01','WD01','PP01']]
        columns.rename(columns={'hour': 'time'}, inplace=True)
        columns.replace(-9998,0.1)
        
        #合併經緯度
        for i in range(len(id_data_array)):
            if id_data_array['sta_id'][i] == int(filename[:6]) :       
                columns.insert(0,'lat',float(id_data_array['lat'][i]))
                columns.insert(1,'lon',float(id_data_array['lon'][i]))

        print(var_arr[0])
        print(var_arr[13104-1])
        print(var_arr[13104])
        print(var_arr[13104*2-1])
        print(var_arr[13104*2])
        
        array=columns.values
        #print(filename, array.shape)
        var_arr[counter:counter+array.shape[0], :7] = array
        
        counter += array.shape[0]
    #print(counter)
    assert counter == 13104*24
    
    #---雷達資料---
    import pygrib as pb
    radar_path = os.path.join('..', 'radar')
    '''
    #print(all_file_list)
    ''' 看沒有的
    selected_file_list = []
    for fn in all_file_list:
        if fn.split('.')[0][-2:] == '00':
            selected_file_list.append(fn)
        if fn == '202207010000.grb2':
            break
    print(len(selected_file_list))
    #print(selected_file_list)
    
    mon_day=[31,28,31,30,31,30,31,31,30,31,30,31]
    y, m, d, h = 2021, 1, 1, 0
    counter = 0
    while True:
        if y==2022 and m==7 and d==1 and h==0:
            break
        ys = str(y)
        ms = str(m) if m//10 != 0 else '0'+str(m)
        ds = str(d) if d//10 != 0 else '0'+str(d)
        hs = str(h) if h//10 != 0 else '0'+str(h)
        s = '{}{}{}{}00.grb2'.format(ys,ms,ds,hs)
        if s not in selected_file_list:
            print(counter, s)
            counter += 1
        
        h += 1
        if h == 24:
            h = 0
            d += 1
        if d == mon_day[m-1]+1:
            d = 1
            m += 1
        if m == 13:
            m = 1
            y += 1
    '''
    '''
    print()
    print('---雷達資料---')
    mon_day=[31,28,31,30,31,30,31,31,30,31,30,31]
    station_lonlat = {
        466880:[121.442017,24.997647],
        466900:[121.448906,25.164889],
        466920:[121.514853,25.037658],
        466940:[121.740475,25.133314],
        466950:[122.079744,25.627975],
        466990:[121.613275,23.975128],
        467050:[121.047486,25.006744],
        467060:[121.857372,24.596736],
        467080:[121.756528,24.763975],
        467110:[118.289281,24.407306],
        467270:[120.581348,23.873776],
        467300:[119.667467,23.256950],
        467350:[119.563094,23.565503],
        467410:[120.204772,22.993239],
        467420:[120.236700,23.038386],
        467440:[120.315733,22.565992],
        467441:[120.312389,22.730500],
        467480:[120.432906,23.495925],
        467490:[120.684075,24.145736],
        467540:[120.903789,22.355675],
        467571:[121.014219,24.827853],
        467590:[120.746339,22.003897],
        467610:[121.373428,23.097486],
        467620:[121.558339,22.036969],
        467660:[121.154586,22.752211],
    }
    lon_begin, lat_begin, reso = 115.0, 18.0, 0.0125
    skip_station_id = 467441
    
    y, m, d, h = 2021, 1, 1, 0
    for t_i in range(13104):
        ys = str(y)
        ms = str(m) if m//10 != 0 else '0'+str(m)
        ds = str(d) if d//10 != 0 else '0'+str(d)
        hs = str(h) if h//10 != 0 else '0'+str(h)
        fn = '{}{}{}{}00.grb2'.format(ys,ms,ds,hs)
        print('t_i, fn', t_i, fn)
        
        if not os.path.exists(os.path.join(radar_path, fn)):
            h += 1
            if h == 24:
                h = 0
                d += 1
            if d == mon_day[m-1]+1:
                d = 1
                m += 1
            if m == 13:
                m = 1
                y += 1
            if y==2022 and m==6 and d==1 and h==1:
                skip_station_id = 467440
            continue
        grbs_obj = pb.open(os.path.join(radar_path, fn))
        try:
            radar_data_arr = grbs_obj.select()[0].values.data
            #plt.contourf(radar_data_arr)
            #plt.colorbar()
            #plt.title(fn)
            #plt.show()
        except ValueError:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', fn)
        #print(type(radar_data_arr), radar_data_arr.shape)
        
        s_counter = 0
        for station_id, lonlat in station_lonlat.items():
            if station_id == skip_station_id:
                continue
            lat_inx = round((lonlat[1]-lat_begin)/reso)
            lon_inx = round((lonlat[0]-lon_begin)/reso)
            var_arr[t_i+s_counter*13104, 7] = radar_data_arr[lat_inx, lon_inx]
            #print(t_i+s_counter*13104, radar_data_arr[lat_inx, lon_inx])
            s_counter += 1
        assert s_counter == 24

        #print(var_arr[0])
        #print(var_arr[1])
        #print(var_arr[13104-1])
        
        #print(var_arr[13104])
        #print(var_arr[13104+1])
        #print(var_arr[13104*2-1])
        #print('--------------------------')
    
        h += 1
        if h == 24:
            h = 0
            d += 1
        if d == mon_day[m-1]+1:
            d = 1
            m += 1
        if m == 13:
            m = 1
            y += 1
        if y==2022 and m==6 and d==1 and h==1:
            skip_station_id = 467440
    print(y,m,d,h)
    assert y==2022 and m==7 and d==1 and h==0
    
    np.save('var_arr.npy', var_arr) #(13104*24, 8)
    '''
    
    var_arr = np.load('var_arr.npy')
    n = 13104
    print(var_arr.shape)
        
    #做label
    y_arr = np.full((n*24, 1), -1, dtype=np.float64)
    for i in range(n*24-1):
        if var_arr[i+1, 6] > 0.0:
            y_arr[i] = 1.0
        else:
            y_arr[i] = 0.0
        
    # 去除不同測站之點
    #print(var_arr.shape)
    #print(n-1, var_arr[n-1], y_arr[n-1])
    #print(n, var_arr[n], y_arr[n])    
    #print(var_arr[-1], y_arr[-1])
    var_arr = np.delete(var_arr, [n*i-1 for i in range(1, 24+1)], axis = 0)
    y_arr = np.delete(y_arr, [n*i-1 for i in range(1, 24+1)], axis = 0)
    #print(var_arr.shape)
    #print((n-1)-1, var_arr[(n-1)-1], y_arr[(n-1)-1])
    #print((n-1), var_arr[(n-1)], y_arr[(n-1)])
    #print(var_arr[-1], y_arr[-1])
    
    # 測站[6]-9998是雨跡，dbz<0或9999就=0
    for i in range(var_arr.shape[0]):
        if var_arr[i,6] == -9998.0:
            var_arr[i,6] = 0.1
        if var_arr[i,7] < 0.0 or var_arr[i,7]==9999:
            var_arr[i,7] = 0.0
    
    # 測站-9991 -9996 -9997 -9999不要，雷達 nan 也不要
    no_list = []
    for i in range(var_arr.shape[0]):
        if  -9991 in var_arr[i] or \
            -9996 in var_arr[i] or \
            -9997 in var_arr[i] or \
            -9999 in var_arr[i] or \
            np.isnan(var_arr[i,7]) or\
            var_arr[i,7] == 9999.0:
            no_list.append(i)
    var_arr = np.delete(var_arr, no_list, axis = 0)
    y_arr = np.delete(y_arr, no_list, axis = 0)
    print('delete no_list:', len(no_list))
    
    print(var_arr.shape, y_arr.shape) #309500
    print('------->', np.count_nonzero(y_arr)) #25343
    
    np.save('var_arr_2.npy', var_arr)
    np.save('y_arr.npy', y_arr)
    
def record_var_range():
    var_name_list = ['lat','lon','time','temp','rh','ws','rainfall','dbz']
    var_range_dict = {}
    print('--- recore_var_range ---')
    with open(os.path.join('.', 'record_var_range.txt'), 'a') as f:
        var_arr = np.load(os.path.join('.', 'var_arr_2.npy')) #(?, 8)
        for i in range(len(var_name_list)):
            f.write('{} min={:.6f}, max={:.6f}\n'.format(var_name_list[i], np.nanmin(var_arr[:,i]), np.nanmax(var_arr[:,i])))
            var_range_dict[var_name_list[i]] = [np.nanmin(var_arr[:,i]), np.nanmax(var_arr[:,i])]
        
        f.write('---record_var_range over---')
        np.save('var_range_dict.npy', var_range_dict)

def print_var_arr_2():
    var_arr_2 = np.load('var_arr_2.npy')
    y_arr = np.load('y_arr.npy')
    for i in range(len(var_arr_2)):
        print(i, var_arr_2[i], y_arr[i, 0])

# 縮放、oversampling
# var_arr是純粹拚好var，var_arr_2是挑掉壞資料並給出匹配y_arr
def make_dataset_npy():
    x_arr = np.load('var_arr_2.npy') #(309500, 8)
    var_name_list = ['lat','lon','time','temp','rh','ws','rainfall','dbz']
    var_range_dict = np.load(os.path.join('.', 'var_range_dict.npy'), allow_pickle=True).item()
    
    for v_i in range(x_arr.shape[1]):
        x_arr[:, v_i] = np.interp(x_arr[:, v_i], (var_range_dict[var_name_list[v_i]][0], var_range_dict[var_name_list[v_i]][1]), (0, 1))
    np.save('x_arr.npy', x_arr)
    
    #for v_i in range(x_arr.shape[1]):
    #    print(np.min(x_arr[:, v_i]), np.max(x_arr[:, v_i]))
    #print(x_arr)
    
    # oversampling flatten
    x_arr = np.load(os.path.join('.', 'x_arr.npy'))
    y_arr = np.load(os.path.join('.', 'y_arr.npy'))
    bool_y = np.reshape((y_arr!=0), (y_arr.shape[0]))
    print('np.count_nonzero(bool_y):', np.count_nonzero(bool_y))
    
    pos_x = x_arr[bool_y]
    neg_x = x_arr[~bool_y]
    pos_y = y_arr[bool_y]
    neg_y = y_arr[~bool_y]

    ids = np.arange(len(pos_x))
    choices = np.random.choice(ids, len(neg_x))
    res_pos_x = pos_x[choices]
    res_pos_y = pos_y[choices]
    #print('res_pos_x.shape:', res_pos_x.shape)

    res_x = np.concatenate([res_pos_x, neg_x], axis=0)
    res_y = np.concatenate([res_pos_y, neg_y], axis=0)
    order = np.arange(len(res_y))
    np.random.shuffle(order)
    res_x = res_x[order]
    res_y = res_y[order]
    print('res_x.shape:', res_x.shape)
    print('res_y.shape:', res_y.shape)
    
    np.save(os.path.join('.', 'x_arr_oversampling.npy'), res_x) #568314
    np.save(os.path.join('.', 'y_arr_oversampling.npy'), res_y)
        
    
def get_data_x_y(train_or_test, datadeal_type, if_to_categorical=True):
    if datadeal_type == 'no':
        data_x = np.load(os.path.join('.', 'x_arr.npy')) #(309500, 8)
        data_y = np.load(os.path.join('.', 'y_arr.npy'))
        train_num = int(309500*0.7)
    elif datadeal_type == 'oversampling':
        data_x = np.load(os.path.join('.', 'x_arr_oversampling.npy')) #(568314, 8)
        data_y = np.load(os.path.join('.', 'y_arr_oversampling.npy'))
        train_num = int(568314*0.7)
    else:
        print('---> get_data_x_y error <---')
        return
    
    if train_or_test == 'train':
        data_x = data_x[:train_num]
        data_y = data_y[:train_num]
        #print('train data shape:', data_x.shape, data_y.shape)
        #print('->', data_x.shape, np.unique(data_x, return_counts=True))
        #print('->', data_y.shape, np.unique(data_y, return_counts=True))
    elif train_or_test == 'test':
        data_x = data_x[train_num:]
        data_y = data_y[train_num:]
        #print('test data shape:', data_x.shape, data_y.shape)
        #print('->', data_x.shape, np.unique(data_x, return_counts=True))
        #print('->', data_y.shape, np.unique(data_y, return_counts=True))
    else:
        print('get_data_x_y train_or_test error!!!')
    if if_to_categorical:
        data_y = to_categorical(data_y, 2)
    return data_x, data_y

def main_dnn():
    print('__main__ gogo')
    save_path = os.path.join('.')
    
    for datadeal_type in ['no', 'oversampling']:
        x_train, y_train = get_data_x_y(train_or_test='train', datadeal_type=datadeal_type)
        x_test, y_test = get_data_x_y(train_or_test='test', datadeal_type=datadeal_type)
        
        model_dict = {
            'dnn_{}_8'.format(datadeal_type):dnn_8_v1(8),
            'dnn_{}_4'.format(datadeal_type):dnn_4_v1(8),
        }

        for model_name, model in model_dict.items():
            print('-----==========',model_name,'==========-----')
            #model.summary()

            if os.path.isfile(os.path.join(save_path, model_name+'.h5')):
                print(model_name+' is trained, just load')
                model = load_model(os.path.join(save_path, model_name+'.h5'))
            else:
            # train
                model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer='adam', metrics=['accuracy']) #loss='categorical_crossentropy'
                earlystop = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
                train_history = model.fit(x_train, y_train, epochs=50, batch_size=1024, callbacks=[earlystop], shuffle=True, validation_split=0.2, verbose=1) #validation_data=(x_test, y_test)
                summarize_diagnostics(train_history, model_name, save_path)
                # save
                save_model(model, os.path.join(save_path, model_name+'.h5'))

                # test
                _, acc = model.evaluate(x_test, y_test, verbose=0)
                print('-----> acc: {:.6f}% <-----'.format(acc*100.0))
                
        for model_name, model in model_dict.items():
            model = load_model(os.path.join(save_path, model_name+'.h5'))
            if 'oversampling' == datadeal_type:
                yes_thr=(309500-25343)/309500
            else:
                yes_thr=0.5
            cal_ETS_F1(model_name, model, x_test, y_test, yes_thr=yes_thr)
            


if __name__ == '__main__':
    #print_var_arr_2()
    #make_var_arr()
    #record_var_range()
    #make_dataset_npy()
    #print_var_arr_2()
    #main_dnn()
    SHAP()