import tkinter.messagebox
import tkinter.messagebox as tkm
import pygame as pg
import os
import random
import sys

root = tkinter.Tk()
root.withdraw()
main_dir = os.path.split(os.path.abspath(__file__))[0]

class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 

class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }
    def __init__(self,image,size,xy):
        self.tori_sfc = pg.image.load(image)
        self.tori_sfc = pg.transform.rotozoom(self.tori_sfc,0,size)
        self.tori_rct = self.tori_sfc.get_rect()
        self.tori_rct.center = xy
    
    def blit(self,scr:Screen):
        scr.sfc.blit(self.tori_sfc,self.tori_rct)

    def update(self,scr:Screen):
        key_dct = pg.key.get_pressed()
        for key,delta in Bird.key_delta.items():
            if key_dct[key]:
                self.tori_rct.centerx += delta[0]
                self.tori_rct.centery += delta[1]
            if check_bound(self.tori_rct,scr.rct) != (+1,+1):
                self.tori_rct.centerx -= delta[0]
                self.tori_rct.centery -= delta[1]
        self.blit(scr)                 



class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def load_sound(file): #音楽が流れる
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    boom_sound = load_sound("boom.wav")
    shoot_sound = load_sound("car_door.wav")
    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)
    clock = pg.time.Clock()
    fonto = pg.font.Font(None,100)
    scr = Screen("逃げろ！こうかとん", (1280, 720), "fig/pg_bg.jpg") #ゲーム画面が飛び出さないように、幅と高さを調整した。
    kkt = Bird("fig/6.png",2.0,(900,400))
    kkt.update(scr)

    bombs = []
    color_lst = ["red", "green", "blue", "yellow", "magenta"] #異なる色を設定
    for i in range(7):
            r  = random.randint(10,30) #ランダムサイズ
            bkd = Bomb(color_lst[i%5], r, (random.choice(range(-2, 3)), random.choice(range(-2, 3))), scr)
            bombs.append(bkd)

    life = 500 #HPを表す変数
    
    while True:
        scr.blit()
        txt = fonto.render("HP:"+str(int(life)),True, (0,0,0)) #HPを表示する
        scr.sfc.blit(txt, (530,10))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        kkt.update(scr)

        for bomb in bombs:
            bomb.update(scr)
            if kkt.tori_rct.colliderect(bomb.rct):
                life -= 1
                if life < -1:
                    return
          
        pg.display.update()
        clock.tick(1000)
    

if __name__ == "__main__":
    pg.init()
    main()
    tkm.showwarning("まけ","GAMEOVER") #ゲームオーバー画面を追加する
    pg.quit()
    sys.exit()