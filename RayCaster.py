import pygame
import pygame_menu

from math import cos, sin, pi
from pygame import mixer


RAY_AMOUNT = 100

# wallcolors = {
#     '1': pygame.Color('red'),
#     '2': pygame.Color('green'),
#     '3': pygame.Color('blue'),
#     '4': pygame.Color('yellow'),
#     '5': pygame.Color('purple')
#     }

wallTextures = {
    '1': pygame.image.load('wall1.png'),
    '2': pygame.image.load('wall2.png'),
    '3': pygame.image.load('wall3.png')

    }



class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.isPaused = True
        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.stepSize = 5
        self.turnSize = 5

        self.player = {
           'x' : 100,
           'y' : 175,
           'fov': 60,
           'angle': 0 ,
           'pitch': 0}


    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append( list(line.rstrip()) )

    def drawBlock(self, x, y, id):
        tex = wallTextures[id]
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
        rect = tex.get_rect()
        rect = rect.move((x,y))
        self.screen.blit(tex, rect)


    def drawPlayerIcon(self, color):
        if self.player['x'] < self.width / 2:
            rect = (self.player['x'] - 2, self.player['y'] - 2, 5,5)
            self.screen.fill(color, rect )

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        stepSize = 1
        stepX = stepSize * cos(rads)
        stepY = stepSize * sin(rads)

        playerPos = (self.player['x'],self.player['y'] )

        x = playerPos[0]
        y = playerPos[1]

        while True:
            dist += stepSize      

            x += stepX
            y += stepY

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':

                        hitX = x - i*self.blocksize
                        hitY = y - j*self.blocksize

                        hit = 0

                        if 1 < hitX < self.blocksize-1:
                            if hitY < 1:
                                hit = self.blocksize - hitX
                            elif hitY >= self.blocksize-1:
                                hit = hitX
                        elif 1 < hitY < self.blocksize-1:
                            if hitX < 1:
                                hit = hitY
                            elif hitX >= self.blocksize-1:
                                hit = self.blocksize - hitY

                        tx = hit / self.blocksize

                        pygame.draw.line(self.screen,pygame.Color('white'), playerPos, (x,y))
                        return dist, self.map[j][i], tx


    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            self.drawBlock(x, y, self.map[j][i])

        self.drawPlayerIcon(pygame.Color('black'))

        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)

            #rayWidth = 0
            rayWidth = int(( 1 / RAY_AMOUNT) * halfWidth)

            startX = halfWidth + int(( (column / RAY_AMOUNT) * halfWidth))

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle)) * wallHeight
            h = self.height / (dist * cos( (angle - self.player["angle"]) * pi / 180)) * self.wallheight
            
            #startY =int(0)
            #endY = int (500)
            startY = int(halfHeight - h/2)
            endY = int(halfHeight + h/2)

            color_k = (1 - min(1, dist / self.maxdistance)) * 255

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            tex.fill((color_k,color_k,color_k), special_flags=pygame.BLEND_MULT)
            tx = int(tx * tex.get_width())
            self.screen.blit(tex, (startX, startY), (tx,0,rayWidth,tex.get_height()))

        # Columna divisora
        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth+1, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth-1, i), pygame.Color('black'))

map = "map2.txt"

def set_difficulty(value, difficulty):
    # Do the job here !
    print("SET LEVEL to"+ str(difficulty))
    if (difficulty==1):
        map="map2.txt"
    else:
        map ="map.txt"
    rCaster.load_map(map)


def start_the_game():
    print("Start the game !!")
    #screen2 = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL )
    menu.disable()
    


    
   


width = 1000 
height = 500

pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL )
screen.set_alpha(None)

menu = pygame_menu.Menu('MAIN MENU', width, height,
                       theme=pygame_menu.themes.THEME_DARK)

