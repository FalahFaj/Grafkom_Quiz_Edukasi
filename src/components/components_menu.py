import cairo
import math

def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

def draw_cloud(ctx, x, y, scale):
    """Awan Gantung dengan Pola Kotak"""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    
    # Tali Putih
    ctx.move_to(0, 0); ctx.line_to(0, -300)
    ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(3); ctx.stroke()
    
    # Bentuk Awan
    ctx.arc(0, 0, 30, 0, 2*math.pi)
    ctx.arc(35, -15, 40, 0, 2*math.pi)
    ctx.arc(70, 0, 30, 0, 2*math.pi)
    ctx.arc(35, 25, 35, 0, 2*math.pi)
    
    # Isi Awan (Biru Muda Pucat + Checkerboard)
    ctx.save(); ctx.clip()
    ctx.set_source_rgb(0.85, 0.92, 0.95); ctx.paint()
    
    ctx.set_source_rgba(0.6, 0.8, 0.8, 0.3) # Warna kotak
    sz = 15
    for i in range(-50, 120, sz):
        for j in range(-50, 120, sz):
            if (i//sz + j//sz) % 2 == 0: ctx.rectangle(i, j, sz, sz); ctx.fill()
    ctx.restore()
    
    # Outline Putih Tebal
    ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(6)
    ctx.arc(0, 0, 30, 0, 2*math.pi); ctx.stroke()
    ctx.arc(35, -15, 40, 0, 2*math.pi); ctx.stroke()
    ctx.arc(70, 0, 30, 0, 2*math.pi); ctx.stroke()
    ctx.arc(35, 25, 35, 0, 2*math.pi); ctx.stroke()
    
    # Drop Shadow Awan (Di luar outline)
    ctx.save()
    ctx.translate(5, 5)
    ctx.set_source_rgba(0, 0, 0, 0.1)
    # (Gambar ulang shape untuk shadow - simplified)
    ctx.arc(35, 5, 60, 0, 2*math.pi); ctx.fill()
    ctx.restore()
    
    ctx.restore()

def draw_glossy_button(ctx, x, y, w, h, text, color="GREEN", state="normal", font_size=40):
    """Tombol Game Mewah dengan status hover dan press"""
    ctx.save()
    
    # Penyesuaian offset untuk efek ditekan
    press_offset = 2 if state == "pressed" else 0
    ctx.translate(x, y + press_offset)

    # Tentukan palet warna dasar
    if color == "GREEN":
        top, mid, bot = (0.5, 0.8, 0.1), (0.3, 0.6, 0.0), (0.2, 0.4, 0.0)
        txt_col = (0.1, 0.3, 0.0)
    else:  # ORANGE
        top, mid, bot = (1.0, 0.8, 0.0), (1.0, 0.6, 0.0), (0.8, 0.4, 0.0)
        txt_col = (0.6, 0.2, 0.0)

    # Penyesuaian warna berdasarkan state
    if state == "hover":
        # Jadikan warna lebih cerah saat hover
        top = tuple(min(1.0, c + 0.15) for c in top)
        mid = tuple(min(1.0, c + 0.15) for c in mid)
    elif state == "pressed":
        # Jadikan warna lebih gelap saat ditekan
        top = tuple(max(0.0, c - 0.15) for c in top)
        mid = tuple(max(0.0, c - 0.15) for c in mid)

    r = 20  # Radius sudut

    # 1. Bayangan Drop Shadow (lebih kecil saat ditekan)
    shadow_offset = 3 if state == "pressed" else 5
    ctx.set_source_rgba(0, 0, 0, 0.3)
    rounded_rect(ctx, 0, shadow_offset, w, h, r)
    ctx.fill()

    # 2. Badan Tombol (Gradien Vertikal)
    # grad = cairo.LinearGradient(0, 0, 0, h)
    # grad.add_color_stop_rgb(0, *top)
    # grad.add_color_stop_rgb(1, *mid)
    # rounded_rect(ctx, 0, 0, w, h, r)
    # ctx.set_source(grad)
    # ctx.fill()
    rounded_rect(ctx, 0, 0, w, h, r)
    ctx.set_source_rgb(*bot)
    ctx.fill()

    # 3. Efek 3D Bawah (Tebal)
    # ctx.save()
    # ctx.rectangle(0, h / 2, w, h)
    # ctx.clip()
    # rounded_rect(ctx, 0, 0, w, h, r)
    # ctx.set_source_rgb(*bot)
    # ctx.set_line_width(6)
    # ctx.stroke()
    # ctx.restore()
    tebal_3d = 6
    rounded_rect(ctx, 0, 0, w, h - tebal_3d, r)
    
    grad = cairo.LinearGradient(0, 0, 0, h - tebal_3d)
    grad.add_color_stop_rgb(0, *top)
    grad.add_color_stop_rgb(1, *mid)
    
    ctx.set_source(grad)
    ctx.fill()

    # 4. Highlight Kaca (dikurangi saat ditekan)
    if state != "pressed":
        gloss_alpha = 0.7 if state == "hover" else 0.6
        grad_gloss = cairo.LinearGradient(0, 0, 0, h / 2)
        grad_gloss.add_color_stop_rgba(0, 1, 1, 1, gloss_alpha)
        grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.1)

        ctx.save()
        rounded_rect(ctx, 10, 5, w - 20, h / 2 - 5, r - 5)
        ctx.set_source(grad_gloss)
        ctx.fill()
        ctx.restore()

    # 5. Teks Tombol
    ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    ext = ctx.text_extents(text)

    # Posisi teks yang benar-benar di tengah
    text_x_pos = w / 2 - ext.width / 2 - ext.x_bearing
    text_y_pos = h / 2 - ext.height / 2 - ext.y_bearing
    
    # Shadow Teks
    ctx.move_to(text_x_pos, text_y_pos)
    ctx.text_path(text)
    ctx.set_source_rgb(1, 1, 0.7)
    ctx.set_line_width(4)
    ctx.stroke()

    # Isi Teks
    ctx.move_to(text_x_pos, text_y_pos)
    ctx.set_source_rgb(*txt_col)
    ctx.show_text(text)

    ctx.restore()

