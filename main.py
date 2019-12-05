import pyxel
import math


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="PyxelBreakout")

        self.player_x = 0
        self.player_y = 100

        self.ball_x = 0
        self.ball_y = 0
        self.ball_direction = math.pi / 180 * 10

        pyxel.run(self.update, self.draw)

    def update(self):
        # プレイヤーの移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2

        # ボールの移動
        self.ball_x += math.cos(self.ball_direction)
        self.ball_y += math.sin(self.ball_direction)
        if self.ball_x < 0 or self.ball_x > 160 or self.ball_y < 0 or self.ball_y > 120:
            self.ball_direction *= -1

        print(self.ball_x, self.ball_y,self.ball_direction)

    def draw(self):
        pyxel.cls(0)

        # プレイヤーの描画
        pyxel.rect(self.player_x, self.player_y, 20, 5, 1)
        # ボールの描画
        pyxel.circ(self.ball_x, self.ball_y, 5, 2)


App()
