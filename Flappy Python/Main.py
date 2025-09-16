import pygame , random

pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)
pygame.init()

width = 480
height = 720

speed= 2

ground_x_pos=0

gravity = 0.25
snake_movment = 0

score = 0
high_score=0

game_font = pygame.font.SysFont('Roboto',70)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('.\\assets\\Flappy Python')
clock = pygame.time.Clock()

#Start menu 
menu_surface = pygame.image.load('.\\assets\\Menu.png').convert()
menu_surface = pygame.transform.scale(menu_surface, (width,height))
menu_rect = menu_surface.get_rect(topleft=(0,0))
game_active = False

#background
bg = pygame.image.load('.\\assets\\background.png').convert()
bg = pygame.transform.scale(bg, (width,height))

#grass
grass = pygame.image.load('.\\assets\\grass.png').convert_alpha()
grass_scale=0.1
grass = pygame.transform.scale(grass, (width,height*grass_scale))

#Game over
game_over_surface = pygame.image.load('.\\assets\\P_Again.png').convert()
game_over_surface = pygame.transform.scale(game_over_surface, (width, height))
game_over_rect = game_over_surface.get_rect(center=(width/2, height/2))

#snake
snake_scale= 0.15
snake_surface = pygame.image.load('.\\assets\\Python.png').convert_alpha()
snake_surface = pygame.transform.scale(snake_surface, (width*snake_scale,height*snake_scale))
snake_rect = snake_surface.get_rect(center = (width/10,(height/2)))

#pipe
pipe_width = 150
pipe_height = 400
pipe_surface = pygame.image.load('.\\assets\\pipe.png').convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (pipe_width,pipe_height))
pipe_list=[]
SpawnPipe = pygame.USEREVENT
pygame.time.set_timer(SpawnPipe,1800)

passed_pipes = []
gap=210
def create_pipe():
    pos_y = random.randrange(200,400)
    bottom_pipe = pipe_surface.get_rect(midtop=(width+width/2,pos_y+gap//2))
    top_pipe = pipe_surface.get_rect(midbottom =( width+width/2,pos_y-gap//2))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    pipes = [pipe for pipe in pipes if pipe.right > -50]
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= (height/1.5):
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

def check_collison(pipes):
    for pipe in pipes:
        if  snake_rect.colliderect(pipe):
            death_sound.play()
            return False
            
    if snake_rect.top <= -10 or snake_rect.bottom>= height+50:
        death_sound.play()
        return False
    
    return True
           
def draw_bg():
    screen.blit(bg, (ground_x_pos, height - bg.get_height()))
    screen.blit(bg, (ground_x_pos + width, height - bg.get_height())) ##second image of bg
    
    screen.blit(grass, (ground_x_pos, height - grass.get_height()))
    screen.blit(grass, (ground_x_pos + width, height - grass.get_height())) #second image of grass

def Imfasterboy():
    global ground_x_pos
    ground_x_pos -= speed
    if ground_x_pos <= -width:
        ground_x_pos = 0

def score_display(game_state):
    if game_state =='main_game': 
        score_surface= game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surface.get_rect(center=(width/2,100))
        screen.blit(score_surface, score_rect)
        
    if game_state == 'game_over':
        
        score_surface= game_font.render(f'SCORE: {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center=(width/2,100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface= game_font.render(f'HIGH SCORE: {int(high_score)}',True,(255,255,255))
        high_score_rect=high_score_surface.get_rect(center=(width/2, 650)) #HIGH SCORE position after loose
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score> high_score:
        high_score = score
    return high_score

def load_high_score():
    try:
        with open('.\\assets\\highscore.txt','r') as f:
            return int(f.read().strip())
    except:
        return 0
def save_high_score(score):
    with open ('.\\assets\\highscore.txt','w') as f:
        f.write(str(score))

high_score = load_high_score()
fly_sound = pygame.mixer.Sound('.\\assets\\fly_fly_fly.mp3')
death_sound = pygame.mixer.Sound('.\\assets\\death_sound.mp3')
score_sound = pygame.mixer.Sound('.\\assets\\score_sound.mp3')

endgame= True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:  #start menu
                    game_active = True
                    pipe_list.clear()
                    snake_rect = snake_surface.get_rect(center=(width/10, height/2))
                    snake_movment = 0
                    score = 0
                    passed_pipes.clear()
                elif endgame:  #movment
                    snake_movment = 0
                    snake_movment -= 6
                    fly_sound.play()
            if event.key == pygame.K_SPACE and endgame == False: #press SPACE to reset the game
                endgame = True
                pipe_list.clear()
                snake_rect = snake_surface.get_rect(center=(width/10, height/2))
                snake_movment = 0
                score=0
        if event.type == SpawnPipe:
            pipe_list.extend(create_pipe())
            print(pipe_list)
            
    draw_bg()   
     

    Imfasterboy()
    
    
    if not game_active:
        screen.blit(menu_surface, menu_rect)
    else:
        if endgame:
            check_collison(pipe_list)
            snake_movment+= gravity
            snake_rect.centery += snake_movment
            screen.blit(snake_surface,snake_rect)
            endgame = check_collison(pipe_list)
            
            for pipe in pipe_list:
                        if pipe.bottom >= height/1.5:
                            if snake_rect.centerx > pipe.centerx and pipe not in passed_pipes:
                                score += 1
                                score_sound.play()
                                passed_pipes.append(pipe)
            
            
            ########### PIPES
            pipe_list= move_pipes(pipe_list)
            draw_pipes(pipe_list)
            score_display('main_game')
        else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            save_high_score(high_score)
            score_display('game_over')
        
    pygame.display.update()
    clock.tick(60)



