import pygame
import sys

#  === SETUP ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime Attacks Goblin")

clock = pygame.time.Clock()
FPS = 10

# === CONSTANTS ===
SPRITE_SIZE = 16
SPRITE_SPACING = 2
SCALED_SIZE = 64

# === LOAD SPRITE SHEETS ===
slime_sheet = pygame.image.load("slime_sheet_v2.png").convert_alpha()
goblin_sheet = pygame.image.load("goblin_sheet_1.png").convert_alpha()

# === FRAME EXTRACTION FUNCTION ===
def get_animation_frames(sheet, row, frame_count):
    frames = []
    for i in range(frame_count):
        x = i * (SPRITE_SIZE + SPRITE_SPACING)
        y = row * (SPRITE_SIZE + SPRITE_SPACING)
        frame = sheet.subsurface(pygame.Rect(x, y, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, (SCALED_SIZE, SCALED_SIZE))
        frames.append(frame)
    return frames

# === SLIME ANIMATIONS ===
slime_run_right = get_animation_frames(slime_sheet, row=5, frame_count=6)
slime_run_left = [pygame.transform.flip(f, True, False) for f in slime_run_right]

slime_attack_r=get_animation_frames(slime_sheet, row=1, frame_count=5)
slime_attack_l=[pygame.transform.flip(i, True, False) for i in slime_attack_r]

# === GOBLIN ANIMATIONS ===
goblin_run_left = get_animation_frames(goblin_sheet, row=5, frame_count=6)
goblin_damage = get_animation_frames(goblin_sheet, row=4, frame_count=4)

# === SLIME STATE ===
slime_x, slime_y = 100, HEIGHT // 2
slime_velocity = 5
slime_direction = "right"
slime_frame_index = 0
slime_action = "run"  # or "attack"
attack_timer = 0


goblin_x, goblin_y = 500, HEIGHT // 2
goblin_health = 5
goblin_alive = True
goblin_frame_index = 0


running = True
while running:
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if attack_timer == 0:  
        if keys[pygame.K_LEFT]:
            slime_x -= slime_velocity
            slime_direction = "left"
            slime_action = "run"
        elif keys[pygame.K_RIGHT]:
            slime_x += slime_velocity
            slime_direction = "right"
            slime_action = "run"


        if keys[pygame.K_SPACE] and attack_timer==0: 
            slime_action="attack"
            attack_timer=6
            
            distance=abs(slime_x-goblin_x)
            if distance<80 and goblin_alive: 
                goblin_health-=1
                
                if goblin_health<=0: 
                    goblin_alive=False 


    slime_frame_index += 1
    if slime_action=="attack":
        if slime_direction=="right":
            slime_frames=slime_attack_r
        else:
            slime_frames=slime_attack_l
    else: 
        slime_frames= slime_run_right if slime_direction=="right" else slime_run_left
    
    if slime_frame_index>=len(slime_frames):
        slime_frame_index=0
        if slime_action=="attack": 
            slime_action=="run"
            attack_timer=0
    
    if attack_timer>0: 
        attack_timer-=1
    
    

    screen.fill((30, 30, 40))  

    screen.blit(slime_frames[slime_frame_index], (slime_x, slime_y))

    if goblin_alive:
        screen.blit(goblin_run_left[goblin_frame_index], (goblin_x, goblin_y))
    else:
        screen.blit(goblin_damage[0], (goblin_x, goblin_y))

   
    font = pygame.font.SysFont(None, 30)
    health_text = font.render(f"Goblin HP: {goblin_health}", True, (255, 50, 50))
    screen.blit(health_text, (goblin_x, goblin_y - 30))

    pygame.display.update()


pygame.quit()
sys.exit()
