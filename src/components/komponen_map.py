import cairo
import math
import random

# --- KONFIGURASI TEMA (PALET WARNA) ---
THEMES = {
    'easy': { # Siang Cerah
        'sky_top': (0.0, 0.5, 0.9, 1.0),    # Biru Langit
        'sky_bot': (0.6, 0.9, 1.0, 1.0),    # Putih Biru
        'sun_color': (1.0, 0.95, 0.6),      # Kuning
        'sun_pos': (0.1, 0.15),
        'cloud_tint': (1, 1, 1, 0.95),
        'hill_back': ((0.3, 0.55, 0.75), (0.6, 0.8, 0.9)),
        'hill_mid': ((0.2, 0.7, 0.3), (0.1, 0.5, 0.2)),
        'hill_front': ((0.4, 0.8, 0.2), (0.2, 0.6, 0.1)),
        'tree_trunk': (0.45, 0.3, 0.15),
        'tree_leaf_l': (0.1, 0.55, 0.2),
        'tree_leaf_d': (0.08, 0.45, 0.18),
        'path_edge': (0.55, 0.5, 0.45),
        'path_center': (0.92, 0.88, 0.7),
        'house': 'castle'
    },
    'medium': { # Sore Sunset (Vibrant)
        'sky_top': (0.25, 0.1, 0.4, 1.0),   # Ungu
        'sky_bot': (1.0, 0.6, 0.2, 1.0),    # Oranye Terang
        'sun_color': (1.0, 0.3, 0.1),       # Merah Oranye
        'sun_pos': (0.15, 0.35),            # Matahari lebih rendah
        'cloud_tint': (1.0, 0.9, 0.8, 0.8), # Awan kekuningan
        'hill_back': ((0.45, 0.3, 0.5), (0.3, 0.2, 0.4)), # Ungu kecoklatan
        'hill_mid': ((0.6, 0.4, 0.2), (0.4, 0.25, 0.1)),  # Oranye kecoklatan
        'hill_front': ((0.5, 0.6, 0.2), (0.3, 0.4, 0.1)), # Hijau zaitun
        'tree_trunk': (0.35, 0.2, 0.1),
        'tree_leaf_l': (0.3, 0.4, 0.1),     # Hijau kekuningan
        'tree_leaf_d': (0.2, 0.3, 0.05),
        'path_edge': (0.5, 0.4, 0.35),
        'path_center': (0.9, 0.8, 0.65),    # Pasir kemerahan
        'house': 'cottage'
    },
    'hard': { # Malam Gelap
        'sky_top': (0.02, 0.02, 0.1, 1.0),  # Hitam
        'sky_bot': (0.1, 0.1, 0.3, 1.0),    # Biru Malam
        'sun_color': (0.9, 0.9, 1.0),       # Bulan
        'sun_pos': (0.85, 0.15),
        'cloud_tint': (0.3, 0.3, 0.4, 0.4), # Awan gelap
        'hill_back': ((0.05, 0.05, 0.15), (0.1, 0.1, 0.2)),
        'hill_mid': ((0.1, 0.1, 0.2), (0.05, 0.05, 0.15)),
        'hill_front': ((0.15, 0.15, 0.25), (0.08, 0.08, 0.15)),
        'tree_trunk': (0.15, 0.1, 0.15),
        'tree_leaf_l': (0.1, 0.2, 0.25),    # Teal gelap
        'tree_leaf_d': (0.05, 0.1, 0.15),
        'path_edge': (0.25, 0.25, 0.3),
        'path_center': (0.4, 0.4, 0.45),    # Jalan batu abu-abu
        'house': 'haunted'
    }
}

# --- Helper Shapes ---

def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

# --- Assets ---

def draw_stars(ctx, w, h, time):
    """Bintang kelap-kelip (Hard)."""
    random.seed(42)
    for i in range(60):
        sx = random.randint(0, int(w))
        sy = random.randint(0, int(h * 0.7))
        alpha = (math.sin(time * 0.05 + i) + 1) / 2 * 0.8 + 0.2
        ctx.set_source_rgba(1, 1, 1, alpha)
        ctx.arc(sx, sy, random.uniform(1, 2.5), 0, 2*math.pi)
        ctx.fill()

