import pygame #ゲームメイン画面
import random
import sys
import start
import game

# Pygameの初期化
pygame.init()

# ゲームウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("シューティングゲーム")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)



# FPSの設定
clock = pygame.time.Clock()
fps = 60

running = True

game_state= "start_menu"

start.draw_menu()


pygame.quit()
sys.exit()

import pygame
import sys
import game

# Pygameの初期化
pygame.init()

# ウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Menu")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# メニュー項目と状態
menu_items = ['Game Start', 'Quit']
selected_item = 0  # 最初の項目を選択

# フォントの設定
font = pygame.font.Font(None, 36)

def load_high_score():
    """ファイルからハイスコアを読み込む。ファイルが存在しない場合は0を返す"""
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    
# ゲーム起動時にハイスコアを読み込む
global high_score
high_score = load_high_score()

def draw_menu():
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        if index == selected_item:
            label = font.render(item, True, RED)
        else:
            label = font.render(item, True, WHITE)
        screen.blit(label, (screen_width / 2 - label.get_width() / 2, 200 + index * 50))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:  # Game Start
                    game.game(high_score)

                elif selected_item == 1:  # Quit
                    pygame.quit()
                    sys.exit()

    draw_menu()
    pygame.time.wait(100)

pygame.quit()

import pygame #ゲームメイン画面
import random
import sys
import math
import start
from game_over import game_over_screen

# Pygameの初期化
pygame.init()

# ゲームウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("シューティングゲーム")
pygame.font.init()  # フォントシステムの初期化
font = pygame.font.SysFont(None, 36)  # スコア表示用のフォントを設定


# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# スピードレベルとスコア係数
speed_levels = {1: 1, 2: 2, 3: 3}
current_speed_level = 1  # 初期スピードレベル
score_multiplier = speed_levels[current_speed_level]  # 初期スコア係数

def handle_key_events(event):
    global current_speed_level, score_multiplier
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            current_speed_level = 1
        elif event.key == pygame.K_2:
            current_speed_level = 2
        elif event.key == pygame.K_3:
            current_speed_level = 3
        score_multiplier = speed_levels[current_speed_level]  # スコア係数を更新

def calculate_score(base_score):
    global score_multiplier
    return base_score * (score_multiplier ** 2)  # スコア係数の2乗を使用


# FPSの設定
def game(high_score):
    global player, enemises, score
    clock = pygame.time.Clock()
    fps = 60
    score = 0
    wave = 1
    game_over = False

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('banko.png').convert_alpha()  # 画像を読み込む
            self.image = pygame.transform.scale(self.image, (64, 64))  # 画像サイズを64x64に変更
            self.rect = self.image.get_rect(center=(screen_width / 2, screen_height - 100))
            self.speed = 3
            self.last_shot_time = 0  # 最後に弾を撃った時刻の初期化
            self.shot_delay = 500  # 弾を撃つことができる間隔（ミリ秒）

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.image = pygame.image.load('banko_left.png').convert_alpha()  # 画像を読み込む
                self.image = pygame.transform.scale(self.image, (64, 64))  # 画像サイズを64x64に変更
                self.rect.x -= self.speed* current_speed_level
            elif keys[pygame.K_RIGHT]:
                self.image = pygame.image.load('banko_right.png').convert_alpha()  # 画像を読み込む
                self.image = pygame.transform.scale(self.image, (64, 64))  # 画像サイズを64x64に変更
                self.rect.x += self.speed* current_speed_level
            elif keys[pygame.K_UP]:  # 上キーが押された場合
                self.rect.y -= self.speed* current_speed_level  # プレイヤーを上に移動
            elif keys[pygame.K_DOWN]:  # 下キーが押された場合
                self.rect.y += self.speed* current_speed_level  # プレイヤーを下に移動
            else:
                self.image = pygame.image.load('banko.png').convert_alpha()  # 画像を読み込む
                self.image = pygame.transform.scale(self.image, (64, 64))  # 画像サイズを64x64に変更
            # 画面外に出ないように制限
            self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
            self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))
            if keys[pygame.K_SPACE]:
                self.shoot()

        def shoot(self):
            now = pygame.time.get_ticks()  # 現在の時刻を取得
            # 最後に弾を撃ってから1秒以上経過しているかを確認
            if now - self.last_shot_time > self.shot_delay:
                self.last_shot_time = now  # 最後に弾を撃った時刻を更新
                bullet = PlayerBullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                player_bullets.add(bullet)
