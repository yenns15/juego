import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

# Colores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Tamaño de celda
CELL_SIZE = 20

# Cargar imágenes
pacman_image = pygame.image.load('pacman.gif')
pacman_image = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))

ghost_image_1 = pygame.image.load('fantasma1.gif')
ghost_image_1 = pygame.transform.scale(ghost_image_1, (CELL_SIZE, CELL_SIZE))

ghost_image_2 = pygame.image.load('fantasma2.gif')
ghost_image_2 = pygame.transform.scale(ghost_image_2, (CELL_SIZE, CELL_SIZE))

ghost_image_3 = pygame.image.load('fantasma.gif')
ghost_image_3 = pygame.transform.scale(ghost_image_3, (CELL_SIZE, CELL_SIZE))

Fondo = pygame.image.load('Fondo.jpg')
Fondo = pygame.transform.scale(Fondo, (WIDTH, HEIGHT))



# Crear el laberinto
maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XX          XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX X      X XX.XXXXXX",
    "     ..              ..     ",
    "XXXXXX.XX X      X XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX          XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X...XX................XX...X",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Dimensiones del laberinto
maze_width = len(maze[0]) * CELL_SIZE
maze_height = len(maze) * CELL_SIZE

# Calcular el desplazamiento para centrar el laberinto
offset_x = (WIDTH - maze_width) // 2
offset_y = (HEIGHT - maze_height) // 2

# Pacman
pacman_x = 1
pacman_y = 1
pacman_direction = (1, 0)

# Fantasmas
ghosts = [
    {"x": 13, "y": 11, "image": ghost_image_1},
    {"x": 14, "y": 11, "image": ghost_image_2},  
    {"x": 13, "y": 12, "image": ghost_image_3}  
]

# Puntuación y tiempo
score = 0
font = pygame.font.Font(None, 36)
start_ticks = pygame.time.get_ticks()  # Obtener ticks al inicio del juego

# Funciones
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "X":
                pygame.draw.rect(screen, BLUE, (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (offset_x + x * CELL_SIZE + CELL_SIZE // 2, offset_y + y * CELL_SIZE + CELL_SIZE // 2), 2)

def draw_pacman():
    rotated_image = pacman_image
    if pacman_direction == (1, 0):  # Derecha
        rotated_image = pygame.transform.rotate(pacman_image, 0)
    elif pacman_direction == (-1, 0):  # Izquierda
        rotated_image = pygame.transform.rotate(pacman_image, 180)
    elif pacman_direction == (0, -1):  # Arriba
        rotated_image = pygame.transform.rotate(pacman_image, 90)
    elif pacman_direction == (0, 1):  # Abajo
        rotated_image = pygame.transform.rotate(pacman_image, -90)

    screen.blit(rotated_image, (offset_x + pacman_x * CELL_SIZE, offset_y + pacman_y * CELL_SIZE))

def draw_ghosts():
    for ghost in ghosts:
        screen.blit(ghost["image"], (offset_x + ghost["x"] * CELL_SIZE, offset_y + ghost["y"] * CELL_SIZE))

def move_pacman():
    global pacman_x, pacman_y, score
    new_x = pacman_x + pacman_direction[0]
    new_y = pacman_y + pacman_direction[1]
    if maze[new_y][new_x] != "X":
        pacman_x = new_x
        pacman_y = new_y
        if maze[pacman_y][pacman_x] == ".":
            maze[pacman_y] = maze[pacman_y][:pacman_x] + " " + maze[pacman_y][pacman_x+1:]
            score += 10

def get_valid_moves(x, y):
    valid_moves = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = x + dx, y + dy
        if maze[new_y][new_x] != "X":
            valid_moves.append((dx, dy))
    return valid_moves

def move_ghost(ghost):
    dx = pacman_x - ghost["x"]
    dy = pacman_y - ghost["y"]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    
    if distance != 0:
        dx, dy = dx / distance, dy / distance
    
    valid_moves = get_valid_moves(ghost["x"], ghost["y"])
    if valid_moves:
        best_move = min(valid_moves, key=lambda move: abs(move[0] - dx) + abs(move[1] - dy))
        ghost["x"] += best_move[0]
        ghost["y"] += best_move[1]

def move_ghosts():
    for ghost in ghosts:
        move_ghost(ghost)

# Función para mostrar mensajes en la pantalla
def show_message(text):
    screen.blit(Fondo,(0, 0))
    message_surface = font.render(text, True, WHITE)
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 - message_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def check_collision():
    for ghost in ghosts:
        if ghost["x"] == pacman_x and ghost["y"] == pacman_y:
            show_message("¡Te atrapó un fantasma!, Has perdido.")
            return True
    return False

def show_menu():
    screen.blit(Fondo,(0, 0))
    title = font.render("PACMAN", True, (0, 191, 255))

    # Opciones del menú
    options = ["Comenzar", "Controles", "Salir"]
    
    # Variable para rastrear la opción seleccionada
    selected_option = 0

    while True:
        # Redibujar el menú con el color correspondiente a la opción seleccionada
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        for i, option in enumerate(options):
            color = (0, 191, 255) if i == selected_option else WHITE
            option_surface = font.render(option, True, color)
            screen.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, HEIGHT // 2 + i * 30 - 30))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start" if selected_option == 0 else "controls" if selected_option == 1 else "exit"
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)

def show_controls():
    screen.blit(Fondo,(0, 0))
    controls_text = font.render("Controles:", True, WHITE)
    up_text = font.render("Arriba: Tecla Arriba", True, WHITE)
    down_text = font.render("Abajo: Tecla Abajo", True, WHITE)
    right_text = font.render("Derecha: Tecla Derecha", True, WHITE)
    left_text = font.render("Izquierda: Tecla Izquierda", True, WHITE)
    back_text = font.render("Presiona ESC para volver", True, WHITE)

    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(up_text, (WIDTH // 2 - up_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(down_text, (WIDTH // 2 - down_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(left_text, (WIDTH // 2 - left_text.get_width() // 2, HEIGHT // 2))
    screen.blit(right_text, (WIDTH // 2 - right_text.get_width() // 2, HEIGHT // 2 + 30))
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

    # Esperar hasta que el jugador presione ESC para volver al menú
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Bucle principal del juego
def game_loop():
    global score, pacman_direction
    clock = pygame.time.Clock()
    running = True

    while running:
        # Calcular el tiempo transcurrido
        time_passed = pygame.time.get_ticks() - start_ticks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    pacman_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman_direction = (1, 0)

        move_pacman()
        move_ghosts()

        if check_collision():
            break

        screen.fill(BLACK)
        draw_maze()
        draw_pacman()
        draw_ghosts()

        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Mostrar el tiempo
        seconds = (time_passed // 1000) % 60  # Obtener segundos
        time_text = font.render(f"Tiempo: {seconds}", True, WHITE)
        screen.blit(time_text, (WIDTH - 150, 10))  # Posicionar en la esquina superior derecha

        pygame.display.flip()
        clock.tick(10)

# Lógica principal
def main():
    while True:
        menu_selection = show_menu()
        if menu_selection == "start":
            game_loop()
        elif menu_selection == "controls":
            show_controls()
        elif menu_selection == "exit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
