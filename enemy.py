import pygame
from spritesheet import *
from bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.Surface((16,16))
        #self.image.fill((255,0,0))
        self.load_frames()
        self.image = self.idle_frames_left[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x , y
        self.bullet_list = []
        self.cooldown = 0 
        self.health = 2

        self.current_frame = 0
        self.last_updated = 0
        self.state = 'idle'
        self.FACING_LEFT = False
    #Every enemy has a list of current bullets that didn't colide with anything yet
    def update_bullet_list(self, camera):
        for bullet in self.bullet_list:
            bullet.update(self.bullet_list, camera)
        
    def update(self, camera, tiles, player, enemy_list):
        self.update_bullet_list(camera)
        self.check_hit(player, enemy_list)
        self.set_state(player)
        self.animate(tiles, player, enemy_list)
    #Drawing the enemy (his current frame image) and his bullets on the surface  
    def draw(self, surface, camera):
        surface.blit(self.image,(self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
        for bullet in self.bullet_list:
            bullet.draw(surface, camera)
        
    def create_bullet(self, tiles, player):
        if self.cooldown == 0:
            if(player.rect.x-self.rect.x) > 0:#Set the bullet direction
                direction=1
                self.FACING_LEFT = False
            else:
                direction=-1
                self.FACING_LEFT = True
            if self.FACING_LEFT:
                self.bullet_list.append(Bullet(self.rect.x + 8, self.rect.y, tiles,direction*1,"e"))
            else:
                self.bullet_list.append(Bullet(self.rect.x, self.rect.y, tiles,direction*1,"e"))
            self.cooldown = 0
        else:
            self.cooldown += 1
    #check if the enemy was hited by one of the player's bullets
    def check_hit(self, player, enemy_list):
        for bullet in player.bullet_list:
            if self.rect.colliderect(bullet):
                self.health -=1
                player.bullet_list.remove(bullet)
                bullet.remove()
        
    #Self.state is used mostly for deciding the enemy's image
    def set_state(self, player):
        if self.state != 'finished':
            self.state = 'idle'
            if self.health <= 0 :
                self.state = 'dead'
            elif self.rect.x - 240 < player.rect.x:
                if self.rect.x + 120 > player.rect.x:
                    self.state = 'attacking'
                else:
                    self.state = 'idle'
                


        
    #Dicide the current frame image for the enemy
    def animate(self, tiles, player, enemy_list):
        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated > 200:#The velocity of the animation
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_right)
                if self.FACING_LEFT:
                    self.image = self.idle_frames_left[self.current_frame]
                else:
                    self.image = self.idle_frames_right[self.current_frame]
        elif self.state == 'attacking':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames_right)
                if self.current_frame == 4:
                    self.create_bullet(tiles, player)
                if self.FACING_LEFT:
                    self.image = self.attack_frames_left[self.current_frame]
                else:
                    self.image = self.attack_frames_right[self.current_frame]
        elif self.state == 'dead':
            if now - self.last_updated > 125:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.death_frames_right)
                if self.FACING_LEFT:
                    self.image = self.death_frames_left[self.current_frame]
                else:
                    self.image = self.death_frames_right[self.current_frame]
                if self.current_frame == len(self.death_frames_right) - 1:
                    self.state = 'finished'
        elif self.state == 'finished':
                print("enemy died")
                enemy_list.remove(self)
                self.remove()
                player.score +=1
    #Loading the frames images for each state
    def load_frames(self):
        idle_spritesheet = Spritesheet('images/enemy/idle/enemy_idle.png')
        attack_spritesheet = Spritesheet('images/enemy/attack/enemy_attack.png')
        death_spritesheet = Spritesheet('images/enemy/death/enemy_death.png')

        self.idle_frames_right = [idle_spritesheet.parse_sprite('enemy_idle1.png'),
                                idle_spritesheet.parse_sprite('enemy_idle2.png'),
                                idle_spritesheet.parse_sprite('enemy_idle3.png'),
                                idle_spritesheet.parse_sprite('enemy_idle4.png')]
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame, True, False))

        self.attack_frames_right = [attack_spritesheet.parse_sprite('enemy_attack1.png'),
                                    attack_spritesheet.parse_sprite('enemy_attack2.png'),
                                    attack_spritesheet.parse_sprite('enemy_attack3.png'),
                                    attack_spritesheet.parse_sprite('enemy_attack4.png'),
                                    attack_spritesheet.parse_sprite('enemy_attack5.png'),
                                    attack_spritesheet.parse_sprite('enemy_attack6.png')]
        self.attack_frames_left = []
        for frame in self.attack_frames_right:
            self.attack_frames_left.append(pygame.transform.flip(frame, True, False))

        self.death_frames_right = [death_spritesheet.parse_sprite('enemy_death1.png'),
                                    death_spritesheet.parse_sprite('enemy_death2.png'),
                                    death_spritesheet.parse_sprite('enemy_death3.png'),
                                    death_spritesheet.parse_sprite('enemy_death4.png'),
                                    death_spritesheet.parse_sprite('enemy_death5.png'),
                                    death_spritesheet.parse_sprite('enemy_death6.png')]
        self.death_frames_left = []
        for frame in self.death_frames_right:
            self.death_frames_left.append(pygame.transform.flip(frame, True, False))

        