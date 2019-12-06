# pyxel で作る簡単ブロック崩し

## はじめに

この資料は Python のゲームライブラリ pyxel を用いてブロック崩しの作り方を説明します。
しっかりとしたブロック崩しを作るのは非常に難しいのでこの資料で作るブロック崩しは簡易的なものです。

## 環境構築

pyxel の公式ドキュメントから自分の環境に合わせて pyxel のインストールをしてください。

## pyxel アプリケーションを作る

App クラスを作ります。
App クラスにはコンストラクタである`__init__`メソッドに加えて、`update`メソッドと`draw`メソッドを作ります。
起動して最初に一度だけ実行される処理は`__init__`内に書きます。ここで pyxel の初期化と実行を行うことで毎フレーム`update`と`draw`が実行されます。
`update`内では座標の移動など値を更新する処理を書き、`draw`内では pyxel で描画するための処理を書きます。

```python
import pyxel

class App:
    def __init__(self):
      # 起動して最初に一度だけ実行される処理
      pyxel.init(160, 120, caption="PyxelBreakout")
      pyxel.run(self.update, self.draw)
    def update(self):
      # 毎フレーム実行する処理
      pass
    def draw(self):
      # 描画するための処理
      pass

# Appを実行
App()
```

これだけ書いたらコンソール上で`python main.py`と打ちましょう。ウインドウが出てくれば成功です。

## ブロック崩しに必要なパーツを描画する

pyxel アプリケーションが起動できたので、早速ブロック崩しを作っていきましょう。
一般的にブロック崩しで必要とされるものは以下のものでしょう

- ボール
- プレイヤーが操作するためのパドル
- ブロック

各パーツにはそれがどの座標に存在するかの情報が必要なので、座標を格納するための変数をコンストラクタ内で宣言していきます。
ここで座標に関する注意ですが pyxel では左上を原点として右方向に正の x 軸、下方向に正の y 軸となっています(pyxel に限らずコンピュータで座標を扱う際は大抵そうですが)。
これを念頭に入れて初期の座標を設定していきましょう。

```python
def __init__(self):
  pyxel.init(160, 120, caption="PyxelBreakout")

  # pyxel.widthはウインドウの幅
  # pyxel.heightはウインドウの高さ
  self.paddle_x = pyxel.width / 2
  self.paddle_y = pyxel.height / 5 * 4
  self.ball_x = pyxel.width / 2
  self.ball_y = pyxel.height / 2

  pyxel.run(self.update, self.draw)
```

これだけでは座標を設定しただけで何も表示されないので`draw`メソッドを以下のように書き換えてボールとプレイヤーを表示します。

```python
# パドルの幅と高さは定数としてクラス外で宣言しておく
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 5
```

```python
def draw(self):
  # 画面をクリア
  pyxel.cls(0)

  # ボールの描画
  pyxel.pix(self.ball_x, self.ball_y, 10)

  # パドルの描画
  pyxel.rect(self.paddle_x, self.paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
```

ここまでで以下のようなソースコードになっていると思うので実行してボールとパドルが表示されるのを確認しましょう。

```python
import pyxel


PADDLE_WIDTH = 20
PADDLE_HEIGHT = 5


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="PyxelBreakout")

        self.paddle_x = pyxel.width / 2
        self.paddle_y = pyxel.height / 5 * 4
        self.ball_x = pyxel.width / 2
        self.ball_y = pyxel.height / 2

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

        # パドルの描画
        pyxel.rect(self.paddle_x, self.paddle_y,
                   PADDLE_WIDTH, PADDLE_HEIGHT, 1)


App()
```

ボールとパドルの描画ができたので次はブロックを作っていきます。
ブロックは複数存在するのでリストで表現したいと思います。

定数でブロックのサイズとブロックを縦に並べる数（行）と横に並べる数（列）を定義します。

```python
BLOCK_WIDTH = 10
BLOCK_HEIGHT = 5

BLOCK_ROW = 4
BLOCK_COL = 11
```

`__init__`メソッド内にブロックの数だけ boolean 型を格納するリストを宣言します。

```python
# Trueが格納されたリストがブロックの数だけ作られる
self.blocks = [True] * BLOCK_ROW * BLOCK_COL
```

続いて`draw`メソッドにブロックの描画処理を書いていきます。

```python
block_index = 0
for row in range(BLOCK_ROW):
  for col in range(BLOCK_COL):
    if self.blocks[block_index]: # リストの値がTrueであるブロックのみ描画する
      # ブロックに隙間を作るために5を足しています
      pyxel.rect(col * (BLOCK_WIDTH + 5), row * (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT, 3)
    block_index += 1
```

ここまでのソースコードは以下になります、実行するとブロックが表示されていると思います。

```python
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
        self.blocks = [True] * BLOCK_ROW * BLOCK_COL

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

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


App()
```

## パドルを動かす

ここまで各パーツの描画ができました、これからはそれぞれのパーツを動かせる処理を書いていきます。
まずはパドルを動かします。パドルはキーボードの矢印キーで操作できるようにします。

`update`メソッドにキーボードが押下されたら移動する処理を書きます。無限に移動できても困るのでウインドウの端に接触した場合それ以上動かさないようにする処理も書きます。

