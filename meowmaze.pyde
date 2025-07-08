add_library('minim')
import random
import os

# Constants
PATH = os.getcwd()
RESOLUTION_W = 800
RESOLUTION_H = 800
NUM_COLS = 20
NUM_ROWS = 20
TILE_WIDTH = RESOLUTION_W // NUM_COLS
TILE_HEIGHT = RESOLUTION_H // NUM_ROWS

# Boolean values
mouse_click1 = False
Exit_Instructions=False
Start = True

#global variables
global level_no, fc
fc = 10 #variable for frame count (used for speedboost)
level_no = 0

#image loading
end_img = loadImage(PATH + "/images/" + "end.png")
game_loss_img=loadImage(PATH+ "/images/" + "gameloss.png")
instructions_img=loadImage(PATH+ "/images/" + "instructions.png")
print(PATH)
player = Minim(this)

# Level Definitions
level0_list = [
    "11111111111111111111",
    "10000000001000000001",
    "10111111101011111101",
    "10100000101000000001",
    "10101110101110111001",
    "10001000100010001001",
    "11111010111010111011",
    "10000000000000000001",
    "10111001111110011001",
    "10100001111110001001",
    "10101001111110011001",
    "10001001111110011001",
    "11111001111110001101",
    "10000000000000000001",
    "10111110101110111001",
    "10100000101000000001",
    "10101110101011111101",
    "10100010100010000001",
    "10000010000000000001",
    "11111111111111111111",
]

level1_list = [
    "11111111111111111111",
    "10000000000000000001",
    "10111111101111111001",
    "10000000100000000001",
    "11101110111110111011",
    "10001000100010001001",
    "11101011101010101111",
    "10000000000000000001",
    "10111001111110011001",
    "10100001111110001001",
    "10101111111111111001",
    "10001001111110011001",
    "11111001111110001101",
    "10000000000000000001",
    "11101110101110111011",
    "10001000101000001001",
    "10101110101011111101",
    "10100010100010000001",
    "10000000000000000001",
    "11111111111111111111",
]


level2_list = [
    "11111111111111111111",
    "10000000000000000001",
    "10111111111111111001",
    "10000000000000000001",
    "11101110101110111011",
    "10001000100010001001",
    "11111010111010111111",
    "10000000001000000001",
    "10111111111110111101",
    "10000001111110000001",
    "10101111111111111001",
    "10000001111110000001",
    "10111111111110111101",
    "10000000001000000001",
    "11111011101110111111",
    "10001000100010001001",
    "11101111101011111011",
    "10000000001000000001",
    "10101010101010101001",
    "11111111111111111111",
]

# List of levels
levels_list = [level0_list, level1_list, level2_list]

# Functions
def hardcoding_list():
    global level_no
    chosen_list = levels_list[level_no]
    hardcoded_list = []
    for row in chosen_list:
        row_list = []
        for char in row:
            row_list.append(int(char))
        hardcoded_list.append(row_list)
    return hardcoded_list

