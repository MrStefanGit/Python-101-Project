
from tiles import *
from spritesheet import Spritesheet
from player import Player
from camera import *
from bullet import *
from enemy import *

#Load a basic window
pygame.init()
WINDOW_SIZE = [720, 480]
DISPLAY_W, DISPLAY_H = 720, 480
canvas = pygame.Surface((WINDOW_SIZE[0] / 3, WINDOW_SIZE[1] / 3))
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60
dead=False
pygame.mouse.set_visible(False)
#Load player and spritesheet
spritesheet = Spritesheet('images/tileset/tileset.png')
player = Player()

#Load camera
camera = Camera(player)

#Load the tilemap
map = TileMap('images/tilemap/tilemap.csv', spritesheet )
player.position.x, player.position.y = map.start_x, map.start_y

#Background
background_image = pygame.image.load('images/background/background.png')
background_image_1 = pygame.image.load('images/background/background1.png')
foreground_image = pygame.image.load('images/background/foreground.png')
foreground_image_1 = pygame.image.load('images/background/foreground1.png')
#Game Loop
def showscore(x,y,font,player,display):
    score=font.render("Score:"+str(player.score),True,(0,255,0))
    display.blit(score,(x,y))
while running:
    #delta time
    dt = clock.tick(60) * .001 * TARGET_FPS
    #check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_DOWN:
                player.ATTACKING = True
                player.create_bullet(map.tiles,2)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_SPACE:
                if player.is_jumping:
                    player.velocity.y *= .25
                    player.is_jumping = False
            elif event.key == pygame.K_DOWN:
                player.ATTACKING = False

    #background
    canvas.blit(background_image_1, (0, 0))
    canvas.blit(background_image, (0, 0))
    canvas.blit(foreground_image_1, (0, 0))
    canvas.blit(foreground_image, (0, 0))

    #draw map
    
    map.draw_enemies(canvas,  camera)
    map.draw_map(canvas, camera)
    
    #draw player
    player.draw(canvas, camera)
    #scroll camera
    camera.scroll()
    #update player
    player.update(dt, map.tiles)

    map.update(camera,player)
    
    #scale canvas & display it
    scaled_canvas = pygame.transform.scale(canvas, WINDOW_SIZE)
    #Show score
    showscore(textX,textY,font_score,player,scaled_canvas)
    
    window.blit(scaled_canvas, (0,0))
    #Ending text
    if dead:
        pygame.time.wait(5000)
        running=False
    if player.state == "finished":
        score=font_gameOver.render("Game Over",True,(255,255,255))
        window.blit(score,(130,100))
        score=font_gameOver.render("Your Score : "+str(player.score),True,(255,255,255))
        window.blit(score,(90,160))
        dead=True
        
    pygame.display.update()
