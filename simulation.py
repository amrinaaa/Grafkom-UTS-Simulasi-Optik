import pygame
import button
import pygame.gfxdraw
import sys
from Inputbox import InputBox, screen, width, height
import math
import random

# Inisialisasi Window
pygame.init()
from pygame.locals import *

# Warna
white = (255, 255, 255)  # Warna putih
black = (0, 0, 0)  # Warna hitam
green = (0, 255, 0)  # Warna hijau
yellow = (255, 255, 0)  # Warna kuning
blue = (0, 0, 255)  # Warna biru
red = (255, 0, 0)  # Warna merah
pink = (255, 182, 193) # Warna pink
purple = (128, 0, 128) # Warna ungu
sky = (202, 228, 241) # Warna biru muda
light_blue = (173, 216, 230)
orange = (255, 165, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
turquoise = (64, 224, 208)
grey = (96, 96, 96)
dimgrey = (105, 105, 105)
raisinblack = (36,33,36)
light_blue = (83, 92, 145)
dark_blue = (27, 26, 85)

font = pygame.font.SysFont(None, 18)
font_2= pygame.font.SysFont(None, 70)
font_3= pygame.font.SysFont(None, 50)

# DDA konversi koordinat x y
def konv_koor_x(x):
    return screen.get_width() // 2 + x * -1

def konv_koor_y(y):
    return screen.get_height() // 2 + y * -1
    
# Algoritma DDA untuk menggambar objek
def dda_objek(x1, y1, x2, y2, color, thickness):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return
    steps = max(abs(dx), abs(dy))

    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    for _ in range(int(steps)):
        pygame.draw.circle(screen, color, (round(x), round(y)), thickness)
        x += x_increment
        y += y_increment

#Algoritma DDA menggambar garis sinar
def dda_sinar(x1, y1, x2, y2, color, thickness):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return
    steps = max(abs(dx), abs(dy))

    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    while 0 <= round(x) < width and -5000 <= round(y) < 5000:
        pygame.draw.circle(screen, color, (round(x), round(y)), thickness)
        x += x_increment
        y += y_increment

def dashed_line_dda(x1, y1, x2, y2, color, thickness):
    step = 0.0

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)

    Xinc = dx / float(step)
    Yinc = dy / float(step)
    x, y = x1, y1

    for i in range(int(step) + 1):
        x += Xinc
        y += Yinc
        if i % 10 == 0:
           pygame.draw.circle(screen, color, (round(x), round(y)), thickness)

def draw_arc(screen, color, rect, start_angle, stop_angle, thickness=1):
    x, y, width, height = rect
    pygame.draw.arc(screen, color, (x, y, width, height), start_angle, stop_angle, thickness)

def draw_circle(xc, yc, x, y, color):
    screen.set_at((xc + x, yc + y), color)
    screen.set_at((xc + x, yc - y), color)
    screen.set_at((xc + y, yc + x), color)
    screen.set_at((xc + y, yc - x), color)
    screen.set_at((xc - x, yc + y), color)
    screen.set_at((xc - x, yc - y), color)
    screen.set_at((xc - y, yc + x), color)
    screen.set_at((xc - y, yc - x), color)

def midpoint_circle_arc(screen, color, rect, start_angle, stop_angle, ratio=1):
    x, y, width, height = rect
    xc = x + width // 2
    yc = y + height // 2
    r = min(width // 2, height // 2)  

    start_angle = start_angle * 180 / 3.14
    stop_angle = stop_angle * 180 / 3.14

    start_angle %= 360
    stop_angle %= 360

    if start_angle >= stop_angle:
        stop_angle += 360

    x = 0
    y = r
    p = 1 - r

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

        angle = (x / r) * 3.14 * ratio

        current_y = yc + y

        if current_y < (y - 1):
            draw_circle(xc, yc, x, y, color)  

        if start_angle <= angle <= stop_angle:
            draw_circle(xc, yc, x, y, r, color)

# Fungsi untuk menampilkan teks di screen
def draw_text1(text, font_2, color, surface, x, y):
    textobj = font_2.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_text_cembung(text, x, y):
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x, y - 15))
    screen.blit(text_surface, text_rect)

# Fungsi untuk menampilkan teks di layar
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y - 15))
    screen.blit(text_surface, text_rect)

# Parameter untuk simulasi
jarak_benda = 210
tinggi_benda = 50
fokus = 140
jarijari = 2*fokus

# Parameter simulasi
input_box_jarak = InputBox(50, height - 40, 100, 20, 'Jarak Benda', '')
input_box_tinggi = InputBox(170, height - 40, 100, 20, 'Tinggi Benda', '')
input_box_fokus = InputBox(290, height - 40, 100, 20, 'Titik Fokus', '')

