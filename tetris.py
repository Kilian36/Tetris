'''

KILIAN LE CREURER 
tizianokil@gmail.com


Old standard tetris : JUST FOR FUN
    


'''

from turtle import update, width
from matplotlib import image
import pygame
import random

map_width=12
map_heigth=18
void_width=220
void_height=5
block_size=35


class Block():
    '''
    Contain the main features of a block and its possible movement
    '''
    def __init__(self, type):
        self.type=type
        
        if type==0: #small a
            self.centre=[5,1]
            self.elements=[[5,0],[6,1]]
        elif type==1: #three b
            self.centre=[5,1]
            self.elements=[[4,1],[5,0],[6,1]]
        elif type==2: #long
            self.centre=[5,0]
            self.elements=[[4,0],[5,0],[6,0],[7,0]]
        elif type==3: #medium a
            self.centre=[5,2]
            self.elements=[[5,0],[5,1],[6,2]]
        elif type==4: #medium b
            self.centre=[5,2]
            self.elements=[[4,2],[5,1],[5,0]]
        elif type==5: #strange a
            self.centre=[5,1]
            self.elements=[[5,2],[6,1],[6,0]]
        elif type==6: #strange b
            self.centre=[5,1]
            self.elements=[[5,0],[6,1],[6,2]]
        elif type==7: #cube
            self.centre=[5,1]
            self.elements=[[5,0],[6,0],[6,1]]
    
    def move_horizontally(self, direction):
        '''
        Move a block left or right depending on direction value
        '''
        if direction==0 and self.centre[0] >0: #Left
            self.centre[0]-=1  
            for element in self.elements:
                element[0]-=1
        elif direction==1 and self.centre[0] < map_width-1: #Right
            self.centre[0]+=1
            for element in self.elements:
                element[0]+=1
    
    def move_vertically(self):
        '''
        move vertically the block
        '''
        self.centre[1]+=1  
        for element in self.elements:
            element[1]+=1

    def rotate_block(self, orientation):
        '''
        Rotate the block clockwise or anti-clockwise depending on the orientation value
          --- Compute local coordinates using the centre as new origin and rotate 
          --- the block
        '''
        if orientation==0: #Clockwise D button
            #Need to refer the coordinates to the centre of te block in order to change values
            for element in self.elements:
                local_coord_x=element[0]-self.centre[0]
                local_coord_y=element[1]-self.centre[1]
                rotated_x=local_coord_y
                rotated_y=-local_coord_x
                element[0]=rotated_x+self.centre[0]
                element[1]=rotated_y+self.centre[1]
        elif orientation==1: #Anticlockwise A button 
            for element in self.elements:
                local_coord_x=element[0]-self.centre[0]
                local_coord_y=element[1]-self.centre[1]
                rotated_x=-local_coord_y
                rotated_y=local_coord_x
                element[0]=rotated_x+self.centre[0]
                element[1]=rotated_y+self.centre[1]
    

