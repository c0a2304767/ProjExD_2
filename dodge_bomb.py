import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1099, 649
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }



DIRECTION = {
    pg.K_UP: -90,
    pg.K_DOWN: 90,
    pg.K_LEFT: 180,
    pg.K_RIGHT: 0,
}  # 演習3の途中

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def timer_bomb(bb_accs: pg.Rect) -> tuple[bool, bool]:
    accs = [a for a in range(1, 11)]
    vx, vy, tmr = +5, -5, 0
    vx *= accs[min(tmr//500, 9)]
    vy *= accs[min(tmr//500, 9)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    return vx, vy, r  # 演習2の途中

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん，または，爆弾Rect
    戻り値：真理値タプル（横判定結果，縦判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    cry_img = pg.image.load("fig/8.png")  # こうかとんの泣き画像
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 空の(Surface
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()  # 爆弾rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, -5
    fin_fonto = pg.font.Font(None, 80)
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾が重なっていたら
            fin = pg.Surface((WIDTH, HEIGHT))
            pg.draw.rect(fin, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            fin.set_alpha(200)
            screen.blit(fin, [0, 0])
            pg.display.update()
            fin_txt = fin_fonto.render("GameOver", True, (255, 255, 255))
            screen.blit(fin_txt, [(WIDTH/2)-160, (HEIGHT/2)-40])
            screen.blit(cry_img, [(WIDTH/2)-240, (HEIGHT/2)-50])
            screen.blit(cry_img, [(WIDTH/2)+160, (HEIGHT/2)-50])
            pg.display.update()
            time.sleep(5)
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横座標, 縦座標
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        bb_accs = timer_bomb(bb_rct)
        bb_accs.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        #bb_imgs = timer_bomb(bb_rct)
        #bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
