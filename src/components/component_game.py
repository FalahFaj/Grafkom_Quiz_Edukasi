# src/components/component_game.py
import cairo
import math
import random
import time

import assets.images.apel as img_apel
import assets.images.jeruk as img_jeruk
import assets.images.hati as img_hati
import assets.images.jam as img_jam

def rounded_rect(ctx, x, y, w, h, r):
    """Fungsi helper untuk membuat kotak dengan sudut melengkung."""
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

def draw_game_background(ctx, w, h, difficulty):
    """Menggambar background dinamis berdasarkan tingkat kesulitan."""
    
    if difficulty == "easy":
        # --- PAGI (Biru Cerah) ---
        pat = cairo.LinearGradient(0, 0, 0, h)
        pat.add_color_stop_rgb(0, 0.4, 0.8, 1.0) # Langit Biru
        pat.add_color_stop_rgb(1, 0.6, 0.9, 1.0)
        ctx.set_source(pat); ctx.paint()

        # Matahari Kuning Cerah
        ctx.save(); ctx.translate(100, 120)
        ctx.set_source_rgb(1, 0.9, 0.2)
        ctx.arc(0, 0, 30, 0, 2*math.pi); ctx.fill()
        ctx.restore()
        
        # Warna Bukit
        bg_hill_color = (0.3, 0.8, 0.3)
        
    elif difficulty == "medium":
        # --- SORE (Oranye/Ungu) ---
        pat = cairo.LinearGradient(0, 0, 0, h)
        pat.add_color_stop_rgb(0, 0.2, 0.1, 0.4) # Ungu Tua Atas
        pat.add_color_stop_rgb(0.6, 0.8, 0.4, 0.2) # Pink/Oranye
        pat.add_color_stop_rgb(1, 1.0, 0.7, 0.3) # Kuning Bawah
        ctx.set_source(pat); ctx.paint()

        # Matahari Terbenam (Oren Kemerahan)
        ctx.save(); ctx.translate(400, 450)
        ctx.set_source_rgba(1, 0.5, 0.1, 0.8)
        ctx.arc(0, 0, 100, 0, 2*math.pi); ctx.fill()
        ctx.restore()

        # Warna Bukit
        bg_hill_color = (0.4, 0.5, 0.2)

    else: # hard
        # --- MALAM (Biru Gelap) ---
        pat = cairo.LinearGradient(0, 0, 0, h)
        pat.add_color_stop_rgb(0, 0.05, 0.05, 0.2) # Biru Gelap
        pat.add_color_stop_rgb(1, 0.1, 0.1, 0.3)
        ctx.set_source(pat); ctx.paint()

        # Bulan dari komponen_map.py
        ctx.save()
        # Pindah ke bawah soal
        ctx.translate(750, 200)
        
        sun_color = (0.9, 0.9, 1.0) # Warna bulan

        # Glow effect
        glow = cairo.RadialGradient(0, 0, 10, 0, 0, 80)
        glow.add_color_stop_rgba(0, sun_color[0], sun_color[1], sun_color[2], 0.6)
        glow.add_color_stop_rgba(1, sun_color[0], sun_color[1], sun_color[2], 0.0)
        ctx.set_source(glow)
        ctx.arc(0, 0, 80, 0, 2*math.pi)
        ctx.fill()
        
        # Badan Bulan
        ctx.set_source_rgb(*sun_color)
        ctx.arc(0, 0, 30, 0, 2*math.pi)
        ctx.fill()
        
        # Kawah Bulan
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.4)
        ctx.arc(-10, -5, 6, 0, 2*math.pi)
        ctx.fill()
        ctx.arc(15, 10, 6, 0, 2*math.pi)
        ctx.fill()
        ctx.restore()

        # Bintang-bintang
        # Kita gunakan pseudo-random based on coordinate agar tidak berkedip aneh setiap frame
        # (Kecuali jika ingin animasi, tapi untuk bg statis lebih baik begini)
        ctx.set_source_rgba(1, 1, 1, 0.6)
        for i in range(30):
            # Rumus sederhana untuk posisi 'acak' yang konsisten
            bx = (i * 137) % 800
            by = (i * 53) % 400
            r = (i % 3) + 1
            ctx.arc(bx, by, r, 0, 2*math.pi)
            ctx.fill()

        # Warna Bukit
        bg_hill_color = (0.1, 0.2, 0.1)

    # Gambar Bukit (Bentuk sama, warna beda sesuai variabel diatas)
    ctx.set_source_rgb(*bg_hill_color)
    ctx.move_to(0, h)
    ctx.line_to(0, 500)
    ctx.curve_to(200, 450, 600, 550, 800, 480)
    ctx.line_to(w, h)
    ctx.close_path()
    ctx.fill()