# class for mazes/paths
class Maze:
    def __init__(self, List):
        # loads different maze walls 
        self.layer_list = List
        self.wall_img1 = loadImage(PATH + "/images/block1.png")
        self.wall_img2=loadImage(PATH + "/images/block2.png")
        self.wall_img3=loadImage(PATH + "/images/block3.png")

        self.img1=loadImage(PATH + "/images/" + "level1block.png")
        self.img2=loadImage(PATH + "/images/" + "level2block.png")
        self.img3=loadImage(PATH + "/images/" + "level3block.png")
        
        # loads cat sprite
        self.cat_left_img=loadImage(PATH + "/images/" + "leftcat.png")

    #displays maze on screen
    def display_maze(self):
        # displays maze block, different block per level
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.layer_list[row][col] == 1:
                    if level_no==0:
                        image(self.wall_img1, col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    elif level_no==1:                        
                        image(self.wall_img2, col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    elif level_no==2:
                        image(self.wall_img3, col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                   
        #displays nyu pic based on level         
        if level_no==0:
            image(self.img1,7*TILE_WIDTH,8*TILE_HEIGHT,6*TILE_WIDTH,5*TILE_HEIGHT)
        elif level_no==1:
            image(self.img2,7*TILE_WIDTH,8*TILE_HEIGHT,6*TILE_WIDTH,5*TILE_HEIGHT)
        elif level_no==2:
            image(self.img3,7*TILE_WIDTH,8*TILE_HEIGHT,6*TILE_WIDTH,5*TILE_HEIGHT)

#class for player (cat)
class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.lives = 9
        self.shield_active = False
        self.speed_boost_active = False
        self.shield_start_time = 0
        self.speed_boost_start_time = 0
        self.shield_duration = 10000 #10s 
        self.speed_boost_duration = 10000 #10s
        self.start_time = millis()  # Initialize to the current time
        self.cat_dir = None
        self.slice=0
        self.num_slices=3
        self.change_pos=False #used for sprite movement handling
        
        #loads cat sprite for up down left and right
        self.cat_left_img=loadImage(PATH + "/images/" + "leftcat.png")
        self.cat_right_img=loadImage(PATH + "/images/" + "rightcat.png")
        self.cat_up_img=loadImage(PATH + "/images/" + "upcat.png")
        self.cat_down_img=loadImage(PATH + "/images/" + "downcat.png")

    #display player method
    def display_player(self):
        #uses time to switch up sprite image
        current_time = millis()
        elapsed_time = (current_time - self.start_time) / 1000.0 
        if elapsed_time<=0.9 or self.change_pos==False:
               image(self.cat_right_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
        else: 
            pass
                
        if self.cat_dir==RIGHT:
            image(self.cat_right_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)

        if self.cat_dir==LEFT:
            image(self.cat_left_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)

        elif self.cat_dir==UP:
            image(self.cat_up_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)

        elif self.cat_dir==DOWN:
            image(self.cat_down_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
        
        #calls update cat slice method
        self.Update_cat_slice()
        
        #adds blue circle around cat when shield is active
        if self.shield_active:
            noFill()
            stroke(129, 216, 255)
            strokeWeight(4)
            ellipse(self.x + TILE_WIDTH // 2, self.y + TILE_HEIGHT // 2, TILE_WIDTH, TILE_HEIGHT)
            noStroke()
            
    #switches up movement based on framecount so cat sprite movement is not same speed as tile advance
    def Update_cat_slice(self):
        if frameCount % 6 == 0 :
            self.slice = (self.slice + 1) % self.num_slices

    #key handling, switch direction based on keycode
    def move(self, maze, obstacles):
        if keyCode == UP or keyCode == DOWN or keyCode == LEFT or keyCode == RIGHT:
            self.change_pos = True
            self.cat_dir = keyCode
            
        #switches x and y variable by adding vx and vy to it
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        grid_x = int(new_x // TILE_WIDTH) 
        grid_y = int(new_y // TILE_HEIGHT)
    
        #makes sure you can't make an illegal move
        if 0 <= grid_x < NUM_COLS and 0 <= grid_y < NUM_ROWS and maze.layer_list[grid_y][grid_x] == 0:
            position_occupied = any(obstacle.effect != "lethal" and obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles)
            if not position_occupied:
                self.x, self.y = round(new_x), round(new_y)

    #checks collision with obstacles        
    def check_collision(self, obstacles):
        collision_occurred = False #resets everytime method is called
        #gets location of cat
        cat_grid_x = round(self.x / TILE_WIDTH)
        cat_grid_y = round(self.y / TILE_HEIGHT)
    
        #gets location of obstacles
        for obstacle in obstacles:
            obstacle_grid_x = round(obstacle.x / TILE_WIDTH)
            obstacle_grid_y = round(obstacle.y / TILE_HEIGHT)
    
            #if cat and obstacle x and y are the same
            if cat_grid_x == obstacle_grid_x and cat_grid_y == obstacle_grid_y:
                if self.shield_active:
                    self.shield_active = False #if sheild is active shield is gone
                else:
                    #if obstacle is lethal and no shield lose one life
                    if obstacle.effect == "lethal":
                        if not collision_occurred:
                           self.lives -= 1
                           collision_occurred = True #makes true
                    #if non-lethal seperate interaction method
                    elif obstacle.effect == "non-lethal":
                        obstacle.interact(self)
                return True  # Collision detected
        return False  # No collision

    #updates powerups class
    def update_buffs(self):
        current_time = millis() #creates a local variable for time
        global fc
        
        #decreases time of shield
        if self.shield_active:
            elapsed_time = current_time - self.shield_start_time
            if elapsed_time >= self.shield_duration:
                self.shield_active = False #deactivates shield

        #speed boost is framecount controlled
        if self.speed_boost_active:
            fc = 5 #switches framecount if speedboost for handlinng in game.update and draw methods
            elapsed_time = current_time - self.speed_boost_start_time
            if elapsed_time >= self.speed_boost_duration:
                self.speed_boost_active = False #deactivates speed boost if time is up
                fc = 10 #switches fc back to original count
                if self.vx > 0:
                    self.vx = TILE_WIDTH
                elif self.vx < 0:
                    self.vx = -TILE_WIDTH
                else:
                    self.vx = 0
                if self.vy > 0:
                    self.vy = TILE_HEIGHT
                elif self.vy < 0:
                    self.vy = -TILE_HEIGHT
                else:
                    self.vy = 0
        else:
            fc = 10 #makes sure the switch is happening 

#creates class for all obstacles
class Obstacle:
    def __init__(self, x, y, effect, img_file, movement_type):
        self.x = x
        self.y = y
        self.effect = effect
        self.img_file=img_file
        self.slice=0
        self.num_slices=self.find_num_slices()
        #loads images and sprites
        self.oimage_file = loadImage(PATH + "/images/" + self.img_file)
        self.dog_up=loadImage(PATH + "/images/" + "updog.png")
        self.dog_down=loadImage(PATH + "/images/" + "downdog.png")
        self.dog_right=loadImage(PATH + "/images/" + "rightdog.png")
        self.dog_left=loadImage(PATH + "/images/" + "leftdog.png")
        self.movement_type = movement_type #movement pattern differs by obstacle 
        self.direction = 1
        self.dog_dir= "left"
     
    #same logic as cat movement    
    def Update(self):
        if frameCount % 6 == 0 :
            self.slice = (self.slice + 1) % self.num_slices            
     
    # direction handling, displays dog images
    def display(self):
        if self.img_file!="dog.png":
            image(self.oimage_file, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
        else:
            if self.dog_dir=="left":
                image(self.dog_left, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
            elif self.dog_dir=="right":
                image(self.dog_right, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
            elif self.dog_dir=="up":
                image(self.dog_up, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
            elif self.dog_dir=="down":
                image(self.dog_down, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)

        self.Update()
    
    #different number of slices per obstacle, changes number for each instance
    def find_num_slices(self):
        if self.img_file=="cucumber.png":
            self.num_slices=3
        elif self.img_file=="vacuum.png":
            self.num_slices=1
        elif self.img_file=="yarn.png":
            self.num_slices=3
        else:
            return 1
            
        return self.num_slices #returns correct amount of slices to the variable
        
    #defines interaction based on obstacle
    def interact(self, player):
        if self.effect == "lethal":
            player.lives -= 1 #lethal decreases lives
        elif self.effect == "non-lethal": #non lethal moves player
            new_x = player.x
            new_y = player.y
   
            if player.vx < 0: 
                new_x += TILE_WIDTH
            elif player.vx > 0:
                new_x -= TILE_WIDTH
            elif player.vy < 0:
                new_y += TILE_HEIGHT
            elif player.vy > 0:
                new_y -= TILE_HEIGHT

            #makes sure its a valid integer
            grid_x = int(new_x // TILE_WIDTH)
            grid_y = int(new_y // TILE_HEIGHT)

        if (0 <= grid_x < NUM_COLS and 0 <= grid_y < NUM_ROWS and game.maze.layer_list[grid_y][grid_x] == 0):
            player.x = new_x
            player.y = new_y
    
    #move method
    def move(self, maze):
        new_x, new_y = self.x, self.y
    
        if self.movement_type == "random":  # It's a cucumber or dog
            direction = random.choice(["left", "right", "up", "down", "none"]) #random movement, choice is random
            #handles dog sprite and movement for cucumber or dog
            if direction == "left": 
                self.dog_dir="left"
                new_x -= TILE_WIDTH
            elif direction == "right":
                self.dog_dir="right"
                new_x += TILE_WIDTH
            elif direction == "up":
                self.dog_dir="up"
                new_y -= TILE_HEIGHT
            elif direction == "down":
                self.dog_dir="down"
                new_y += TILE_HEIGHT
    
        elif self.movement_type == "horizontal":  # Move left and right
            new_x += self.direction * TILE_WIDTH
    
        elif self.movement_type == "vertical": #move up and down
            new_y += self.direction * TILE_HEIGHT
    
        #update location
        grid_x, grid_y = int(new_x // TILE_WIDTH), int(new_y // TILE_HEIGHT)
        if 0 <= grid_x < NUM_COLS and 0 <= grid_y < NUM_ROWS and maze.layer_list[grid_y][grid_x] == 0:
            self.x, self.y = round(new_x), round(new_y)
        else:
            self.direction *= -1

# class for powerups   
class PowerUp:
    def __init__(self, x, y, effect, pimg_file_name):
        self.x = x
        self.y = y
        self.effect = effect
        self.slice=0
        self.pimg_file_name=pimg_file_name
        self.num_slices=  self.find_slice_num() 
        self.pimage = loadImage(PATH + "/images/" + self.pimg_file_name) #loads image
    
    #finds slice number depending on image    
    def find_slice_num(self):
        if self.pimg_file_name=="speedboost.png":
            self.num_slices=4
        elif self.pimg_file_name=="life.png":
            self.num_slices=4
        elif self.pimg_file_name=="shield.png":
            self.num_slices=8
        return self.num_slices
            
    #displays powerups
    def display(self):
        image(self.pimage, self.x, self.y, TILE_WIDTH, TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
        self.Update()

    #updates powerup slices
    def Update(self):
        if frameCount % 6 == 0 :
            self.slice = (self.slice + 1) % self.num_slices
    
    def interact(self, player, game):
        #local time variable to measure time spent in boost
        current_time = millis()

        if self.effect == "speedboost":
            player.speed_boost_active = True #activates speed boost
            player.speed_boost_start_time = current_time

        elif self.effect == "life":
            player.lives += 1 #adds life

        elif self.effect == "shield":
            player.shield_active = True #activates shield
            player.shield_start_time = current_time
        game.powerups.remove(self) #removes powerups


#class for points/fish
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.slice=0
        self.num_slices=8 
        self.points_img=loadImage(PATH + "/images/" + "fish.png")
    
    #updates sprite slices for fish     
    def Points_Update_Slice(self):
        if frameCount % 6 == 0 :
            self.slice = (self.slice + 1) % self.num_slices

    # displays image
    def display(self):
        fill(0)
        image(self.points_img,self.x,self.y,TILE_WIDTH,TILE_HEIGHT,self.slice*TILE_WIDTH,0,(self.slice+1)*TILE_WIDTH,TILE_HEIGHT)
        self.Points_Update_Slice()

#game class, contains everything
class Game:
    def __init__(self,old_score):
        self.maze = Maze(hardcoding_list())
        self.cat = Cat(1 * TILE_WIDTH, 1 * TILE_HEIGHT)
        self.obstacles = []
        self.powerups = []
        self.points = []
        self.lives = self.cat.lives
        self.score = 0 + old_score #score stays the same across levels
        self.old_score=0
        self.game_over = False
        self.won_level = False
        self.time_up = False
        self.timer_started = False
        self.timer = self.decide_timer()
        self.menu_timer_started=False
        self.progress_level = False
        self.num_slices=8
        self.game_completed=False
        self.last_time_update = millis()  # Record the time at the start of the level
        self.menu_start_time=None
        self.time_lost=0
        self.start_img = loadImage(PATH + "/images/home.png") #loads home image
        #finds all available positions for points, powerups and obstacles
        self.available_positions = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.maze.layer_list[row][col] == 0:
                    self.available_positions.append((row, col))
        self.place_powerups()
        self.place_obstacles()
        self.place_points()

    #different time per level
    def decide_timer(self):
        global level_no
        if level_no == 2:
            return 85
        elif level_no == 1:
            return 95
        if level_no == 0:
            return 100
    
     #displays menu and instructions           
    def Display_Menu(self):
        global mouse_click1
        global Start
        image(self.start_img, 0, 0, 800, 800)
        # Initialize menu_start_time only once when the menu is first shown
        if self.menu_start_time == None:
            self.menu_start_time = millis() #used to calculate time spent on this page
            
        #if mouse within range of play button
        if (mouseX >= 281.6 and mouseX <= 281.6 + 219.2) and (mouseY >= 554.2 and mouseY <= 554.2 + 58.6):
            if mouse_click1:
                Start = False
                self.menu_end_time = millis()  # Initialize timer reference
                self.menu_elapsed_time = (self.menu_end_time - self.menu_start_time) / 1000  # Calculate elapsed time in seconds
        
        # if mouse within range of instructions button        
        if (mouseX >= 281.6 and mouseX <= 281.6 + 219.2) and (mouseY >= 636.4 and mouseY <= 636.4 + 58.6):
                Exit_Instructions=False
                image(instructions_img,150,150,500,500)

    # places one of each powerup randomly in the maze
    def place_powerups(self):
        powerup_list = [("speedboost", "speedboost.png"), ("life", "life.png"), ("shield", "shield.png")]
       
        for powerup in powerup_list:
            placed = False
            while not placed and self.available_positions:
                random_index = random.randint(0, len(self.available_positions) - 1)
                row, col = self.available_positions[random_index]
                effect = powerup[0]
                image_name = powerup[1]
                self.powerups.append(PowerUp(col * TILE_WIDTH, row * TILE_HEIGHT, effect, image_name))
                self.available_positions.pop(random_index) #removes position index from available positions list
                placed = True
    
    # places one of each obstacle randomly in the maze
    def place_obstacles(self):        
        obstacle_types = [("lethal", "dog.png", "random"), ("lethal", "cucumber.png", "random"), ("non-lethal", "vacuum.png", "vertical"), ("non-lethal", "yarn.png", "horizontal")]
   
        for i in range(len(obstacle_types)):
            effect = obstacle_types[i][0] #effect within list (lethal or nonlethal)
            image = obstacle_types[i][1] #image of the obstacle
            movement = obstacle_types[i][2] #movement type per obstacle
           
            placed = False
            while not placed and self.available_positions:
                random_index = random.randint(0, len(self.available_positions) - 1)
                row, col = self.available_positions[random_index]
               
               #makes sure that depending on obstacle location it has at least one valid movement as obstacle should move
                valid_movement = False
                if movement == "horizontal":
                    if (col > 0 and self.maze.layer_list[row][col - 1] == 0) or (col < NUM_COLS - 1 and self.maze.layer_list[row][col + 1] == 0):
                        valid_movement = True
                elif movement == "vertical":
                    if (row > 0 and self.maze.layer_list[row - 1][col] == 0) or (row < NUM_ROWS - 1 and self.maze.layer_list[row + 1][col] == 0):
                        valid_movement = True
                elif movement == "random":
                    valid_movement = True
                
                #append to maze
                if valid_movement:
                    self.obstacles.append(Obstacle(col * TILE_WIDTH, row * TILE_HEIGHT, effect, image, movement))
                    self.available_positions.pop(random_index)
                    placed = True
                else:
                    self.available_positions.pop(random_index)
                    
    #add points in every empty spot in maze    
    def place_points(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.maze.layer_list[row][col] == 0:
                    self.points.append(Point(col * TILE_WIDTH, row * TILE_HEIGHT))

        #display of the game
    def display_game(self):
        self.maze.display_maze() #display maze
        self.cat.display_player() #display player
        for point in self.points:
            point.display() #display all points in list
        for powerup in self.powerups:
            powerup.display() #display all powerups in list
        for obstacle in self.obstacles:
            obstacle.display() #display all obstacles in list

            
    # updates every frame
    def update(self):
        global fc
        
        #timer
        current_time = millis()
        elapsed_time = (current_time - self.last_time_update) / 1000.0
    
        if elapsed_time >= 1:
            self.timer -= int(elapsed_time)
            self.last_time_update = current_time
        
           
        self.cat.update_buffs()
        if fc==10:
            self.cat.move(self.maze, self.obstacles) #only if speed boost not active
    
        #check if cat is colliding with any point
        for point in self.points[:]:
            if int(self.cat.x // TILE_WIDTH) == int(point.x // TILE_WIDTH) and int(self.cat.y // TILE_HEIGHT) == int(point.y // TILE_HEIGHT):
                self.points.remove(point)
                self.score += 10 # +10 to score per point collected
                
        #move obstacles
        for obstacle in self.obstacles:
            obstacle.move(self.maze)
    
        #check if cat is colliding with any powerup
        for powerup in self.powerups[:]:
            if int(self.cat.x // TILE_WIDTH) == int(powerup.x // TILE_WIDTH) and int(self.cat.y // TILE_HEIGHT) == int(powerup.y // TILE_HEIGHT):
                powerup.interact(self.cat, self)
                self.score += 5 # +5 to score per powerup
        
        #checks for game over conditions (no lives left, time runs out)
        if level_no==0:
            if self.cat.lives <= 0 or self.timer+game.menu_elapsed_time <= 1:
                self.game_over = True
        elif level_no==1 or level_no==2:
            if self.cat.lives <= 0 or self.timer <= 0:
                self.game_over = True

            
        #checks for collision, declares game over if live lose
        collision_happened = self.cat.check_collision(self.obstacles)
        if collision_happened:
            if self.cat.lives <= 0:
                self.game_over = True
    
        if not self.points:  # Check if all points are eaten
            self.won_level = True
            self.game_over = True  # Temporarily end the level
        
        
        if self.game_over and self.won_level:
            global level_no
            level_no += 1 #move on to next level
            self.score += self.cat.lives*10 #add 10 points per lifeleft
            if level_no < len(levels_list): #if there r still levels to play
                self.old_score=self.score
        
                # Progress to the next level
                self.__init__(self.old_score)
            else:
                #all levels are done
                self.game_completed = True
                self.won_level=True
                self.game_over=True
    
    #restart the game            
    def restart(self):
        global Start, level_no, bg_music,lose_music,win_music
        Start = True
        level_no = 0
        
        #plays bg music when appropriate
        if bg_music and not bg_music.isPlaying():
            bg_music.loop()
        
        #plays lose music when appropriate
        if lose_music and lose_music.isPlaying():
            lose_music.pause()
            lose_music.rewind()
            
        #plays win music when appropriate
        if win_music and win_music.isPlaying():
            win_music.pause()
            win_music.rewind()
            
        self.__init__(self.old_score) #adds old score so that the score is cumulative across all 3 levels
        

# Setup and draw functions
def setup():
    global bg_music,lose_music,win_music
    size(RESOLUTION_W, RESOLUTION_H)
    frameRate = 60
    player = Minim(this)

    #loads sounds
    bg_music = player.loadFile(PATH + "/sounds/bg.mp3")
    lose_music = player.loadFile(PATH + "/sounds/lose.mp3")
    win_music = player.loadFile(PATH + "/sounds/win.mp3")

    bg_music.loop()


    
def draw():
    global Start, mouse_click1, fc, game

    if Start:  # Display the home menu
        lose_music.pause() 
        if not bg_music.isPlaying():  
            bg_music.loop()

        game.Display_Menu() #calls display method
        
        #checks for mouse location to display start menu or instructions
        if mouse_click1:
            if (mouseX >= 281.6 and mouseX <= 281.6 + 219.2) and (mouseY >= 554.2 and mouseY <= 554.2 + 58.6):
                Start = False
            mouse_click1 = False
        
        if (mouseX >= 281.6 and mouseX <= 281.6 + 219.2) and (mouseY >= 636.4 and mouseY <= 636.4 + 58.6):
                fill(100)
                image(instructions_img,150,150,500,500)

    else:  # Game logics
        if game.game_over and game.game_completed : #if win
        #display win image and score
            background(0)
            image(end_img, 0, 0, RESOLUTION_W, RESOLUTION_H)
            fill(255)
            textSize(40)
            text(str(game.score),530,540)
            fill(255)
            
            if bg_music.isPlaying():
                bg_music.pause() #pause bg music
            
            if not win_music.isPlaying(): #play win music
                win_music.rewind()
                win_music.play()

            #if mouse click restart
            
            if mouse_click1:
        
                Start = True
                win_music.pause()
                win_music.rewind()
                mouse_click1 = False
                game.restart()

                    
        elif game.game_over and not(game.game_completed): #game loss
            background(0)
            image(game_loss_img, 0, 0, RESOLUTION_W, RESOLUTION_H)
            fill(255)  # Set text color
            textSize(40)
            text(str(game.score),550,620)
            fill(255)
            if bg_music.isPlaying():
                bg_music.pause() #stop bg music
                
            if not lose_music.isPlaying():
                lose_music.rewind() #start playing lose music
                lose_music.play()
            #game restarts, stop lose music
            if mouse_click1:
                lose_music.pause()
                lose_music.rewind()
                mouse_click1 = False
                game.restart()

        else: #game is still being played
            background(255)
            
            #play bg music
            if not bg_music.isPlaying():
               bg_music.loop() 

            if game.cat.speed_boost_active:
                #controls speed boost
                if frameCount % fc == 0 and frameCount % 10 == 0: #so cat.move is not being called twice 
                    pass
                elif frameCount % fc == 0: 
                    game.cat.move(game.maze, game.obstacles)

            game.display_game()
            if frameCount % 10 == 0: #calls the gamme update method
                game.update()

            textSize(24)
            fill(255)
            rect(0, 0, 200, 40)
            rect(500, 0, 300, 40)
            fill(0)
            #shows timer on top left screen
            textAlign(LEFT, TOP)
            text("Time Left: " + str(int(game.timer+game.menu_elapsed_time)) + "s", 10, 10)
            textAlign(RIGHT, TOP)
            #shows score and lives on top right screen
            text("Score: " + str(game.score) + "  Lives: " + str(game.cat.lives), RESOLUTION_W - 10, 10)

            #shows time left for speed boost and shield
            if game.cat.speed_boost_active:
                remaining_speed = (game.cat.speed_boost_duration - (millis() - game.cat.speed_boost_start_time)) // 1000
                text("Speed Boost: " + str(remaining_speed) + "s", RESOLUTION_W // 2, RESOLUTION_H - 40)
            if game.cat.shield_active:
                remaining_shield = (game.cat.shield_duration - (millis() - game.cat.shield_start_time)) // 1000
                text("Shield: " + str(remaining_shield) + "s", RESOLUTION_W // 2, RESOLUTION_H - 20)

#handles key pressed event
def keyPressed():
    
    if keyCode == RIGHT: #move right
        game.cat.vx = TILE_WIDTH
        game.cat.vy = 0
    elif keyCode == LEFT: #move left
        game.cat.vx = -TILE_WIDTH
        game.cat.vy = 0
    elif keyCode == UP: #move up
        game.cat.vx = 0
        game.cat.vy = -TILE_HEIGHT
    elif keyCode == DOWN: #move down
        game.cat.vx = 0
        game.cat.vy = TILE_HEIGHT

#handles mouse click events        
def mouseClicked():
    global mouse_click1
    if Start or game.game_completed or game.game_over: #to prevent against accidental mouse clicks
        mouse_click1 = True
   
game = Game(0) #instantiates a game object
