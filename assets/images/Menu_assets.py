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

def draw_glossy_button(ctx, x, y, w, h, text, color="GREEN"):
    """Tombol Game Mewah"""
    ctx.save()
    ctx.translate(x, y)
    
    if color == "GREEN":
        top, mid, bot = (0.5, 0.8, 0.1), (0.3, 0.6, 0.0), (0.2, 0.4, 0.0)
        txt_col = (0.1, 0.3, 0.0)
    else: # ORANGE
        top, mid, bot = (1.0, 0.8, 0.0), (1.0, 0.6, 0.0), (0.8, 0.4, 0.0)
        txt_col = (0.6, 0.2, 0.0)

    r = 20 # Radius sudut
    
    # 1. Bayangan Drop Shadow
    ctx.set_source_rgba(0, 0, 0, 0.3)
    rounded_rect(ctx, 0, 5, w, h+5, r); ctx.fill()
    
    # 2. Badan Tombol (Gradien Vertikal)
    grad = cairo.LinearGradient(0, 0, 0, h)
    grad.add_color_stop_rgb(0, *top)
    grad.add_color_stop_rgb(1, *mid)
    rounded_rect(ctx, 0, 0, w, h, r)
    ctx.set_source(grad); ctx.fill()
    
    # 3. Efek 3D Bawah (Tebal)
    ctx.save()
    ctx.rectangle(0, h/2, w, h); ctx.clip() # Potong setengah bawah
    rounded_rect(ctx, 0, 0, w, h, r)
    ctx.set_source_rgb(*bot); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    
    # 4. Highlight Kaca (Oval Putih Transparan di atas)
    grad_gloss = cairo.LinearGradient(0, 0, 0, h/2)
    grad_gloss.add_color_stop_rgba(0, 1, 1, 1, 0.6) # Putih terang
    grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.1) # Pudar
    
    ctx.save()
    rounded_rect(ctx, 10, 5, w-20, h/2 - 5, r-5)
    ctx.set_source(grad_gloss); ctx.fill()
    ctx.restore()
    
    # 5. Teks Tombol
    ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(40)
    ext = ctx.text_extents(text)
    
    # Shadow Teks (Kuning/Putih Outline)
    ctx.move_to(w/2 - ext.width/2, h/2 + ext.height/2)
    ctx.text_path(text)
    ctx.set_source_rgb(1, 1, 0.7); ctx.set_line_width(4); ctx.stroke()
    
    # Isi Teks
    ctx.move_to(w/2 - ext.width/2, h/2 + ext.height/2)
    ctx.set_source_rgb(*txt_col); ctx.show_text(text)
    
    ctx.restore()

def draw_logo_monster(ctx, x, y):
    ctx.save()
    ctx.translate(x, y)
    
    # --- Fungsi Gambar Teks Outline Tebal ---
    def text_blob(txt, tx, ty, color, size=80):
        ctx.save(); ctx.translate(tx, ty)
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(size)
        
        # Shadow Oranye Tua
        ctx.move_to(3, 3); ctx.text_path(txt)
        ctx.set_source_rgb(0.8, 0.4, 0.0); ctx.fill()
        
        # Outline Putih Tebal
        ctx.move_to(0, 0); ctx.text_path(txt)
        ctx.set_source_rgb(1,1,1); ctx.set_line_width(8); ctx.stroke()
        
        # Isi Gradien Kuning-Oranye
        grad = cairo.LinearGradient(0, -size, 0, 0)
        grad.add_color_stop_rgb(0, 1.0, 0.9, 0.2) # Kuning
        grad.add_color_stop_rgb(1, 1.0, 0.6, 0.0) # Oranye
        ctx.move_to(0, 0); ctx.set_source(grad); ctx.show_text(txt)
        ctx.restore()

    # 1. Teks "Eduiz" (Disatukan agar rapi di tengah)
    # Geser ke kiri (-110) agar titik tengahnya pas di tengah layar
    text_blob("Eduiz", -110, 30, (1, 0.6, 0))
    
    # Monster Hijau DIHAPUS sesuai permintaan
    
    # 2. Monster Ungu (Geser ke kanan jadi 180 agar tidak menabrak teks)
    ctx.save(); ctx.translate(180, -20); ctx.rotate(0.2)
    # Badan
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    ctx.set_source_rgb(1,1,1); ctx.set_line_width(6); ctx.stroke() # Outline
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    grad_p = cairo.LinearGradient(0, -35, 0, 35)
    grad_p.add_color_stop_rgb(0, 0.8, 0.4, 0.9) # Ungu pinkish
    grad_p.add_color_stop_rgb(1, 0.5, 0.1, 0.7) # Ungu gelap
    ctx.set_source(grad_p); ctx.fill()
    # Mata Melotot
    ctx.translate(-15, -10)
    ctx.set_source_rgb(1,1,1); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(1,0.2,0.5); ctx.arc(0,0, 6, 0, 2*math.pi); ctx.fill() 
    ctx.set_source_rgb(0,0,0); ctx.arc(0,0, 2, 0, 2*math.pi); ctx.fill()
    ctx.translate(30, 0)
    ctx.set_source_rgb(1,1,1); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(1,0.2,0.5); ctx.arc(0,0, 6, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(0,0,0); ctx.arc(0,0, 2, 0, 2*math.pi); ctx.fill()
    # Mulut Gerigi
    ctx.translate(-15, 25)
    ctx.set_source_rgb(0.3, 0, 0.2); ctx.arc(0,0, 12, math.pi, 0); ctx.fill() 
    ctx.set_source_rgb(1,1,1) 
    ctx.move_to(-8, 0); ctx.line_to(-5, 5); ctx.line_to(-2, 0); ctx.fill()
    ctx.move_to(2, 0); ctx.line_to(5, 5); ctx.line_to(8, 0); ctx.fill()
    ctx.restore()

    ctx.restore()

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