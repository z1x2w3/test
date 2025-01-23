import pyodbc
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def data_sol(position,force):
    position = np.array(position)
    force = np.array(force)
    max_position = round(np.max(position),1)
    max_force = round(np.max(force),1)
    sol_force = force[force >(max_force*0.01)]
    sol_position = position[len(force)-len(sol_force):]
    sol_position = sol_position-sol_position[0]
    return sol_position,sol_force

def import_data(test_file_path):#文件选择，导入实验数据
    data_dict = {}
    test_file_name = test_file_path.split('/')[-1].split('.')[0]
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+test_file_path)    
    query = 'SELECT * FROM testdata'
    data_frame = pd.read_sql(query,conn).sort_values('position')
    conn.close()
    for i in range(1,max(data_frame['num'])+1): #通过num进行分类
        data_name = test_file_name + ' 第' + str(i) + '组数据'
        df = data_frame[data_frame['num']==i]
        force_data = df.iloc[:,1]
        position_data = df.iloc[:,4]
        force_list = list(force_data)
        position_list = list(position_data)
        position_force_data = data_sol(position_list,force_list)
        data_dict1 = {
            data_name:position_force_data
            }
        data_dict.update(data_dict1)
    return data_dict

def data_deal(mov,force):
    f = np.array(force)
    m = np.array(mov)
    max_m = round(np.max(m),1)
    max_f = round(np.max(f),1)
    deal_mov = np.arange(0,max_m,0.1)
    fun = interp1d(m,f,kind='linear')
    deal_force = fun(deal_mov)
    deal_mov = deal_mov[:len(deal_force)]
    dict = [deal_mov,deal_force]
    return dict

def csv_deal(csv_path):
    csv_df = pd.read_csv(csv_path)
    cae_mov = list(csv_df.iloc[:,0])
    cae_force = list(csv_df.iloc[:,1])
    dict = [cae_mov,cae_force]
    return dict

def get_sheet_name(excel_path): #提取每个sheet的dataframe
    excel_df = pd.read_excel(excel_path,engine='openpyxl',sheet_name=None)
    sheet_names = [i for i in excel_df.keys() if i != '使用标准']
    sheet_name = []
    dict1 = []
    dict2 = []
    for sheet in sheet_names:
        sheet_df = pd.read_excel(excel_path,engine='openpyxl',sheet_name=sheet)
        for i in range(0,10):
            demo_l = str(sheet_df.columns[i*10+2])
            demo_w = str(sheet_df.columns[i*10+4])
            demo_h = str(sheet_df.columns[i*10+6])
            demo_name = str(sheet_df.columns[i*10])
            if demo_l.count('输入') or demo_w.count('输入') or demo_h.count('输入'):
                    continue
            else:
                name = sheet+' '+demo_name
                sheet_name.append(name)
                test_force = list(sheet_df.iloc[:,i*10+1])
                test_mov = list(sheet_df.iloc[:,i*10+4])
                dict1 = [test_mov,test_force]
                dict2.append(data_deal(test_mov,test_force))
    return sheet_name,dict1,dict2

def get_sheet_def(excel_path,sheet_name,demo_name):
    i = int(demo_name[2:])-1
    sheet_df = pd.read_excel(excel_path,engine='openpyxl',sheet_name=sheet_name)
    demo_l = str(sheet_df.columns[i*10+2])
    demo_w = str(sheet_df.columns[i*10+4])
    demo_h = str(sheet_df.columns[i*10+6])
    inf = sheet_name+' '+demo_name+"信息为长："+demo_l+'mm，宽：'+demo_w+'mm，厚：'+demo_h+'mm'
    test_force = list(sheet_df.iloc[:,i*10+1])
    test_mov = list(sheet_df.iloc[:,i*10+4])
    mf_dict = data_deal(test_mov,test_force)
    return inf,mf_dict