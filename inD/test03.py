import csv
from decimal import Decimal
import os 
import pygame 
import time
import random
import math

def init_pygame():
    x = 0
    y = 50
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    pygame.init()
    
    X = 900
    Y = 600
    ds = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Image')

    return ds

class ScenarioData():
    def __init__(self,map_id,road_lenth,road_width,X,Y):
        self.recordingMeta = csv.DictReader(open(str(map_id) + '_recordingMeta.csv')).__next__()
        self.tracks = csv.DictReader(open(str(map_id) + '_tracks.csv'))
        self.tracksMeta = csv.DictReader(open(str(map_id) + '_tracksMeta.csv'))
        self.running = True
        self.timestep = 1/25
        self.start_time = 0
        self.t_count = 1
        self.white = (255, 255, 255)
        self.image = pygame.image.load(str(map_id)+'_background.png')
        self.image = pygame.transform.scale(self.image, (X, Y))
        self.road_lenth = road_lenth
        self.road_width = road_width
        self.X=X
        self.Y=Y
        
    def init_scenario(self):
        print('scenario initializing, please wait')
        self.frame_list = []
        self.frame_len = int(Decimal(self.recordingMeta['duration']) * int(float(self.recordingMeta['frameRate'])))
        for i in range(self.frame_len):
            self.frame_list.append([])
        i_len = 0
        for i in self.tracksMeta:
            i_len = i_len + int(i['numFrames'])
        i = 0
        for row in self.tracks:
            self.frame_list[int(row['frame'])].append(row)
            if i%10000 == 0: 
                print('scenario initializing, please wait',i,'/',i_len)
            i = i + 1
        self.numVehicles = int(self.recordingMeta['numVehicles'])
        self.vehicle_list = []
        for i in range(self.numVehicles):
            self.vehicle_list.append(pygame.Color(int(random.random()*256), int(random.random()*256), int(random.random()*256)))
        # for i in range(len(self.frame_list)):
            # print(i+1,len(self.frame_list[i]))

    def plot_scenario(self,display_surface):
        print('scenario start')
        self.start_time = time.time()
        # max_x=0
        # min_x=100
        # max_y=0
        # min_y=100
        while self.running:
            display_surface.fill(self.white)
            display_surface.blit(self.image, (0, 0))
            try:
                for row in self.frame_list[self.t_count - 1]:
                    # print(row['trackId'],row['xCenter'],row['yCenter'],
                        # row['heading'],row['width'],row['length'])
                    # if max_x<float(row['xCenter']):
                        # max_x=float(row['xCenter'])
                    # if min_x>float(row['xCenter']):
                        # min_x=float(row['xCenter'])
                    # if max_y<float(row['yCenter']):
                        # max_y=float(row['yCenter'])
                    # if min_y>float(row['yCenter']):
                        # min_y=float(row['yCenter'])
                    vehicle_color = self.vehicle_list[int(row['trackId'])-1]
                    a = float(row['xCenter']) * self.X / self.road_lenth
                    b = -(float(row['yCenter'])) * self.Y / self.road_width
                    w = float(row['width']) * self.X / self.road_lenth / 2
                    l = float(row['length']) * self.Y / self.road_width / 2
                    h = (90-float(row['heading'])) / 180 * math.pi
                    sin_h = math.sin(h)
                    #sin_h = 0
                    cos_h = math.cos(h)
                    #cos_h = 1
                    points = [
                        (a+w*cos_h-l*sin_h, b+w*sin_h+l*cos_h), 
                        (a+w*cos_h+l*sin_h, b+w*sin_h-l*cos_h), 
                        (a-w*cos_h+l*sin_h, b-w*sin_h-l*cos_h), 
                        (a-w*cos_h-l*sin_h, b-w*sin_h+l*cos_h)]
                    pygame.draw.polygon(display_surface, vehicle_color, points)
                pygame.display.update()
            except IndexError:
                print('scenario end')
                #print(min_x,max_x,'/n',min_y,max_y)
                break
            for event in pygame.event.get() : 
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()
            self.sleep()
            self.t_count = self.t_count + 1
            # if self.t_count%250 == 0: 
                # pygame.display.update()
                # print(self.t_count,'/',self.frame_len,'running')
    
    def sleep(self):
        local_time = time.time() - self.start_time
        sleep_time = self.t_count * self.timestep - local_time
        if sleep_time > 0.1:
            sleep_time = 0.1
        if sleep_time > 0:
            time.sleep(sleep_time)
        print('time:',self.t_count,sleep_time,len(self.frame_list[self.t_count - 1]))

    def close(self):
        self.running = False
        
if __name__ == '__main__':
    display_surface = init_pygame()
    scenario_data = ScenarioData(32,(84.1939-5.22106)*1.45,(65.00644+1.68455)*1.15,900,600)
    scenario_data.init_scenario()
    scenario_data.plot_scenario(display_surface)