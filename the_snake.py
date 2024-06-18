from random import choice, randint

import pygame

# Константы для поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс для описания игровых объектов"""

    def __init__(self, body_color, position):
        """Описывает базовые параметры объектов"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода"""
        raise NotImplementedError(
            'Определите draw в %s.' % (self.__class__.__name__)
        )


class Snake(GameObject):
    """Класс для описания змейки"""

    def __init__(self, body_color, position):
        """
        Задаёт стартовые параметры змейки.Цвет, начальное расположениеб
        длина, напраление движения
        """
        super().__init__(body_color, position)
        self.positions = [position]
        self.direction = RIGHT
        self.length = 1
        self.last = None
        self.next_direction = None

# Метод draw класса Snake
    def draw(self):
        """Рисует змейку"""
    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Изменяет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку по экрану"""
        head = self.get_head_position()
        new_head_position_x = head[0] + self.direction[0] * GRID_SIZE
        new_head_position_y = head[1] + self.direction[1] * GRID_SIZE
        if new_head_position_x >= SCREEN_WIDTH:
            new_head_position_x = 0
        elif new_head_position_x < 0:
            new_head_position_x = SCREEN_WIDTH - GRID_SIZE
        if new_head_position_y >= SCREEN_HEIGHT:
            new_head_position_y = 0
        elif new_head_position_y < 0:
            new_head_position_y = SCREEN_HEIGHT - GRID_SIZE
        list.insert(
            self.positions, 0, (new_head_position_x, new_head_position_y)
        )
        if self.length < len(self.positions):
            self.last = list.pop(self.positions, -1)

    def get_head_position(self):
        """Получаем значения позиции головы змейки"""
        return self.positions[0]

    def reset(self):
        """
        Перезапускает змейку,
        задает случайное начальное направление движения
        """
        if self.length == 1:
            pass
        else:
            for position in self.positions[1: -1]:
                if self.get_head_position() == position:
                    screen.fill(BOARD_BACKGROUND_COLOR)
                    directions = [UP, LEFT, RIGHT, DOWN]
                    self.direction = choice(directions)
                    self.positions = [START_POSITION]
                    self.length = 1


class Apple(GameObject):
    """Класс для описания яблока"""

    def __init__(self, body_color, position):
        """
        Задаёт цвет яблока и вызывает метод randomize_position,
        чтобы установить начальную позицию яблока.
        """
        super().__init__(body_color, position)
        self.randomize_position()

    def draw(self):
        """Рисует яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Определяет случайную позицию на экране"""
        self.position = (
            (choice(range(0, GRID_WIDTH))) * GRID_SIZE,
            (choice(range(0, GRID_HEIGHT))) * GRID_SIZE
        )


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запуск игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple(APPLE_COLOR, None)
    snake = Snake(SNAKE_COLOR, START_POSITION)
    while True:
        apple.draw()
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        snake.reset()
        pygame.display.update()
        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            apple.draw()


if __name__ == '__main__':
    main()
