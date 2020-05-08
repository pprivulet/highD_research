import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot()


plt.hlines([0, -3.65,-15.22,-20.88,-32.54, -32.54-3.65],-50,450,colors='k', linestyles='solid', linewidth=0.5)
plt.hlines([-7.62,-11.42,-24.86,-28.48],-50,450,colors='k', linestyles=(0,(3,15)), linewidth=0.5)  
plt.axis('equal')
plt.text(-40, -50, "Frame num:")
plt.text(-40, -60, "Frame delay:")


df11_tracks = pd.read_csv('11_tracks.csv')
df11_tm = pd.read_csv('11_tracksMeta.csv')
df11_rm = pd.read_csv('11_recordingMeta.csv')

track_meta = {}

global_frame_num = df11_tm['finalFrame'].to_numpy()[-1]



for frame in range(1, global_frame_num + 1):
    track_meta[frame] = df11_tracks[df11_tracks['frame']==frame]

for frame in range(1, global_frame_num + 1):
    start_time = time.time()   
    car_recs = []
    for idx, row in track_meta[frame].iterrows():     
        car_rec = []
        col = 'b'
        if row['width'] > 10: col = 'g'       
        car_rec = patches.Rectangle((row['x'], -1*row['y']-row['height']), row['width'], row['height'], color=col)
        ax.add_patch(car_rec)   
        car_recs.append(car_rec)
    txt = plt.text(0,-50, str(frame))
    end_time = time.time()
    duration = end_time - start_time
    txt_d = plt.text(0,-60, str(duration))  
    plt.pause(1/25)   
       
    for car in car_recs: car.remove()
    txt.remove()
    txt_d.remove()

    
plt.show()