def atur_gerakan():
    global jarak_benda, tinggi_benda, fokus, jarak_bayangan, tinggi_bayangan

    # Buat ngambil key yang ditekan
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        jarak_benda -= 1
        input_box_jarak.text = str(jarak_benda)
    if keys[pygame.K_LEFT]:
        jarak_benda += 1
        input_box_jarak.text = str(jarak_benda)

    # Memastikan tinggi_benda tidak melewati batas atas dan bawah layar
    if keys[pygame.K_UP]:
        tinggi_benda += 3
        tinggi_benda = min(tinggi_benda, screen.get_height() // 2 - 10)  # Batas atas
        input_box_tinggi.text = str(tinggi_benda)
    if keys[pygame.K_DOWN]:
        tinggi_benda -= 3
        tinggi_benda = max(tinggi_benda, -screen.get_height() // 2 + 340)  # Batas bawah
        input_box_tinggi.text = str(tinggi_benda)

    # Perbarui jarak bayangan dan tinggi bayangan
    try:
        jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus))
        tinggi_bayangan = ((jarak_bayangan / jarak_benda) * tinggi_benda) * -1
    except ZeroDivisionError:
        jarak_bayangan = 0
        tinggi_bayangan = 0

click = False

def draw_textbox(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(left=x, centery=y + height / 2)
    screen.blit(text_surface, text_rect)

def draw_textbox_sifatbygn(sifat_bayangan, x, y, width, height, color):
    if jarak_benda < fokus and jarak_benda != jarijari:
        if jarak_benda < fokus:
            sifat_bayangan = "Maya, tegak, diperbesar"
        else:
            sifat_bayangan = "Nyata, terbalik, diperbesar"
    elif jarak_benda > fokus and jarak_benda != jarijari:
        if jarak_benda > fokus * 2:
            sifat_bayangan = "Nyata, terbalik, diperkecil"
        else:
            sifat_bayangan = "Nyata, terbalik, diperbesar"
    elif jarak_benda == jarijari :
        sifat_bayangan = "Nyata, terbalik, sama besar"
    else:
        sifat_bayangan = "Bayangan di jauh tak hingga"

    text_surface = font.render("Sifat Bayangan", True, white)
    text_rect = text_surface.get_rect(center=(x + width / 2, y - 5))
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, white, (x+20, y+10, 250, 20), border_radius=10)

    text_surface = font.render(sifat_bayangan, True, black)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height + 15))
    screen.blit(text_surface, text_rect)

def draw_coordinate_axes(screen, black):
    # Gambar garis x
    x1, y1 = 0, screen.get_height() // 2
    x2, y2 = screen.get_width(), screen.get_height() // 2
    dda_sinar(x1, y1, x2, y2, black, 1)

    # Gambar garis y
    x1, y1 = screen.get_width() // 2, 0
    x2, y2 = screen.get_width() // 2, screen.get_height()
    dda_objek(x1, y1, x2, y2, black, 1)

def draw_garis_fokus(tinggi_bayangan, jarak_bayangan):

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, green, 1)

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_sinar(x1, y1, x2, y2, green, 1)

    x1, y1 = konv_koor_x(0), konv_koor_y(0)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, pink, 1)

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, yellow, 1)

def cekg ():
    # sinar hijau
    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, green, 1)

    # Sinar kuning
    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(fokus), konv_koor_y(0)
    dda_sinar(x1, y1, x2, y2, yellow, 1)

    # Sinar pink
    x1, y1 = konv_koor_x(0), konv_koor_y(0)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(-tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, pink, 1)

def cemb ():
    
     #cahaya ijo
     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dda_sinar(x1, y1, x2, y2, white, 1)

     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dashed_line_dda(x1, y1, x2, y2, green, 1)

     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
     x2, y2 = konv_koor_x(-width), konv_koor_y(tinggi_bayangan)
     dda_objek(x1, y1, x2, y2, green, 1)

     #cahaya kuning
     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dda_sinar(x1, y1, x2, y2, white, 1)

     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dashed_line_dda(x1, y1, x2, y2, yellow, 1)

     x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
     x2, y2 = konv_koor_x(-fokus), konv_koor_y(0)
     dda_sinar(x1, y1, x2, y2, yellow, 1)

     #cahaya biru
     x1, y1 = konv_koor_x(0), konv_koor_y(0)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dda_sinar(x1, y1, x2, y2, white, 1)

     x1, y1 = konv_koor_x(0), konv_koor_y(0)
     x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
     dashed_line_dda(x1, y1, x2, y2, blue, 1)

     x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
     x2, y2 = konv_koor_x(0), konv_koor_y(0)
     dda_sinar(x1, y1, x2, y2, blue, 1)

