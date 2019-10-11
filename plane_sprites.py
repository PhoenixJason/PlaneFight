import pygame
import random

# 定义屏幕变量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 定义刷新帧率
FRAME_PER_SEC = 60
# 设置敌人出现的事件
ENEMY_APPEAR_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

WHITE = (255, 255, 255)


class GameSprites(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""
    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []
        self.active = True
        self.energy = 1
        self.hit = False

    def update(self):
        self.rect.y += self.speed
        if self.active is False:
            self.speed = 0


class BackGround(GameSprites):
    def __init__(self, is_alt=True):

        super().__init__("./images/background.png")

        if is_alt is False:
            self.rect.y = -SCREEN_RECT.height

    def update(self):

        # 1.调用父类的方法实现移动

        self.rect.y += self.speed
        # 2.判断是否移出屏幕，如果移出，就应该移动回去
        if self.rect.y == SCREEN_RECT.height:

            self.rect.y = -self.rect.height


class Enemy(GameSprites):
    """敌机精灵"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵，同事指定敌机图片以及初始随机速度
        super().__init__("./images/enemy1.png", random.randrange(3, 5))
        self.destroy_images.extend([
            pygame.image.load("./images/enemy1_down1.png"),
            pygame.image.load("./images/enemy1_down2.png"),
            pygame.image.load("./images/enemy1_down3.png"),
            pygame.image.load("./images/enemy1_down4.png")
        ])

        # 指定敌机出现的随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randrange(0, max_x)

    def update(self):
        # 调用父类方法,保持垂直飞行
        super().update()

        # 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()
            # print("飞出屏幕，需要从精灵组删除")

    def destroy(self):
        for i in (0, 1, 2, 3):
            self.image = self.destroy_images[i]
            self.update()


class MidEnemy(GameSprites):
    """中型敌机精灵"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵，同事指定敌机图片以及初始随机速度
        super().__init__("./images/enemy2.png", 2)
        self.destroy_images.extend([
            pygame.image.load("./images/enemy2_down1.png"),
            pygame.image.load("./images/enemy2_down2.png"),
            pygame.image.load("./images/enemy2_down3.png"),
            pygame.image.load("./images/enemy2_down4.png"),
            pygame.image.load("./images/enemy2_down4.png")
        ])
        self.hit_image = pygame.image.load("./images/enemy2_hit.png")
        # 指定敌机出现的随机位置
        self.rect.bottom = random.randint(-SCREEN_RECT.height * 3, -SCREEN_RECT.height * 2)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randrange(0, max_x)
        self.energy = 8

    def update(self):
        # 调用父类方法,保持垂直飞行
        super().update()

        # 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()
            # print("飞出屏幕，需要从精灵组删除")


class BigEnemy(GameSprites):
    """大型敌机精灵"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵，同事指定敌机图片以及初始随机速度
        super().__init__("./images/enemy3_n1.png", 1)
        self.destroy_images.extend([
            pygame.image.load("./images/enemy3_down1.png"),
            pygame.image.load("./images/enemy3_down2.png"),
            pygame.image.load("./images/enemy3_down3.png"),
            pygame.image.load("./images/enemy3_down4.png"),
            pygame.image.load("./images/enemy3_down5.png"),
            pygame.image.load("./images/enemy3_down6.png")
        ])
        self.hit_image = pygame.image.load("./images/enemy3_hit.png")

        # 指定敌机出现的随机位置
        self.rect.bottom = random.randint(-SCREEN_RECT.height * 5, -SCREEN_RECT.height * 2)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.energy = 16

    def update(self):
        # 调用父类方法,保持垂直飞行
        super().update()

        # 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()
            # print("飞出屏幕，需要从精灵组删除")


class Bullet(GameSprites):
    """子弹精灵"""
    def __init__(self):
        super().__init__("./images/bullet1.png", -12)

    def update(self):
        super().update()
        if self.rect.y < 0:
            self.kill()


class Hero(GameSprites):

    """英雄精灵"""
    def __init__(self, num=False):
        # 1.调用父类方法，设定图片和速度
        super().__init__("./images/me1.png", 0)

        self.destroy_images.extend([
            pygame.image.load("./images/me_destroy_1.png"),
            pygame.image.load("./images/me_destroy_2.png"),
            pygame.image.load("./images/me_destroy_3.png"),
            pygame.image.load("./images/me_destroy_4.png"),
        ])

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100
        # 设置y轴上的运动速度
        self.speed_y = 0
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()
        self.bullets = 0

        # 创建生命条精灵组
        self.life_group = pygame.sprite.Group()
        self.index = [1, 2, 3]

    def update(self):

        self.rect.x += self.speed
        self.rect.y += self.speed_y

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        for i in (0, 1, 2):
            if self.bullets == 0:
                bullet = Bullet()
                bullet.rect.bottom = self.rect.y - i * 20
                bullet.rect.centerx = self.rect.centerx

                self.bullet_group.add(bullet)
            elif self.bullets == 1:
                bullet1 = Bullet()
                bullet2 = Bullet()
                bullet1.rect.bottom = self.rect.y - i * 20 + 10
                bullet1.rect.centerx = self.rect.centerx - 20
                bullet2.rect.bottom = self.rect.y - i * 20 + 10
                bullet2.rect.centerx = self.rect.centerx + 20
                self.bullet_group.add(bullet1, bullet2)
            elif self.bullets == 2:
                bullet = Bullet()
                bullet.rect.bottom = self.rect.y - i * 20 + 10
                bullet.rect.centerx = self.rect.centerx
                bullet1 = Bullet()
                bullet2 = Bullet()
                bullet1.rect.bottom = self.rect.y - i * 20 + 10
                bullet1.rect.centerx = self.rect.centerx - 35
                bullet2.rect.bottom = self.rect.y - i * 20
                bullet2.rect.centerx = self.rect.centerx + 35
                self.bullet_group.add(bullet, bullet1, bullet2)

    def life(self):
        for i in self.index:
            life = HeroLife()
            life.rect.left = SCREEN_RECT.width - 50 * i
            life.rect.bottom = SCREEN_RECT.bottom - 10
            self.life_group.add(life)


class BulletSupply(GameSprites):
    def __init__(self):
        super().__init__("./images/bullet_supply.png", 5)
        self.bottom = 100
        self.rect.left = random.randint(0, SCREEN_RECT.width - self.rect.width)


class BombSupply(GameSprites):
    def __init__(self):
        super().__init__("./images/bomb_supply.png", 5)
        self.bottom = 100
        self.rect.left = random.randint(0, SCREEN_RECT.width - self.rect.width)


class BombNum(GameSprites):
    def __init__(self):
        super().__init__("./images/bomb.png", 0)
        self.font = pygame.font.Font("font/font.ttf", 48)
        self.bomb_num = 3
        self.rect.left = 10
        self.rect.top = SCREEN_RECT.height - 10 - self.rect.height


class Button(GameSprites):
    # TODO 完成各类按键的交互
    def __init__(self):
        super().__init__("./images/pause_nor.png", 0)
        self.pause_nor_image = pygame.image.load("./images/pause_nor.png")
        self.pause_pressed_image = pygame.image.load("./images/pause_pressed.png")
        self.resume_nor_image = pygame.image.load("./images/resume_nor.png")
        self.resume_pressed_image = pygame.image.load("./images/resume_pressed.png")
        self.life_image = pygame.image.load("./images/life.png")
        self.game_over = pygame.image.load("./images/gameover.png")
        self.bomb_image = pygame.image.load("./images/bomb.png")
        self.again_image = pygame.image.load("./images/again.png")
        self.paused = False
        self.rect.left = SCREEN_RECT.width - self.rect.width - 10
        self.rect.top = 10


class HeroLife(GameSprites):
    def __init__(self):
        super().__init__("./images/life.png", 0)

    def update(self):
        super().update()
