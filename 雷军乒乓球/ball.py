import sys, pygame
import time
import random

pygame.init()

pygame.display.set_caption('雷军打乒乓球')
# 隐藏鼠标
pygame.mouse.set_visible(False)


size = width, height = 900, 600

speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

# convert 能将图片转换成统一的数据格式
# 使其显示时更快

ball = pygame.image.load('resources/leijun.png').convert_alpha()

ball = pygame.transform.scale(ball, [100, 100])

pygame.display.set_icon(ball)

plate = pygame.Surface([100, 20])
plate.fill([255, 0, 0])
plate_position = plate.get_rect(x=400, y=500)

angle = 0

speed = [2, 2]

position = ball.get_rect(x=random.randint(0, 800), y=0)

count = 0


def print_text_with_center(text, center, alpha=255, size=36, color=(255, 255, 255)):
    font = pygame.font.SysFont('simhei', size)
    text = font.render(text, True, color)
    text.set_alpha(alpha)

    textpos = text.get_rect(center=center)
    screen.blit(text, textpos)


def get_alpha():
    alpha = 255
    if get_passed_time() > 1:
        alpha = int(max(3 - get_passed_time(), 0) / 2 * 255)
    return alpha


def welcome():
    center_pos = [screen.get_rect().centerx, 100]

    alpha = get_alpha()
    ball.set_alpha(alpha)

    screen.blit(ball, ball.get_rect(center=center_pos))
    center_pos[1] += 80
    print_text_with_center('雷总打乒乓球 v0.1', center_pos, alpha=alpha, color=(255, 0, 0))
    center_pos[1] += 100

    print_text_with_center('健康游戏忠告', center_pos, alpha=alpha)
    center_pos[1] += 50
    print_text_with_center('抵制不良游戏，拒绝盗版游戏。', center_pos, alpha=alpha)
    center_pos[1] += 40
    print_text_with_center('注意自我保护，谨防受骗上当。', center_pos, alpha=alpha)
    center_pos[1] += 40
    print_text_with_center('适度游戏益脑，沉迷游戏伤身。', center_pos, alpha=alpha)
    center_pos[1] += 40
    print_text_with_center('合理安排时间，享受健康生活。', center_pos, alpha=alpha)
    center_pos[1] += 100
    print_text_with_center(
        'by 三眼鸭的编程教室', center_pos, alpha=alpha, size=16, color=(255, 255, 0)
    )


start_sound = pygame.mixer.Sound('resources/welcome.mp3')
fail_sound = pygame.mixer.Sound('resources/fail.mp3')
background_sound = pygame.mixer.Sound('resources/background.mp3')
kill_sound_list = [
    pygame.mixer.Sound('resources/first_blood.mp3'),
    pygame.mixer.Sound('resources/double_kill.mp3'),
    pygame.mixer.Sound('resources/triple_kill.mp3'),
    pygame.mixer.Sound('resources/ultra_kill.mp3'),
    pygame.mixer.Sound('resources/rampage.mp3'),
]

status = 'welcome'
angle = 0

start_sound.play()

begin = time.time()


def get_passed_time():
    return time.time() - begin


hited = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    angle += 1

    screen.fill(black)

    if status == 'welcome':
        welcome()
        if get_passed_time() > 4:
            status = 'playing'
            background_sound.play(loops=-1)
            ball.set_alpha(255)
    elif status == 'playing':
        if keys[pygame.K_LEFT]:
            plate_position = plate_position.move(-10, 0)
        elif keys[pygame.K_RIGHT]:
            plate_position = plate_position.move(10, 0)

        if position.left < 0 or position.right > width:
            speed[0] = -speed[0]

        # 上边界反弹的处理
        if position.top < 0 or position.bottom > height:
            speed[1] = -speed[1]

        # 超过下边界则输掉比赛
        if position.bottom >= height:
            status = 'lose'
            background_sound.stop()
            fail_sound.play()

        if plate_position.colliderect(position):
            if not hited:
                hited = True
                index = min(count, 4)
                kill_sound_list[index].play()

                speed[1] = -speed[1]
                count += 1

                speed[0] += 1 if speed[0] > 0 else -1
                speed[1] += 1 if speed[1] > 0 else -1
        else:
            hited = False

        position = position.move(speed)
    elif status == 'lose':
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                status = 'playing'
                position = ball.get_rect(x=random.randint(0, 800), y=0)
                speed = [2, 2]
                count = 0
                background_sound.play(loops=-1)

        font = pygame.font.SysFont('simhei', 36)
        text = font.render('你已被雷总斩杀，按方向上键继续', 1, (255, 0, 0))

        text_center = [screen.get_rect().centerx, 200]
        textpos = text.get_rect(center=text_center)

        screen.blit(text, textpos)

    if status == 'playing' or status == 'lose':
        font = pygame.font.SysFont('simhei', 36)
        text = font.render(f'击杀：{count}', 1, (255, 255, 255))
        textpos = text.get_rect(x=10, y = 10)
        screen.blit(text, textpos)

        roll_ball = pygame.transform.rotate(ball, angle)

        roll_ball_rect = roll_ball.get_rect(center=position.center)
        screen.blit(roll_ball, roll_ball_rect)
        screen.blit(plate, plate_position)
        # sprites.draw(screen)
        # sprites.update()

    # pygame.draw.circle(ball, [255, 255, 255], [50, 50], 50)

    # pygame.draw.rect(screen, [255, 0, 0], [100, 100, 100, 10])

    pygame.display.update()
    clock.tick(100)

    # keys = pygame.key.get_pressed()

    #
    # if keys[pygame.K_LEFT]:
    #     # 左方向键被按下
    #     plate_position.x -= 10
    # elif keys[pygame.K_RIGHT]:
    #     # 右方向键被按下
    #     plate_position.x += 10