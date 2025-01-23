import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def yddq(position,force,cae_mov_bz,cae_force_bz):
    position = np.array(position)
    force = np.array(force)
    fun = interp1d(force,position,kind='linear')
    position_bz = fun(cae_force_bz)
    sol_position = position-position_bz
    fun = interp1d(sol_position,force,kind='linear')
    max_position = round(np.max(sol_position),1)
    deal_mov = np.arange(0,max_position,0.1)
    deal_force = fun(deal_mov)
    slop,intercept = np.polyfit(deal_mov[0:2],deal_force[0:2],1)
    # x_0 = -(intercept/slop)
    # deal_mov = deal_mov - x_0
    # sol_position = sol_position-intercept
    append_mov = np.arange(-cae_mov_bz+0.1,0,0.1)
    append_force = [slop*i+intercept for i in append_mov]
    deal_mov = np.append(append_mov,deal_mov)
    deal_force = np.append(append_force,deal_force)
    return deal_mov,deal_force


def inter(position,force):
    position = np.array(position)
    force = np.array(force)
    max_position = round(np.max(position),1)
    max_force = round(np.max(force),1)
    deal_position = np.arange(0,max_position,0.1)
    fun = interp1d(position,force,kind='linear')
    deal_force = fun(deal_position)
    return deal_position,deal_force

def data_deal(position,force,cae_mov,cae_force):
    force_list = list(force)
    position_list = list(position)
    inter_position,inter_force = inter(position_list,force_list)
    inter_position_force_slop = []

    for n in range(len(inter_position)-1):
        slop,intercept = np.polyfit(inter_position[n:n+2],inter_force[n:n+2],1)
        inter_position_force_slop.append(slop)

    for n in range(len(inter_position_force_slop)-1):
        if inter_position_force_slop[n] > 10:
            inter_position = inter_position[n:]
            inter_force = inter_force[n:]
            inter_position_force_slop = inter_position_force_slop[n:]
            for n in range(len(inter_position_force_slop)-3):
                i = abs(inter_position_force_slop[n]-inter_position_force_slop[n+1])
                j = abs(inter_position_force_slop[n]-inter_position_force_slop[n+2])
                k = abs(inter_position_force_slop[n]-inter_position_force_slop[n+3])
                if i < 10 and j < 10 and k < 10:
                    inter_position = inter_position[n:]
                    inter_force = inter_force[n:]
                    break
            break
    cae_force_bz = cae_force[np.abs(inter_force[0]-cae_force).argmin()]
    cae_mov_bz = cae_mov[np.abs(inter_force[0]-cae_force).argmin()]
    deal_mov,deal_force = yddq(position,force,cae_mov_bz,cae_force_bz)
    deal_mov = deal_mov+cae_mov_bz
    return deal_mov,deal_force

def csv_deal(csv_path):
    csv_df = pd.read_csv(csv_path)
    cae_mov = list(csv_df.iloc[:,0])
    cae_force = list(csv_df.iloc[:,1])
    dict = [cae_mov,cae_force]
    return dict