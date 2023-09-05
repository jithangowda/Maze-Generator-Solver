import pygame
import random
import time
import sys


class MAZE:
    
    def __init__(self):
        
        # initialize pygame window
        self.screen_width = 800
        self.screen_height = 700
        self.screen_fps = 60
        
        # initialize colours
        self.WHITE = (255, 255, 255)
        self.GREEN = (191, 228, 93)
        self.PURPLE = (192,136,216)
        self.YELLOW = (255 ,255 ,0)
        self.BLACK = (0,0,0)
        self.BLUE = (0, 255, 255)
        
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)
        pygame.display.set_caption("MAZE")
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        
        # setup maze variables
        self.x = 0                    # x axis
        self.y = 0                    # y axis
        self.w = 30                  # width of individual cell
        self.n_row = 20               # no. of rows
        self.n_col = 20               # no. of cols
        self.grid = []
        self.visited = []
        self.stack = []
        self.solution = {}
        
    # function to build the grid
    def make_grid(self, gx, gy):
        self.screen.fill(self.WHITE)
        for i in range(1,self.n_row + 1):
            gx = self.w                                                          
            gy = gy + self.w                                                   
            for j in range(1, self.n_col + 1):
                pygame.draw.line(self.screen, self.BLACK, [gx, gy], [gx + self.w, gy])         
                pygame.draw.line(self.screen, self.BLACK, [gx + self.w, gy], [gx + self.w, gy + self.w])   
                pygame.draw.line(self.screen, self.BLACK, [gx + self.w, gy + self.w], [gx, gy + self.w])   
                pygame.draw.line(self.screen, self.BLACK, [gx, gy + self.w], [gx, gy])         
                self.grid.append((gx,gy))                                          
                gx = gx + self.w    

    # stack operations
    def push_up(self, gx, gy):
        pygame.draw.rect(self.screen, self.BLUE, (gx + 1, gy - self.w + 1, self.w-1, (self.w*2)-1), 0)        
        pygame.display.update()                       


    def push_down(self,gx, gy):
        pygame.draw.rect(self.screen, self.BLUE, (gx +  1, gy + 1, self.w-1, (self.w*2)-1), 0)
        pygame.display.update()


    def push_left(self,gx, gy):
        pygame.draw.rect(self.screen, self.BLUE, (gx - self.w +1, gy +1, (self.w*2)-1, self.w-1), 0)
        pygame.display.update()


    def push_right(self, gx, gy):
        pygame.draw.rect(self.screen, self.BLUE, (gx +1, gy +1, (self.w*2)-1, self.w-1), 0)
        pygame.display.update()


    # creates a single coloured cell used while backtracking
    def single_cell(self, gx, gy):
        pygame.draw.rect(self.screen, self.GREEN, (gx +1, gy +1, self.w-2, self.w-2), 0)         
        pygame.display.update()


    def backtracking_cell(self, gx, gy):
        pygame.draw.rect(self.screen, self.BLUE, (gx +1, gy +1, self.w-2, self.w-2), 0)     
        pygame.display.update()                                     

    # function to visualize a way back to the beginning
    def solution_cell(self, gx, gy):
        pygame.draw.rect(self.screen, self.PURPLE, (gx+10, gy+10, 7, 7), 0)            
        pygame.display.update()                                  

    # function to make the maze
    def make_maze(self, gx, gy):
        self.single_cell(gx, gy)                                            
        self.stack.append((gx, gy))                                          
        self.visited.append((gx, gy))                                    
        while len(self.stack) > 0:                                      
            time.sleep(.01)                                      
            cell = []                                     
            if (gx + self.w, gy) not in self.visited and (gx + self.w, gy) in self.grid:    
                cell.append("right")                              

            if (gx - self.w, gy) not in self.visited and (gx - self.w, gy) in self.grid:      
                cell.append("left")

            if (gx , gy + self.w) not in self.visited and (gx , gy + self.w) in self.grid:   
                cell.append("down")

            if (gx, gy - self.w) not in self.visited and (gx , gy - self.w) in self.grid:      
                cell.append("up")

            if len(cell) > 0:                                       
                cell_chosen = (random.choice(cell))               

                if cell_chosen == "right":                           
                    self.push_right(gx, gy)                                  
                    self.solution[(gx + self.w, gy)] = gx, gy                        
                    gx = gx + self.w                                       
                    self.visited.append((gx, gy))                              
                    self.stack.append((gx, gy))                              

                elif cell_chosen == "left":
                    self.push_left(gx, gy)
                    self.solution[(gx - self.w, gy)] = gx, gy
                    gx = gx - self.w
                    self.visited.append((gx, gy))
                    self.stack.append((gx, gy))

                elif cell_chosen == "down":
                    self.push_down(gx, gy)
                    self.solution[(gx , gy + self.w)] = gx, gy
                    gy = gy + self.w
                    self.visited.append((gx, gy))
                    self.stack.append((gx, gy))

                elif cell_chosen == "up":
                    self.push_up(gx, gy)
                    self.solution[(gx , gy - self.w)] = gx, gy
                    gy = gy - self.w
                    self.visited.append((gx, gy))
                    self.stack.append((gx, gy))
            else:
                gx, gy = self.stack.pop()                                  
                self.single_cell(gx, gy)                                   
                time.sleep(.01)                                       
                self.backtracking_cell(gx, gy)                              
    
    #function to track back the solution dictionary    
    def solve_maze(self, gx, gy):
        self.solution_cell(gx, gy)                                        
        while (gx, gy) != (self.w,self.w):                                 
            gx, gy = self.solution[gx, gy]                                
            self.solution_cell(gx, gy)                                     
            time.sleep(.1)
          
    # main function starts here    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def game_loop(self):
        self.x, self.y = self.w, self.w
        self.make_grid(20, 0)
        self.make_maze(self.x, self.y)
        self.solve_maze(self.w*self.n_col, self.w*self.n_row)

        self.running = True
        while self.running:
            self.clock.tick(self.screen_fps)
            self.handle_events()
            pygame.display.update()
        pygame.quit()
        sys.exit()

#if __name__ == "__main__":
maze = MAZE()
maze.game_loop()