def draw_cloud_puff(ctx, cx, cy, radius, tint):
    ctx.save()
    grad = cairo.RadialGradient(cx, cy, radius*0.2, cx, cy, radius)
    r, g, b, a = tint
    grad.add_color_stop_rgba(0, r, g, b, a)
    grad.add_color_stop_rgba(1, r, g, b, 0.0)
    ctx.set_source(grad); ctx.arc(cx, cy, radius, 0, 2*math.pi); ctx.fill()
    ctx.restore()

def draw_cloud(ctx, x, y, scale, time, speed_offset, difficulty):
    """Menggambar awan kartun yang lebih 'fluffy'."""
    t_conf = THEMES.get(difficulty, THEMES['easy'])
    tint = t_conf['cloud_tint']
    
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    
    # Gerakan awan halus kiri-kanan
    move_x = math.sin((time * 0.015) + speed_offset) * 40
    ctx.translate(move_x, 0)

    # Definisi bulatan-bulatan awan (x, y, radius)
    circles = [
        (0, 0, 30),       # Tengah
        (25, -5, 25),     # Kanan atas
        (45, 10, 20),     # Kanan bawah
        (-25, 5, 22),     # Kiri tengah
        (-45, 15, 18),    # Kiri bawah
        (15, 15, 25)      # Bawah tengah
    ]

    # Agar transparan tidak tumpang tindih (overlap), kita gunakan Group
    ctx.push_group()
    
    # Gambar bentuk awan (Putih solid dulu)
    for cx, cy, r in circles:
        ctx.arc(cx, cy, r, 0, 2*math.pi)
        ctx.fill()
    
    # Isi dengan gradien (Putih di atas, sedikit gelap di bawah untuk volume)
    ctx.set_operator(cairo.OPERATOR_SOURCE) # Timpa warna yang ada
    ctx.set_source_rgba(1, 1, 1, 1) # Reset source
    
    # Terapkan gradien pada bentuk yang sudah digambar
    # Kita gunakan preserve untuk fill ulang
    # Sederhananya: Gambar ulang circle dengan gradien
    grad = cairo.LinearGradient(0, -40, 0, 40)
    grad.add_color_stop_rgba(0, 1, 1, 1, 1) # Putih bersih di atas
    # Bagian bawah sedikit gelap sesuai tint
    r_tint, g_tint, b_tint = tint[:3]
    grad.add_color_stop_rgba(1, r_tint*0.9, g_tint*0.9, b_tint*0.9, 1) 
    
    ctx.set_source(grad)
    for cx, cy, r in circles:
        ctx.arc(cx, cy, r, 0, 2*math.pi)
        ctx.fill()
        
    ctx.pop_group_to_source()
    # Gambar group ke layar dengan alpha keseluruhan dari tint
    ctx.paint_with_alpha(tint[3])
    
    ctx.restore()

def draw_sky_background(ctx, w, h, time, difficulty="easy"):
    t_conf = THEMES.get(difficulty, THEMES['easy'])
    
    # 1. Langit
    grad = cairo.LinearGradient(0, 0, 0, h)
    grad.add_color_stop_rgba(0, *t_conf['sky_top'])
    if difficulty == 'medium': # Tambah warna tengah untuk sunset
        grad.add_color_stop_rgba(0.5, 0.8, 0.4, 0.3, 1.0) # Pinkish
    grad.add_color_stop_rgba(1, *t_conf['sky_bot'])
    ctx.set_source(grad); ctx.paint()

    # 2. Bintang (Jika Hard)
    if difficulty == 'hard': draw_stars(ctx, w, h, time)

    # 3. Matahari / Bulan
    ctx.save()
    pos_x, pos_y = t_conf['sun_pos']
    ctx.translate(w * pos_x, h * pos_y)
    
    # Glow
    glow = cairo.RadialGradient(0, 0, 10, 0, 0, 80)
    sc = t_conf['sun_color']
    glow.add_color_stop_rgba(0, sc[0], sc[1], sc[2], 0.6)
    glow.add_color_stop_rgba(1, sc[0], sc[1], sc[2], 0.0)
    ctx.set_source(glow); ctx.arc(0, 0, 80, 0, 2*math.pi); ctx.fill()
    
    # Body
    ctx.set_source_rgb(*sc); ctx.arc(0, 0, 40 if difficulty=='hard' else 45, 0, 2*math.pi); ctx.fill()
    
    # Kawah Bulan
    if difficulty == 'hard':
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.4)
        ctx.arc(-10, -5, 8, 0, 2*math.pi); ctx.fill()
        ctx.arc(15, 10, 6, 0, 2*math.pi); ctx.fill()
    ctx.restore()

    # 4. Awan
    if difficulty == 'hard':
        draw_cloud(ctx, w*0.5, h*0.2, 1.0, time, 0, difficulty)
    else:
        draw_cloud(ctx, w*0.25, h*0.2, 1.2, time, 0, difficulty)
        draw_cloud(ctx, w*0.75, h*0.15, 0.9, time, 2, difficulty)