```python
# 左矢印キーが押されたら左に移動
if pyxel.btn(pyxel.KEY_LEFT):
    self.paddle_x -= 2
# 右矢印キーが押されたら右に移動
if pyxel.btn(pyxel.KEY_RIGHT):
    self.paddle_x += 2
# パドルの左端が壁に接触した場合それ以上進まないように
if self.paddle_x <= 0:
    self.paddle_x = 0
# パドルの右端が壁に接触した場合それ以上進まないように
if self.paddle_x + PADDLE_WIDTH >= 160:
    self.paddle_x = 160 - PADDLE_WIDTH
```

ここまでのソースコードは以下のとおりです、実行するとパドルが操作できるようになっているはずです。

```python
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

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

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


App()
```

## ボールを動かす

次にはボールを動かします。ボールを動かす方法としてはシンプルに、x・y 方向それぞれの移動量を持つ変数を用意し、それらを毎フレームごとに加算していくことにします。

まずは`__init__`メソッドで変数の宣言をします。

```python
# x・y座標に対してそれぞれ1フレームごとに加算していく値
self.ball_vx = 1
self.ball_vy = 1
```

次に`update`メソッドにボールの移動処理を書いていきます。

```python
self.ball_x += self.ball_vx
self.ball_y += self.ball_vy
```

ここまでのソースコードです。実行するとボールが動きます。

```python
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

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

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


App()
```

## ボールと壁の衝突判定をして反射させる

ここまででボールを動かすことができましたが、移動するボールは画面外へ行ってしまうと戻ってきません。
ということで、ボールが壁に衝突したら反射する処理を書いていきましょう。

`update`メソッド内にボールが壁に衝突した場合、移動量の値を反転（-1 を掛ける）する処理を書きます。
ブロック崩しですので下の壁に衝突した場合、ゲームを終了させます（本来はゲームオーバー処理を実装すべきですが今回は面倒なので）。

```python
# 左右の壁に衝突したら反射
if self.ball_x <= 0 or self.ball_x >= 160:
    self.ball_vx *= -1
# 上の壁に衝突したら反射
if self.ball_y <= 0:
    self.ball_vy *= -1
# 下の壁に衝突したら終了
if self.ball_y >= 120:
    pyxel.quit()
```

ここまでのソースコードです。実行するとボールが壁に衝突すると反射しますが、現在の状態だとボールは右下に移動しそのまま下の壁に衝突するため、ゲームが終了します。
反射を確認したければ`self.ball_vy`の値を`-1`などに書き換えるか、下の壁に衝突したときに終了せず反射する処理に書き換えてください。

```python
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

    def draw(self):
        pyxel.cls(0)

        # ボールの描画
        pyxel.pix(self.ball_x, self.ball_y, 10)

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


App()
```

## パドルやブロックとの衝突判定を実装する

壁の反射までできました。ここまでくればあと一息です。最後のパドルやブロックの衝突処理はこれまでより若干複雑ですが、頑張っていきましょう。

まずはボールとパドル衝突です。`update`メソッド内に書きましょう。
衝突の判定にパドルの上と左右の座標情報が必要なので、処理の前に宣言します。
本来であればボールがパドル側面に衝突した時の処理も書くのですが、パドルが左右に動かせるゆえ意図した通りの挙動にするのが難しいため今回はなしとします。

```python
# パドルの左端のx座標(left)
paddle_lx = self.paddle_x
# パドルの右端のx座標(right)
paddle_rx = self.paddle_x + PADDLE_WIDTH
# パドルの上端のy座標(top)
paddle_ty = self.paddle_y

# 上から衝突したときにy方向を反転
if self.ball_y == paddle_ty and self.ball_x >= paddle_lx and self.ball_x <= paddle_rx:
  self.ball_vy *= -1
```

次にボールとブロックの衝突です。同じく`update`メソッド内に書きます。
基本的にすべてのブロックに対してパドルの衝突と同じことをすればよいのですが今回は上下左右すべての方向から衝突しても反射できるようにします。

```python
block_index = 0
for row in range(BLOCK_ROW):
    for col in range(BLOCK_COL):
        if self.blocks[block_index]:
            # ブロックのx,y座標
            block_x = col * (BLOCK_WIDTH + 5)
            block_y = row * (BLOCK_HEIGHT + 5)

            # 上下左右の座標
            block_lx = block_x
            block_rx = block_x + BLOCK_WIDTH
            block_ty = block_y
            block_by = block_y + BLOCK_HEIGHT

            if self.ball_x >= block_lx and self.ball_x <= block_rx and self.ball_y >= block_ty and self.ball_y <= block_by:
                # 衝突したらリスト内の値をFalseにすることで破壊となる
                self.blocks[block_index] = False
                # 上下からの衝突
                if self.ball_x >= block_lx or self.ball_x <= block_rx:
                    self.ball_vx *= -1
                # 左右からの衝突
                if self.ball_y >= block_ty or self.ball_y <= block_by:
                    self.ball_vy *= -1
          block_index += 1
```

最後にブロックが全てなくなったら終了する処理を書いて終了です。お疲れさまでした。

```python
if not any(self.blocks):
    pyxel.quit()
```

完成形となるソースコードは以下のとおりです。

```python
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
```
