import pandas as pd
import numpy as np

def close(position,force):
    position = np.array(position)
    force = np.array(force)
    max_position = round(np.max(position),1)
    max_force = round(np.max(force),1)
    deal_position = np.arange(0,max_position,0.1)
    deal_force = []
    for i in deal_position:
        deal_force.append(force[np.abs(position-i).argmin()])
    return deal_position,deal_force

def data_deal(position,force):
    force_list = list(force)
    position_list = list(position)
    close_position,close_force = close(position_list,force_list)
    close_position_force_slop = []

    for n in range(len(close_position)-1):
        slop,intercept = np.polyfit(close_position[n:n+2],close_force[n:n+2],1)
        close_position_force_slop.append(slop)
    for n in range(len(close_position_force_slop)-1):
        if close_position_force_slop[n] > 10:
            close_position = close_position[n:]
            close_force = close_force[n:]
            close_position_force_slop = close_position_force_slop[n:]
            for n in range(len(close_position_force_slop)-3):
                i = abs(close_position_force_slop[n]-close_position_force_slop[n+1])
                j = abs(close_position_force_slop[n]-close_position_force_slop[n+2])
                k = abs(close_position_force_slop[n]-close_position_force_slop[n+3])
                if i < 10 and j < 10 and k < 10:
                    close_position = close_position[n:]
                    close_force = close_force[n:]
                    break
            break
    return [close_position,close_force]

def csv_deal(csv_path):
    csv_df = pd.read_csv(csv_path)
    cae_mov = list(csv_df.iloc[:,0])
    cae_force = list(csv_df.iloc[:,1])
    dict = [cae_mov,cae_force]
    return dict