def draw_hill_layer(ctx, w, h, y_start, wave_height, colors, offset_x=0):
    ctx.save()
    grad = cairo.LinearGradient(0, y_start, 0, h)
    grad.add_color_stop_rgb(0, *colors[0]); grad.add_color_stop_rgb(1, *colors[1])
    ctx.set_source(grad)
    ctx.move_to(0, h); ctx.line_to(0, y_start)
    steps = 30; step_w = w / steps
    for i in range(steps + 2):
        x = i * step_w
        y = y_start + math.sin((x+offset_x)*0.008)*wave_height + math.sin((x+offset_x)*0.003)*(wave_height*1.5)
        ctx.line_to(x, y)
    ctx.line_to(w, h); ctx.close_path(); ctx.fill(); ctx.restore()

def draw_tree(ctx, x, y, scale, difficulty):
    t_conf = THEMES.get(difficulty, THEMES['easy'])
    ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale)
    
    # Batang
    ctx.set_source_rgb(*t_conf['tree_trunk']); ctx.rectangle(-6, -25, 12, 25); ctx.fill()
    
    # Daun Segitiga
    leafs = [(0, -50, 35, 35), (0, -70, 30, 30), (0, -90, 22, 25)]
    for px, py, pw, ph in leafs:
        yb = py + ph
        # Kiri Terang
        ctx.set_source_rgb(*t_conf['tree_leaf_l']); ctx.move_to(px, py); ctx.line_to(px-pw, yb); ctx.line_to(px, yb); ctx.fill()
        # Kanan Gelap
        ctx.set_source_rgb(*t_conf['tree_leaf_d']); ctx.move_to(px, py); ctx.line_to(px+pw, yb); ctx.line_to(px, yb); ctx.fill()
    ctx.restore()

def draw_foreground_scenery(ctx, w, h, time, difficulty="easy"):
    t_conf = THEMES.get(difficulty, THEMES['easy'])
    draw_hill_layer(ctx, w, h, h*0.42, 35, t_conf['hill_back'], offset_x=100)
    draw_hill_layer(ctx, w, h, h*0.58, 45, t_conf['hill_mid'], offset_x=350)
    
    random.seed(42)
    for i in range(18):
        tx = random.randint(50, int(w)-50)
        hill_y = h*0.58 + math.sin((tx+350)*0.008)*45 + math.sin((tx+350)*0.003)*67.5
        ty = hill_y + random.randint(-20, 50)
        s = random.uniform(0.7, 1.1)
        draw_tree(ctx, tx, ty, s, difficulty)
        
    draw_hill_layer(ctx, w, h, h*0.78, 55, t_conf['hill_front'], offset_x=0)


# --- RUMAH & BANGUNAN ---