class Map():
    '''
    Class wich contains the map scheme with traces of the presence of a block in a 
    specific position 
    --- array with a boolean for every element that store the information of the element
    --- methods : 
                check line and update
                check block position (control if a block has to stop )
    '''        
    def __init__(self, width, height):
        self.map_elements=[]
        self.width=width
        self.height=height
        type = -1
        for i in range(0,height):
            for j in range(0,width):
                self.map_elements.append([[j,i],False,type])
    
    def check_lines(self):
        '''
        Clear the map lines and count how many are
        '''
        count=0
        for j in range(0,self.height):
            line_full=True
            for i in range(0,self.width): 
                idx=j*map_width+i
                if self.map_elements[idx][1]==False:
                    line_full=False
                    break 
            #If is full clean it
            if line_full:
                count+=1
                for i in range(0,self.width):
                    idx=j*map_width+i
                    self.map_elements[idx][1]=False
        return count
    
    
    def update_map(self, block):
        for block_part in block.elements:
                idx=block_part[1]*map_width+block_part[0]
                self.map_elements[idx][1]=True
                self.map_elements[idx][2]=block.type
    

    def control_block(self, block):
        '''
        Compare block positions with the map coordinates in order to update the map
        '''
        #First, control if the block reached the bound of map

        #Get the index in the map of the centre
        idx_centre=block.centre[1]*map_width+block.centre[0]
        for block_part in block.elements:
            if block_part[1]==map_heigth-1 or block.centre[1]==map_heigth-1:
                self.map_elements[idx_centre][1]=True #Update the centre of the block in the map
                self.map_elements[idx_centre][2]=block.type
                self.update_map(block) #Update the rest of the map
                return True
        #Second, check if an element the block is exactly above a truth point of the map
        #if it's the case, update the map
        idx_under_centre=(block.centre[1]+1)*map_width +block.centre[0]
        for block_part in block.elements:
            idx=(block_part[1]+1)*map_width+block_part[0]
            if idx >= 0 and idx < self.height*self.width:
                if self.map_elements[idx][1] or self.map_elements[idx_under_centre][1]:
                    self.map_elements[idx_centre][1]=True
                    self.map_elements[idx_centre][2]=block.type
                    self.update_map(block)
                    return True
    
    def control_first_row(self):
        for i in range(0,self.width*3):
            if self.map_elements[i][1]==True:
                return True

        

def check_movements(block,map,type):
    '''
    Control if a movement is possible based on the map elements
    '''
    if type==0: #Horizontal left movement
        #Check if the block is near to a boundary of the map
        idx_centre_left=block.centre[1]*map_width+block.centre[0]-1
        for block_part in block.elements:
            idx=block_part[1]*map_width+block_part[0]-1
            if idx<map.height*map_width and idx_centre_left<map.height*map_width:
                if map.map_elements[idx][1] or map.map_elements[idx_centre_left][1] or block_part[0]==0:
                    return False
        return True
    if type==1: #Horizontal right movement
        idx_centre_left=block.centre[1]*map_width+block.centre[0]+1
        for block_part in block.elements:
            idx=block_part[1]*map_width+block_part[0]+1
            if idx<map.height*map_width and idx_centre_left<map.height*map_width:
                if map.map_elements[idx][1] or map.map_elements[idx_centre_left][1] or block_part[0]==map_width-1:
                    return False
        return True
    if type==2: #Clockwise rotation
        block.rotate_block(0)
        #Check if the block can rotate remaining in the map
        for block_part in block.elements:
            if block_part[0]<0 or block_part[0]>map_width or block_part[1]>map_heigth-1:
                block.rotate_block(1)
                return False
        for block_part in block.elements:
            idx=block_part[1]*map_width+block_part[0]
            if map.map_elements[idx][1]==True:
                block.rotate_block(1)
                return False
    if type==3: #Anti-clockwise rotation
        block.rotate_block(1)
        #Check if the block can rotate remaining in the map
        for block_part in block.elements:
            if block_part[0]<0 or block_part[0]>map_width or block_part[1]>map_heigth:
                block.rotate_block(0)
                return False
        for block_part in block.elements:
            idx=block_part[1]*map_width+block_part[0]
            if idx<map_heigth*map_width:
                if map.map_elements[idx][1]==True:
                    block.rotate_block(0)
                    return False

def compute_points(line_count):
    return 100*(line_count**2)


def wait_time():
    start_ticks=pygame.time.get_ticks() #starter tick  
    finish=False
    while not finish:
            ##TIMING DEL LEVEL FINISHED
            seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
            if seconds>2: 
               finish=True
    
#GAME SECTION
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('./Tetris.mp3')
loops=10
pygame.mixer.music.play(loops)
height=630
width=800
keys=5 #0 1 2  A S D
screen=pygame.display.set_mode((width, height))


#Creation of the map boundaries
my_rect=pygame.Rect(void_width-5,void_height-5,map_width*block_size+10,map_heigth*block_size+10)

#Variable which contains points
points=0

#Block movement parameters
contatore=0
start_controller=450

#Refresh rate parameters
frame_counter=0
frame_control=50

