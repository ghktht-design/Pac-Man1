import arcade
import random

# Load Map From File
with open("map.txt", "r") as f:
    MAP_LEVEL = [line.strip() for line in f]

ROWS = len(MAP_LEVEL)
COLS = len(MAP_LEVEL[0])

SIZE_TILE = 32
WIDTH_WINDOW = COLS * SIZE_TILE
HEIGHT_WINDOW = ROWS * SIZE_TILE
TITLE_WINDOW = "Pacman"
PLAYER_SPEED = 4
POWER_TIME = 3
# =========================
# Player
# =========================
class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(SIZE_TILE, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

# =========================
# Ghost
# =========================
class Ghost(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(SIZE_TILE, arcade.color.RED)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        self.timer = 0

# =========================
# Game
# =========================
class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.walls = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.powers = arcade.SpriteList()
        self.ghosts = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.player = None
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.power_timer = 0

        arcade.set_background_color(arcade.color.BLACK)

    # =========================
    def setup(self):
        rows = len(MAP_LEVEL)

        for row_i, row in enumerate(MAP_LEVEL):
            for col_i, cell in enumerate(row):
                x = col_i * SIZE_TILE + SIZE_TILE / 2
                y = (rows - row_i - 1) * SIZE_TILE + SIZE_TILE / 2

                if cell == "#":
                    wall = arcade.Sprite()
                    wall.texture = arcade.make_soft_square_texture(SIZE_TILE, arcade.color.BLUE, 255)
                    wall.center_x = x
                    wall.center_y = y
                    self.walls.append(wall)

                elif cell == ".":
                    coin = arcade.Sprite()
                    coin.texture = arcade.make_circle_texture(8, arcade.color.YELLOW)
                    coin.center_x = x
                    coin.center_y = y
                    self.coins.append(coin)

                elif cell == "O":
                    power = arcade.Sprite()
                    power.texture = arcade.make_circle_texture(12, arcade.color.GREEN)
                    power.center_x = x
                    power.center_y = y
                    self.powers.append(power)

                elif cell == "P":
                    self.player = Player(x, y)
                    self.player_list.append(self.player)
                    self.start_x = x
                    self.start_y = y

                elif cell == "G":
                    ghost = Ghost(x, y)
                    self.ghosts.append(ghost)

    # =========================
    def on_draw(self):
        self.clear()
        self.walls.draw()
        self.coins.draw()
        self.powers.draw()
        self.ghosts.draw()
        self.player_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, HEIGHT_WINDOW-30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 10, HEIGHT_WINDOW-50, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text("GAME OVER", WIDTH_WINDOW/2, HEIGHT_WINDOW/2,
                             arcade.color.RED, 40, anchor_x="center")

    # =========================
    def on_update(self, dt):
        if self.game_over:
            return

        self.player.update()

        # Wall collision
        if arcade.check_for_collision_with_list(self.player, self.walls):
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        # Coins
        for c in arcade.check_for_collision_with_list(self.player, self.coins):
            c.remove_from_sprite_lists()
            self.score += 10

        # Power coin
        for p in arcade.check_for_collision_with_list(self.player, self.powers):
            p.remove_from_sprite_lists()
            self.power_timer = POWER_TIME

        if self.power_timer > 0:
            self.power_timer -= dt

        # Ghosts
        for g in self.ghosts:
            if self.power_timer <= 0:
                g.update()
                g.timer += dt
                if g.timer > 0.5:
                    g.timer = 0
                    g.change_x, g.change_y = random.choice([
                        (PLAYER_SPEED,0), (-PLAYER_SPEED,0),
                        (0,PLAYER_SPEED), (0,-PLAYER_SPEED)
                    ])

            if arcade.check_for_collision_with_list(g, self.walls):
                g.center_x -= g.change_x
                g.center_y -= g.change_y
                g.change_x = g.change_y = 0

        # Player hit ghost
        if arcade.check_for_collision_with_list(self.player, self.ghosts):
            if self.power_timer <= 0:
                self.lives -= 1
                self.player.center_x = self.start_x
                self.player.center_y = self.start_y
                if self.lives <= 0:
                    self.game_over = True

        # Win
        if len(self.coins) == 0:
            self.game_over = True

    # =========================
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0

# =========================
def main():
    window = arcade.Window(WIDTH_WINDOW, HEIGHT_WINDOW, TITLE_WINDOW)
    game = PacmanGame()
    window.show_view(game)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()