def draw_castle(ctx, x, y):
    """Istana (Easy) - Tampilan Lebih Bagus & Detail."""
    ctx.save()
    ctx.translate(x, y - 20)  # Adjust position slightly up
    ctx.scale(1.2, 1.2)       # Make it slightly larger

    # --- Palet Warna ---
    wall_color_light = (0.9, 0.9, 0.95)   # Putih kebiruan
    wall_color_dark = (0.7, 0.7, 0.75)    # Bayangan dinding
    roof_color_light = (0.4, 0.6, 1.0)    # Biru cerah
    roof_color_dark = (0.2, 0.3, 0.6)     # Biru gelap
    door_color = (0.4, 0.25, 0.1)         # Coklat kayu

    # --- Helper: Menara ---
    def draw_tower(tx, ty, w, h, roof_h):
        # 1. Dinding (Gradien Horizontal untuk efek silinder)
        ctx.save()
        grad_wall = cairo.LinearGradient(tx - w/2, 0, tx + w/2, 0)
        grad_wall.add_color_stop_rgb(0, *wall_color_dark)
        grad_wall.add_color_stop_rgb(0.4, *wall_color_light)
        grad_wall.add_color_stop_rgb(1, *wall_color_dark)
        
        ctx.rectangle(tx - w/2, ty - h, w, h)
        ctx.set_source(grad_wall)
        ctx.fill()
        
        # Detail Bata (Sedikit garis-garis tipis)
        ctx.set_source_rgba(0, 0, 0, 0.1)
        ctx.set_line_width(1)
        for i in range(1, 5):
            line_y = ty - h + (h/5) * i
            if i % 2 == 0:
                ctx.move_to(tx - w/2 + 5, line_y); ctx.line_to(tx + w/2 - 5, line_y)
            else:
                ctx.move_to(tx - w/2 + 10, line_y); ctx.line_to(tx + w/2 - 10, line_y)
            ctx.stroke()
        ctx.restore()

        # 2. Atap Kerucut
        ctx.save()
        ctx.move_to(tx - w/2 - 5, ty - h)       # Kiri bawah atap
        ctx.line_to(tx + w/2 + 5, ty - h)       # Kanan bawah atap
        ctx.line_to(tx, ty - h - roof_h)        # Puncak
        ctx.close_path()
        
        grad_roof = cairo.LinearGradient(tx - w/2, ty - h, tx + w/2, ty - h)
        grad_roof.add_color_stop_rgb(0, *roof_color_dark)
        grad_roof.add_color_stop_rgb(0.5, *roof_color_light)
        grad_roof.add_color_stop_rgb(1, *roof_color_dark)
        ctx.set_source(grad_roof)
        ctx.fill()
        ctx.restore()

        # 3. Jendela Kecil
        ctx.set_source_rgb(0.2, 0.2, 0.3)
        ctx.arc(tx, ty - h/2 - 5, 4, 0, 2*math.pi)
        ctx.fill()
        rounded_rect(ctx, tx - 3, ty - h/2 - 5, 6, 12, 2)
        ctx.fill()

    # --- Gambar Menara ---
    # Menara Kiri & Kanan (Belakang)
    draw_tower(-50, 0, 30, 60, 40)
    draw_tower(50, 0, 30, 60, 40)

    # Bangunan Tengah (Utama)
    ctx.save()
    # Dinding Tengah
    grad_main = cairo.LinearGradient(-35, 0, 35, 0)
    grad_main.add_color_stop_rgb(0, *wall_color_dark)
    grad_main.add_color_stop_rgb(0.5, *wall_color_light)
    grad_main.add_color_stop_rgb(1, *wall_color_dark)
    
    ctx.rectangle(-40, -50, 80, 50) # Kotak dasar
    ctx.set_source(grad_main)
    ctx.fill()
    
    # Gerbang Besar
    ctx.save()
    ctx.translate(0, 0)
    # Frame Pintu (Batu)
    ctx.set_source_rgb(0.5, 0.5, 0.55)
    ctx.arc(0, 0, 24, math.pi, 0) # Lengkungan
    ctx.stroke() # Hanya garis luar
    
    # Pintu Kayu
    ctx.new_path()
    ctx.arc(0, 0, 20, math.pi, 0)
    ctx.set_source_rgb(*door_color)
    ctx.fill()
    
    # Detail Pintu (Garis vertikal kayu)
    ctx.set_source_rgba(0,0,0,0.3)
    ctx.set_line_width(2)
    ctx.move_to(0, -20); ctx.line_to(0, 0); ctx.stroke()
    ctx.restore()
    ctx.restore()

    # Menara Tengah Tinggi (Di atas bangunan tengah)
    draw_tower(0, -50, 40, 50, 50)

    # --- Bendera di Puncak ---
    ctx.save()
    ctx.translate(0, -100) # Di puncak menara tengah
    
    # Tiang
    ctx.set_source_rgb(0.3, 0.3, 0.3)
    ctx.set_line_width(2)
    ctx.move_to(0, 0); ctx.line_to(0, -25); ctx.stroke()
    
    # Kain Bendera (Merah)
    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.move_to(0, -25)
    ctx.curve_to(10, -30, 20, -20, 30, -25) # Atas bergelombang
    ctx.line_to(30, -10)
    ctx.curve_to(20, -5, 10, -15, 0, -10)   # Bawah bergelombang
    ctx.close_path()
    ctx.fill()
    ctx.restore()

    ctx.restore()