def gambar_garis_putus_ckg(jarak_bayangan, tinggi_bayangan):

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dashed_line_dda(x1, y1, x2, y2, green, 2)

    x1, y1 = konv_koor_x(0), konv_koor_y(0)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dashed_line_dda(x1, y1, x2, y2, pink, 2)

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dashed_line_dda(x1, y1, x2, y2, yellow, 2)

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_sinar(x1, y1, x2, y2, green, 1)

show_input_boxes = False
show_choose_object = False
show_detail = False

def gambar_benda(jarak_benda, tinggi_benda):
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(0)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    x1, y1 = konv_koor_x(jarak_benda-5), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    x1, y1 = konv_koor_x(jarak_benda +5), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    draw_text("Benda", x1+5, y1, blue)

def gambar_stickman(jarak_benda, tinggi_benda):
    # Kepala
    x, y = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 1.25)
    pygame.draw.circle(screen, black, (x, y), tinggi_benda // 5)
    # Badan
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, black, 1)
    # Lengan
    panjang_lengan = tinggi_benda // 4
    x1, y1 = konv_koor_x(jarak_benda - panjang_lengan), konv_koor_y(tinggi_benda // 2)
    x2, y2 = konv_koor_x(jarak_benda + panjang_lengan), konv_koor_y(tinggi_benda // 2)
    dda_objek(x1, y1, x2, y2, black, 1)
    # Kaki
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda - panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, black, 1)
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda + panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, black, 1)
    draw_text("Benda", x, y - 60, blue)

def gambar_bayangan(jarak_bayangan, tinggi_bayangan) :
    # Buat bayangan benda
    x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(0)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)
    x1, y1 = konv_koor_x(jarak_bayangan -5), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)
    x1, y1 = konv_koor_x(jarak_bayangan +5), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)
    if jarak_benda != fokus :
        draw_text("Bayangan", x1, y1+10, purple) 