def draw_hud(ctx, w, h, lives, timer, difficulty, display_level):
    """Menggambar Heads-Up Display (Nyawa, Timer, Info Level)."""
    
    # 1. Nyawa (Kiri Atas)
    ctx.save(); ctx.translate(30, 30)
    for i in range(lives):
        ctx.save()
        ctx.translate(i * 30, 0)
        ctx.scale(0.15, 0.15)
        img_hati.gambar(ctx, 0, 0)
        ctx.restore()
    ctx.restore()

    # 2. Timer (Kanan Atas)
    ctx.save(); ctx.translate(720, 40)
    ctx.save()
    ctx.scale(0.3, 0.3)
    # Gunakan timer sebagai frame_count untuk animasi jarum jam sederhana
    img_jam.gambar(ctx, 0, 0, frame_count=int(time.time() * 10)) 
    ctx.restore()
    
    # Teks Timer
    ctx.set_font_size(24)
    ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    # Warna merah jika waktu < 10 detik
    if timer > 10:
        ctx.set_source_rgb(1, 1, 1)
    else:
        ctx.set_source_rgb(1, 0, 0)
        
    ctx.move_to(-15, 45)
    ctx.show_text(f"{timer}s")
    ctx.restore()

    # 3. Info Level (Tengah Atas)
    if difficulty == "hard":
        ctx.set_source_rgb(1, 1, 1) # Putih di malam
    else:
        ctx.set_source_rgb(0, 0.3, 0.6) # Biru di siang/sore

    ctx.set_font_size(30)
    label = f"LEVEL {display_level}"
    ext = ctx.text_extents(label)
    ctx.move_to((w - ext.width)/2, 50)
    ctx.show_text(label)

def draw_fruit_group(ctx, count, fruit_type, center_x, center_y):
    """Menggambar sekumpulan buah dalam grid."""
    renderer = img_apel if fruit_type == "apel" else img_jeruk
    
    # Grid layout
    if count > 25:
        cols = 6
    elif count > 15:
        cols = 5
    else:
        cols = 4
    rows = math.ceil(count / cols)
    size = 45 
    
    # Hitung Ukuran Kontainer Background
    total_w = min(count, cols) * size
    total_h = rows * size
    padding = 15

    # 1. Gambar Background Kontainer Buah (Transparan Putih)
    ctx.save()
    ctx.translate(center_x, center_y)
    ctx.set_source_rgba(1, 1, 1, 0.3) # Putih transparan
    rounded_rect(ctx, -total_w/2 - padding, -total_h/2 - padding, 
                   total_w + padding*2, total_h + padding*2, 15)
    ctx.fill()
    # Border tipis
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.restore()

    # 2. Gambar Buah
    ctx.save()
    ctx.translate(center_x, center_y)
    
    start_x = -((min(count, cols) * size) / 2) + size/2
    start_y = -((rows * size) / 2) + size/2
    
    for i in range(count):
        c = i % cols
        r = i // cols
        ctx.save()
        ctx.translate(start_x + c*size, start_y + r*size)
        ctx.scale(0.12, 0.12)
        renderer.gambar(ctx, 0, 0)
        ctx.restore()
    ctx.restore()

def draw_question_visuals(ctx, width, height, question_data):
    """Menggambar visualisasi soal (buah kiri, operator, buah kanan, teks soal)."""
    q = question_data
    
    # Koordinat Layout
    y_visual = 200 # Posisi tengah buah
    y_soal = 385   # Posisi teks soal
    
    x_left = 220
    x_right = 580
    x_mid = 400 
    
    # Tentukan karakter operator
    op_char = "+"
    if q['op'] == "x": op_char = "×"
    elif q['op'] == ":": op_char = "÷"
    elif q['op'] == "-": op_char = "-"

    # 1. Gambar Buah Kiri & Kanan
    draw_fruit_group(ctx, q['a'], q['fruit'], x_left, y_visual)
    draw_fruit_group(ctx, q['b'], q['fruit'], x_right, y_visual)
    
    # 2. Operator di Tengah
    ctx.set_font_size(70)
    ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    # Shadow Operator
    ctx.move_to(x_mid - 20 + 3, y_visual + 20 + 3)
    ctx.set_source_rgba(0,0,0,0.5); ctx.show_text(op_char)
    # Operator Utama (Putih)
    ctx.move_to(x_mid - 20, y_visual + 20)
    ctx.set_source_rgb(1, 1, 1); ctx.show_text(op_char)

    # 3. Box Teks Soal Lengkap di Bawah
    # Format: "4 + 2 = ?"
    full_q = f"{q['a']}  {op_char}  {q['b']}  =  ?"
    
    ctx.set_font_size(50)
    ext_q = ctx.text_extents(full_q)
    q_x = (width - ext_q.width)/2
    
    # Background Box Soal
    ctx.set_source_rgba(1, 1, 1, 0.6)
    rounded_rect(ctx, q_x - 20, y_soal - 50, ext_q.width + 40, 70, 10)
    ctx.fill()

    # Teks Soal
    ctx.set_source_rgb(0, 0, 0.4) 
    ctx.move_to(q_x, y_soal)
    ctx.show_text(full_q)