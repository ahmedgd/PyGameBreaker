import json
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BALL_RADIUS = 10
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 10
BALL_SPEED_X = 7
BALL_SPEED_Y = -7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SILVER = (192, 192, 192)
BLUE_BLACK = (10, 10, 40)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bricks Breaker")
copilot_background = pygame.image.load(r"static/Copilot.jpg")
copilot_background = pygame.transform.scale(copilot_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
microsoft_logo = pygame.image.load(r"static/microsoft_logo.png")
microsoft_logo = pygame.transform.scale(microsoft_logo, (BRICK_WIDTH, BRICK_HEIGHT))
cns_logo = pygame.image.load(r"static/CNS.png")
cns_logo = pygame.transform.scale(cns_logo, (BRICK_WIDTH, BRICK_HEIGHT))

ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for row in range(5) for col in range(10)]
score = 0
game_over = False
win = False
font = pygame.font.Font(None, 36)

REGISTRATION_LINK = "https://forms.office.com/Pages/ResponsePage.aspx?id=Se8oF0VYv0ij-tILIIJR2WHObAW-S8lKjVDM86zOFEpUNUtBQk81Tko4SDlIRTgwVExNWkxSSTU5Sy4u"

def load_user_data():
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
            return users[-1]["name"] if users else "Player"
    except (FileNotFoundError, IndexError):
        return "Player"

username = load_user_data()

def reset_game():
    global ball, ball_speed, paddle, bricks, score, game_over, win
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]
    paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for row in range(5) for col in range(10)]
    score = 0
    game_over = False
    win = False

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(copilot_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if retry_button.collidepoint(mouse_x, mouse_y):
                reset_game()

    mouse_x = pygame.mouse.get_pos()[0]
    paddle.x = mouse_x - PADDLE_WIDTH // 2

    if not game_over:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        if ball.bottom >= SCREEN_HEIGHT:
            game_over = True

        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                score += 10

        if not bricks:
            win = True
            game_over = True

    pygame.draw.rect(screen, BLACK, paddle)
    pygame.draw.ellipse(screen, BLUE, ball)

    for index, brick in enumerate(bricks):
        if index % 2 == 0:
            screen.blit(microsoft_logo, brick)
        else:
            screen.blit(cns_logo, brick)

    score_text = font.render("Score: " + str(score), True, WHITE)
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40))
    screen.blit(score_text, score_text_rect)

    if game_over:
        if win:
            win_text = f"Congratulations, {username}! You Won!"
            win_message = font.render(win_text, True, BLUE_BLACK)
            win_rect = win_message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(win_message, win_rect)

            # Add celebration effect (changing text color and movement)
            celebration_text = font.render("🎉 Celebrate your victory! 🎉", True, (255, 215, 0))
            celebration_rect = celebration_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
            screen.blit(celebration_text, celebration_rect)
            
            # Additional flashing effect for celebration
            pygame.draw.circle(screen, (255, 223, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 60, 10)  # Flashing circle
            pygame.draw.circle(screen, (255, 255, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 10)  # Larger flashing circle
            print("Register here:", REGISTRATION_LINK)
        else:
            lose_text = f"Sorry, {username}. Try Again!"
            lose_message = font.render(lose_text, True, BLUE_BLACK)
            lose_rect = lose_message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(lose_message, lose_rect)

        retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, retry_button)

        retry_text = font.render("Retry", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=retry_button.center)
        screen.blit(retry_text, retry_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
