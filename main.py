import pygame as game
import random, time
import asyncio
game.init()
clock = game.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
light_grey = (200, 200, 200)
beautiful_grey = (175, 175, 175)
grey = (150, 150, 150)
medium_grey = (115, 115, 115)
dark_grey = (75, 75, 75)
blue = (50, 50, 255)
light_blue = (100, 200, 255)
win_width = 800
win_height = 600
screen = game.display.set_mode((win_width, win_height))
game.display.set_caption('Ultimate Mario Game')
vx = 0
vy = 0
ground_height = 514
jump = 0
player_knockback = 0
sprint = False
max_health = 300
health = max_health
jump_height = 40
extra_speed = 2
max_jumps = 1
speed = 30
enemy_speed = 5
coins = 0
wave = 1
random_ahh_variable = 0
type3enemy_directions = {}
boss_spawned_in_this_wave = False
boss_max_health = 50
boss_health = boss_max_health
boss_alive = False
boss_last_tick = 0
boss_last_spawn = 0
health_regen = 10
energy_regen = 10
running = True
safe_zone = True
wave_types = []
wave_enemies = []
wave_spawn_timer = 0
wave_spawn_interval = 1
wave_button_rect = game.Rect(win_width//2-60, win_height-70, 120, 50)
pressed_keys = []
small_font = game.font.Font(None, 30)
medium_font = game.font.Font(None, 50)
large_font = game.font.Font(None, 70)
player_size = 40
player_pos = [win_width // 2, ground_height - player_size]
vy = 0
jump = 0
player_energy = 30
max_energy = 30
energy_last_regen = time.time()
health_last_regen = time.time()
player_image = game.image.load('./assets/images/mario.png')
player_image = game.transform.scale(player_image, (player_size, player_size)) 
small_enemy_size = 45
enemy_size = 60
large_enemy_size = 100
boss_size = 150
enemy_data = []
type1enemy = game.image.load('./assets/images/type1enemy.png')
type1enemy = game.transform.scale(type1enemy, (enemy_size, enemy_size))
type2enemy = game.image.load('./assets/images/type2enemy.png')
type2enemy = game.transform.scale(type2enemy, (enemy_size, enemy_size))
type3enemy = game.image.load('./assets/images/type3enemy.png')
type3enemy = game.transform.scale(type3enemy, (enemy_size, enemy_size))
type4enemy = game.image.load('./assets/images/type4enemy.png')
type4enemy = game.transform.scale(type4enemy, (small_enemy_size, small_enemy_size))
type5enemy = game.image.load('./assets/images/type5enemy.png')
type5enemy = game.transform.scale(type5enemy, (boss_size, boss_size))
enemy_images = {
    1: type1enemy,
    2: type2enemy,
    3: type3enemy,
    4: type4enemy,
    5: type5enemy
}

bg_image = game.image.load('./assets/images/background.jpg')
bg_image = game.transform.scale(bg_image, (win_width, win_height))

game_state = 1

def create_enemy(x, y, enemy_data, type):
    image = enemy_images[type]
    health = boss_max_health if type == 5 else 10
    enemy_data.append([x, y, image, type, health])

def spawn_boss():
    global boss_health, boss_alive, boss_last_tick, boss_last_spawn
    if not boss_spawned_in_this_wave:
        create_enemy(win_width // 2 - boss_size // 2, 100, enemy_data, 5)
        boss_health = boss_max_health
        boss_last_tick = 0
        boss_last_spawn = 0

def setup_wave():
    global wave_types, wave_enemies, boss_alive, boss_spawned_in_this_wave, wave_spawn_timer, wave_spawn_interval, wave_time_start, wave_duration, wave_display_time
    wave_types = []
    wave_enemies = []
    boss_alive = False
    boss_spawned_in_this_wave = False
    wave_display_time = time.time()
    wave_time_start = time.time()
    wave_duration = 10 + wave
    if random.randint(1, 10) == 1 and not boss_spawned_in_this_wave:
        wave_types = [5]
        wave_enemies = [5]
        spawn_boss()
        boss_alive = True
        boss_spawned_in_this_wave = True
        
    else:
        num_types = min(2, random.randint(1, 4))
        wave_types = random.sample([1, 2, 3, 4], num_types)
        wave_enemies = wave_types.copy()
    wave_spawn_timer = time.time()
    wave_spawn_interval = random.uniform(1/3, 3)



def update_enemies(enemy_data):
    global coins, boss_alive, boss_last_tick, boss_last_spawn

    for id1, enemy in enumerate(enemy_data[:]):
        x1, y1, image1, type1, health1 = enemy
        size1 = boss_size if type1 == 5 else small_enemy_size if type1 == 4 else enemy_size
        hitbox1 = game.Rect(x1, y1, size1, size1)

        for id2, other_enemy in enumerate(enemy_data[:]):
            if id1 == id2:
                continue
            x2, y2, image2, type2, health2 = other_enemy
            size2 = boss_size if type2 == 5 else small_enemy_size if type2 == 4 else enemy_size
            hitbox2 = game.Rect(x2, y2, size2, size2)
            if hitbox1.colliderect(hitbox2):
                overlap_x = (hitbox1.right - hitbox2.left) if x1 < x2 else (hitbox2.right - hitbox1.left)
                separation = overlap_x // 2 + 1
                if x1 < x2:
                    enemy[0] -= separation
                    other_enemy[0] += separation
                else:
                    enemy[0] += separation
                    other_enemy[0] -= separation
                enemy[0] = max(0, min(enemy[0], win_width - size1))
                other_enemy[0] = max(0, min(other_enemy[0], win_width - size2))

        if type1 == 5:
            boss_alive = True
            target_x = player_pos[0] + player_size // 2 - boss_size // 2
            if abs(x1 - target_x) > 2:
                if x1 < target_x:
                    x1 += min(enemy_speed / 3, target_x - x1)
                elif x1 > target_x:
                    x1 -= min(enemy_speed / 3, x1 - target_x)
            else:
                x1 = target_x
            x1 = max(0, min(x1, win_width - boss_size))
            enemy[0], enemy[1] = x1, 100
            screen.blit(image1, (x1, 100))
            now = time.time()
            if boss_last_tick == 0:
                boss_last_tick = now
            if boss_last_spawn == 0:
                boss_last_spawn = now
            if now - boss_last_tick >= 1:
                enemy[4] -= 1
                boss_last_tick = now
            if enemy[4] <= 0 and boss_alive:
                boss_alive = False
                
                enemy_data.remove(enemy)
                for _ in range(10):
                    ex = random.randint(int(x1), int(x1 + boss_size - small_enemy_size))
                    ey = boss_size - 100
                    create_enemy(ex, ey, enemy_data, 4)
                coins += boss_max_health
                continue
            if boss_alive and now - boss_last_spawn >= 1:
                spawn_types = [random.choice([1, 2, 4]), random.choice([1, 2, 3]), random.choice([2, 3])]
                spawn_x_center = x1 + boss_size // 2 - enemy_size // 2
                spawn_y = 100 + boss_size
                spawn_x_left = x1 + 10
                spawn_x_right = x1 + boss_size - enemy_size - 10
                create_enemy(spawn_x_center, spawn_y, enemy_data, spawn_types[0])
                create_enemy(spawn_x_left, spawn_y, enemy_data, spawn_types[1])
                create_enemy(spawn_x_right, spawn_y, enemy_data, spawn_types[2])
                boss_last_spawn = now

        elif type1 == 4:
            if y1 + small_enemy_size < ground_height:
                y1 += enemy_speed + 3
            else:
                y1 = ground_height - small_enemy_size
                if x1 < player_pos[0] - 10:
                    x1 += enemy_speed / 2
                elif x1 > player_pos[0] + 10:
                    x1 -= enemy_speed / 2
                x1 = max(0, min(x1, win_width - small_enemy_size))
            enemy[0], enemy[1] = x1, y1
            screen.blit(image1, (x1, y1))

        elif y1 + enemy_size < ground_height or type1 == 4:
            if type1 == 1:
                y1 += enemy_speed * 2
            elif type1 == 2:
                if x1 < player_pos[0] - 5:
                    x1 += 3
                elif x1 > player_pos[0] + 5:
                    x1 -= 3
                y1 += enemy_speed
            elif type1 == 3:
                enemy_id = id(enemy)
                if enemy_id not in type3enemy_directions:
                    type3enemy_directions[enemy_id] = random.choice([-1, 1])
                direction = type3enemy_directions[enemy_id]
                if direction == 1 and x1 + enemy_size + 5 >= win_width:
                    type3enemy_directions[enemy_id] = -1
                elif direction == -1 and x1 - 5 <= 0:
                    type3enemy_directions[enemy_id] = 1
                x1 += 5 * type3enemy_directions[enemy_id]
                y1 += enemy_speed
                x1 = max(0, min(x1, win_width - enemy_size))
            enemy[0], enemy[1] = x1, y1
            screen.blit(image1, (x1, y1))

        else:
            if type1 == 1:
                enemy_data.remove(enemy)
                coins += 1
            elif type1 == 2:
                enemy_data.remove(enemy)
                coins += 2
            elif type1 == 3:
                enemy_data.remove(enemy)
                coins += 3




def mousein(tuple, x1, y1, x2, y2):
    if tuple[0] > x1 - 1 and tuple[0] < x1 + x2 + 1 and tuple[1] > y1 - 1 and tuple[1] < y1 + y2 + 1:
        return True
    else:
        return False

def collision_check(enemy_data, player_pos):
    global running, health, game_state, player_knockback, coins, boss_health, boss_alive

    for enemy in enemy_data[:]:
        x, y, image_data, type, enemy_health = enemy
        player_x, player_y = player_pos[0], player_pos[1]
        enemy_hitbox = game.Rect(x, y, boss_size if type == 5 else (enemy_size if type != 4 else small_enemy_size), boss_size if type == 5 else (enemy_size if type != 4 else small_enemy_size))
        player_hitbox = game.Rect(player_x, player_y, player_size, player_size)
        if type == 1:
            if player_hitbox.colliderect(enemy_hitbox):
                health -= 10
                enemy_data.remove(enemy)
        if type == 2:
            if player_hitbox.colliderect(enemy_hitbox):
                health -= 15
                enemy_data.remove(enemy)
        if type == 3:
            if player_hitbox.colliderect(enemy_hitbox):
                health -= 80
                enemy_data.remove(enemy)
        if type == 4:
            if player_hitbox.colliderect(enemy_hitbox):
                if player_pos[1] + player_size - 5 <= y and vy > 0:
                    enemy_data.remove(enemy)
                    coins += 3
                elif player_pos[0] < x:
                    player_knockback -= 5
                    health -= 2
                else:
                    player_knockback += 5
                    health -= 2
        if type == 5:
            if player_hitbox.colliderect(enemy_hitbox):
                health -= 30
        if health < 1:
            health = 0
            game_state = 2

def update_player_bars():
    game.draw.rect(screen, red, (player_pos[0] - 5, player_pos[1] - 15, player_size + 10, 10))
    game.draw.rect(screen, green, (player_pos[0] - 5, player_pos[1] - 15, (player_size + 10) / max_health * health, 10))
    game.draw.rect(screen, dark_grey, (player_pos[0] - 5, player_pos[1] - 15, player_size + 10, 10), 2)
    game.draw.rect(screen, beautiful_grey, (player_pos[0] - 5, player_pos[1] - 25, player_size + 10, 10))
    game.draw.rect(screen, blue, (player_pos[0] - 5, player_pos[1] - 25, (player_size + 10) / max_energy * player_energy, 10))
    game.draw.rect(screen, dark_grey, (player_pos[0] - 5, player_pos[1] - 25, player_size + 10, 10), 2)
    
def update_boss_bar():
    if boss_alive:
        for enemy in enemy_data:
            x, y, image, type, health = enemy
            if type == 5:
                game.draw.rect(screen, red, (x - 25, y - 20, boss_size + 50, 10))
                game.draw.rect(screen, green, (x - 25, y - 20, (boss_size + 50) / boss_max_health * health, 10))
                game.draw.rect(screen, dark_grey, (x - 25, y - 20, boss_size + 50, 10), 2)
                               

def draw_wave_button():
    btn_color = beautiful_grey if mousein(game.mouse.get_pos(), wave_button_rect.x, wave_button_rect.y, wave_button_rect.width, wave_button_rect.height) else grey
    game.draw.rect(screen, btn_color, wave_button_rect)
    game.draw.rect(screen, black, wave_button_rect, 3)
    txt = small_font.render("Start Wave", True, black)
    screen.blit(txt, (wave_button_rect.x + (wave_button_rect.width - txt.get_width()) // 2, wave_button_rect.y + (wave_button_rect.height - txt.get_height()) // 2))


async def main():
    global running, game_state, random_ahh_variable, safe_zone, health, health_last_regen, player_energy, energy_last_regen
    global vx, vy, sprinting, jump, player_knockback, player_pos, wave, wave_spawn_interval, wave_spawn_timer
    global coins, type3enemy_directions
    global boss_health, boss_alive, boss_last_tick, boss_last_spawn, boss_spawned_in_this_wave

    while running:
        if game_state == 1:

            if random.randint(1, 2) == 1:
                random_ahh_variable = 0
            else:
                random_ahh_variable = 1
            for event in game.event.get():
                if safe_zone:
                    if event.type == game.MOUSEBUTTONDOWN:
                        if mousein(event.pos, wave_button_rect.x, wave_button_rect.y, wave_button_rect.width, wave_button_rect.height):
                            safe_zone = False
                            health = min(max_health, health + 10)
                            player_energy = min(max_energy, player_energy + 0)
                            setup_wave()
                if event.type == game.QUIT:
                    running = False
                elif event.type == game.MOUSEBUTTONDOWN:
                    pressed_keys.append(["MOUSE", event.pos])
                elif event.type == game.KEYDOWN:
                    if event.key == game.K_a and "a" not in pressed_keys:
                        pressed_keys.append("a")
                    elif event.key == game.K_d and "d" not in pressed_keys:
                        pressed_keys.append("d")
                    elif event.key == game.K_SPACE and "SPACE" not in pressed_keys:
                        pressed_keys.append("SPACE")
                    elif event.key == game.K_LSHIFT and "SHIFT" not in pressed_keys:
                        pressed_keys.append("SHIFT")
                elif event.type == game.KEYUP:
                    if event.key == game.K_a and "a" in pressed_keys:
                        pressed_keys.remove("a")
                    elif event.key == game.K_d and "d" in pressed_keys:
                        pressed_keys.remove("d")
                    elif event.key == game.K_LSHIFT and "SHIFT" in pressed_keys:
                        pressed_keys.remove("SHIFT")
                    elif event.key == game.K_SPACE and "SPACE" in pressed_keys:
                        pressed_keys.remove("SPACE")
            vx = 0
            sprinting = "SHIFT" in pressed_keys and player_energy > 0
            if "a" in pressed_keys:
                vx -= speed/10
            if "d" in pressed_keys:
                vx += speed/10
            if sprinting:
                vx *= extra_speed
            if "SPACE" in pressed_keys and jump < max_jumps and player_energy >= 2:
                vy -= jump_height / 3
                jump += 1
                if not safe_zone:
                    player_energy -= 2
                    if player_energy < 0:
                        player_energy = 0
            if player_pos[1] + vy >= ground_height - player_size:
                jump = 0
                player_pos[1] = ground_height - player_size
                vy = 0
            if jump > 0:
                vy += 1
            if player_pos[0] + vx < 0:
                player_pos[0] = 0
                vx = 0
                player_knockback = 0
            if player_pos[0] + player_size + vx > win_width:
                player_pos[0] = win_width - player_size
                vx = 0
                player_knockback = 0
            if player_knockback < 0:
                player_knockback += 1
            elif player_knockback > 0:
                player_knockback -= 1
            vx += player_knockback
            if player_pos[0] + vx < 0:
                player_pos[0] = 0
                vx = 0
                player_knockback = 0
            if player_pos[0] + player_size + vx > win_width:
                player_pos[0] = win_width - player_size
                vx = 0
                player_knockback = 0
            player_pos[0] += vx
            player_pos[1] += vy
            now = time.time()
            if not safe_zone and sprinting and now - energy_last_regen >= 1 and player_energy > 0:
                player_energy -= 1
                energy_last_regen = now
                if player_energy < 0:
                    player_energy = 0
            if not safe_zone and now - energy_last_regen >= 0.1 and player_energy < max_energy:
                player_energy = min(max_energy, player_energy + energy_regen / 150)
                energy_last_regen = now
            if not safe_zone and now - health_last_regen >= 0.1 and health < max_health:
                health = min(max_health, health + health_regen / 20)
                health_last_regen = now
            screen.blit(bg_image, (0, 0))
            screen.blit(player_image, (player_pos[0], player_pos[1]))
            coins_render = small_font.render(f"Coins: {coins}", True, (200, 150, 0))
            wave_render = small_font.render(f"Wave: {wave}", True, (0, 100, 200))
            screen.blit(coins_render, (20, 20))
            screen.blit(wave_render, (20, 40))
            if safe_zone:
                draw_wave_button()
            else:
                if not boss_alive:
                    wave_spawn_interval = random.uniform(1/3, 3)
                if now - wave_spawn_timer >= wave_spawn_interval and not boss_alive and now - wave_time_start < (10 + wave):
                    for t in wave_enemies:
                        x = random.randint(0, win_width - enemy_size)
                        y = 0
                        create_enemy(x, y, enemy_data, t)
                    wave_spawn_timer = now
                update_enemies(enemy_data)
                collision_check(enemy_data, player_pos)
                update_player_bars()
                update_boss_bar()
                if now - wave_time_start >= (10 + wave) and len(enemy_data) == 0:
                    wave += 1
                    safe_zone = True
                    setup_wave()
        
        elif game_state == 2:
            screen.blit(bg_image, (0, 0))
            game.draw.rect(screen, light_grey, (200, 200, win_width - 400, win_height - 400))
            game.draw.rect(screen, black, (200, 200, win_width - 400, win_height - 400), 5)
            game.draw.rect(screen, dark_grey, (250, 325, 100, 50), 3)
            game.draw.rect(screen, dark_grey, (450, 325, 100, 50), 3)
            text1 = large_font.render("You Lose!", True, red)
            text2 = small_font.render("restart", True, black)
            text3 = small_font.render("quit", True, black)
            text4 = small_font.render(f"wave survived: {wave - 1}", True, black)
            text5 = small_font.render(f"coins collected: {coins}", True, black)
            screen.blit(text1, ((win_width - text1.get_width()) / 2, 220))
            screen.blit(text2, (250 + (100 - text2.get_width()) / 2, 340))
            screen.blit(text3, (450 + (100 - text3.get_width()) / 2, 340))
            screen.blit(text4, ((win_width - text4.get_width()) / 2, 270))
            screen.blit(text5, ((win_width - text5.get_width()) / 2, 290))
            if mousein(game.mouse.get_pos(), 250, 325, 100, 50):
                game.draw.rect(screen, beautiful_grey, (250, 325, 100, 50))
                game.draw.rect(screen, black, (250, 325, 100, 50), 3)
                screen.blit(text2, (250 + (100 - text2.get_width()) / 2, 340))
            else:
                game.draw.rect(screen, dark_grey, (250, 325, 100, 50), 3)
            if mousein(game.mouse.get_pos(), 450, 325, 100, 50):
                game.draw.rect(screen, beautiful_grey, (450, 325, 100, 50))
                game.draw.rect(screen, black, (450, 325, 100, 50), 3)
                screen.blit(text3, (450 + (100 - text3.get_width()) / 2, 340))
            else:
                game.draw.rect(screen, dark_grey, (450, 325, 100, 50), 3)
            for event in game.event.get():
                if event.type == game.MOUSEBUTTONDOWN:
                    if mousein(event.pos, 250, 325, 100, 50):
                        game.draw.rect(screen, grey, (250, 325, 100, 50))
                        game.draw.rect(screen, dark_grey, (250, 325, 100, 50), 3)
                        screen.blit(text2, (250 + (100 - text2.get_width()) / 2, 340))
                        game.display.flip()
                        time.sleep(0.3)
                        
                        # game restarts
                        player_pos = [win_width // 2, ground_height - player_size]
                        health = max_health
                        coins = 0
                        enemy_data.clear()
                        jump = 0
                        vy = 0
                        vx = 0
                        player_knockback = 0
                        pressed_keys.clear()
                        random_ahh_variable = 0
                        type3enemy_directions = {}
                        boss_health = boss_max_health
                        boss_alive = False
                        boss_last_tick = 0
                        boss_last_spawn = 0
                        boss_spawned_in_this_wave = False
                        player_energy = max_energy
                        wave = 1
                        safe_zone = True
                        setup_wave()
                        game_state = 1
                        
                    elif mousein(event.pos, 450, 325, 100, 50):
                        game.draw.rect(screen, grey, (450, 325, 100, 50))
                        game.draw.rect(screen, dark_grey, (450, 325, 100, 50), 3)
                        screen.blit(text3, (450 + (100 - text3.get_width()) / 2, 340))
                        game.display.flip()
                        running = False
                        time.sleep(0.3)
                        break
                if event.type == game.QUIT:
                    game.draw.rect(screen, grey, (450, 325, 100, 50))
                    game.draw.rect(screen, dark_grey, (450, 325, 100, 50), 3)
                    screen.blit(text3, (450 + (100 - text3.get_width()) / 2, 340))
                    game.display.flip()
                    running = False
                    break

        clock.tick(30)
        game.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())