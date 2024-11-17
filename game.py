import pyxel, ctypes
#import PyxelUniversalFont as puf

score = 0
money = 0
watched = False
#writer = puf.Writer("ipa_gothic.ttf")

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
        pyxel.cls(7)
        #writer.draw(352, 16, 'バイトマニュアル', 16, 5)
        #writer.draw(32, 16, '軍手を落とすだけ！　手軽に高収入！', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 48, '超ホワイト！　時給最高3000円！', 16, pyxel.COLOR_BLACK)
        #if watched:
        #    writer.draw(272, 160, '...そんなバイトはありません')
        #writer.draw(64, 96, '軍手落とし', 48, pyxel.COLOR_RED)
        #writer.draw(160, 208, '-PRESS ENTER TO START-', 16, pyxel.COLOR_BLACK)

class Help:
    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            state.set(Title())
    def draw(self):
        pyxel.cls(7)
        #writer.draw(16, 16, '仕事内容', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 48, '　軍手を投げて、街中のコインを集めます。落下中の軍手で', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 80, 'ないと、上手くコインが入らないので注意してください。', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 112, '前投げ　　　→　F', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 144, '落とす　　　→　D', 16, pyxel.COLOR_BLACK)
        #writer.draw(32, 176, '後ろ投げ　　→　S', 16, pyxel.COLOR_BLACK)
        #writer.draw(288, 112, 'ジャンプ　　→　スペース', 16, pyxel.COLOR_BLACK)
        #writer.draw(288, 144, 'リスタート　→　エンター', 16, pyxel.COLOR_BLACK)
        #writer.draw(288, 176, 'タイトルへ　→　Q', 16, pyxel.COLOR_BLACK)
        #writer.draw(160, 208, '-PRESS ENTER TO CLOSE-', 16, pyxel.COLOR_BLACK)

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
        pyxel.cls(0)
        #writer.draw(32, 64, f'？？？「今回の報酬は{score*100}円だ...受け取れ...」', 16, pyxel.COLOR_WHITE)
        #writer.draw(256, 160, f'これまでに稼いだ金額　{money}円', 16, pyxel.COLOR_WHITE)
        #writer.draw(160, 192, '-PRESS ENTER TO RESTART-', 16, pyxel.frame_count % 16)

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
        #if self.darkness >= pyxel.height:
        #    writer.draw(32, 32, 'BAD END...', 48, pyxel.COLOR_RED)
        #    writer.draw(16, 144, '逮捕されてしまった...', 16, pyxel.COLOR_WHITE)
        #    writer.draw(16, 160, 'あんな怪しいバイトに手を出していなければ...', 16, pyxel.COLOR_WHITE)
        #    writer.draw(160, 224, '-PRESS ENTER TO TITLE-', 16, pyxel.frame_count % 16)
            

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
        #writer.draw(8, 8, f'Gloves: {self.glove_count}', 16, pyxel.COLOR_RED)
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
        pyxel.init(512, 256, title="軍手落とし")
        pyxel.load('sample.pyxres')
        pyxel.run(self.update, self.draw)
        
    def update(self):
        state.state.update()

    def draw(self):
        state.state.draw()
        
state = State(Title())
if __name__ == "__main__":
    App()
