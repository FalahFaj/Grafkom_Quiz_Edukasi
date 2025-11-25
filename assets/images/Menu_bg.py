import cairo
import math
import random

def draw_sunburst(ctx, w, h):
    """Efek sinar matahari berputar samar di latar belakang"""
    ctx.save()
    ctx.translate(w/2, h/2)
    ctx.set_source_rgba(1, 1, 1, 0.1) # Putih sangat transparan
    
    for i in range(0, 360, 15): # Setiap 15 derajat
        ctx.save()
        ctx.rotate(i * math.pi / 180)
        ctx.move_to(0, 0)
        ctx.line_to(w, -50) # Lebar sinar
        ctx.line_to(w, 50)
        ctx.close_path()
        ctx.fill()
        ctx.restore()
    ctx.restore()

def draw_wood_frame(ctx, w, h):
    """Bingkai Kayu dengan tekstur"""
    border = 35
    
    # Fungsi tekstur kayu internal
    def wood_texture(x, y, bw, bh, horizontal=True):
        ctx.save()
        # Warna Dasar Kayu
        ctx.rectangle(x, y, bw, bh)
        ctx.set_source_rgb(0.7, 0.45, 0.2) 
        ctx.fill()
        
        # Serat Kayu
        ctx.rectangle(x, y, bw, bh); ctx.clip()
        ctx.set_source_rgba(0.4, 0.2, 0.0, 0.3)
        ctx.set_line_width(2)
        
        limit = int(bw if horizontal else bh)
        step = 10
        random.seed(42) 
        
        for i in range(0, limit, step):
            if horizontal:
                ctx.move_to(x + i, y)
                mid_y = y + bh/2 + random.randint(-5, 5)
                ctx.curve_to(x + i + 20, mid_y, x + i - 20, mid_y, x + i, y + bh)
            else:
                ctx.move_to(x, y + i)
                mid_x = x + bw/2 + random.randint(-5, 5)
                ctx.curve_to(mid_x, y + i + 20, mid_x, y + i - 20, x + bw, y + i)
            ctx.stroke()
        ctx.restore()

    # Gambar 4 Sisi
    wood_texture(0, 0, w, border) # Atas
    wood_texture(0, h-border, w, border) # Bawah
    wood_texture(0, 0, border, h, False) # Kiri
    wood_texture(w-border, 0, border, h, False) # Kanan
    
    # Pojokan Dekoratif (Sudut Melengkung)
    ctx.set_source_rgb(0.6, 0.35, 0.1) # Kayu lebih gelap
    corner_size = 60
    
    corners = [
        (0, 0, 1, 1),      # Kiri Atas
        (w, 0, -1, 1),     # Kanan Atas
        (0, h, 1, -1),     # Kiri Bawah
        (w, h, -1, -1)     # Kanan Bawah
    ]
    
    for cx, cy, sx, sy in corners:
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(sx, sy)
        ctx.move_to(0, 0)
        ctx.line_to(corner_size, 0)
        ctx.curve_to(30, 10, 10, 30, 0, corner_size)
        ctx.close_path()
        ctx.fill()
        # Highlight pinggir
        ctx.set_source_rgba(1, 1, 1, 0.3); ctx.set_line_width(3)
        ctx.move_to(corner_size, 0); ctx.curve_to(30, 10, 10, 30, 0, corner_size); ctx.stroke()
        ctx.restore()

def draw_pattern_hill(ctx, x, y, w, h, color, pattern):
    ctx.save()
    ctx.translate(x, y)
    
    # Bentuk Bukit (Gunung Kecil)
    ctx.move_to(0, h)
    # Kurva bukit yang lebih 'gemuk' dan kartunis
    ctx.curve_to(w*0.2, -h*0.2, w*0.8, -h*0.2, w, h)
    ctx.close_path()
    
    # Clip untuk pola
    ctx.save(); ctx.clip()
    
    # Warna Dasar
    ctx.set_source_rgb(*color)
    ctx.paint()
    
    # Pola-pola
    ctx.set_source_rgba(1, 1, 1, 0.2) # Pola putih transparan
    
    if pattern == "STRIPE":
        ctx.set_line_width(15)
        # Garis miring
        for i in range(-100, int(w)+100, 30):
            ctx.move_to(i, -h); ctx.line_to(i-100, h*2); ctx.stroke()
            
    elif pattern == "STAR":
        for i in range(0, int(w), 35):
            for j in range(int(-h), int(h), 35):
                # Bintang 5 titik
                ctx.save(); ctx.translate(i, j); ctx.scale(0.5, 0.5)
                ctx.move_to(0, -15)
                for k in range(5):
                    ctx.rotate(math.pi*0.4); ctx.line_to(0, -15)
                    ctx.rotate(-math.pi*0.8); ctx.line_to(0, -7)
                ctx.fill(); ctx.restore()
                
    elif pattern == "DOT":
        for i in range(0, int(w), 25):
            for j in range(int(-h), int(h), 25):
                ctx.arc(i, j, 8, 0, 2*math.pi); ctx.fill()
                
    ctx.restore() # Lepas clip
    
    # Outline Putih Tebal
    ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()

def gambar(ctx, width, height):
    # Scaling Virtual 800x600
    ctx.scale(width / 800, height / 600)

    # 1. Langit Biru Cerah
    grad_sky = cairo.LinearGradient(0, 0, 0, 600)
    grad_sky.add_color_stop_rgb(0, 0.0, 0.6, 0.95) # Biru Langit Tua
    grad_sky.add_color_stop_rgb(1, 0.2, 0.7, 1.0)  # Biru Cerah
    ctx.set_source(grad_sky)
    ctx.paint()
    
    # 2. Efek Sunburst
    draw_sunburst(ctx, 800, 600)

    # 3. Bukit-Bukit (Layering dari belakang ke depan)
    # Ungu Garis (Kiri Bawah Belakang)
    draw_pattern_hill(ctx, -80, 500, 350, 250, (0.5, 0.3, 0.6), "STRIPE")
    
    # Ungu Bintang (Kanan Bawah Belakang)
    draw_pattern_hill(ctx, 580, 520, 300, 250, (0.5, 0.3, 0.6), "STAR")

    # Oranye Bintang (Kiri Depan)
    draw_pattern_hill(ctx, 80, 600, 250, 180, (1.0, 0.6, 0.2), "STAR")
    
    # Hijau Dot (Kanan Depan)
    draw_pattern_hill(ctx, 500, 620, 280, 200, (0.5, 0.7, 0.2), "DOT")
    
    # Kuning Polos (Tengah Bawah - Tempat Tombol)
    ctx.save()
    ctx.translate(180, 550)
    ctx.move_to(0, 200)
    ctx.curve_to(100, -50, 350, -50, 450, 200)
    ctx.set_source_rgb(0.9, 0.8, 0.1)
    ctx.fill()
    # Pola kotak samar di bukit kuning
    ctx.save(); ctx.clip()
    ctx.set_source_rgba(1, 1, 1, 0.15)
    for i in range(0, 450, 20):
        for j in range(-50, 200, 20):
            if (i//20 + j//20)%2==0: ctx.rectangle(i,j,20,20); ctx.fill()
    ctx.restore()
    ctx.set_source_rgb(1,1,1); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()

    # 4. Bingkai Kayu
    draw_wood_frame(ctx, 800, 600)