import pyxel

score = 0
money = 0
watched = False

class Title:
    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            state.set(Game())
        elif pyxel.btnp(pyxel.KEY_H):
            state.set(Help())
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            state.set(Help())
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            state.set(Game())
    def draw(self):
        # 画像を描画する（画面の座標(0, 0)に描画）
        pyxel.blt(0, 0, title_image, 0, 0, 512, 256)

class Help:
    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            state.set(Title())
    def draw(self):
        pyxel.blt(0, 0, help_image, 0, 0, 512, 256)

class Result:
    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if money < 10000 or watched:
                state.set(Game())
            else:
                state.set(Event())
            
        if pyxel.btnp(pyxel.KEY_Q):
            state.set(Title())
    def draw(self):
        pyxel.blt(0, 0, result_image, 0, 0, 512, 256)
        n = score // 10
        n2 = score % 10
        if n:
            pyxel.blt(192, 64, 0, 8*n, 80, 8, 16, 0)
            pyxel.blt(200, 64, 0, 8*n2, 80, 8, 16, 0)
            pyxel.blt(208, 64, 0, 0, 80, 8, 16, 0)
        elif n2:
            pyxel.blt(200, 64, 0, 8*n2, 80, 8, 16, 0)
            pyxel.blt(208, 64, 0, 0, 80, 8, 16, 0)
        pyxel.blt(216, 64, 0, 0, 80, 8, 16, 0)

        n = money//10000
        n2 = money // 1000 % 10
        n3 = money //100 % 10
        if n:
            pyxel.blt(430, 160, 0, 8*n, 80, 8, 16, 0)
            pyxel.blt(438, 160, 0, 8*n2, 80, 8, 16, 0)
            pyxel.blt(446, 160, 0, 8*n3, 80, 8, 16, 0)
            pyxel.blt(454, 160, 0, 0, 80, 8, 16, 0)
        elif n2:
            pyxel.blt(438, 160, 0, 8*n2, 80, 8, 16, 0)
            pyxel.blt(446, 160, 0, 8*n3, 80, 8, 16, 0)
            pyxel.blt(454, 160, 0, 0, 80, 8, 16, 0)
        elif n3:
            pyxel.blt(446, 160, 0, 8*n3, 80, 8, 16, 0)
            pyxel.blt(454, 160, 0, 0, 80, 8, 16, 0)
        pyxel.blt(462, 160, 0, 0, 80, 8, 16, 0)
        
class Event:
    def __init__(self):
        global watched
        watched = True
        wait_time = 1
        time = 3
        frame = time * 30
        self.speed = pyxel.height / frame
        wait_time = 1
        wait_frame = wait_time*30
        self.darkness = wait_frame * self.speed * -1  # 暗転の度合い
    def update(self):
        # 暗転の度合いを徐々に増加させる
        if self.darkness < pyxel.height:
            self.darkness += self.speed
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            state.set(Title())
        
        
    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 512, 256)
        pyxel.blt(128, 192, 0, 24, 0, 16, 16, 9)# Player
        pyxel.blt(144, 192, 0, 72, 0, 16, 16, 9)# Police
        #writer.draw(128, 224, '警察官「そこの君ちょっといいかな？」', 16, pyxel.COLOR_BLACK)
        # 暗転の度合いに応じて黒い矩形を描画
        if self.darkness:
            pyxel.rect(0, 0, pyxel.width, int(self.darkness), 0)
        #暗転が終わっていたら追加で文字を描画
        if self.darkness >= pyxel.height:
            pyxel.blt(0, 0, end_image, 0, 0, 512, 256)