def draw_cottage(ctx, x, y): 
    """Rumah Villa Kartun (Medium) - POSISI PINTU DIPERBAIKI."""
    ctx.save()
    
    # PERBAIKAN UTAMA DI SINI:
    # x - 35: Geser rumah ke kiri, karena pintu digambar di koordinat x=35. 
    #         Ini membuat pintu pas di tengah jalan (x=0 relatif terhadap jalan).
    # y - 15: Geser rumah sedikit ke atas agar jalan terlihat 'masuk' ke ambang pintu.
    ctx.translate(x - 38, y - 25) 
    
    ctx.scale(1.3, 1.3)

    # Warna Custom Villa
    c_wall_light = (0.95, 0.9, 0.8)
    c_wall_dark = (0.85, 0.8, 0.7)
    c_roof_light = (0.6, 0.3, 0.2)
    c_roof_dark = (0.4, 0.2, 0.1)
    
    # Bangunan Utama (Kanan)
    # Gradasi Dinding
    grad_wall = cairo.LinearGradient(0, -60, 0, 0)
    grad_wall.add_color_stop_rgb(0, *c_wall_light)
    grad_wall.add_color_stop_rgb(1, *c_wall_dark)
    rounded_rect(ctx, 0, -60, 70, 60, 2)
    ctx.set_source(grad_wall); ctx.fill()

    # Bangunan Samping (Kiri - Lebih gelap dikit)
    ctx.set_source_rgb(*c_wall_dark)
    rounded_rect(ctx, -50, -40, 50, 40, 2); ctx.fill()

    # Fungsi Atap Kartun (Agak melengkung)
    def draw_cartoon_roof(cx, cy, w, h):
        ctx.save()
        grad_roof = cairo.LinearGradient(cx, cy-h, cx, cy)
        grad_roof.add_color_stop_rgb(0, *c_roof_light)
        grad_roof.add_color_stop_rgb(1, *c_roof_dark)
        ctx.set_source(grad_roof)
        # Segitiga dengan sisi agak cembung
        ctx.move_to(cx - w/2 - 5, cy)
        ctx.curve_to(cx - w/4, cy - h*0.5, cx, cy - h - 5, cx, cy - h)
        ctx.curve_to(cx, cy - h - 5, cx + w/4, cy - h*0.5, cx + w/2 + 5, cy)
        ctx.close_path()
        ctx.fill()
        # Garis bawah atap
        ctx.set_source_rgb(0.3, 0.15, 0.1)
        ctx.set_line_width(3)
        ctx.move_to(cx - w/2 - 5, cy); ctx.line_to(cx + w/2 + 5, cy); ctx.stroke()
        ctx.restore()

    # Gambar Atap
    draw_cartoon_roof(35, -60, 80, 40) # Atap Kanan
    draw_cartoon_roof(-25, -40, 60, 30) # Atap Kiri

    # Cerobong Asap
    ctx.set_source_rgb(0.5, 0.2, 0.1); ctx.rectangle(50, -85, 12, 25); ctx.fill()
    ctx.set_source_rgb(0.9, 0.9, 0.95); ctx.rectangle(48, -87, 16, 5); ctx.fill() # Topi cerobong

    # Asap Bulat-bulat
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.arc(56, -95, 5, 0, 2*math.pi); ctx.fill()
    ctx.arc(62, -102, 7, 0, 2*math.pi); ctx.fill()

    # Jendela Glossy (Kuning Terang)
    ctx.set_source_rgb(1.0, 0.9, 0.3)
    rounded_rect(ctx, 15, -50, 15, 15, 2); ctx.fill()
    rounded_rect(ctx, 40, -50, 15, 15, 2); ctx.fill()
    rounded_rect(ctx, -35, -30, 15, 15, 2); ctx.fill()
    
    # Frame Jendela
    ctx.set_source_rgb(0.4, 0.25, 0.15); ctx.set_line_width(2)
    ctx.rectangle(15, -50, 15, 15); ctx.stroke()
    ctx.rectangle(40, -50, 15, 15); ctx.stroke()
    ctx.rectangle(-35, -30, 15, 15); ctx.stroke()

    # Pintu Bulat (Pusatnya ada di x=35, y=-15)
    ctx.set_source_rgb(0.4, 0.2, 0.1)
    ctx.arc(35, -15, 12, math.pi, 0); ctx.fill() # Atas pintu
    ctx.rectangle(23, -15, 24, 15); ctx.fill()   # Bawah pintu
    
    # Gagang Pintu
    ctx.set_source_rgb(1, 0.8, 0.2); ctx.arc(42, -10, 2, 0, 2*math.pi); ctx.fill() 

    ctx.restore()
    
