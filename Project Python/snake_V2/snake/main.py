import pygame as pg
import random
import sys
import json

# Initialize Pygame and mixer
pg.init()
pg.mixer.init()

#region Khỏi tạo các thuột tính
WINDOW_HEIGH = 600
WINDOW_WIDTH = 1000
SNAKE_PART = 40

GRID_WIDTH = WINDOW_WIDTH// SNAKE_PART
GRID_HEIGH = WINDOW_HEIGH// SNAKE_PART

FPS = 60
# Biến kiểm tra xem người chơi có đang ở màn hình menu chính không
global in_menu 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)  
YELLOW = (255, 255, 0)
BG_COLOR = (46, 139, 87) 
GOLD = (218, 165, 32)

# Game variables
score1 = score2 = 0
highscore = 0
x1 = (WINDOW_WIDTH // 4 // SNAKE_PART) * SNAKE_PART
y1 = (WINDOW_HEIGH // 4 // SNAKE_PART) * SNAKE_PART
x2 = (3 * WINDOW_WIDTH // 4 // SNAKE_PART) * SNAKE_PART
y2 = (3 * WINDOW_HEIGH // 4 // SNAKE_PART) * SNAKE_PART
x1_change = y1_change = x2_change = y2_change = 0
body_snake1 = [(x1, y1)]
body_snake2 = [(x2, y2)]
print(f"x1, y1: {x1, y1}, x2, y2: {x2, y2}")
length1 = length2 = 1
speed = 5
food_positions = [(0, 0)]
bonus_food_position = [(0, 0)]
health1 = health2 = 100
food_list = ["images/bo.png", "images/dau.png", "images/nho.png", "images/dua.png", "images/tao.png" ]
food_bonus_list = ["images/taovang.png", "images/xoai.png", "images/chuoi.png", "images/duoi.png"]

 # Load images
body_image = pg.image.load('images/than.png')
body_image2 = pg.image.load('images/than2.png')
body_image = pg.transform.scale(body_image, (SNAKE_PART, SNAKE_PART))
body_image2 = pg.transform.scale(body_image2, (SNAKE_PART, SNAKE_PART))

previous_position = (-1, -1)
previous_position2 = (-1, -1)
current_food_image = random.choice(food_list)
current_bonusfood_image = random.choice(food_bonus_list)

# Default controls
DEFAULT_CONTROLS = {
    "p1_up": pg.K_w,
    "p1_down": pg.K_s,
    "p1_left": pg.K_a,
    "p1_right": pg.K_d,
    "p2_up": pg.K_UP,
    "p2_down": pg.K_DOWN,
    "p2_left": pg.K_LEFT,
    "p2_right": pg.K_RIGHT
}
#endregion

#region đĩnh nghĩa cửa sổ, âm thanh, diều kiển
# Load and Scale
try:
    bg = pg.image.load('images/theme.png')  
    bg = pg.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGH)) 
except:
    print("Warning: Background image not found!")
    bg = None

# Load sounds
try:
    eat_sound = pg.mixer.Sound('sounds/eat.wav')
    collision_sound = pg.mixer.Sound('sounds/collision.wav')
    pickup_sound = pg.mixer.Sound('sounds/pickup.wav')
    game_over_sound = pg.mixer.Sound('sounds/gameover.wav')
except:
    print("Warning: Sound files not found!")



# Try to load controls from file, use defaults if file doesn't exist
try:
    with open('controls.json', 'r') as f:
        CONTROLS = json.load(f)
except:
    CONTROLS = DEFAULT_CONTROLS

def save_controls():
    with open('controls.json', 'w') as f:
        json.dump(CONTROLS, f)


# Create window
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGH))

# Create clock
clock = pg.time.Clock()

# Load font
font = pg.font.Font(None, 48)  
small_font = pg.font.Font(None, 36)

#endregion

#region Các hàm xử lí giao diện
def spawn_food():
    while True:
        new_food_position = (random.randint(0, GRID_WIDTH - 1) * SNAKE_PART,
                             random.randint(0, GRID_HEIGH - 1) * SNAKE_PART)
        if new_food_position not in body_snake1:
            food_positions[0] = new_food_position
            break