def gambar_bayangan_stickman(jarak_bayangan, tinggi_bayangan) :
    # Kepala
    if jarak_benda <= fokus :
        radius_kepala = tinggi_bayangan // 5
    else :
        radius_kepala = tinggi_bayangan // 5 *-1

    x, y = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan // 1.25)
    pygame.draw.circle(screen, grey, (x, y), radius_kepala)
    # Badan
    x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, grey, 1)
    # Lengan
    panjang_lengan = tinggi_bayangan // 4
    x1, y1 = konv_koor_x(jarak_bayangan - panjang_lengan), konv_koor_y(tinggi_bayangan // 2)
    x2, y2 = konv_koor_x(jarak_bayangan + panjang_lengan), konv_koor_y(tinggi_bayangan // 2)
    dda_objek(x1, y1, x2, y2, grey, 1)
    # Kaki
    x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(jarak_bayangan - panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, grey, 1)
    x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(jarak_bayangan + panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, grey, 1)
    if jarak_benda != fokus :
        draw_text("Bayangan", x, y + 60, purple)

# Fungsi untuk membuat radio button
def draw_radio_button(surface, x, y, text, active_radio_button1, active_radio_button2, draw_benda=True, draw_stickman=True):
    radio_button_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(surface, black, radio_button_rect, 2)

    if active_radio_button1 and not active_radio_button2 and draw_benda:
        gambar_benda(jarak_benda, tinggi_benda)
        gambar_bayangan(jarak_bayangan, tinggi_bayangan)
        pygame.draw.circle(surface, red, (x + 10, y + 10), 6)
    elif active_radio_button2 and not active_radio_button1 and draw_stickman:
        gambar_stickman(jarak_benda, tinggi_benda)
        gambar_bayangan_stickman(jarak_bayangan, tinggi_bayangan)
        pygame.draw.circle(surface, red, (x + 100, y + 10), 6)

    text_surface = font.render(text, True, black)
    surface.blit(text_surface, (x + 30, y+5))

    return radio_button_rect

def draw_navigation_bar():
    global show_input_boxes, show_choose_object,  show_detail

    keterangan_button = pygame.Rect(0, height - 100, 180, 30)
    keterangan_button_color = light_blue if keterangan_button.collidepoint(pygame.mouse.get_pos()) else dark_blue
    pygame.draw.rect(screen, keterangan_button_color, keterangan_button, border_top_left_radius=10, border_top_right_radius=10)
    text = font.render("Detail", True, white)
    text_rect = text.get_rect(center=keterangan_button.center)
    screen.blit(text, text_rect)

    if keterangan_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            show_detail = True
            show_choose_object = False
            
    # Tombol home
    home_button = pygame.Rect(180, height - 100, 140, 30)
    home_button_color = light_blue if home_button.collidepoint(pygame.mouse.get_pos()) else dark_blue
    pygame.draw.rect(screen, home_button_color, home_button, border_top_left_radius =10, border_top_right_radius =10)
    text = font.render("Home", True, white)
    text_rect = text.get_rect(center=home_button.center)
    screen.blit(text, text_rect)

    if home_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            show_input_boxes = False
            show_choose_object = False
            show_detail =  False
            menu()

# Membuat layar dengan ukuran tertentu
screen = pygame.display.set_mode((width, height))

def draw_star(surface, x, y, size, color):
    outer_radius = size
    inner_radius = size // 2
    num_points = 10
    angle = -math.pi / 2
    angle_increment = math.pi * 2 / num_points
    points = []
    for _ in range(num_points * 2):
        radius = outer_radius if len(points) % 2 == 0 else inner_radius
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
        angle += angle_increment
    pygame.draw.polygon(surface, color, points)

def menu():
    global show_input_boxes, show_choose_object

    bintang_list = []
    for _ in range(20):
        bintang = {
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'speed': 1,
            'angle': random.uniform(0, 360),
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        }
        bintang_list.append(bintang)

    while True:
        screen.fill((sky))

        mx, my = pygame.mouse.get_pos()

        # Load Foto
        cekung_img = pygame.image.load('image\cekunggg.png').convert_alpha()
        cembung_img = pygame.image.load('image\cembunggg.png').convert_alpha()
        background_img = pygame.image.load('image\Langit.jpeg').convert_alpha()

        background_img = pygame.transform.scale(background_img, (width, height))
        screen.blit(background_img, (0, 0))

        # Menggambar gambar latar belakang di seluruh layar
        draw_text1('PILIH PROGRAM SIMULASI-NYA', font_2, white, screen, 224, 120)
        draw_text1('Cermin Cekung', font_3, white, screen, 200, 500)
        draw_text1('Lensa Cembung', font_3, white, screen, 730, 500)

        for bintang in bintang_list:
            x = bintang['x']
            y = bintang['y']
            color = bintang['color']
            draw_star(screen, x, y, 20, color)

            # Update posisi bintang berdasarkan kecepatan dan arahnya
            radian_angle = math.radians(bintang['angle'])
            x_change = bintang['speed'] * math.cos(radian_angle)
            y_change = bintang['speed'] * math.sin(radian_angle)
            bintang['x'] += x_change
            bintang['y'] += y_change

            # Memastikan bintang tetap berada di dalam area layar
            if bintang['x'] < 0 or bintang['x'] > width or bintang['y'] < 0 or bintang['y'] > height:
                bintang['x'] = random.randint(0, width)
                bintang['y'] = random.randint(0, height)
                bintang['angle'] = random.uniform(0, 360)

        cekung_button = button.Button(100, 200, cekung_img, 0.41)
        cembung_button = button.Button(630, 200, cembung_img, 0.41)

        if cekung_button.draw(screen):
            Cermin_cekung()
        if cembung_button.draw(screen):
            Lensa_Cembung()

        pygame.display.update()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

def Cermin_cekung():
    global jarak_benda, tinggi_benda, fokus, jarak_bayangan, tinggi_bayangan, show_input_boxes, show_choose_object, show_detail
    running = True
    active_radio_button1 = False
    active_radio_button2 = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if radio_button_rect1.collidepoint(mouse_pos):
                    active_radio_button1 = not active_radio_button1
                    active_radio_button2 = False
                elif radio_button_rect2.collidepoint(mouse_pos):
                    active_radio_button2 = not active_radio_button2
                    active_radio_button1 = False

            new_fokus = input_box_fokus.handle_event(event)
            if new_fokus is not None:
                fokus = new_fokus

            new_tinggi = input_box_tinggi.handle_event(event)
            if new_tinggi is not None:
                tinggi_benda = new_tinggi
            
            new_jarak = input_box_jarak.handle_event(event)
            if new_jarak is not None:
                jarak_benda = new_jarak

        # Gambar Background
        screen.fill(white)

        stickman_img = pygame.image.load('image\Stickman.jpg').convert_alpha()
        stickman_img = pygame.transform.scale(stickman_img, (80,80))
        xp, yp = 1060, 510
        screen.blit(stickman_img, (xp, yp))
        pygame.draw.rect(screen, blue, (xp, yp - 4, 80, 80), 2)

        paku_img = pygame.image.load('image\Paku.jpg').convert_alpha()
        paku_img = pygame.transform.scale(paku_img, (70,70))
        xs, ys = 970, 510
        screen.blit(paku_img, (xs, ys))
        pygame.draw.rect(screen, blue, (xs - 4, ys - 4, 80, 80), 2)

        # Atur perubahan posisi benda
        atur_gerakan()

        try:
            jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus))
        except ZeroDivisionError:
            jarak_bayangan = jarak_benda

            x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(0)
            x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(680)
            dda_sinar(x1, y1, x2, y2, green, 1)

            x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(0)
            x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(-680)
            dda_sinar(x1, y1, x2, y2, green, 1)

        else:
            try:
                tinggi_bayangan = ((jarak_bayangan / jarak_benda) * tinggi_benda) * -1
            except:
                tinggi_bayangan = tinggi_benda

        draw_coordinate_axes(screen, black)

        # Gambar radio button pertama
        radio_button_rect1 = draw_radio_button(screen, xp + 28, yp - 30, "", active_radio_button1, active_radio_button2, False, False)
        
        # Gambar radio button kedua
        radio_button_rect2 = draw_radio_button(screen, xs + 28, ys - 30, "", active_radio_button2, active_radio_button1, True, True)

        rect = ((konv_koor_x(0)-fokus), 0, fokus, height)
        color = (0, 0, 255)
        start_angle = 1.5 * 3.14
        stop_angle = 2.5 * 3.14
        draw_arc(screen, color, rect, start_angle, stop_angle, 2)

        # Midpoint circle
        midpoint_circle_arc(screen, color, rect, start_angle, stop_angle, ratio=0.5)

        # Buat titik fokus
        x_fokus, y_fokus = konv_koor_x(fokus), konv_koor_y(0)
        pygame.draw.circle(screen, red, (x_fokus, y_fokus), 5)
        draw_text("F", x_fokus, y_fokus, red)

        # Buat titik R
        x_R, y_R = konv_koor_x(fokus*2), konv_koor_y(0)
        pygame.draw.circle(screen, green, (x_R, y_R), 5)
        draw_text("R", x_R, y_R, green)

        # Buat sinar istimewa 1 sejajar tinggi benda
        x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
        x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
        dda_sinar(x1, y1, x2, y2, yellow, 1)

        # Buat sinar istimewa 2 ke titik tengah
        x1, y1 = konv_koor_x(0), konv_koor_y(0)
        x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
        dda_sinar(x1, y1, x2, y2, pink, 1)
        
        if  jarak_benda != fokus and jarak_benda >= fokus:
            draw_garis_fokus(tinggi_bayangan, jarak_bayangan)
        if  jarak_benda <= fokus and jarak_benda != fokus :
            try:
                gambar_garis_putus_ckg(jarak_bayangan, tinggi_bayangan)
                cekg()
            except :
                ZeroDivisionError

        # Menambahkan tulisan "Ruang 1", "Ruang 2", "Ruang 3", dan "Ruang 4"
        text_surface = font.render("Ruang 1", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus -50), konv_koor_y(80)))

        text_surface = font.render("Ruang 2", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * 1.4 + 30), konv_koor_y(80)))

        text_surface = font.render("Ruang 3", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * 3 + 10), konv_koor_y(80)))

        text_surface = font.render("Ruang 1", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus -50), konv_koor_y(-60)))

        text_surface = font.render("Ruang 2", True, black)
        screen.blit(text_surface, (konv_koor_x((fokus * 1.4)+ 30), konv_koor_y(-60)))

        text_surface = font.render("Ruang 3", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * 3 + 10), konv_koor_y(-60)))

        text_surface = font.render("Ruang 4", True, black)
        screen.blit(text_surface, (konv_koor_x(-160), konv_koor_y(80)))

        # Membuat tulisan ruang bayangan dan benda
        text_surface = font.render("Ruang Bayangan", True, black)
        screen.blit(text_surface, (konv_koor_x(400), konv_koor_y(-200)))

        text_surface = font.render("Ruang Benda", True, black)
        screen.blit(text_surface, (konv_koor_x(400), konv_koor_y(250)))

        text_surface = font.render("Ruang Bayangan", True, black)
        screen.blit(text_surface, (konv_koor_x(-300), konv_koor_y(250)))

        draw_navigation_bar()
        pygame.draw.rect(screen, light_blue, (0, 604, 1200, 100))
        # pygame.draw.rect(screen, black, (0, 604, 1200, 3))

        # Membuat textbox
        x1, y1 = 820, height - 70
        draw_textbox("Jarak Fokus: " + str(fokus), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 70
        draw_textbox("Jari-jari: " + str(jarijari), x1, y1, 280, 30, light_blue)
        x1, y1 = 500, height - 50
        draw_textbox_sifatbygn("Sifat Bayangan", x1, y1, 280, 5, white)       
        
        x1, y1 = 820, height - 50
        draw_textbox("Jarak Benda: " + str(jarak_benda), x1, y1, 280, 30, light_blue)
        x1, y1 = 820, height - 30
        draw_textbox("Tinggi Benda: " + str(tinggi_benda), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 50
        draw_textbox("Jarak Bayangan: " + str(round(jarak_bayangan)), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 30
        draw_textbox("Tinggi Bayangan: " + str(round(tinggi_bayangan)), x1, y1, 280, 30, light_blue) 
        if jarak_benda == fokus :
            x1, y1 = 997, height - 50
            draw_textbox("Jarak Bayangan: " + str("Tak hingga"), x1, y1, 280, 30, light_blue)
            x1, y1 = 997, height - 30
            draw_textbox("Tinggi Bayangan: " + str("Tak hingga"), x1, y1, 280, 30, light_blue) 
        
        if show_detail :
            input_box_jarak.draw(screen)
            input_box_tinggi.draw(screen)
            input_box_fokus.draw(screen)

        pygame.display.flip()

def gambar_benda_cembung(jarak_benda, tinggi_benda):
    # Buat benda
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(0)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    x1, y1 = konv_koor_x(jarak_benda+5), konv_koor_y(tinggi_benda)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, blue, 3)
    draw_text("Benda", x1+5, y1, blue)

def gambar_bayangan_cembung(jarak_bayangan, tinggi_bayangan):
    x, y = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    # Buat bayangan benda
    x1, y1 = konv_koor_x(-jarak_bayangan), konv_koor_y(0)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)
    x1, y1 = konv_koor_x(-jarak_bayangan-5), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)
    x1, y1 = konv_koor_x(-jarak_bayangan+5), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, purple, 3)

    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_sinar(x1, y1, x2, y2, green, 1)

    # sinar pantul yg sinar fokus
    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, green, 1)

    # sinar pantul dri titik tengah
    x1, y1 = konv_koor_x(0), konv_koor_y(0)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, blue, 1)
    if jarak_benda != fokus :
        draw_text("Bayangan", x, y + 60, purple)