#Control the velocity of horizontal and vertical movements of the player keeps 
# the correspondind keys pressed
velocity=0
velocity_controller=100

type=random.randint(0,7)
block=Block(type)
map=Map(map_width,map_heigth)

graphic_block=pygame.image.load("./cube.png")
blocks=[
    graphic_block,
    pygame.image.load("./blue.png"),
    pygame.image.load("./green.png"),
    pygame.image.load("./orange.png"),
    pygame.image.load("./pink.png"),
    pygame.image.load("./purple.png"),
    pygame.image.load("./yellow.png")
]
#Read record from file 
with open("C:/Users/Kilian/Desktop/Games/Snake/record.txt") as file:
    data=file.readline()
    record=int(data)
    
#INITIALIZE THE VARIABLE WHICH CONTROL THE VELOCITY OF THE BLOCKS THAT GO DOWN 
#IT CHANGHES THEN DURING THE GAME    
divisore=start_controller
#YOU LOSE IMG
lose_img=pygame.image.load("./you_lose.png")

while 1:
    #Update the 3 velocity variables
    contatore += 1
    frame_counter += 1
    velocity += 1

    #Screen drawing
    if frame_counter==frame_control:
        frame_counter=0
        screen.fill(0)
        #print the centre of the actual block 
        x=void_width+block.centre[0]*block_size
        y=void_height+block.centre[1]*block_size
        screen.blit(blocks[type-1],(x,y))
        #then print all it's elements
        for element in block.elements:
            x_coord=void_width+element[0]*block_size
            y_coord=void_height+element[1]*block_size
            screen.blit(blocks[type-1],(x_coord,y_coord))
        #print all the true elements of the map
        for element in map.map_elements:
            if element[1]==True:
                x_coord=void_width+element[0][0]*block_size
                y_coord=void_height+element[0][1]*block_size
                screen.blit(blocks[element[2]-1],(x_coord,y_coord))
        #Print points and record        
        myfont = pygame.font.SysFont("monospace", 16)
        scoretext = myfont.render( "Score = "+str(points), False, (255,255,255))
        record_print = myfont.render("Record = "+str(record), False, (255,255,255))
        screen.blit(record_print, (0,20))
        screen.blit(scoretext, (0, 0))
        pygame.draw.rect(screen,(255,255,255), my_rect, width=5)
    pygame.display.flip()

    #Read events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                keys=0 #Left horizontal
            elif event.key == K_s:
                keys=1 #Down fast
            elif event.key == K_d:
                keys=2 #Right horizontal
            elif event.key == K_q:
                keys=3 #Anticlockwise rotation
            elif event.key == K_e:
                keys=4 #Clockwise rotoation
        if event.type == pygame.KEYUP:
            keys = -1
    if velocity==velocity_controller:
        velocity = 0
        if keys==0:
            possible=check_movements(block,map,0)
            if possible:
                block.move_horizontally(0)
    
        if keys==1:
            create_new=map.control_block(block)
            if create_new:
                del(block)
                type=random.randint(0,7)
                block=Block(type)
            block.move_vertically()

        if keys==2:
            possible=check_movements(block,map,1)
            if possible:
                block.move_horizontally(1)
        
    if keys==4:
        check_movements(block,map,2)
        keys =-1
    if keys==3:
        check_movements(block,map,3)
        keys =-1
    if contatore==divisore:
        contatore=0
        create_new=map.control_block(block)
        if create_new:
            del(block)
            type=random.randint(0,7)
            block=Block(type)
        block.move_vertically()
        count=map.check_lines()
        if count!=0:
            divisore//=1.1
        points+=compute_points(count)
        youlose=map.control_first_row()
        if youlose:
            divisore = start_controller
            screen.blit(lose_img,(235,300))
            if points>record:
                with open("C:/Users/Kilian/Desktop/Games/Snake/record.txt", 'w') as file:
                    file.write(str(points))
            pygame.display.flip()
            wait_time()
            del(map)
            map=Map(map_width,map_heigth)


        





