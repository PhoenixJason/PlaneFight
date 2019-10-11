import random
import pygame
from plane_sprites import *
pygame.init()
pygame.mixer.init()

# 定义颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 载入音乐
pygame.mixer.music.load("./sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound("./sound/bullet.wav")
bullet_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound("./sound/use_bomb.wav")
bomb_sound.set_volume(0.2)

supply_sound = pygame.mixer.Sound("./sound/supply.wav")
supply_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound("./sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound("./sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound("./sound/upgrade.wav")
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound("./sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound("./sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)

enemy2_down_sound = pygame.mixer.Sound("./sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound("./sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)

me_down_sound = pygame.mixer.Sound("./sound/me_down.wav")
me_down_sound.set_volume(0.5)


# av14551047
class GameMain(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__creat_sprites()

        # 敌人出场--设置定时器事件，创建敌机
        pygame.time.set_timer(ENEMY_APPEAR_EVENT, 1000)
        # 设置英雄发射子弹的事件
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __creat_sprites(self):
        bg1 = BackGround()
        bg2 = BackGround(False)
        self.bk_group = pygame.sprite.Group(bg1, bg2)

        # 创建英雄的精灵和精灵组
        self.hero1 = Hero()
        self.hero_group1 = pygame.sprite.Group(self.hero1)
        # 创建敌机的精灵组
        self.small_enemy_group = pygame.sprite.Group()
        self.mid_enemy_group = pygame.sprite.Group()
        self.big_enemy_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.paused = Button()
        self.paused_group = pygame.sprite.Group(self.paused)

        self.bomb_num = BombNum()
        self.bomb_num_group = pygame.sprite.Group(self.bomb_num)

        self.bullet_supply_group = pygame.sprite.Group()
        self.bomb_supply_group = pygame.sprite.Group()

    def start_game(self):
        print("小游戏开始！")
        pygame.mixer.music.play(-1)
        # 定义得分变量
        score = 0
        score_font = pygame.font.Font("./font/font.ttf", 36)
        # 定义子弹补给时间变量
        bullet_time = 0
        # 定义炸弹时间变量
        bomb_time = 0
        # 定义敌机的索引
        s_e = 0
        m_e = 0
        b_e = 0
        # 定义hero的索引
        hero1 = 0
        # 定义延迟变量
        delay = 100
        # 定义切换布尔
        switch_image = True

        # 用于阻止重复打开记录文件
        record_force = False

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(60)

            # 2.事件监听
            self.__event_handler()

            if not self.paused.paused:
                # 3.碰撞检测
                self.__check_collide()

                if not delay % 15:
                    self.hero1.fire()
                    self.hero1.life()
                if bullet_time == 1800:
                    bullet_supply = BulletSupply()
                    self.bullet_supply_group.add(bullet_supply)
                    bullet_sound.play()
                    bullet_time = 0
                if bomb_time == 1500:
                    bomb_supply = BombSupply()
                    self.bomb_supply_group.add(bomb_supply)
                    bomb_time = 0
                bomb_time += 1
                bullet_time += 1

                # 更新绘制精灵
                self.__update_sprites()

                score_text = score_font.render("Score : %s" % str(score), True, WHITE)
                self.screen.blit(score_text, (10, 5))
                bomb_text = self.bomb_num .font.render("× %d" % self.bomb_num.bomb_num, True, WHITE)
                self.screen.blit(bomb_text, (80, 635))

                for i in self.mid_enemy_group:
                    """中型敌机的摧毁"""
                    if not i.active:
                        if not delay % 3:
                            if m_e == 0:
                                enemy1_down_sound.play()
                            i.image = i.destroy_images[m_e]
                            m_e = (m_e + 1) % 5
                            if m_e == 0:
                                enemy1_down_sound.stop()
                                score += 5000
                                i.kill()
                    else:

                        if i.hit:
                            i.image = i.hit_image
                            i.hit = False
                        else:
                            i.image = pygame.image.load("./images/enemy2.png")
                        pygame.draw.line(
                            self.screen, BLACK,
                            (i.rect.left, i.rect.top - 5),
                            (i.rect.right, i.rect.top - 5),
                            2
                        )
                        life_remain = i.energy / 8
                        if life_remain >= 0.2:
                            life_line_color = GREEN
                        else:
                            life_line_color = RED
                        pygame.draw.line(
                            self.screen, life_line_color,
                            (i.rect.left, i.rect.top - 5),
                            (i.rect.left + life_remain * i.rect.width, i.rect.top - 5),
                            2
                        )

                for i in self.small_enemy_group:
                    """小型敌机的摧毁"""
                    if not i.active:
                        if not delay % 3:
                            if s_e == 0:
                                enemy1_down_sound.play()
                            i.image = i.destroy_images[s_e]
                            s_e = (s_e + 1) % 4
                            if s_e == 0:
                                enemy1_down_sound.stop()
                                score += 1000
                                i.kill()

                for e in self.big_enemy_group:
                    """大型敌机存活与击毁"""
                    if e.active:

                        pygame.draw.line(
                            self.screen, BLACK,
                            (e.rect.left, e.rect.top - 5),
                            (e.rect.right, e.rect.top - 5),
                            2
                        )
                        life_remain = e.energy / 16
                        if life_remain >= 0.2:
                            life_line_color = GREEN
                        else:
                            life_line_color = RED
                        pygame.draw.line(
                            self.screen, life_line_color,
                            (e.rect.left, e.rect.top - 5),
                            (e.rect.left + life_remain * e.rect.width, e.rect.top - 5),
                            2
                        )
                        if e.hit:
                            e.image = e.hit_image
                            e.hit = False
                        else:
                            if switch_image:
                                e.image = pygame.image.load("./images/enemy3_n1.png")
                            if not switch_image:
                                e.image = pygame.image.load("./images/enemy3_n2.png")
                    else:
                        if not delay % 3:
                            if b_e == 0:
                                enemy3_down_sound.play()
                            e.image = e.destroy_images[b_e]
                            b_e = (b_e + 1) % 6
                            if b_e == 0:
                                enemy3_down_sound.stop()
                                score += 8000
                                e.kill()

                if self.hero1.active:
                    # 5.英雄动画显示
                    if switch_image:
                        self.hero1.image = pygame.image.load("./images/me2.png")
                    elif not switch_image:
                        self.hero1.image = pygame.image.load("./images/me1.png")
                else:
                    if not delay % 3:
                        if hero1 == 0:
                            me_down_sound.play()
                        self.hero1.image = self.hero1.destroy_images[hero1]
                        hero1 = (hero1 + 1) % 4
                        if hero1 == 0:
                            me_down_sound.stop()
                            if len(self.hero1.index) > 0:
                                self.hero1.index.pop()
                                self.hero1.life_group.empty()
                                self.hero1.active = True
                            else:
                                self.hero1.kill()
                                self.__game_over()
                                # pygame.mixer.music.stop()
                                # pygame.mixer.stop()
                                # if not record_force:
                                #     record_force = True
                                #     with open("./record.txt", "r") as f:
                                #         record_score = int(f.read())
                                #
                                #     if score > record_score:
                                #         with open("./record.txt", "w") as f:
                                #             f.write(str(score))
                                # # 绘制结束界面

                if not (delay % 5):
                    switch_image = not switch_image
                delay -= 1
                if not delay:
                    delay = 100
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        # 设置敌机的最大数量
        small_num = 10
        mid_num = 5
        big_num = 1

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                print("退出游戏...")
                GameMain.__game_over()
            elif event.type == ENEMY_APPEAR_EVENT:
                small_enemy_sprite = []
                if len(small_enemy_sprite) <= small_num:
                    small_enemy_sprite = Enemy()
                    self.small_enemy_group.add(small_enemy_sprite)
                    self.enemies_group.add(small_enemy_sprite)
                if len(self.mid_enemy_group) <= mid_num:
                    mid_enemy_sprite = MidEnemy()
                    self.mid_enemy_group.add(mid_enemy_sprite)
                    self.enemies_group.add(mid_enemy_sprite)

                if len(self.big_enemy_group) <= big_num:
                    big_enemy_sprite = BigEnemy()
                    self.big_enemy_group.add(big_enemy_sprite)
                    self.enemies_group.add(big_enemy_sprite)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.paused.rect.collidepoint(event.pos):
                    self.paused.paused = not self.paused.paused
                    self.paused.update()
                    self.paused_group.draw(self.screen)

            elif event.type == pygame.MOUSEMOTION:
                if self.paused.rect.collidepoint(event.pos):
                    if self.paused.paused:
                        self.paused.image = self.paused.resume_pressed_image
                    else:
                        self.paused.image = self.paused.pause_pressed_image
                else:
                    if self.paused.paused:
                        self.paused.image = self.paused.resume_nor_image
                    else:
                        self.paused.image = self.paused.pause_nor_image

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.bomb_num.bomb_num:
                        self.bomb_num.bomb_num -= 1
                        bomb_sound.play()
                        for every in self.enemies_group:
                            if every.rect.bottom > 0:
                                every.active = False

            # elif event.type == HERO_FIRE_EVENT:
            #     self.hero1.fire()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.hero1.speed = 10
        if key_pressed[pygame.K_LEFT]:
            self.hero1.speed = -10
        if key_pressed[pygame.K_UP]:
            self.hero1.speed_y = -10
        if key_pressed[pygame.K_DOWN]:
            self.hero1.speed_y = 10

        if not key_pressed[pygame.K_RIGHT] and not key_pressed[pygame.K_LEFT] \
                and not key_pressed[pygame.K_DOWN] and not key_pressed[pygame.K_UP]:
            self.hero1.speed = 0
            self.hero1.speed_y = 0

    def __check_collide(self):
        bullets = pygame.sprite.spritecollide(self.hero1, self.bullet_supply_group, True, pygame.sprite.collide_mask)
        if len(bullets) > 0:
            if self.hero1.bullets < 2:
                self.hero1.bullets += 1
                for e in self.bullet_supply_group:
                    e.kill()
            else:
                for e in self.bullet_supply_group:
                    e.kill()
        bombs = pygame.sprite.spritecollide(self.hero1, self.bomb_supply_group, True, pygame.sprite.collide_mask)
        if len(bombs) > 0:
            if self.bomb_num.bomb_num < 3:
                self.bomb_num.bomb_num += 1
                for e in self.bomb_supply_group:
                    e.kill()
            else:
                for e in self.bomb_supply_group:
                    e.kill()

        down = pygame.sprite.groupcollide(self.enemies_group, self.hero1.bullet_group, 0, 1, pygame.sprite.collide_mask)
        if len(down) > 0:
            for e in down:
                e.energy -= 1
                e.hit = True
                if e.energy == 0:
                    e.active = False
                # e.kill()
        enemies = pygame.sprite.spritecollide(self.hero1, self.enemies_group, True, pygame.sprite.collide_mask)

        if len(enemies) > 0:
            self.hero1.active = False

            # self.hero1.kill()
            #
            # game.__game_over()

    def __update_sprites(self):

        self.bk_group.update()
        self.bk_group.draw(self.screen)
        self.big_enemy_group.update()
        self.big_enemy_group.draw(self.screen)

        self.enemies_group.update()
        self.enemies_group.draw(self.screen)

        self.hero_group1.update()
        self.hero_group1.draw(self.screen)
        self.hero1.bullet_group.update()
        self.hero1.bullet_group.draw(self.screen)
        self.paused.update()
        self.paused_group.draw(self.screen)

        self.bomb_num.update()
        self.bomb_num_group.draw(self.screen)

        self.bullet_supply_group.update()
        self.bullet_supply_group.draw(self.screen)
        self.bomb_supply_group.update()
        self.bomb_supply_group.draw(self.screen)

        self.hero1.life_group.update()
        self.hero1.life_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = GameMain()

    # 启动游戏
    game.start_game()
