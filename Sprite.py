import pygame
import random, math

#基础单元
class Scene(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#加载图块集
		self.tilesets = pygame.image.load("res/map/Tilesets/PSF_A5_Forest.png")
		self.size = 48  #图块集中的尺寸
		self.x = 4   #图块序号
		self.y = 1
		self.w = 50  #场景地图大小
		self.h = 50
		#把小块从图块集中取出来
		self.tilemap = self.tilesets.subsurface((self.x*self.size,self.y*self.size,self.size,self.size))
		#创建地图大小
		self.surface = pygame.Surface((self.size*self.w,self.size*self.h-1))
		for i in range(self.w):
			for j in range(self.h):
				self.surface.blit(self.tilemap,(i*self.size,j*self.size))
		self.rect = self.surface.get_rect()

class TileMap(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		

#英雄
class Hero(pygame.sprite.Sprite):
	def __init__(self,FPS):
		super().__init__()
		self.image = pygame.image.load("res/images/PSF_HeroesB_Casual.png")
		self.surface = self.image.subsurface((0,0,54,96))
		self.rect = self.surface.get_rect()
		self.speed = 1
		self.dt = int(FPS*300/1000)  #100毫秒一帧画面
		self.dt = self.dt if self.dt > 1 else 1  #除数不能为0
		self.index = 0
		self.direction = 3  #"left":1,"right":2,"up":3,"down":0
		self.state = 0      #"weak":1,"idle"0
		self.acceleration = 200.
		self.resistance = 30.
		self.speed = 0.
	def update(self):
		self.index += 1
		super().update()
		self.surface = self.image.subsurface(((self.index//self.dt)%3 * 54,0,54,96))
		self.surface = pygame.transform.flip(self.surface, True, False)  #Y轴镜像
	def idle(self):
		self.state = 0

class Weapon(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#self.image = pygame.image.load()


#怪物
class Enemy(pygame.sprite.Sprite):
	def __init__(self,FPS,image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.speed = 5.0
	def move(self,delta,x,y):
		distance2 = (x - self.rect.centerx) ** 2 + (y - self.rect.centery)**2
		distance = math.sqrt(distance2)
		distance = distance if distance > 0.01 else 0.01
		self.rect.centerx += int((x-self.rect.centerx)/distance*self.speed)
		self.rect.centery += int((y-self.rect.centery)/distance*self.speed)
	def play(self):
		pass
	