#            player_x = player.rect.centerx
#            player_y = player.rect.centery

    class EnemyBullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(EnemyBullet, self).__init__()
            self.image = pygame.Surface((4, 10))
            self.image.fill(RED)
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 3 * current_speed_level

        def update(self):
            self.rect.y += self.speed
            if self.rect.y > screen_height:
                self.kill()  # 画面外に出たら削除

    class PlayerBullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((5, 7))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = -6 * current_speed_level  # 上に向かって移動するため、速度は負の値
            self.attack_power = 1  # 弾の攻撃力を1に設定

        def update(self):
            self.rect.y += self.speed
            if self.rect.bottom < 0:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 30))
            self.image.fill(GREEN)
            self.hp = 2  # 敵の体力を2に設定


    class HomingBullet(pygame.sprite.Sprite):
        def __init__(self, start_x, start_y, target_x, target_y, angle=0):
            super().__init__()
            self.image = pygame.Surface((5, 10))  # 弾のサイズを設定
            self.image.fill(WHITE)  # 弾の色を白に設定
            self.rect = self.image.get_rect(center=(start_x, start_y))
            target_x = player.rect.centerx
            target_y = player.rect.centery
            self.angle = math.radians(angle)  # 角度をラジアンに変換
            
            self.speed = 3 * current_speed_level  # 弾の速さ
            # 目標位置に向かう速度ベクトルを計算
            self.vx, self.vy = self.calculate_velocity(start_x, start_y, target_x, target_y)

        def calculate_velocity(self, start_x, start_y, target_x, target_y):
            dx = target_x - start_x
            dy = target_y - start_y
            dist = math.hypot(dx, dy)
            if dist == 0:  # 自機と敵が同じ位置にいる場合は除外
                return 0, 0
            return (dx / dist) * self.speed, (dy / dist) * self.speed

        def update(self):
            # 計算された速度ベクトルに従って位置を更新
            self.rect.x += self.vx
            self.rect.y += self.vy
            
            # 画面外に出たら削除
            if (self.rect.y < 0 or self.rect.y > screen_height or
                self.rect.x < 0 or self.rect.x > screen_width):
                self.kill()

    class Enemy3way(Enemy):
        def __init__(self, player):
            super().__init__()
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.player = player  # 自機の参照を保持
            self.shoot_delay = 1000  # 弾を発射する間隔 (ミリ秒)
            self.last_shot = pygame.time.get_ticks()  # 最後に弾を発射した時刻

        def update(self):