def spawn_bonus_food():
    while True:
        new_bonus_food_position = (random.randint(0, GRID_WIDTH - 1) * SNAKE_PART,
                                   random.randint(0, GRID_HEIGH - 1) * SNAKE_PART)
        if new_bonus_food_position not in body_snake2 and new_bonus_food_position not in body_snake1:
            bonus_food_position[0] = new_bonus_food_position
            break

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_game(players):
    

    # Tải hình ảnh nền
    background_image = pg.image.load("images/bg_ingame.jpg")
    # Điều chỉnh kích thước hình ảnh nếu cần
    background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGH))
    # Vẽ hình ảnh nền
    screen.blit(background_image, (0, 0))

    # Draw grid (fainter and semi-transparent)
    grid_surface = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGH), pg.SRCALPHA)
    for i in range(0, WINDOW_WIDTH, SNAKE_PART):
        pg.draw.line(screen, (40, 40, 50), (i, 0), (i, WINDOW_HEIGH))
    # Vẽ các đường ngang
    for i in range(0, WINDOW_HEIGH, SNAKE_PART):
        pg.draw.line(screen, (40, 40, 50), (0, i), (WINDOW_WIDTH, i))
    screen.blit(grid_surface, (0, 0))


    # Draw grid (fainter)
    for i in range(0, WINDOW_WIDTH, SNAKE_PART):
        pg.draw.line(screen, (40, 40, 50), (i, 0), (i, WINDOW_HEIGH))
    # Vẽ các đường ngang
    for i in range(0, WINDOW_HEIGH, SNAKE_PART):
        pg.draw.line(screen, (40, 40, 50), (0, i), (WINDOW_WIDTH, i))
        

    # Draw snake
    for part_x, part_y in body_snake1:
            screen.blit(body_image, (part_x, part_y))
            
    if players == 2:
        for part_x, part_y in body_snake2:
            screen.blit(body_image2, (part_x, part_y))


    global previous_position, previous_position2 , current_bonusfood_image, current_food_image
    # Draw food
    food_x, food_y = food_positions[0]
    if previous_position != (food_x, food_y):
        current_food_image = random.choice(food_list)
        previous_position = (food_x, food_y)
    food_image = pg.image.load(current_food_image)
    food_image = pg.transform.scale(food_image, (SNAKE_PART, SNAKE_PART))
    screen.blit(food_image, (food_x, food_y))

    if players == 2: 
        # Draw bonus food
        bonus_x, bonus_y = bonus_food_position[0]
        if previous_position2 != (bonus_x, bonus_y):
            current_bonusfood_image = random.choice(food_bonus_list)
            previous_position2 = (bonus_x, bonus_y)
        food_bonus_image = pg.image.load(current_bonusfood_image)
        food_bonus_image = pg.transform.scale(food_bonus_image, (SNAKE_PART, SNAKE_PART))
        screen.blit(food_bonus_image, (bonus_x, bonus_y))


    # Draw scores and stats
    draw_text(f'P1: {score1}', GREEN, 10, 10)
    if players == 2:
        draw_text(f'P2: {score2}', WHITE, 10, 50)
    draw_text(f'Best: {highscore}', GOLD, 10, 90)