def draw_haunted_house(ctx, x, y):
    """Rumah Hantu (Hard) - Mansion Gothic yang lebih detail."""
    ctx.save()
    ctx.translate(x, y + 5)
    ctx.scale(1.4, 1.4)

    # Warna Tema Gelap
    c = {
        'wall': (0.2, 0.2, 0.25),       # Abu-abu kebiruan mati
        'wall_dark': (0.15, 0.15, 0.2), # Sisi gelap
        'roof': (0.08, 0.08, 0.12),     # Hitam pekat
        'glow': (1.0, 0.2, 0.1),        # Merah menyala (Mata/Jendela)
        'door': (0.1, 0.08, 0.05),          # Kayu busuk
        'detail': (0.05, 0.05, 0.08)    # Hitam (Pagar/Besi)
    }

    # Efek Miring (Agar terlihat tua/seram)
    ctx.save()
    ctx.rotate(0.05)

    # --- Bangunan Utama ---
    # Menara Utama (Tengah)
    ctx.set_source_rgb(*c['wall'])
    ctx.rectangle(-20, -70, 40, 70); ctx.fill()
    
    # Menara Samping (Kiri - Lebih Pendek)
    ctx.set_source_rgb(*c['wall_dark'])
    ctx.rectangle(-55, -50, 35, 50); ctx.fill()
    
    # Menara Samping (Kanan - Kurus)
    ctx.rectangle(20, -60, 20, 60); ctx.fill()

    # --- Atap Runcing (Gothic) ---
    ctx.set_source_rgb(*c['roof'])
    
    # Atap Utama (Melengkung Runcing)
    ctx.move_to(-25, -70)
    ctx.curve_to(-10, -110, 10, -110, 25, -70)
    ctx.close_path(); ctx.fill()
    # Puncak Menara Utama
    ctx.move_to(-2, -110); ctx.line_to(0, -135); ctx.line_to(2, -110); ctx.fill()

    # Atap Kiri
    ctx.move_to(-60, -50); ctx.line_to(-37, -90); ctx.line_to(-20, -50); ctx.fill()
    
    # Atap Kanan
    ctx.move_to(15, -60); ctx.line_to(30, -95); ctx.line_to(45, -60); ctx.fill()

    # --- Jendela Menyala (Seperti Wajah) ---
    ctx.set_source_rgba(*c['glow'], 0.9)
    
    # Jendela Utama (Bulat besar di atas)
    ctx.arc(0, -55, 6, 0, 2*math.pi); ctx.fill()
    
    # Jendela Bawah (Dua mata marah)
    # Kiri
    ctx.move_to(-12, -30); ctx.line_to(-4, -30); ctx.line_to(-12, -22); ctx.fill()
    # Kanan
    ctx.move_to(12, -30); ctx.line_to(4, -30); ctx.line_to(12, -22); ctx.fill()

    # Jendela Menara Samping (Sempit panjang)
    rounded_rect(ctx, -45, -35, 6, 15, 2); ctx.fill()
    rounded_rect(ctx, 27, -40, 6, 12, 2); ctx.fill()

    # --- Pintu Gerbang (Besi Berkarat) ---
    ctx.set_source_rgb(*c['door'])
    ctx.arc(0, 0, 12, math.pi, 0); ctx.fill()
    
    # Jeruji Besi
    ctx.set_source_rgb(*c['detail']); ctx.set_line_width(1.5)
    for i in range(-8, 9, 4):
        ctx.move_to(i, -10); ctx.line_to(i, 0); ctx.stroke()

    # --- Detail Tambahan (Balkon/Kayu) ---
    ctx.set_line_width(2); ctx.set_source_rgb(0.1, 0.1, 0.15)
    ctx.move_to(-55, -20); ctx.line_to(-20, -20); ctx.stroke() # Garis menara kiri
    ctx.move_to(20, -30); ctx.line_to(40, -30); ctx.stroke()   # Garis menara kanan

    ctx.restore() # Selesai rotasi gedung

    # --- Lingkungan Sekitar ---
    
    # Pohon Mati / Ranting Kering (Kiri)
    ctx.set_source_rgb(0.1, 0.05, 0.05); ctx.set_line_width(2)
    ctx.save(); ctx.translate(-65, 0)
    ctx.move_to(0, 0); ctx.curve_to(-5, -15, 5, -20, -2, -35); ctx.stroke() # Batang utama
    ctx.move_to(-2, -15); ctx.line_to(-10, -25); ctx.stroke() # Cabang
    ctx.move_to(0, -20); ctx.line_to(8, -28); ctx.stroke()    # Cabang
    ctx.restore()

    # Batu Nisan Miring (Kanan)
    ctx.save(); ctx.translate(55, 5); ctx.rotate(0.2)
    ctx.set_source_rgb(0.3, 0.3, 0.35)
    rounded_rect(ctx, -8, -15, 16, 15, 4); ctx.fill() # Batu
    ctx.set_source_rgba(0,0,0,0.5); ctx.set_line_width(2)
    ctx.move_to(0, -10); ctx.line_to(0, -2); ctx.stroke() # Salib vertikal
    ctx.move_to(-3, -7); ctx.line_to(3, -7); ctx.stroke() # Salib horizontal
    ctx.restore()

    # Kelelawar Kecil (Siluet di atas)
    ctx.set_source_rgb(0, 0, 0)
    def draw_bat(bx, by, s):
        ctx.save(); ctx.translate(bx, by); ctx.scale(s, s)
        ctx.move_to(0, 0)
        ctx.curve_to(5, -5, 10, 0, 15, -2) # Sayap kanan
        ctx.line_to(0, 5)                  # Badan bawah
        ctx.line_to(-15, -2)               # Sayap kiri
        ctx.curve_to(-10, 0, -5, -5, 0, 0)
        ctx.fill(); ctx.restore()
    
    draw_bat(30, -110, 0.6)
    draw_bat(-40, -120, 0.4)

    ctx.restore()

