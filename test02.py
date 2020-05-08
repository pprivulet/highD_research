import csv
from decimal import Decimal
import os 
import pygame 
import time
import random

def init_pygame():
    x = 0
    y = 300
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    pygame.init()
    
    X = 1366
    Y = 118
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
        self.image = pygame.image.load(r'11_highway.png')
        self.image = pygame.transform.scale(self.image, (X, Y))
        self.road_lenth = road_lenth
        self.road_width = road_width
        self.X=X
        self.Y=Y
        
    def init_scenario(self):
        print('scenario initializing, please wait')
        self.frame_list = []
        self.frame_len = int(Decimal(self.recordingMeta['duration']) * int(self.recordingMeta['frameRate']))
        for i in range(self.frame_len):
            self.frame_list.append([])
        i_len = 0
        for i in self.tracksMeta:
            i_len = i_len + int(i['numFrames'])
        i = 0
        for row in self.tracks:
            self.frame_list[int(row['frame'])-1].append(row)
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
        while self.running:
            display_surface.fill(self.white)
            display_surface.blit(self.image, (0, 0))
            try:
                for row in self.frame_list[self.t_count - 1]:
                    #print(row['id'],row['x'],row['y'],row['width'],row['height'])
                    vehicle_color = self.vehicle_list[int(row['id'])-1]
                    a = float(row['x']) * self.X / self.road_lenth
                    b = (float(row['y'])+0.2) * self.Y / self.road_width
                    w = float(row['width']) * self.X / self.road_lenth
                    h = float(row['height']) * self.Y / self.road_width
                    points = [(a, b), (a+w, b), (a+w, b+h), (a, b+h)]
                    pygame.draw.polygon(display_surface, vehicle_color, points)
            except IndexError:
                print('scenario end')
                break 
            for event in pygame.event.get() : 
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()
            pygame.display.update()
            self.sleep()
            self.t_count = self.t_count + 1
    
    def sleep(self):
        local_time = time.time() - self.start_time
        sleep_time = self.t_count * self.timestep - local_time
        if sleep_time > 0.1:
            sleep_time = 0.1
        if sleep_time > 0:
            time.sleep(sleep_time)
        print('time:',self.t_count,sleep_time)

    def close(self):
        self.running = False
        
if __name__ == '__main__':
    display_surface = init_pygame()
    scenario_data = ScenarioData(11,420,36.12,1366,118)
    scenario_data.init_scenario()
    scenario_data.plot_scenario(display_surface)