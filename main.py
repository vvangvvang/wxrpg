#导入游戏库
import pygame
import cv2
import numpy as np
import time,random
from Sprite import *
#屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 640)
#刷新的帧率
FPS = 10

CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1
ANIMATION_FRAME_EVENT = pygame.USEREVENT + 2   #


class Game(object):
    def __init__(self):
        print("初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.enemy_image = pygame.image.load("res/images/char_red_1.png")
        self.enemy_image2 = self.enemy_image.subsurface((0,0,56*1,56))
        self.__create_sprite()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 750)
        pygame.time.set_timer(HERO_FIRE_EVENT,375)
        pygame.time.set_timer(ANIMATION_FRAME_EVENT, 100)   #动画帧100毫秒一帧
        
    def __create_sprite(self):
        self.scene = Scene()
        self.hero = Hero(FPS)   #角色更新时的时间基准
        self.hero.rect.center = self.scene.rect.center  #主角位置在地图中心
        print(dir(self.hero))
        self.enemy_group = pygame.sprite.Group()
        for i in range(100):
            enemy = Enemy(FPS,self.enemy_image2)
            enemy.rect.x = random.randint(0,self.scene.rect.width-enemy.rect.width)
            enemy.rect.y = random.randint(0,self.scene.rect.height-enemy.rect.height)
            self.enemy_group.add(enemy)
        print(dir(self.enemy_group))
        print(len(self.enemy_group))
        for i in self.enemy_group:
            print(i.speed)
            break

    def run(self):
        while True:
            self.__event_handler()
            self.__check_cllide()
            self.__update_sprite()
            pygame.display.update()
            self.clock.tick(FPS)
            print(self.clock.get_time())
            print(self.clock.get_fps())

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            if event.type == ANIMATION_FRAME_EVENT:
                for enemy in self.enemy_group:
                    enemy.play()
                self.hero.update()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            self.hero.speed = 200
            self.hero.rect.y += 20
        if keys_pressed[pygame.K_DOWN]:
            self.hero.speed = 200
            self.hero.rect.y -= 20
        if keys_pressed[pygame.K_LEFT]:
            self.hero.speed = 200
            self.hero.rect.x += 20
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 200
            self.hero.rect.x -= 20
        
    def __check_cllide(self):
        pass

    def __update_sprite(self):
        self.scene.update()
        posx = self.hero.rect.centerx -SCREEN_RECT.centerx
        posy = self.hero.rect.centery - SCREEN_RECT.centery
        #窗口范围限制
        posx = posx if posx > 0 else 0
        posx = posx if posx < self.scene.rect.width - SCREEN_RECT.width else self.scene.rect.width - SCREEN_RECT.width
        posy = posy if posy > 0 else 0
        posy = posy if posy < self.scene.rect.height - SCREEN_RECT.height else self.scene.rect.height - SCREEN_RECT.height
        
        #把窗口大小的图，从场景中取出来
        buffer_rect = pygame.Rect(posx,posy,SCREEN_RECT.width,SCREEN_RECT.height)
        buffer_frame = self.scene.surface.subsurface(buffer_rect)
        buffer_frame2 = buffer_frame.copy()
        fps, x, y = self.clock.get_fps(), self.hero.rect.centerx, self.hero.rect.centery
        for enemy in self.enemy_group:
            if buffer_rect.colliderect(enemy.rect):
                buffer_frame2.blit(enemy.image,(enemy.rect.x-posx,enemy.rect.y-posy))
            enemy.move(fps, x, y)
        self.screen.blit(buffer_frame2,(0,0))
        posx = SCREEN_RECT.width//2 -self.hero.rect.width//2
        posy = SCREEN_RECT.height//2 -self.hero.rect.height//2
        self.screen.blit(self.hero.surface,(posx,posy))
        
    def fire(self):
        pass
        
    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit(12)

if __name__ == "__main__":
    pygame.init()
    plane_start = Game()
    plane_start.run()
            
