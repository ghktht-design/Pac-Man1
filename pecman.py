import arcade
import random

# =========================
# Constants
# =========================
WIDTH_WINDOW = 800
HEIGHT_WINDOW = 600
TITLE_WINDOW = "Pacman"
SIZE_TILE = 32
PLAYER_SPEED = 4

# Wall color
WALL_COLOR = arcade.color.BLUE

MAP_LEVEL = [
    "#########################",
    "#..........###..........#",
    "#.####.#####.#.####.#####",
    "#.......................#",
    "#.####.##.########.##.#.#",
    "#......##....##....##.###",
    "######.#####.##.#####.#.#",
    "#...........G...........#",
    "#.####.####.##.####.#####",
    "#..........##...........#",
    "#.####.##.########.##.#.#",
    "#......##....##....##.#.#",
    "##########.######.###.#.#",
    "#P.......................#",
    "#########################"
]

# =========================
# Player Class
# =========================
class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Create a yellow circle texture for the player
        self.texture = arcade.make_circle_texture(
            SIZE_TILE, arcade.color.YELLOW
        )
        self.center_x = x
        self.center_y = y

        # Player movement speed
        self.change_x = 0
        self.change_y = 0


# =========================
# Ghost Class (Red circle)
# =========================
class Ghost(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Create a red circle texture for the ghost
        self.texture = arcade.make_circle_texture(
            SIZE_TILE, arcade.color.RED
        )
        self.center_x = x
        self.center_y = y

        # Ghost movement speed
        self.change_x = 0
        self.change_y = 0

        # Timer to change direction
        self.time_to_change = 0


# =========================
# Pacman Game View
# =========================
class PacmanGame(arcade.View):

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.list_wall = arcade.SpriteList()
        self.list_coin = arcade.SpriteList()
        self.list_ghost = arcade.SpriteList()
        self.list_player = arcade.SpriteList()

        self.player = None
        self.score = 0
        self.lives = 3
        self.over_game = False

        self.wall_color = WALL_COLOR
        self.background_color = arcade.color.BLACK
        self.x_start = 0
        self.y_start = 0

        # Set background color
        arcade.set_background_color(self.background_color)

    # =========================
    # Setup the game
    # =========================
    def setup(self):
        self.list_wall = arcade.SpriteList()
        self.list_coin = arcade.SpriteList()
        self.list_ghost = arcade.SpriteList()
        self.list_player = arcade.SpriteList()

        self.score = 0
        self.lives = 3
        self.over_game = False

        rows = len(MAP_LEVEL)

        for row_idx, row in enumerate(MAP_LEVEL):
            for col_idx, cell in enumerate(row):
                x = col_idx * SIZE_TILE + SIZE_TILE / 2
                y = (rows - row_idx - 1) * SIZE_TILE + SIZE_TILE / 2

                if cell == "#":
                    # Create wall
                    wall = arcade.Sprite()
                    wall.texture = arcade.make_soft_square_texture(
                        SIZE_TILE, WALL_COLOR, outer_alpha=255
                    )
                    wall.center_x = x
                    wall.center_y = y
                    self.list_wall.append(wall)

                elif cell == ".":
                    # Create coin
                    coin = arcade.Sprite()
                    coin.texture = arcade.make_circle_texture(
                        8, arcade.color.YELLOW
                    )
                    coin.center_x = x
                    coin.center_y = y
                    self.list_coin.append(coin)

                elif cell == "P":
                    # Create player
                    self.player = Player(x, y)
                    self.list_player.append(self.player)

                    # Save start position
                    self.x_start = x
                    self.y_start = y

                elif cell == "G":
                    # Create ghost
                    ghost = Ghost(x, y)
                    self.list_ghost.append(ghost)

    # =========================
    # Draw everything
    # =========================
    def on_draw(self):
        self.clear()

        self.list_wall.draw()
        self.list_coin.draw()
        self.list_ghost.draw()
        self.list_player.draw()

        # Draw score
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            HEIGHT_WINDOW - 30,
            arcade.color.WHITE,
            14
        )

        # Draw lives
        arcade.draw_text(
            f"Lives: {self.lives}",
            10,
            HEIGHT_WINDOW - 55,
            arcade.color.WHITE,
            14
        )

        # Draw game over or win message
        if self.over_game:
            if self.lives <= 0:
                arcade.draw_text(
                    "GAME OVER",
                    WIDTH_WINDOW / 2,
                    HEIGHT_WINDOW / 2,
                    arcade.color.RED,
                    40,
                    anchor_x="center"
                )
            else:
                arcade.draw_text(
                    "YOU WIN",
                    WIDTH_WINDOW / 2,
                    HEIGHT_WINDOW / 2,
                    arcade.color.RED,
                    40,
                    anchor_x="center"
                )

    # =========================
    # Game update logic
    # =========================
    def on_update(self, delta_time):
        if self.over_game:
            return

        # Update player movement
        self.player.update()

        # Player collision with walls
        if arcade.check_for_collision_with_list(self.player, self.list_wall):
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        # Player collision with coins
        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.list_coin
        )
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10

        # ======= Ghost movement =======
        for ghost in self.list_ghost:
            ghost.update()

            # Change direction every 0.5 seconds
            ghost.time_to_change += delta_time
            if ghost.time_to_change >= 0.5:
                ghost.time_to_change = 0
                direction = random.choice(["up", "down", "left", "right"])
                if direction == "up":
                    ghost.change_x = 0
                    ghost.change_y = PLAYER_SPEED
                elif direction == "down":
                    ghost.change_x = 0
                    ghost.change_y = -PLAYER_SPEED
                elif direction == "left":
                    ghost.change_x = -PLAYER_SPEED
                    ghost.change_y = 0
                elif direction == "right":
                    ghost.change_x = PLAYER_SPEED
                    ghost.change_y = 0

            # Ghost collision with walls
            if arcade.check_for_collision_with_list(ghost, self.list_wall):
                ghost.center_x -= ghost.change_x
                ghost.center_y -= ghost.change_y
                ghost.change_x = 0
                ghost.change_y = 0

        # ======= Player collision with ghost =======
        if arcade.check_for_collision_with_list(self.player, self.list_ghost):
            self.lives -= 1

            # Return player to start position
            self.player.center_x = self.x_start
            self.player.center_y = self.y_start

            # Stop player movement
            self.player.change_x = 0
            self.player.change_y = 0

            # Game over if no lives left
            if self.lives <= 0:
                self.over_game = True

        # Win if all coins are collected
        if len(self.list_coin) == 0:
            self.over_game = True

    # =========================
    # Keyboard input
    # =========================
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0


# =========================
# Main function
# =========================
def main():
    window = arcade.Window(WIDTH_WINDOW, HEIGHT_WINDOW, TITLE_WINDOW)
    game = PacmanGame()
    window.show_view(game)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
