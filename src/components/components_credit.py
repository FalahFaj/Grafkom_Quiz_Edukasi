# src/components/components_credit.py
import cairo
import math
import random

def draw_starry_background(ctx, w, h, time=0):
    """Menggambar latar belakang luar angkasa dengan bintang berkelip."""
    # Gradien langit malam
    grad = cairo.LinearGradient(0, 0, 0, h)
    grad.add_color_stop_rgb(0, 0.05, 0.0, 0.1) # Ungu tua
    grad.add_color_stop_rgb(0.5, 0.1, 0.05, 0.2)
    grad.add_color_stop_rgb(1, 0.2, 0.1, 0.3)   # Biru gelap
    ctx.set_source(grad)
    ctx.paint()

    # Menggambar bintang-bintang
    random.seed(42) # Seed untuk posisi bintang yang konsisten
    for i in range(150): # Jumlah bintang
        x = random.uniform(0, w)
        y = random.uniform(0, h)
        
        # Bintang berkelip berdasarkan waktu
        alpha = 0.5 + (math.sin(time * 0.01 * random.uniform(0.5, 1.5) + i) * 0.5)
        radius = random.uniform(0.5, 2.0)
        
        # Glow effect
        glow_radius = radius * 4
        glow = cairo.RadialGradient(x, y, 0, x, y, glow_radius)
        glow.add_color_stop_rgba(0, 1, 1, 1, alpha * 0.7)
        glow.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(glow)
        ctx.arc(x, y, glow_radius, 0, 2 * math.pi)
        ctx.fill()
        
        # Bintang utama
        ctx.set_source_rgba(1, 1, 1, alpha)
        ctx.arc(x, y, radius, 0, 2 * math.pi)
        ctx.fill()

def draw_credit_title(ctx, w):
    """Menggambar judul 'Credits' dengan gaya yang sama seperti judul 'Pengaturan'."""
    ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(70)
    text = "Credits"
    ext = ctx.text_extents(text)
    
    x_pos = w / 2 - ext.width / 2
    y_pos = 120

    # Gambar bayangan (shadow)
    ctx.move_to(x_pos + 3, y_pos + 3)
    ctx.set_source_rgb(0.2, 0.1, 0.3) # Warna shadow ungu gelap agar sesuai tema
    ctx.show_text(text)

    # Gambar teks utama
    ctx.move_to(x_pos, y_pos)
    ctx.set_source_rgb(1, 1, 1) # Teks putih
    ctx.show_text(text)

def draw_scrolling_credits(ctx, w, h, scroll_y, credits):
    """Menggambar teks kredit yang bisa di-scroll."""
    ctx.save()
    ctx.rectangle(0, 180, w, h - 280)
    ctx.clip()

    ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    current_y = h - scroll_y

    for item in credits:
        role = item['role']
        name = item['name']

        # Gambar Role (e.g., "Game Director")
        ctx.set_font_size(28)
        ctx.set_source_rgb(0.5, 0.8, 1.0) # Biru neon
        role_ext = ctx.text_extents(role)
        ctx.move_to(w / 2 - role_ext.width / 2, current_y)
        ctx.show_text(role)
        current_y += 40

        # Gambar Name
        ctx.set_font_size(36)
        ctx.set_source_rgb(1, 1, 1)
        name_ext = ctx.text_extents(name)
        ctx.move_to(w / 2 - name_ext.width / 2, current_y)
        ctx.show_text(name)
        current_y += 70

    ctx.restore()