#            self.rect.y += self.speedy
#            if self.rect.top > screen_height + 10:
#                self.rect.x = random.randrange(screen_width - self.rect.width)
#                self.rect.y = random.randrange(-100, -40)
#                self.speedy = random.randrange(1, 3)
                
            self.shoot()

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = HomingBullet(self.rect.centerx, self.rect.top, self.player.rect.centerx, self.player.rect.centery)
                all_sprites.add(bullet)
                # 左に15度傾けた弾
                bullet_left = HomingBullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, angle=-45)
                # 右に15度傾けた弾
                bullet_right = HomingBullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, angle=45)
                all_sprites.add(bullet_right)
                all_sprites.add(bullet_left)
                enemy_bullets.add(bullet,bullet_right,bullet_left)

    class EnemyHoming(Enemy):
        def __init__(self, player):
            super().__init__()
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.player = player  # 自機の参照を保持
            self.shoot_delay = 2000  # 弾を発射する間隔 (ミリ秒)
            self.last_shot = pygame.time.get_ticks()  # 最後に弾を発射した時刻

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > screen_height + 10:
                self.rect.x = random.randrange(screen_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 3)
                
            self.shoot()

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = HomingBullet(self.rect.centerx, self.rect.top, self.player.rect.centerx, self.player.rect.centery)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

    class NomalEnemy(Enemy):
        def __init__(self):
            super().__init__()
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.shoot_delay = 1800  # 弾を発射する間隔(ms)
            self.last_shot = pygame.time.get_ticks()  # 最後に弾を発射した時刻


        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > screen_height + 10:
                self.rect.x = random.randrange(screen_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 3)
                
            self.shoot()

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)


    all_sprites = pygame.sprite.Group()
    player = Player()
    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()  # 敵の弾のためのグループ
    player_bullets = pygame.sprite.Group()

    all_sprites.add(player)  # 自機をall_spritesグループに追加
    # 音楽ファイルを読み込む
    pygame.mixer.music.load('Loop2.mp3')  # 音楽ファイルのパスを指定

    # 音楽を無限にループさせて再生
    pygame.mixer.music.play(-1)  # -1 は無限ループを意味する

    def create_enemy(wave):
        for _ in range(wave+2):  # 敵を5体生成し、all_spritesに追加
            enemy = NomalEnemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        for _ in range(wave+1):  # 敵を5体生成し、all_spritesに追加
            enemy = EnemyHoming(player)
            all_sprites.add(enemy)
            enemies.add(enemy)

        for _ in range(wave):  # 敵を5体生成し、all_spritesに追加
            enemy = Enemy3way(player)
            all_sprites.add(enemy)
            enemies.add(enemy)

    create_enemy(wave)
    # 敵を生成する間隔（ミリ秒）
    enemy_spawn_interval = 10000  # 5秒ごとに新たな敵を生成
    last_enemy_spawn_time = pygame.time.get_ticks()  # 最後に敵を生成した時刻

    running = True      
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_key_events(event)  # キー入力の処理

        current_time = pygame.time.get_ticks()  # 現在の時刻を取得    
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 指定した間隔ごとに敵を生成
        if current_time - last_enemy_spawn_time > enemy_spawn_interval:
            create_enemy(wave)
            wave += 1
            last_enemy_spawn_time = current_time  # 最後に敵を生成した時刻を更新


        for bullet in player_bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for hit in hit_enemies:
                hit.hp -= bullet.attack_power  # 敵の体力を弾の攻撃力で減らす
                bullet.kill()  # 弾を削除
                if hit.hp <= 0:
                    hit.kill()  # 体力が0以下の敵を削除
                    score += calculate_score(1000)

        # イベント処理...



        # スプライトの更新
        all_sprites.update()
        score += calculate_score(1)
        player.update()  # プレイヤーの状態を更新


        if pygame.sprite.spritecollide(player, enemy_bullets, False):
            pygame.mixer.music.stop()
            game_over = True  # 衝突した場合、ゲームオーバー

        if game_over:
            selected_option = game_over_screen(score,high_score)  # game_over.pyの関数を呼び出し、スコアを渡す
            if selected_option == "retry":  # 
                score = 0
                high_score = start.load_high_score()
                game(high_score)

            elif selected_option == "quit":  # Quit
                pygame.quit()
                sys.exit()

        # 画面への描画
        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))  # スコアを文字列に変換
        screen.blit(score_text, (10, 10))  # スコアテキストを画面の左上に描画

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

# game_over.py
import pygame
import sys

# Pygameの初期化
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# フォントの初期化
pygame.font.init()
font = pygame.font.SysFont(None, 36)

def save_high_score(score):
    """ハイスコアをファイルに保存する"""
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# ゲームオーバー画面の関数
def game_over_screen(score,high_score):
    selected = "retry"  # デフォルトの選択肢

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected = "quit" if selected == "retry" else "retry"
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return selected

        if score > high_score:
            save_high_score(score)
            high_score = score  # ハイスコアを更新

        screen.fill((0, 0, 0))
        # スコア表示
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 100))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (10, 10))  # 画面の左上にハイスコアを表示

        # リトライ選択肢
        retry_color = (255, 255, 255) if selected == "retry" else (100, 100, 100)
        retry_text = font.render("Retry", True, retry_color)
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, 200))

        # Quit選択肢
        quit_color = (255, 255, 255) if selected == "quit" else (100, 100, 100)
        quit_text = font.render("Quit Game", True, quit_color)
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 250))

        pygame.display.flip()

# 例のスコアとゲームオーバー画面の呼び出し
#score = 100  # 仮のスコア
#result = game_over_screen(score)
#print(f"Selected option: {result}")
