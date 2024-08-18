import pygame
import math
import numpy as np
class ImageCreator:
    def __init__(self):
        self.dimensions= [200, 144]
        self.center = [100,220]
        self.start_val = [0,108]
        self.max_lenght = 220 #px
        pygame.init()
        self.surface = pygame.image.load("empty.png")



    def calc_new_coordinate(self,coordinate,distance):#TODO add also wrapper to get distancve from pixels to relative
        p = self.cart_to_polar(coordinate)
        dela_phi = distance/p[0] # assuming radius stays the SAME
        p[1] = p[1]+dela_phi
        return self.polar_to_cart(p)

    def cart_to_polar(self,coordinate):
        # Transform into Coordinate System from Center Circle
        x = coordinate[0] - self.center[0]
        y = coordinate[1] - self.center[1]
        # Transform into polar Coodinates
        r = math.sqrt(x*x+y*y) #should match the radius of the circle
        phi = math.atan(y/x)
        if x < 0 :
            phi = phi+ math.pi
        elif y < 0:
            phi = phi+2*math.pi
        return [r,phi]

    def polar_to_cart(self,coordinate):
        #Transform into Kartesian Coordiantes
        r = coordinate[0]
        phi = coordinate[1]
        x = r*math.cos(phi)
        y = r*math.sin(phi)
        #transform into Image coordinate System
        x = x + self.center[0]
        y = y + self.center[1]
        return [x,y]

    def save_image(self,name="arc_image.png"):
        pygame.image.save(self.surface, name)

    def draw_lines(self,subsections = 7):
        line = np.linspace(0,220,num=subsections) # if issues occur dtype=int
        for point in line:
            pygame.draw.circle(self.surface,color=1,center=self.calc_new_coordinate(self.start_val,point),radius=3)

        #pygame.draw.circle(self.surface, color=1, center=self.center, radius=150)
    def __del__(self):
        pygame.quit()


if __name__ == "__main__":
    creator = ImageCreator()
    creator.draw_lines()
    creator.save_image()
    #pygame.draw.ellipse(surface,color=(20, 20, 0),rect=[(-extendw), 72, width+2*extendw, height],width=line_width)
    #pygame.draw.arc(surface, (0, 0, 0), [-10, height/2, width+20, height], 0, 3.15, 4)
    #pygame.draw.arc(surface, (255, 255, 255), [(-extendw), 72, width+2*extendw, height], 0, 0.7, line_width+1)
    #pygame.draw.arc(surface, (255, 255, 255), [(-extendw), 72, width+2*extendw, height],  2.5, 3.14,line_width+1)
    #pygame.draw.circle(surface,color=0,center=start_val,radius=3)

