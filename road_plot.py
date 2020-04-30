import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import datetime

fig = plt.figure()
ax = fig.add_subplot()
df11_tracks = pd.read_csv('11_tracks.csv')
df11_tm = pd.read_csv('11_tracksMeta.csv')

plt.hlines([0, -3.65,-15.22,-20.88,-32.54, -32.54-3.65],-50,450,colors='k', linestyles='solid', linewidth=0.5)
plt.hlines([-7.62,-11.42,-24.86,-28.48],-50,450,colors='k', linestyles=(0,(3,15)), linewidth=0.5)  
plt.axis('equal')
plt.text(-40, -50, "Frame num:")
plt.text(-40, -60, "Frame rate:")


total_frame = df11_tracks.shape[0]



def get_car_current_position(frame, car_running):
    car_current_position_list = []

    

    for idx, row in df11_tm.iterrows():        
        if frame - row['initialFrame'] == 0:
            car_running[row['id']] = frame - row['initialFrame'] + 1
        elif frame - row['finalFrame'] == 0:            
            del car_running[row['id']]
        else:
            if row['id'] in car_running.keys():                
                car_running[row['id']] = frame - row['initialFrame'] + 1
            else:
                pass   

    for k,v in car_running.items():
        id_rows  = df11_tracks[df11_tracks['id']==k]
        id_frame_row = id_rows[id_rows['frame']==v]
        if not id_frame_row.empty:
            car_current_position_list.append(
                [
                    id_frame_row['x'].item(), 
                    id_frame_row['y'].item(), 
                    id_frame_row['width'].item(), 
                    id_frame_row['height'].item()
                ]
            )
    
    return car_current_position_list

car_running = {}
    

for f in range(15277):
    start_time = datetime.datetime.now()
    frame = f+1

    car_running_position = get_car_current_position(frame, car_running)
    car_recs = []
    for car in car_running_position:       
        car_rec = []
        col = 'b'
        if car[2] > 10: col = 'g'       
        car_rec = patches.Rectangle((car[0], -1*car[1]-car[3]), car[2], car[3], color=col)
        ax.add_patch(car_rec)   
        car_recs.append(car_rec)
    txt = plt.text(0,-50, str(frame))
    end_time = datetime.datetime.now()
    duration = start_time - end_time    
    plt.pause(1/25)    
    for car in car_recs: car.remove()
    txt.remove()
 
    
    
plt.show()