class Game:
    def __init__(self):
        global score
        score = 0
        self.glove_count = 30
        self.player_x = 96
        self.player_y = 192
        self.player_vy = 0 # プレイヤーの垂直速度
        self.scroll = -3    #画面のスクロール速度
        self.g = 1    #重力加速度
        self.is_jumping = False # ジャンプ中かどうかを示すフラグ
        self.gloves = []
        self.coins = []
        self.last_time = pyxel.frame_count
        self.bg_x = 0
        self.bg2_x = 512
    
    def update(self):
        global score, money
        #終了
        if self.glove_count <= 0 and not self.gloves:
            money += score*100
            state.set(Result())
            
        #コインを一定時間ごとに描画
        if pyxel.frame_count - self.last_time > 60:#pyxelはデフォが30fpsなので秒数n*30
            r = pyxel.rndi(0, 7)
            if not r:
                self.coins.append((pyxel.width, 204))
            elif not r % 7:
                self.coins.append((pyxel.width, 80))
            else:
                self.coins.append((pyxel.width, pyxel.rndi(92, 192)))                
            self.last_time = pyxel.frame_count

        #リスタート
        if pyxel.btnp(pyxel.KEY_RETURN):
            state.set(Game())
        #タイトルへ
        if pyxel.btnp(pyxel.KEY_Q):
            state.set(Title())

        # ジャンプの処理
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) and not self.is_jumping:
            self.player_vy = -10
            self.is_jumping = True
            
        # 重力の適用
        self.player_vy += self.g
        self.player_y += self.player_vy
        # 地面に着地したらジャンプをリセット
        if self.player_y > 192:
            self.player_y = 192
            self.player_vy = 0
            self.is_jumping = False
            
        if self.glove_count > 0:
            # 軍手を真下に投げる
            if pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.gloves.append((self.player_x+4, self.player_y+8, 0, 0))
                self.glove_count -= 1
            # 軍手を左斜め上に投げる
            elif pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.gloves.append((self.player_x+4, self.player_y+8, -4, -10)) # -4, -10 は軍手の速度
                self.glove_count -= 1
            # 軍手を右斜め上に投げる
            elif pyxel.btnp(pyxel.KEY_F) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.gloves.append((self.player_x+4, self.player_y+8, 4, -10))# 4, -10 は軍手の速度（斜め上
                self.glove_count -= 1
            
        # 軍手の位置更新
        new_gloves = []
        for x, y, vx, vy in self.gloves:
            # 重力の影響を与える
            vy = vy + self.g
            y = min(y + vy, 204)
            # 軍手が画面内にいる場合のみ位置を更新して描画を継続
            if y < pyxel.height and -8 < x:
                if y >= 204:
                    vx = self.scroll
                    vy = 0
                new_gloves.append((x+vx, y+vy, vx, vy))
                self.gloves = new_gloves
        self.gloves = new_gloves

        # 衝突判定 & コインの位置更新
        new_coins = []
        for tx, ty in self.coins:
            hit = False
            #当たっていたら加点（落下中のみ判定）
            for gx, gy, _, gvy in self.gloves:
                if  gvy >= 0 and abs((gx - tx)) < 8 and abs((gy - ty)) < 8:
                    score += 1
                    hit = True
                    break
            #当たっていなければ位置を更新して描画を継続
            if not hit:
                tx += self.scroll
                #画面外に行ってしまったらペナルティ
                if tx < -8 and self.glove_count > 0:
                    self.glove_count -= 1
                else:
                    new_coins.append((tx, ty))
        self.coins = new_coins
        
        #背景の位置更新
        self.bg_x += self.scroll
        self.bg2_x += self.scroll
        if self.bg_x <= -512:
            self.bg_x = 0
            self.bg2_x = 512

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 512, 64)    #空の部分だけ固定
        pyxel.bltm(self.bg_x, 64, 0, 0, 64, 512, 192)    #background
        pyxel.bltm(self.bg2_x, 64, 0, 0, 64, 512, 192)    #background2

        #軍手の残機
        n = self.glove_count // 10
        n2 = self.glove_count % 10
        if n:
            pyxel.blt(104, 16, 0, 8*n, 80, 8, 16, 0)
        pyxel.blt(112, 16, 0, 8*n2, 80, 8, 16, 0)
        frame = (pyxel.frame_count // 5) % 4  # 3フレームのアニメーション
        #ジャンプの間は画像を固定
        if self.is_jumping:
            frame = 0
        
        for x, y, vx, vy in self.gloves:
            #x, y, image_bank, px_x, px_y, width, height, color)
            pyxel.blt(x, y, 0, 0, 0, 8, 8, 0)# Glove
        for tx, ty in self.coins:
            if ty == 204:
                pyxel.blt(tx, ty, 0, 0, 24, 8, 8, 0)# coin
            else:
                pyxel.blt(tx, ty-8, 0, 0, 8, 8, 8, 0)#パラソル
                pyxel.blt(tx, ty, 0, 0, 16, 8, 8, 0)# coin
        pyxel.blt(self.player_x, self.player_y, 0, 8 + 16*frame, 0, 16, 16, 9)# Player

class State:
    def __init__(self, state):
        self.set(state)
    def set(self, state):
        self.state = state
class App:
    def __init__(self):
        global title_image, help_image, end_image, result_image
        pyxel.init(512, 256, title="軍手落とし")
        pyxel.load('sample.pyxres')
        title_image = pyxel.Image(512, 256)
        title_image.load(0, 0, "title.png")
        help_image = pyxel.Image(512, 256)
        help_image.load(0, 0, "help.png")
        end_image = pyxel.Image(512, 256)
        end_image.load(0, 0, "end.png")
        result_image = pyxel.Image(512, 256)
        result_image.load(0, 0, "result.png")
        pyxel.run(self.update, self.draw)
        
    def update(self):
        state.state.update()

    def draw(self):
        state.state.draw()
        
state = State(Title())
if __name__ == "__main__":
    App()
