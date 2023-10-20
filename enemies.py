import pygame
import heapq


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("images/slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def choose_direction(self, player, method):
        if self.rect.top == player.rect.top and self.rect.bottom == player.rect.bottom:
            if self.rect.left - player.rect.left > self.rect.left - player.rect.right:
                return "r"
            return "l"
        elif self.rect.left == player.rect.left and self.rect.right == player.rect.right:
            if self.rect.top - player.rect.top > self.rect.top - player.rect.bottom:
                return "d"
            return "u"

        return self.choose_direction_with_greedy_method(player) if method == "greedy" \
            else self.choose_direction_with_astar_method(player)

    @staticmethod
    def heuristic(player, enemy):
        # A simple heuristic based on Manhattan distance
        return abs(player[0] - enemy[0]) + abs(player[1] - enemy[1])

    def choose_direction_with_astar_method(self, player):
        player_x, player_y = player.rect.x // 32, player.rect.y // 32
        enemy_x, enemy_y = self.rect.x // 32, self.rect.y // 32

        # Define possible moves: up, down, left, right
        moves = [(-1, 0, "l"), (1, 0, "r"), (0, -1, "u"), (0, 1, "d")]
        way_len = abs(player_x - enemy_x) + abs(player_y - enemy_y)

        # Initialize the priority queue (min-heap)
        open_set = []
        heapq.heappush(open_set, (0, (enemy_x, enemy_y), ""))

        while open_set:
            _, current, path = heapq.heappop(open_set)
            if current == (player_x, player_y) or len(path) > way_len // 2:
                return path

            for dx, dy, direction in moves:
                new_x, new_y = current[0] + dx, current[1] + dy
                new_coordinates = (new_x, new_y)
                h = self.heuristic(new_coordinates, (player_x, player_y))
                f = len(path) + h
                heapq.heappush(open_set, (f, new_coordinates, path + direction))

    def choose_direction_with_greedy_method(self, player):

        player_x, player_y = player.rect.x // 32, player.rect.y // 32
        enemy_x, enemy_y = self.rect.x // 32, self.rect.y // 32
        way = ""

        while enemy_x != player_x or enemy_y != player_y:
            dx = player_x - enemy_x
            dy = player_y - enemy_y

            if dx > 0:
                way += "r"
                enemy_x += 1
            elif dx < 0:
                way += "l"
                enemy_x -= 1
            elif dy > 0:
                way += "d"
                enemy_y += 1
            elif dy < 0:
                way += "u"
                enemy_y -= 1
        return way

    def update(self, horizontal_blocks, vertical_blocks, player):
        """
        This method is implemented with the Astar algorithm
        """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = 800
        elif self.rect.left > 800:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = 576
        elif self.rect.top > 576:
            self.rect.bottom = 0

        if self.rect.topleft in self.get_intersection_position():
            direction = self.choose_direction(player, "greedy")
            # direction = self.choose_direction(player, "astar")
            if direction[0] == "l" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction[0] == "r" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction[0] == "u" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction[0] == "d" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2

    @staticmethod
    def get_intersection_position():
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 3:
                    items.append((j * 32, i * 32))

        return items


def enviroment():
    grid = (
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
    )

    return grid


def draw_enviroment(screen):
    for i, row in enumerate(enviroment()):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(
                    screen, (0, 0, 255), [j * 32, i * 32], [j * 32 + 32, i * 32], 3
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    [j * 32, i * 32 + 32],
                    [j * 32 + 32, i * 32 + 32],
                    3,
                )
            elif item == 2:
                pygame.draw.line(
                    screen, (0, 0, 255), [j * 32, i * 32], [j * 32, i * 32 + 32], 3
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    [j * 32 + 32, i * 32],
                    [j * 32 + 32, i * 32 + 32],
                    3,
                )
