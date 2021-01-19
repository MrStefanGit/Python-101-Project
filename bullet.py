import pygame, sys
from spritesheet import Spritesheet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, tiles, velocity, bullet_type):
        pygame.sprite.Sprite.__init__(self)
        # Bullet type
        self.type = bullet_type
        # Bullet visuals
        self.load_frames()
        self.image = self.bullet_frames[0]
        # Bullet animation
        self.current_frame = 0
        self.last_updated = 0

    def update(self, bullet_list, camera):
        self.rect.x += self.velocity
        self.check_collisions(bullet_list, camera)
        self.animate()
        
    def draw(self,surface,camera):
        #print(str(self.rect.x-camera.offset.x)+" "+str(self.rect.y-camera.offset.y) )
        surface.blit(self.image,(self.rect.x-camera.offset.x ,self.rect.y-camera.offset.y))

    def load_frames(self):
        bullet_spritesheet = Spritesheet('images/bullet/player/bullet.png')
        e_bullet_spritesheet = Spritesheet('images/bullet/enemy/bullet.png')
        self.bullet_frames = [bullet_spritesheet.parse_sprite('bullet1.png'),
                            bullet_spritesheet.parse_sprite('bullet2.png'),
                            bullet_spritesheet.parse_sprite('bullet3.png'),
                            bullet_spritesheet.parse_sprite('bullet4.png'),
                            bullet_spritesheet.parse_sprite('bullet5.png'),
                            bullet_spritesheet.parse_sprite('bullet6.png'),]

        self.enemy_bullet_frames = [e_bullet_spritesheet.parse_sprite('bullet1.png'),
                                    e_bullet_spritesheet.parse_sprite('bullet2.png'),
                                    e_bullet_spritesheet.parse_sprite('bullet3.png')]

        

    def animate(self):
        now = pygame.time.get_ticks()
        if self.type == 'p':
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.bullet_frames)
                self.image = self.bullet_frames[self.current_frame]
        elif self.type == 'e':
            if now - self.last_updated > 80:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.enemy_bullet_frames)
                self.image = self.enemy_bullet_frames[self.current_frame]