def gambar_stickman_cembung(jarak_benda, tinggi_benda):
    # Buat benda
    # Kepala
    x, y = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 1.25)
    # Badan
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_objek(x1, y1, x2, y2, black, 1)
    # Lengan
    panjang_lengan = tinggi_benda // 4
    x1, y1 = konv_koor_x(jarak_benda - panjang_lengan), konv_koor_y(tinggi_benda // 2)
    x2, y2 = konv_koor_x(jarak_benda + panjang_lengan), konv_koor_y(tinggi_benda // 2)
    dda_objek(x1, y1, x2, y2, black, 1)
    # Kaki
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda - panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, black, 1)
    x1, y1 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda // 3)
    x2, y2 = konv_koor_x(jarak_benda + panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, black, 1)
    draw_text("Benda", x, y - 60, blue)

def gambar_bayangan_stickman_cembung(jarak_bayangan, tinggi_bayangan):
    # Buat benda
    # Kepala
    if jarak_benda >= fokus :
        radius_kepala = tinggi_bayangan // 5 * -1
    else :
        radius_kepala = tinggi_bayangan // 5

    x, y = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan // 1.25)
    pygame.draw.circle(screen, grey, (x, y), radius_kepala)
    # Badan
    x1, y1 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_objek(x1, y1, x2, y2, grey, 1)
    # Lengan
    panjang_lengan = tinggi_bayangan // 4
    x1, y1 = konv_koor_x(-jarak_bayangan - panjang_lengan), konv_koor_y(tinggi_bayangan // 2)
    x2, y2 = konv_koor_x(-jarak_bayangan + panjang_lengan), konv_koor_y(tinggi_bayangan // 2)
    dda_objek(x1, y1, x2, y2, grey, 1)
    # Kaki
    x1, y1 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(-jarak_bayangan - panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, grey, 1)
    x1, y1 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan // 3)
    x2, y2 = konv_koor_x(-jarak_bayangan + panjang_lengan ), konv_koor_y(0)
    dda_objek(x1, y1, x2, y2, grey, 1)
    if jarak_benda != fokus :
        draw_text("Bayangan", x, y + 60, purple)

def draw_garis_fokus_cembung(jarak_bayangan, jarak_benda, tinggi_benda, tinggi_bayangan):
    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
    dda_sinar(x1, y1, x2, y2, green, 1)

    # sinar pantul yg sinar fokus
    x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_bayangan)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, green, 1)

    # sinar pantul dri titik tengah
    x1, y1 = konv_koor_x(0), konv_koor_y(0)
    x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
    dda_sinar(x1, y1, x2, y2, blue, 1)

def draw_radio_button_cembung(surface, x, y, text, active_radio_button1, active_radio_button2, draw_benda=True, draw_stickman=True):
    radio_button_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(surface, black, radio_button_rect, 2)

    if active_radio_button1 and not active_radio_button2 and draw_benda:
        gambar_benda_cembung(jarak_benda, tinggi_benda)
        gambar_bayangan_cembung(jarak_bayangan, tinggi_bayangan)
        pygame.draw.circle(surface, red, (x + 10, y + 10), 6)
    elif active_radio_button2 and not active_radio_button1 and draw_stickman:
        gambar_stickman(jarak_benda, tinggi_benda)
        gambar_bayangan_stickman_cembung(jarak_bayangan, tinggi_bayangan)
        pygame.draw.circle(surface, red, (x + 100, y + 10), 6)

    text_surface = font.render(text, True, black)
    surface.blit(text_surface, (x + 30, y+5))

    return radio_button_rect
def Lensa_Cembung():
    global jarak_benda, tinggi_benda, fokus, jarak_bayangan, tinggi_bayangan, show_input_boxes, show_choose_object, show_detail
    running = True
    active_radio_button1 = False
    active_radio_button2 = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if radio_button_rect1.collidepoint(mouse_pos):
                    active_radio_button1 = not active_radio_button1
                    active_radio_button2 = False
                elif radio_button_rect2.collidepoint(mouse_pos):
                    active_radio_button2 = not active_radio_button2
                    active_radio_button1 = False

            new_fokus = input_box_fokus.handle_event(event)
            if new_fokus is not None:
                fokus = new_fokus

            new_tinggi = input_box_tinggi.handle_event(event)
            if new_tinggi is not None:
                tinggi_benda = new_tinggi
            
            new_jarak = input_box_jarak.handle_event(event)
            if new_jarak is not None:
                jarak_benda = new_jarak

        # Gambar Background
        screen.fill(white)

        stickman_img = pygame.image.load('image\Stickman.jpg').convert_alpha()
        stickman_img = pygame.transform.scale(stickman_img, (80,80))
        xp, yp = 1060, 510
        screen.blit(stickman_img, (xp, yp))
        pygame.draw.rect(screen, blue, (xp, yp - 4, 80, 80), 2)

        paku_img = pygame.image.load('image\Paku.jpg').convert_alpha()
        paku_img = pygame.transform.scale(paku_img, (70,70))
        xs, ys = 970, 510
        screen.blit(paku_img, (xs, ys))
        pygame.draw.rect(screen, blue, (xs - 4, ys - 4, 80, 80), 2)

        atur_gerakan()

        try:
            jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus))
        except:
            jarak_bayangan = jarak_benda

            x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(0)
            x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(680)
            dda_sinar(x1, y1, x2, y2, green, 1)

            x1, y1 = konv_koor_x(jarak_bayangan), konv_koor_y(0)
            x2, y2 = konv_koor_x(jarak_bayangan), konv_koor_y(-680)
            dda_sinar(x1, y1, x2, y2, green, 1)

            x1, y1 = konv_koor_x(0), konv_koor_y(0)
            x2, y2 = konv_koor_x(-jarak_benda*5), konv_koor_y(-tinggi_benda*5)
            dda_sinar(x1, y1, x2, y2, blue, 1)

        else:
            try:
                tinggi_bayangan = ((jarak_bayangan / jarak_benda) * tinggi_benda) * -1
            except:
                tinggi_bayangan = 0

        
        # Gambar garis X dan Y
        draw_coordinate_axes(screen, black)

        # Gambar radio button pertama
        radio_button_rect1 = draw_radio_button_cembung(screen, xp + 28, yp - 30, "", active_radio_button1, active_radio_button2, False, False)
        
        # Gambar radio button kedua
        radio_button_rect2 = draw_radio_button_cembung(screen, xs + 28, ys - 30, "", active_radio_button2, active_radio_button1, True, True)

        rect = (((konv_koor_x(0))- fokus*0.14), 0.5, fokus*0.28, height)
        color = (0, 0, 255)
        start_angle = 1.7 * 3.14
        stop_angle = 1.69 * 3.14
        draw_arc(screen, color, rect, start_angle, stop_angle, 2)

        # Midpoint circle
        midpoint_circle_arc(screen, color, rect, start_angle, stop_angle, ratio=1)
        
        # Menambahkan tulisan "Ruang 1", "Ruang 2", "Ruang 3", dan "Ruang 4"
        text_surface = font.render("Ruang 1", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * 0.7), konv_koor_y(20)))

        text_surface = font.render("Ruang 2", True, black)
        screen.blit(text_surface, (konv_koor_x((fokus * 1.5)+ 30), konv_koor_y(20)))

        text_surface = font.render("Ruang 3", True, black)
        screen.blit(text_surface, (konv_koor_x((fokus * 2.5)+30), konv_koor_y(20)))

        text_surface = font.render("Ruang 4", True, black)
        screen.blit(text_surface, (konv_koor_x(-130), konv_koor_y(40)))
        
        # Menambahkan tulisan "Ruang 1", "Ruang 2", "Ruang 3", dan "Ruang 4"
        text_surface = font.render("Ruang 1", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * -0.3), konv_koor_y(-10)))

        text_surface = font.render("Ruang 2", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * -1.3), konv_koor_y(-10)))

        text_surface = font.render("Ruang 3", True, black)
        screen.blit(text_surface, (konv_koor_x(fokus * -2.3), konv_koor_y(-10)))

        text_surface = font.render("Ruang 4", True, black)
        screen.blit(text_surface, (konv_koor_x(180), konv_koor_y(-30)))

        # Membuat tulisan ruang benda dan bayangan
        text_surface = font.render("Ruang Bayangan", True, black)
        screen.blit(text_surface, (konv_koor_x(-200), konv_koor_y(-230)))

        text_surface = font.render("Ruang Benda", True, black)
        screen.blit(text_surface, (konv_koor_x(350), konv_koor_y(250)))
        
        text_surface = font.render("Ruang Benda", True, black)
        screen.blit(text_surface, (konv_koor_x(-350), konv_koor_y(250)))

        text_surface = font.render("Ruang Bayangan", True, black)
        screen.blit(text_surface, (konv_koor_x(250), konv_koor_y(-230)))

        # Buat titik fokus
        x_fokus, y_fokus = konv_koor_x(fokus), konv_koor_y(0)
        pygame.draw.circle(screen, red, (x_fokus, y_fokus), 5)
        draw_text_cembung("F2", x_fokus, y_fokus)
        x_fokus, y_fokus = konv_koor_x(-fokus), konv_koor_y(0)
        pygame.draw.circle(screen, red, (x_fokus, y_fokus), 5)
        draw_text_cembung("F1", x_fokus, y_fokus)

        # Buat titik R
        x_R, y_R = konv_koor_x(fokus*2), konv_koor_y(0)
        pygame.draw.circle(screen, green, (x_R, y_R), 5)
        draw_text_cembung("2F2", x_R, y_R) 
        x_R, y_R = konv_koor_x(-fokus*2), konv_koor_y(0)
        pygame.draw.circle(screen, green, (x_R, y_R), 5)
        draw_text_cembung("2F1", x_R, y_R)

        # membuat sinar atas pada benda
        x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
        x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
        dda_sinar(x1, y1, x2, y2, yellow, 1)

        # membuat sinar pantul 1
        x1, y1 = konv_koor_x(0), konv_koor_y(tinggi_benda)
        x2, y2 = konv_koor_x(-jarak_bayangan), konv_koor_y(tinggi_bayangan)
        dda_sinar(x1, y1, x2, y2, yellow, 1)

        # sinar ke titik tengah
        x1, y1 = konv_koor_x(0), konv_koor_y(0)
        x2, y2 = konv_koor_x(jarak_benda), konv_koor_y(tinggi_benda)
        dda_sinar(x1, y1, x2, y2, blue, 1)

        if jarak_benda != fokus :
            draw_garis_fokus_cembung(jarak_bayangan, jarak_benda, tinggi_benda, tinggi_bayangan)
        if  jarak_benda != fokus and jarak_benda <= fokus:
            try:
               cemb()
            except :
                ZeroDivisionError
        
        pygame.draw.rect(screen, sky, (0, 600, 1200, 100))
        pygame.draw.rect(screen, black, (0, 597, 1200, 3))
        draw_navigation_bar()
        pygame.draw.rect(screen, light_blue, (0, 604, 1200, 100))

        # Membuat textbox
        x1, y1 = 820, height - 70
        draw_textbox("Jarak Fokus: " + str(fokus), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 70
        draw_textbox("Jari-jari: " + str(jarijari), x1, y1, 280, 30, light_blue)
        x1, y1 = 500, height - 50
        draw_textbox_sifatbygn("Sifat Bayangan", x1, y1, 280, 5, white)       
        
        x1, y1 = 820, height - 50
        draw_textbox("Jarak Benda: " + str(jarak_benda), x1, y1, 280, 30, light_blue)
        x1, y1 = 820, height - 30
        draw_textbox("Tinggi Benda: " + str(tinggi_benda), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 50
        draw_textbox("Jarak Bayangan: " + str(round(jarak_bayangan)), x1, y1, 280, 30, light_blue)
        x1, y1 = 997, height - 30
        draw_textbox("Tinggi Bayangan: " + str(round(tinggi_bayangan)), x1, y1, 280, 30, light_blue) 
        if jarak_bayangan == fokus :
            x1, y1 = 997, height - 50
            jarak_bayangan = 00
            draw_textbox("Jarak Bayangan: " + str("Tak hingga"), x1, y1, 280, 30, light_blue)
            x1, y1 = 997, height - 30
            draw_textbox("Tinggi Bayangan: " + str("Tak hingga"), x1, y1, 280, 30, light_blue) 

        # Menambahkan input box ke layar
        if show_detail :
            input_box_jarak.draw(screen)
            input_box_tinggi.draw(screen)
            input_box_fokus.draw(screen)

        pygame.display.flip()
        
menu()

pygame.quit()
