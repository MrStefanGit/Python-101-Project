import pygame
from spritesheet import Spritesheet
from camera import *
from bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #player looks
        #load the frames and create rect
        self.load_frames()
        self.rect = self.idle_frames_right[0].get_rect()
        #frame info
        self.current_frame = 0
        self.last_updated = 0
        self.state = 'idle'
        #image
        self.image = self.idle_frames_right[0]
        #player physics
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT, self.ATTACKING = False, False, True, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        #bullet
        self.bullet_list = []
        
        self.score=0
        self.health=5
        self.dead = False
        
    #If the player isn't dead (finished state ) we are drawing it on the map and its bullet list
    def draw(self, display, camera):
        if self.state != 'finished':
            display.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
            for bullet in self.bullet_list:
                bullet.draw(display, camera)
    #Updating the position and checking if the player's bullets didn't colide with something 
    def update_bullet_list(self, camera):
        for bullet in self.bullet_list:
            bullet.update(self.bullet_list, camera)

    def update(self, dt, tiles, camera, enemy_list):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
        self.set_state()
        self.animate()
        self.update_bullet_list(camera)
        self.check_hit(enemy_list)
        self.check_score()
        
    #All enemies are dead you finished the game
    def check_score(self):
        if self.score == 18:
            self.dead = True
            
    def check_hit(self, enemy_list):
        for enemy in enemy_list:
            for bullet in enemy.bullet_list:
                if self.rect.colliderect(bullet):
                    self.health -=1
                    enemy.bullet_list.remove(bullet)
                    bullet.remove()
        if self.health <= 0:
            self.dead = True
            #print('player dead')

    def create_bullet(self, tiles, velocity):
        if self.FACING_LEFT != True:#Set the direction of the bullet
            bullet = Bullet(self.rect.x - 2, self.rect.y + 5, tiles, -velocity,"p")
        else:
            bullet = Bullet(self.rect.x + 11, self.rect.y + 5, tiles, velocity,"p")
        self.bullet_list.append(bullet)
    
    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                hits.append(tile)
        return hits

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .1) * (dt * dt)
        self.rect.x = self.position.x
    
    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
    #Self.state is used mostly for deciding the player's image
    def set_state(self):
        if self.state != 'finished':
            self.state = 'idle'
            if self.dead:
                self.state = 'dead'
            elif self.velocity[1] > 0:
                self.state = 'jumping'
            elif self.ATTACKING == True:
                self.state = 'attacking'
            elif self.velocity[0] < 0:
                self.state = 'moving'
                self.FACING_LEFT = False
            elif self.velocity[0] > 0:
                self.state = 'moving'
                self.FACING_LEFT = True
            
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.image = self.idle_frames_right[self.current_frame]
        elif self.state == 'dead':
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.death_frames_left)
                self.image = self.death_frames_left[self.current_frame]
                if self.current_frame == len(self.death_frames_left) - 1:
                    self.state = 'finished'
        elif self.state == 'jumping':
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_left)
                if self.FACING_LEFT:
                    self.image = self.jump_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.image = self.jump_frames_right[self.current_frame]
        elif self.state == 'attacking':
            if now - self.last_updated > 80:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames_left)
                if self.FACING_LEFT:
                    self.image = self.attack_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.image = self.attack_frames_right[self.current_frame]
        elif self.state == 'moving':
            if now - self.last_updated > 50:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_left)
                if self.FACING_LEFT:
                    self.image = self.run_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.image = self.run_frames_right[self.current_frame]
        elif self.state == 'finished':
            self.image.set_alpha(0)
            print('player gone')
    
                    
                
            
    def load_frames(self):
        idle_spritesheet = Spritesheet('images/player/idle/player_idle.png')
        run_spritesheet = Spritesheet('images/player/run/player_run.png')
        jump_spritesheet = Spritesheet('images/player/jump/player_jump.png')
        attack_spritesheet = Spritesheet('images/player/attack/player_attack.png')
        death_spritesheet = Spritesheet('images/player/death/player_death.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [idle_spritesheet.parse_sprite("player_idle1.png"),
                                idle_spritesheet.parse_sprite("player_idle2.png"),
                                idle_spritesheet.parse_sprite("player_idle3.png"),
                                idle_spritesheet.parse_sprite("player_idle4.png")]
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append( pygame.transform.flip(frame,True, False) )

        self.run_frames_left = [run_spritesheet.parse_sprite("player_run1.png"),
                                run_spritesheet.parse_sprite("player_run2.png"),
                                run_spritesheet.parse_sprite("player_run3.png"),
                                run_spritesheet.parse_sprite("player_run4.png"),
                                run_spritesheet.parse_sprite("player_run5.png"),
                                run_spritesheet.parse_sprite("player_run6.png")]
        self.run_frames_right = []
        for frame in self.run_frames_left:
            self.run_frames_right.append(pygame.transform.flip(frame, True, False))

        self.jump_frames_left = [jump_spritesheet.parse_sprite("player_jump1.png"),
                                jump_spritesheet.parse_sprite("player_jump2.png"),
                                jump_spritesheet.parse_sprite("player_jump3.png")]
        self.jump_frames_right = []
        for frame in self.jump_frames_left:
            self.jump_frames_right.append(pygame.transform.flip(frame, True, False))

        self.attack_frames_left = [attack_spritesheet.parse_sprite("player_attack1.png"),
                                    attack_spritesheet.parse_sprite("player_attack2.png"),
                                    attack_spritesheet.parse_sprite("player_attack3.png"),
                                    attack_spritesheet.parse_sprite("player_attack4.png"),]
        self.attack_frames_right = []
        for frame in self.attack_frames_left:
            self.attack_frames_right.append(pygame.transform.flip(frame, True, False))

        finished_img = pygame.image.load('images/player/death/player_finished.png').convert()
        self.death_frames_left = [death_spritesheet.parse_sprite("player_death1.png"),
                                death_spritesheet.parse_sprite("player_death2.png"),
                                death_spritesheet.parse_sprite("player_death3.png"),
                                death_spritesheet.parse_sprite("player_death4.png"),
                                death_spritesheet.parse_sprite("player_death5.png"),
                                death_spritesheet.parse_sprite("player_death6.png"),
                                death_spritesheet.parse_sprite("player_death7.png"),
                                death_spritesheet.parse_sprite("player_death8.png"),
                                finished_img]
        
        