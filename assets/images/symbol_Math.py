import cairo
import math

# =====================================================
# 1. FUNGSI GAMBAR SIMBOL (Dibuat lebih tebal & tumpul)
# =====================================================

def draw_plus(ctx):
    ctx.set_line_width(12)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # Garis Horizontal
    ctx.move_to(-20, 0)
    ctx.line_to(20, 0)
    # Garis Vertikal
    ctx.move_to(0, -20)
    ctx.line_to(0, 20)
    ctx.stroke()

def draw_minus(ctx):
    ctx.set_line_width(12)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # Garis Horizontal
    ctx.move_to(-25, 0)
    ctx.line_to(25, 0)
    ctx.stroke()

def draw_times(ctx):
    ctx.set_line_width(12)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # Silang (X)
    ctx.move_to(-18, -18)
    ctx.line_to(18, 18)
    ctx.move_to(18, -18)
    ctx.line_to(-18, 18)
    ctx.stroke()

def draw_divide(ctx):
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    # Garis Tengah
    ctx.move_to(-22, 0)
    ctx.line_to(22, 0)
    ctx.stroke()
    
    # Titik Atas
    ctx.arc(0, -22, 6, 0, 2*math.pi)
    ctx.fill()
    # Titik Bawah
    ctx.arc(0, 22, 6, 0, 2*math.pi)
    ctx.fill()

# =====================================================
# 2. FUNGSI TOMBOL BASE (Gradien & Efek 3D)
# =====================================================

def draw_fancy_button(ctx, x, y, base_color, symbol_function):
    ctx.save()
    ctx.translate(x, y)

    # --- A. BAYANGAN BAWAH (DROP SHADOW) ---
    ctx.save()
    ctx.translate(0, 8) # Geser ke bawah
    ctx.scale(1, 0.9)   # Sedikit gepeng
    ctx.arc(0, 0, 55, 0, 2*math.pi)
    # Warna Hitam Transparan
    ctx.set_source_rgba(0, 0, 0, 0.3) 
    ctx.fill()
    ctx.restore()

    # --- B. BADAN TOMBOL (GRADIEN) ---
    # Membuat efek bola bulat
    # Cahaya datang dari kiri atas (-20, -20)
    gradient = cairo.RadialGradient(-20, -20, 5, 0, 0, 60)
    
    # Warna Highlight (Lebih terang dari warna dasar)
    r, g, b = base_color
    gradient.add_color_stop_rgb(0, min(1, r+0.3), min(1, g+0.3), min(1, b+0.3))
    # Warna Dasar
    gradient.add_color_stop_rgb(0.5, r, g, b)
    # Warna Bayangan (Lebih gelap)
    gradient.add_color_stop_rgb(1, r*0.6, g*0.6, b*0.6)
    
    ctx.arc(0, 0, 60, 0, 2*math.pi)
    ctx.set_source(gradient)
    ctx.fill()

    # --- C. RING PUTIH TIPIS (INNER GLOW) ---
    # Memberi kesan tajam di pinggir
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(3)
    ctx.arc(0, 0, 57, 0, 2*math.pi)
    ctx.stroke()

    # --- D. GAMBAR SIMBOL ---
    ctx.set_source_rgb(1, 1, 1) # Simbol Putih Bersih
    # Tambahkan sedikit bayangan pada simbol biar timbul
    ctx.save()
    ctx.translate(2, 2)
    ctx.set_source_rgba(0, 0, 0, 0.2)
    symbol_function(ctx) # Gambar bayangan simbol dulu
    ctx.restore()
    
    # Gambar simbol utama (Putih)
    ctx.set_source_rgb(1, 1, 1) 
    symbol_function(ctx)

    # --- E. KILAUAN KACA (GLOSS) ---
    # Oval putih transparan di bagian atas
    ctx.save()
    ctx.translate(0, -25)
    ctx.scale(1, 0.6) # Pipihkan jadi oval
    ctx.arc(0, 0, 45, 0, 2*math.pi)
    
    # Gradien Transparan (Putih -> Bening)
    grad_gloss = cairo.LinearGradient(0, -20, 0, 30)
    grad_gloss.add_color_stop_rgba(0, 1, 1, 1, 0.5) # Putih setengah transparan
    grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.0) # Bening
    
    ctx.set_source(grad_gloss)
    ctx.fill()
    ctx.restore()

    ctx.restore() # Selesai satu tombol

# =====================================================
# 3. FUNGSI UTAMA (Dipanggil Main)
# =====================================================

def gambar(ctx, width, height):
    # Background abu-abu sangat muda (Biar warna tombol pop-up)
    ctx.set_source_rgb(0.95, 0.95, 0.95) 
    ctx.paint()

    # Daftar Simbol & Warna Base-nya
    icons = [
        (draw_plus,   (0.9, 0.3, 0.3)), # Merah
        (draw_minus,  (0.9, 0.7, 0.2)), # Kuning/Oranye
        (draw_times,  (0.2, 0.6, 0.9)), # Biru
        (draw_divide, (0.3, 0.8, 0.4)), # Hijau
    ]

    # Logika posisi agar rapi di tengah (Responsif)
    # Kita bagi layar jadi 4 kolom imajiner
    total_icons = len(icons)
    spacing = width / (total_icons + 1)
    y_pos = height / 2

    for i, (func, color) in enumerate(icons):
        x_pos = spacing * (i + 1)
        draw_fancy_button(ctx, x_pos, y_pos, color, func)