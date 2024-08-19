import pygame
import math
import numpy as np
class ImageCreator:
    def __init__(self):
        self.dimensions= [200, 144]
        self.center = [100,220]
        self.start_val = [0,108]
        self.max_lenght = 220 #px
        self.title_higth = 43
        self.icon_size = [43,43]
        self.icon_only = [70,70]
        self.font_text = "Nasa21-l23X.ttf"
        self.font_numbers = "Pixellettersfull-BnJ5.ttf"
        pygame.init()
        pygame.font.init()
        self.surface = pygame.image.load("empty.png")
        self.lines_end_points = [] #allows us to later refer to those lines.




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

    def draw_lines(self,subsections = 5,line_length = 12, line_width=3,fill=False):
        line = np.linspace(0,220,num=subsections) # if issues occur dtype=int
        for segment in line:
            point = self.calc_new_coordinate(self.start_val,segment)
            line_end = self.move_point_R_direction(point, line_length)
            self.lines_end_points.append(line_end)
            #pygame.draw.circle(self.surface,color=1,center=point,radius=3)
            pygame.draw.line(self.surface,color=1,start_pos=point,end_pos=line_end,width=line_width)

        #pygame.draw.circle(self.surface, color=1, center=self.center, radius=150)

    def set_legend(self,start,end,center=None,size = 16,unit=None):
        legend_font = pygame.font.Font(self.font_numbers, size)
        #Start
        text_surface = legend_font.render(start, False, 1)
        self.surface.blit(text_surface, self.lines_end_points[0])
        #END
        text_surface = legend_font.render(end, False, 1)
        pose = self.lines_end_points[-1]
        pose[0] -= text_surface.get_width() # makes sure that all the Text is visible
        self.surface.blit(text_surface, pose)
        #Center
        if center is not None :
            #get center line
            entrys = len(self.lines_end_points)
            if entrys%2 != 0: #only continue if there is a center
                text_surface = legend_font.render(center, False, 1)
                pose = self.lines_end_points[int((entrys-1)/2)]
                pose = self.move_point_R_direction(pose,2) # get some Distance to the Line
                pose[0] -= text_surface.get_width()/2  # makes sure that all the Text is centered
                self.surface.blit(text_surface, pose)
        if unit is not None :
            text_surface = legend_font.render(unit, False, 1)
            self.surface.blit(text_surface, [self.dimensions[0]/2-text_surface.get_width()/2,self.dimensions[1]-text_surface.get_height()])

    def set_title(self,Title,size=22):
        title_font = pygame.font.Font(self.font_text, size)
        text_surface = title_font.render(Title, False, 1)
        pose = [self.dimensions[0]/2-text_surface.get_width()/2,self.title_higth]
        self.surface.blit(text_surface, pose)
    def move_point_R_direction(self, point, line_length):
        polar_point = self.cart_to_polar(point)
        polar_point[0] -= line_length  # adjust r the way you like
        line_end = self.polar_to_cart(polar_point)
        return line_end

    def add_icon(self,file,icon_only=False):
        icon = pygame.image.load(file)
        if icon_only:
            icon = pygame.transform.scale(icon, self.icon_only)
            self.surface.blit(icon, [self.dimensions[0] / 2 - self.icon_only[0]/2, 0])
        else:
            icon = pygame.transform.scale(icon, self.icon_size)
            self.surface.blit(icon, [self.dimensions[0]/2-self.icon_size[0]/2,0])

    def create(self,dial,filepath):
        self.draw_lines(dial.segments)
        self.set_legend(dial.range[0],dial.range[1],dial.range[2],unit=dial.unit)
        if dial.title is not None:
            self.set_title(dial.title)
        if dial.icon is not None:
            self.add_icon(dial.icon,dial.title is None)
        self.save_image(filepath)

    def __del__(self):
        pygame.quit()


if __name__ == "__main__":
    creator = ImageCreator()
    creator.draw_lines()
    creator.set_legend("15","50","30",unit="kWh")
    #creator.set_title("Hallo ihr")
    creator.add_icon("solar-panel.jpg",True)
    creator.save_image()
    #pygame.draw.ellipse(surface,color=(20, 20, 0),rect=[(-extendw), 72, width+2*extendw, height],width=line_width)
    #pygame.draw.arc(surface, (0, 0, 0), [-10, height/2, width+20, height], 0, 3.15, 4)
    #pygame.draw.arc(surface, (255, 255, 255), [(-extendw), 72, width+2*extendw, height], 0, 0.7, line_width+1)
    #pygame.draw.arc(surface, (255, 255, 255), [(-extendw), 72, width+2*extendw, height],  2.5, 3.14,line_width+1)
    #pygame.draw.circle(surface,color=0,center=start_val,radius=3)

