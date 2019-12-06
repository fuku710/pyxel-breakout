import pyxel


PADDLE_WIDTH = 20
PADDLE_HEIGHT = 5

BLOCK_WIDTH = 10
BLOCK_HEIGHT = 5

BLOCK_ROW = 4
BLOCK_COL = 11


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="PyxelBreakout")

        self.paddle_x = pyxel.width / 2
        self.paddle_y = pyxel.height / 5 * 4
        self.ball_x = pyxel.width / 2
        self.ball_y = pyxel.height / 2
        self.ball_vx = 1
        self.ball_vy = 1
        self.blocks = [True] * BLOCK_ROW * BLOCK_COL

        pyxel.run(self.update, self.draw)

    def update(self):
        # パドルの移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.paddle_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.paddle_x += 2
        if self.paddle_x <= 0:
            self.paddle_x = 0
        if self.paddle_x + PADDLE_WIDTH >= 160:
            self.paddle_x = 160 - PADDLE_WIDTH

        # ボールの移動
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # ボールと壁の衝突
        if self.ball_x <= 0 or self.ball_x >= 160:
            self.ball_vx *= -1
        if self.ball_y <= 0:
            self.ball_vy *= -1
        if self.ball_y >= 120:
            pyxel.quit()

        # ボールとパドルの衝突
        paddle_lx = self.paddle_x
        paddle_rx = self.paddle_x + PADDLE_WIDTH
        paddle_ty = self.paddle_y

        if self.ball_y == paddle_ty and self.ball_x >= paddle_lx and self.ball_x <= paddle_rx:
            self.ball_vy *= -1

        # ボールとブロックの衝突
        block_index = 0
        for row in range(BLOCK_ROW):
            for col in range(BLOCK_COL):
                if self.blocks[block_index]:
                    block_x = col * (BLOCK_WIDTH + 5)
                    block_y = row * (BLOCK_HEIGHT + 5)

                    block_lx = block_x
                    block_rx = block_x + BLOCK_WIDTH
                    block_ty = block_y
                    block_by = block_y + BLOCK_HEIGHT

                    if self.ball_x >= block_lx and self.ball_x <= block_rx and self.ball_y >= block_ty and self.ball_y <= block_by:
                        self.blocks[block_index] = False
                        if self.ball_x >= block_lx or self.ball_x <= block_rx:
                            self.ball_vx *= -1
                        if self.ball_y >= block_ty or self.ball_y <= block_by:
                            self.ball_vy *= -1
                block_index += 1

    def draw(self):
        pyxel.cls(0)

        # パドルの描画
        pyxel.rect(self.paddle_x, self.paddle_y,
                   PADDLE_WIDTH, PADDLE_HEIGHT, 1)

        # ブロックの描画
        block_index = 0
        for row in range(BLOCK_ROW):
            for col in range(BLOCK_COL):
                if self.blocks[block_index]:
                    pyxel.rect(col * (BLOCK_WIDTH + 5), row *
                               (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT, 3)
                block_index += 1

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)


App()