def draw_logo_monster(ctx, x, y, time=0):
    """Menggambar logo dengan font kartun dan monster yang beranimasi."""
    ctx.save()
    ctx.translate(x, y)
    
    # --- Fungsi Gambar Teks Outline Tebal ---
    def text_blob(txt, tx, ty, color, size=80):
        ctx.save()
        ctx.translate(tx, ty)
        # Menggunakan font yang lebih kartunis
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(size)
        
        # Shadow Oranye Tua
        ctx.move_to(3, 3)
        ctx.text_path(txt)
        ctx.set_source_rgb(0.8, 0.4, 0.0)
        ctx.fill()
        
        # Outline Putih Tebal
        ctx.move_to(0, 0)
        ctx.text_path(txt)
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(8)
        ctx.stroke()
        
        # Isi Gradien Kuning-Oranye
        grad = cairo.LinearGradient(0, -size, 0, 0)
        grad.add_color_stop_rgb(0, 1.0, 0.9, 0.2) # Kuning
        grad.add_color_stop_rgb(1, 1.0, 0.6, 0.0) # Oranye
        ctx.move_to(0, 0)
        ctx.set_source(grad)
        ctx.show_text(txt)
        ctx.restore()

    # 1. Teks "Eduiz"
    text_blob("Eduiz", -140, 80, (1, 0.6, 0), 120)
    
    # 2. Monster Ungu Beranimasi
    ctx.save()
    ctx.translate(180, -20)
    # Goyangan lembut menggunakan sinus dari waktu
    rotation_angle = math.sin(time * 0.05) * 0.2  # ayunan 0.2 radian
    ctx.rotate(rotation_angle)
    
    # Badan
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    ctx.set_source_rgb(1,1,1); ctx.set_line_width(6); ctx.stroke() # Outline
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    grad_p = cairo.LinearGradient(0, -35, 0, 35)
    grad_p.add_color_stop_rgb(0, 0.8, 0.4, 0.9) # Ungu pinkish
    grad_p.add_color_stop_rgb(1, 0.5, 0.1, 0.7) # Ungu gelap
    ctx.set_source(grad_p); ctx.fill()
    
    # Mata Melotot (sedikit bergerak berlawanan arah untuk efek paralaks)
    eye_offset_x = math.sin(time * 0.05 + math.pi) * 2 # Bergerak horizontal
    ctx.translate(-15 + eye_offset_x, -10)
    ctx.set_source_rgb(1,1,1); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(1,0.2,0.5); ctx.arc(0,0, 6, 0, 2*math.pi); ctx.fill() 
    ctx.set_source_rgb(0,0,0); ctx.arc(0,0, 2, 0, 2*math.pi); ctx.fill()
    ctx.translate(30, 0)
    ctx.set_source_rgb(1,1,1); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(1,0.2,0.5); ctx.arc(0,0, 6, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(0,0,0); ctx.arc(0,0, 2, 0, 2*math.pi); ctx.fill()
    
    # Mulut Gerigi
    ctx.translate(-15 - eye_offset_x, 25) # Reset translasi mata
    ctx.set_source_rgb(0.3, 0, 0.2); ctx.arc(0,0, 12, math.pi, 0); ctx.fill() 
    ctx.set_source_rgb(1,1,1) 
    ctx.move_to(-8, 0); ctx.line_to(-5, -5); ctx.line_to(-2, 0); ctx.fill()
    ctx.move_to(2, 0); ctx.line_to(5, -5); ctx.line_to(8, 0); ctx.fill()
    
    ctx.restore() # Mengembalikan state dari monster
    ctx.restore() # Mengembalikan state dari keseluruhan logo

def gambar(ctx, width, height):
    # Scaling Virtual 800x600
    ctx.scale(width / 800, height / 600)

    # 1. Awan Gantung
    draw_cloud(ctx, 150, 80, 1.2) # Kiri Besar
    draw_cloud(ctx, 100, 200, 0.8) # Kiri Kecil
    draw_cloud(ctx, 700, 120, 1.1) # Kanan

    # 2. Logo Utama (Teks + Monster)
    draw_logo_monster(ctx, 400, 130)

    # 3. Tombol Menu (Play, Options, Help)
    # Tombol Play (Hijau Besar)
    draw_glossy_button(ctx, 250, 250, 300, 80, "Play", "GREEN")
    # Tombol Options
    draw_glossy_button(ctx, 250, 345, 300, 70, "Options", "ORANGE")
    # Tombol Help
    draw_glossy_button(ctx, 250, 430, 300, 70, "Help", "ORANGE")

def draw_lock_icon(ctx, x, y, size):
    """Menggambar ikon gembok sederhana"""
    # Warna Gembok (Emas/Kuning Logam)
    ctx.set_source_rgb(0.9, 0.8, 0.2) 
    
    body_w = size * 0.8
    body_h = size * 0.6
    body_x = x + (size - body_w) / 2
    body_y = y + size * 0.4
    
    # 1. Gagang Gembok (Shackle) - Setengah lingkaran di atas
    ctx.set_line_width(size * 0.1)
    ctx.set_source_rgb(0.7, 0.7, 0.7) # Warna besi perak
    
    # Gambar kurva gagang
    radius = body_w * 0.35
    center_x = x + size / 2
    center_y = body_y
    
    ctx.new_sub_path()
    ctx.arc(center_x, center_y, radius, 3.14, 0) # Setengah lingkaran
    ctx.line_to(center_x + radius, center_y + (body_h * 0.2)) # Kaki gagang kanan
    ctx.move_to(center_x - radius, center_y) 
    ctx.line_to(center_x - radius, center_y + (body_h * 0.2)) # Kaki gagang kiri
    ctx.stroke()
    
    # 2. Badan Gembok (Kotak Emas)
    ctx.set_source_rgb(0.9, 0.7, 0.1) # Emas
    rounded_rect(ctx, body_x, body_y, body_w, body_h, 5)
    ctx.fill()
    
    # 3. Lubang Kunci (Hiasan hitam di tengah)
    ctx.set_source_rgb(0.2, 0.1, 0)
    ctx.arc(center_x, body_y + body_h/2, size * 0.1, 0, 6.28)
    ctx.fill()