def menu_screen():
    while True:
        # Vẽ nền menu
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # Tạo lớp phủ trong suốt để dễ đọc chữ
        overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGH), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128)) 
        screen.blit(overlay, (0, 0))

        # Vẽ các tùy chọn trong menu
        draw_text('1. Single Player', WHITE, WINDOW_WIDTH // 2 - 150, WINDOW_HEIGH // 2)
        draw_text('2. Two Players', WHITE, WINDOW_WIDTH // 2 - 150, WINDOW_HEIGH // 2 + 60)
        draw_text('3. Settings', WHITE, WINDOW_WIDTH // 2 - 150, WINDOW_HEIGH // 2 + 120)
        draw_text('Press 1, 2 or 3 to select', YELLOW, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGH // 2 + 180)

        # Cập nhật màn hình
        pg.display.update()

        # Chờ xử lý sự kiện từ người dùng
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    return 1  # Chọn chế độ 1 người chơi
                elif event.key == pg.K_2:
                    return 2  # Chọn chế độ 2 người chơi
                elif event.key == pg.K_3:
                    settings_screen()  # Mở màn hình cài đặt
  
def settings_screen():
    global CONTROLS

    selected_control = None
    waiting_for_key = False

    while True:
        # Hiển thị màn hình cài đặt
        screen.fill(BG_COLOR)

        # Vẽ tiêu đề
        draw_text('Settings', GOLD, WINDOW_WIDTH // 2 - 100, 50)

        # Hiển thị danh sách điều khiển
        y_pos = 150
        controls_text = [
            ("Player 1 Up", "p1_up"),
            ("Player 1 Down", "p1_down"),
            ("Player 1 Left", "p1_left"),
            ("Player 1 Right", "p1_right"),
            ("Player 2 Up", "p2_up"),
            ("Player 2 Down", "p2_down"),
            ("Player 2 Left", "p2_left"),
            ("Player 2 Right", "p2_right")
        ]

        for text, control in controls_text:
            color = YELLOW if selected_control == control else WHITE
            draw_text(f"{text}: {get_key_name(CONTROLS[control])}",
                      color, WINDOW_WIDTH // 2 - 200, y_pos)
            y_pos += 50

        draw_text("Press ESC to return", WHITE, WINDOW_WIDTH // 2 - 150, y_pos + 50)

        # Cập nhật màn hình
        pg.display.update()

        # Xử lý sự kiện
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if waiting_for_key and selected_control is not None:
                    # Ghi lại phím được nhấn
                    CONTROLS[selected_control] = event.key
                    waiting_for_key = False
                    selected_control = None
                elif event.key == pg.K_ESCAPE:
                    # Quay về menu khi nhấn ESC
                    return
                else:
                    # Chọn phím điều khiển để thay đổi
                    for _, control in controls_text:
                        if CONTROLS[control] == event.key:
                            selected_control = control
                            waiting_for_key = True
                            break

#endregion

#region gameplay
def get_key_name(key_code):
    return pg.key.name(key_code).upper()

def wait_for_key():
    while True:
        event = pg.event.wait()
        if event.type == pg.KEYDOWN:
            return event.key
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()

def reset_game(players):
    global x1, y1, x2, y2, x1_change, y1_change, x2_change, y2_change, body_snake1
    global body_snake2, length1, length2, score1, score2, speed, health1, health2
    global armor1, armor2, health_items, armor_items
    
    x1 = (WINDOW_WIDTH // 4 // SNAKE_PART) * SNAKE_PART
    y1 = (WINDOW_HEIGH // 4 // SNAKE_PART) * SNAKE_PART
    x2 = (3 * WINDOW_WIDTH // 4 // SNAKE_PART) * SNAKE_PART
    y2 = (3 * WINDOW_HEIGH // 4 // SNAKE_PART) * SNAKE_PART
    x1_change = y1_change = x2_change = y2_change = 0
    body_snake1 = []
    body_snake2 = []
    length1 = length2 = 1
    score1 = score2 = 0
    speed = 5
    health1 = health2 = 100
    armor1 = armor2 = 0
    health_items = []
    armor_items = []
    spawn_food()
    spawn_bonus_food()

def check_collision_with_winner(x1, y1, body_snake1, x2, y2, body_snake2, window_width, window_height, snake_part):
    """
        Điều kiện xác định người chiến thắng:
        Loại 1: Người chơi nào va chạm tường hay vào bản thân -> Người còn lại sẽ thắng
        Loại 2:  Nếu phần đầu rắn va chạm với phần thân rắn của đối phương -> Đối phương thắng
    """
    # Kiểm tra va chạm với tường (Loại 1)
    if x1 < 0 or x1 >= window_width or y1 < 0 or y1 >= window_height:
        return 1  # Người chơi 1 thua
    if x2 < 0 or x2 >= window_width or y2 < 0 or y2 >= window_height:
        return 2  # Người chơi 2 thua

    # Kiểm tra va chạm với thân đối phương (Loại 2)
    if (x1, y1) in body_snake2:
        return 1  # Người chơi 1 thua
    if (x2, y2) in body_snake1:
        return 2  # Người chơi 2 thua

    # Kiểm tra va chạm với chính thân mình (self-collision)
    if (x1, y1) in body_snake1[:-1]:  # Kiểm tra với các đoạn trừ đoạn cuối (vừa được thêm vào)
        return 1  # Người chơi 1 thua
    if (x2, y2) in body_snake2[:-1]:  # Tương tự cho người chơi 2
        return 2  # Người chơi 2 thua

    # Không có va chạm
    return 0

def game_over_screen(players, winner):
    # Giữ nguyên trạng thái màn hình hiện tại (không cập nhật hình nền mới)
    while True:
        # Hiển thị các thông điệp kết thúc trò chơi
        if players == 1:
            draw_text(f'Game Over!', RED, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 100)
            draw_text(f'Score: {score1}', GREEN, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 40)
        elif players == 2:
            if winner == 1:
                draw_text('Player 1 Wins!', GREEN, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 140)
            elif winner == 2:
                draw_text('Player 2 Wins!', WHITE, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 140)
            else:
                draw_text('Draw!', YELLOW, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 140)
            draw_text(f'P1 Score: {score1}', GREEN, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 - 40)
            draw_text(f'P2 Score: {score2}', WHITE, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGH // 2 + 20)

        draw_text('Press SPACE to play again', YELLOW, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGH // 2 + 80)
        draw_text('Press ESC to return to menu', YELLOW, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGH // 2 + 140)

        # Cập nhật màn hình (chỉ cập nhật phần chữ)
        pg.display.update()

        # Xử lý sự kiện
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return "restart"  # Chơi lại
                elif event.key == pg.K_ESCAPE:
                    return "menu"  # Quay lại menu

#endregion

def main():
    global x1, y1, x2, y2, x1_change, y1_change, x2_change, y2_change
    global body_snake1, body_snake2, length1, length2, score1, score2, highscore, speed, health1, health2

    # Trạng thái ban đầu
    in_menu = True  # Đang ở menu chính
    gameplay = False  # Trạng thái chơi game
    players = 1  # Số người chơi mặc định là 1

    while True:
        # Vòng lặp hiển thị menu
        while in_menu:
            selected_mode = menu_screen()  # Hiển thị menu và chờ chọn chế độ
            if selected_mode == 1:
                players = 1
                in_menu = False
                gameplay = True
            elif selected_mode == 2:
                players = 2
                in_menu = False
                gameplay = True
            elif selected_mode == 3:
                settings_screen()  # Mở màn hình cài đặt

        # Bắt đầu trò chơi
        if gameplay:
            reset_game(players)

        # Vòng lặp chính của trò chơi
        move_timer = 0  # Bộ đếm thời gian di chuyển
        while gameplay:
            # Xử lý sự kiện
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    # Quay lại menu khi nhấn ESC
                    if event.key == pg.K_ESCAPE:
                        gameplay = False
                        in_menu = True

                    # Điều khiển rắn 1
                    if event.key == CONTROLS["p1_left"] and x1_change == 0:
                        x1_change = -SNAKE_PART
                        y1_change = 0
                    elif event.key == CONTROLS["p1_right"] and x1_change == 0:
                        x1_change = SNAKE_PART
                        y1_change = 0
                    elif event.key == CONTROLS["p1_up"] and y1_change == 0:
                        x1_change = 0
                        y1_change = -SNAKE_PART
                    elif event.key == CONTROLS["p1_down"] and y1_change == 0:
                        x1_change = 0
                        y1_change = SNAKE_PART

                    # Điều khiển rắn 2 (nếu có 2 người chơi)
                    if players == 2:
                        if event.key == CONTROLS["p2_left"] and x2_change == 0:
                            x2_change = -SNAKE_PART
                            y2_change = 0
                        elif event.key == CONTROLS["p2_right"] and x2_change == 0:
                            x2_change = SNAKE_PART
                            y2_change = 0
                        elif event.key == CONTROLS["p2_up"] and y2_change == 0:
                            x2_change = 0
                            y2_change = -SNAKE_PART
                        elif event.key == CONTROLS["p2_down"] and y2_change == 0:
                            x2_change = 0
                            y2_change = SNAKE_PART



            # Cập nhật thời gian di chuyển
            move_timer += clock.get_time()
            if move_timer >= 1000 / speed:
                move_timer = 0

                # Cập nhật vị trí rắn
                x1 += x1_change
                y1 += y1_change
                body_snake1.append((x1, y1))
                if len(body_snake1) > length1:
                    del body_snake1[0]

                if players == 2:
                    x2 += x2_change
                    y2 += y2_change
                    body_snake2.append((x2, y2))
                    if len(body_snake2) > length2:
                        del body_snake2[0]

            # Kiểm tra va chạm với thức ăn
            food_x, food_y = food_positions[0]
            if x1 == food_x and y1 == food_y:
                length1 += 1
                score1 += 1
                spawn_food()
                try:
                    eat_sound.play()
                except:
                    print("Warning: eat_sound not found!")
            if players == 2 and x2 == food_x and y2 == food_y:
                length2 += 1
                score2 += 1
                spawn_food()
                try:
                    eat_sound.play()
                except:
                    print("Warning: eat_sound not found!")
            # Kiểm tra va chạm với thức ăn thưởng (bonus_food)
            bonus_x, bonus_y = bonus_food_position[0]
            if x1 == bonus_x and y1 == bonus_y:
                length1 += 2  # Tăng thêm độ dài lớn hơn so với thức ăn thường
                score1 += 5   # Thêm nhiều điểm hơn khi ăn thức ăn thưởng
                spawn_bonus_food()
                try:
                    eat_sound.play()
                except:
                    print("Warning: eat_sound not found!")
            if players == 2 and x2 == bonus_x and y2 == bonus_y:
                length2 += 2
                score2 += 5
                spawn_bonus_food()
                try:
                    eat_sound.play()
                except:
                    print("Warning: eat_sound not found!")

            # Kiểm tra va chạm và xác định người thắng cuộc
            collision_result = check_collision_with_winner(
                x1, y1, body_snake1, x2, y2, body_snake2, WINDOW_WIDTH, WINDOW_HEIGH, SNAKE_PART
            )

            if collision_result == 1:  # Người chơi 1 thua
                result = game_over_screen(players, 2)  # Người chơi 2 thắng
                if result == "menu":
                    gameplay = False
                    in_menu = True
                elif result == "restart":
                    reset_game(players)

            elif collision_result == 2:  # Người chơi 2 thua
                result = game_over_screen(players, 1)  # Người chơi 1 thắng
                if result == "menu":
                    gameplay = False
                    in_menu = True
                elif result == "restart":
                    reset_game(players)


            # Vẽ màn hình
            draw_game(players)
            pg.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    main()