menu.add.selector('Level :', [('1', 1), ('2', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

isRunning = True
isPaused= False

mixer.music.load('music.mp3')
mixer.music.play(-1)

rCaster = Raycaster(screen)
rCaster.load_map(map)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)


menu.mainloop(screen)
#menu.mainloop(screen,None,False)





def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white")) 
    return fps

def updateStatus():
    if (not isPaused):
        mode = "Playing"
    else:
        mode ="Game is paused"
    stat = font.render(mode, 1, pygame.Color("yellow")) 
    return stat

m_forward=False
m_backward=False
m_left= False
m_right= False
t_right=False
t_left=False

while isRunning:
    newX = rCaster.player['x']
    newY = rCaster.player['y']
    forward = rCaster.player['angle'] * pi / 180
    right = (rCaster.player['angle'] + 90) * pi / 180
    #forward = rCaster.player['angle'] * pi / 180
    #right = (rCaster.player['angle'] + 90) * pi / 180


    if m_forward==True and isPaused==False :
        newX += cos(forward) * rCaster.stepSize
        newY += sin(forward) * rCaster.stepSize
        # i = int(newX/rCaster.blocksize)
        # j = int(newY/rCaster.blocksize)

        # if rCaster.map[j][i] == ' ':
        #     rCaster.player['x'] = newX
        #     rCaster.player['y'] = newY

    if m_backward==True and isPaused==False :
        
        newX -= cos(forward) * rCaster.stepSize
        newY -= sin(forward) * rCaster.stepSize
        # i = int(newX/rCaster.blocksize)
        # j = int(newY/rCaster.blocksize)

        # if rCaster.map[j][i] == ' ':
        #     rCaster.player['x'] = newX
        #     rCaster.player['y'] = newY

    if m_right==True and isPaused==False:
        
        newX += cos(right) * rCaster.stepSize
        newY += sin(right) * rCaster.stepSize
        # i = int(newX/rCaster.blocksize)
        # j = int(newY/rCaster.blocksize)

        # if rCaster.map[j][i] == ' ':
        #     rCaster.player['x'] = newX
        #     rCaster.player['y'] = newY
    if m_left==True and isPaused==False :
        
        newX -= cos(right) * rCaster.stepSize
        newY -= sin(right) * rCaster.stepSize
        # i = int(newX/rCaster.blocksize)
        # j = int(newY/rCaster.blocksize)

        # if rCaster.map[j][i] == ' ':
        #     rCaster.player['x'] = newX
        #     rCaster.player['y'] = newY


    if t_left and isPaused==False:
        rCaster.player['angle'] -= rCaster.turnSize

    if t_right and isPaused==False:
        rCaster.player['angle'] += rCaster.turnSize

    i = int(newX/rCaster.blocksize)
    j = int(newY/rCaster.blocksize)

    if rCaster.map[j][i] == ' ':
        rCaster.player['x'] = newX
        rCaster.player['y'] = newY


    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        elif ev.type == pygame.KEYDOWN:

            if ev.key == pygame.K_ESCAPE:
                isPaused = not isPaused
            elif isPaused==False:
                #navigation forward
                if ev.key == pygame.K_w:
                    m_forward=True
                else:
                    m_forward=False
                #NANAvigation left
                if ev.key == pygame.K_s:
                    m_backward=True
                else:
                    m_backward=False
                #navigation left
                if ev.key == pygame.K_a:
                    m_left = True
                    
                else:
                    m_left=False
                #navigation right
                if ev.key == pygame.K_d:
                    m_right = True
                    
                else:
                    m_right=False
                if ev.key == pygame.K_q:
                    t_left=True
                else:
                    t_left=False
                if ev.key == pygame.K_e:
                    t_right=True
                else:
                    t_right=False
        elif ev.type == pygame.KEYUP:
            #print("Released")
            m_forward=False
            m_backward=False
            m_left= False
            m_right= False
            t_right=False
            t_left=False
                    

            #226324
            #4B7238



    screen.fill(pygame.Color(75,110,50,255))

    # Techo
    screen.fill(pygame.Color(115,240,245,255), (int(width / 2), 0,  int(width / 2), int(height / 2)))

    # Piso
    screen.fill(pygame.Color(75,110,50,255), (int(width / 2), int(height / 2),  int(width / 2), int(height / 2)))


    rCaster.render()

    #FPS
    screen.fill(pygame.Color("black"), (0,0,250,30) )
    screen.blit(updateFPS(), (0,0))

    screen.blit(updateStatus(),(50,0))
    clock.tick(120)


    pygame.display.flip()

pygame.quit()
