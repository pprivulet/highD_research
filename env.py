# observarion  {centerx,centery, width, height, distanceToLeftLane, distaneToRightLane, froneVehicleDis, backendVehicleDis, leftSideVehicleDis, rightSideVehicleDis}
# action {Vx, Vy, heading}
# trajectory {observation, action}



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

df11_tracks = pd.read_csv('11_tracks.csv')
df11_tm = pd.read_csv('11_tracksMeta.csv')
df11_rm = pd.read_csv('11_recordingMeta.csv')

