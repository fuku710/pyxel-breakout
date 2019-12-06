import pyxel
import math

BALL_RADIUS = 4

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 5

BLOCK_WIDTH = 10
BLOCK_HEIGHT = 5

BLOCK_ROW = 4
BLOCK_COL = 6


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="PyxelBreakout")

        self.player_x = pyxel.width / 2
        self.player_y = 100
        self.ball_x = 60
        self.ball_y = 60
        self.ball_vx = 1
        self.ball_vy = 1
        self.blocks = [True] * BLOCK_ROW * BLOCK_COL

        pyxel.run(self.update, self.draw)

    def update(self):

        # プレイヤーの移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2
        if self.player_x <= 0:
            self.player_x = 0
        if self.player_x + PLAYER_WIDTH >= 160:
            self.player_x = 160 - PLAYER_WIDTH

        # ボールの移動
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # ボールと壁の衝突
        if self.ball_x <= 0 or self.ball_x >= 160:  # 左右の壁に衝突したら反射
            self.ball_vx *= -1
        if self.ball_y <= 0:                        # 上の壁に衝突したら反射
            self.ball_vy *= -1
        if self.ball_y >= 120:                      # 下の壁に衝突したら終了
            pyxel.quit()

        # ボールとプレイヤーの衝突
        player_l = self.player_x
        player_r = self.player_x + PLAYER_WIDTH
        player_t = self.player_y
        player_b = self.player_y + PLAYER_HEIGHT

        if self.ball_x >= player_l and self.ball_x <= player_r and self.ball_y >= player_t and self.ball_y <= player_b:
            if self.ball_x == player_l and self.ball_x == player_r:
                self.ball_vx *= -1
            if self.ball_y == player_t or self.ball_y == player_b:
                self.ball_vy *= -1

        # ボールとブロックの衝突
        block_index = 0
        for row in range(BLOCK_ROW):
            for col in range(BLOCK_COL):
                if self.blocks[block_index]:
                    block_x = col * (BLOCK_WIDTH + 5)
                    block_y = row * (BLOCK_HEIGHT + 5)

                    block_l = block_x
                    block_r = block_x + BLOCK_WIDTH
                    block_t = block_y
                    block_b = block_y + BLOCK_HEIGHT

                    if self.ball_x >= block_l and self.ball_x <= block_r and self.ball_y >= block_t and self.ball_y <= block_b:
                        self.blocks[block_index] = False
                        if self.ball_x == block_l or self.ball_x == block_r:

                            self.ball_vx *= -1
                        if self.ball_y == block_t or self.ball_y == block_b:
                            self.ball_vy *= -1
                block_index += 1

        # ブロックが全てなくなったら終了
        if not any(self.blocks):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

        # プレイヤーの描画
        pyxel.rect(self.player_x, self.player_y,
                   PLAYER_WIDTH, PLAYER_HEIGHT, 1)

        # ブロックの描画
        block_index = 0
        for row in range(BLOCK_ROW):
            for col in range(BLOCK_COL):
                if self.blocks[block_index]:
                    pyxel.rect(col * (BLOCK_WIDTH + 5), row * (BLOCK_HEIGHT + 5),
                               BLOCK_WIDTH, BLOCK_HEIGHT, 3)
                block_index += 1


App()