# --- FUNGSI UTAMA: JALAN & NODE ---

def get_bezier_points(points, segments=20):
    """Smoothing jalan."""
    spline = []
    if len(points) < 2: return points
    for i in range(len(points) - 1):
        p0, p1 = points[i], points[i+1]
        dx, dy = p1[0]-p0[0], p1[1]-p0[1]
        cx1, cy1 = p0[0]+dx*0.5, p0[1]+dy*0.1; cx2, cy2 = p1[0]-dx*0.5, p1[1]-dy*0.1
        for j in range(segments):
            t = j/segments
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*cx1 + 3*(1-t)*t**2*cx2 + t**3*p1[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*cy1 + 3*(1-t)*t**2*cy2 + t**3*p1[1]
            spline.append((x,y))
    spline.append(points[-1])
    return spline

def draw_3d_winding_path(ctx, levels, time, difficulty="easy"):
    if not levels: return
    t_conf = THEMES.get(difficulty, THEMES['easy'])
    path_points = get_bezier_points([l['pos'] for l in levels], segments=40)
    
    ctx.save()
    # Bayangan
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(55); ctx.set_source_rgba(0,0,0,0.3)
    ctx.move_to(*path_points[0]); 
    for p in path_points[1:]: ctx.line_to(*p); 
    ctx.stroke()
    # Pinggir
    ctx.set_line_width(48); ctx.set_source_rgb(*t_conf['path_edge'])
    ctx.move_to(*path_points[0]); 
    for p in path_points[1:]: ctx.line_to(*p); 
    ctx.stroke()
    # Tengah
    ctx.set_line_width(38); ctx.set_source_rgb(*t_conf['path_center'])
    ctx.move_to(*path_points[0]); 
    for p in path_points[1:]: ctx.line_to(*p); 
    ctx.stroke()
    # Garis Putus
    ctx.set_line_width(4); ctx.set_dash([8, 12]); ctx.set_source_rgba(0,0,0,0.2)
    ctx.move_to(*path_points[0]); 
    for p in path_points[1:]: ctx.line_to(*p); 
    ctx.stroke()
    ctx.restore()

    # RUMAH DI UJUNG
    if path_points:
        last = path_points[-1]
        ht = t_conf['house']
        if ht == 'cottage': draw_cottage(ctx, last[0], last[1])
        elif ht == 'haunted': draw_haunted_house(ctx, last[0], last[1])
        else: draw_castle(ctx, last[0], last[1])

def draw_crystal_level_node(ctx, x, y, level_id, state, is_hovered, time, difficulty="easy"):
    ctx.save(); ctx.translate(x, y)
    ctx.translate(0, math.sin(time * 0.05 + level_id * 0.5) * 5)
    ctx.scale(1.2 if is_hovered else 1.0, 1.2 if is_hovered else 1.0)

    # Warna Node sesuai tema
    if state == 'locked':
        fill = (0.5, 0.5, 0.5); border = (0.3, 0.3, 0.3)
    elif state == 'current':
        fill = (1.0, 0.9, 0.2); border = (0.8, 0.6, 0.0)
    else:
        if difficulty == 'medium': fill, border = (0.9, 0.5, 0.2), (0.6, 0.3, 0.1) # Oranye
        elif difficulty == 'hard': fill, border = (0.5, 0.2, 0.7), (0.3, 0.1, 0.5) # Ungu
        else: fill, border = (0.3, 0.8, 0.4), (0.1, 0.5, 0.2) # Hijau

    # Bayangan & Badan
    ctx.set_source_rgba(0,0,0,0.3); ctx.arc(0, 5, 23, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgb(*fill); ctx.arc(0, 0, 25, 0, 2*math.pi); ctx.fill()
    ctx.set_line_width(4); ctx.set_source_rgb(*border); ctx.stroke()
    ctx.set_source_rgba(1,1,1,0.4); ctx.arc(-8, -8, 6, 0, 2*math.pi); ctx.fill()

    # Isi Node
    if state == 'locked':
        ctx.set_source_rgba(0.2,0.2,0.2,0.6); rounded_rect(ctx, -8, -6, 16, 14, 2); ctx.fill()
        ctx.set_line_width(3); ctx.move_to(-7,-6); ctx.line_to(-7,-12); ctx.arc(0,-12,7,math.pi,0); ctx.line_to(7,-6); ctx.stroke()
    else:
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(24); t=str(level_id); ext=ctx.text_extents(t)
        ctx.set_source_rgba(0,0,0,0.5); ctx.move_to(-ext.width/2+2, -ext.height/2-ext.y_bearing+2); ctx.show_text(t)
        ctx.set_source_rgb(1,1,1); ctx.move_to(-ext.width/2, -ext.height/2-ext.y_bearing); ctx.show_text(t)
    ctx.restore()

def draw_ui_button(ctx, x, y, w, h, text, color="GREEN", state="normal", font_size=40):
    """Tombol Game Mewah dengan status hover dan press"""
    ctx.save()
    
    # Penyesuaian offset untuk efek ditekan
    press_offset = 2 if state == "pressed" else 0
    ctx.translate(x, y + press_offset)

    # Tentukan palet warna dasar
    if color == "GREEN":
            top, mid, bot = (0.5, 0.8, 0.1), (0.3, 0.6, 0.0), (0.2, 0.4, 0.0)
            txt_col = (0.1, 0.3, 0.0)
            txt_shadow_col = (1, 1, 0.7)
    elif color == "BLUE":
            top, mid, bot = (0.2, 0.3, 0.7), (0.1, 0.2, 0.5), (0.0, 0.1, 0.3)
            txt_col = (0.8, 0.9, 1.0) # Reverted to original
            txt_shadow_col = (0.1, 0.1, 0.2)
    elif color == "PURPLE":
            top, mid, bot = (0.4, 0.2, 0.6), (0.3, 0.1, 0.5), (0.2, 0.0, 0.3)
            txt_col = (1.0, 0.9, 1.0) # Light lavender
            txt_shadow_col = (0.2, 0.0, 0.3)
    else:  # ORANGE
            top, mid, bot = (1.0, 0.8, 0.0), (1.0, 0.6, 0.0), (0.8, 0.4, 0.0)
            txt_col = (0.6, 0.2, 0.0)
            txt_shadow_col = (1, 1, 0.7)
            
    # Penyesuaian warna dan ukuran font berdasarkan state
    if state == "hover":
        # Jadikan warna lebih cerah saat hover
        top = tuple(min(1.0, c + 0.15) for c in top)
        mid = tuple(min(1.0, c + 0.15) for c in mid)
        font_size *= 1.05 # Sedikit perbesar font
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