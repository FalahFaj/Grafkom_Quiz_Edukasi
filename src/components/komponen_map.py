import cairo
import math

# Fungsi helper dari components_menu.py, agar monster bisa digambar
def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

def draw_cartoon_cloud(ctx, x, y, scale, time=0):
    """Menggambar awan kartun dengan animasi halus."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    
    # Animasi awan bergerak perlahan
    cloud_move = math.sin(time * 0.01) * 5
    
    # Warna dasar awan
    ctx.set_source_rgb(1, 1, 1)
    
    # Menggambar beberapa lingkaran yang tumpang tindih
    ctx.arc(0 + cloud_move, 0, 30, 0, 2 * math.pi)
    ctx.fill()
    ctx.arc(-25 + cloud_move, 15, 25, 0, 2 * math.pi)
    ctx.fill()
    ctx.arc(25 + cloud_move, 10, 35, 0, 2 * math.pi)
    ctx.fill()
    ctx.arc(0 + cloud_move, 20, 20, 0, 2 * math.pi)
    ctx.fill()
    
    # Bayangan lembut di bawah
    ctx.set_source_rgba(0.8, 0.85, 0.9, 0.7)
    ctx.arc(0 + cloud_move, 5, 30, 0, 2*math.pi)
    ctx.arc(-25 + cloud_move, 20, 25, 0, 2*math.pi)
    ctx.arc(25 + cloud_move, 15, 35, 0, 2*math.pi)
    ctx.fill()

    ctx.restore()

def draw_map_monster(ctx, x, y, time=0):
    """Menggambar monster ungu dari menu, disesuaikan untuk peta."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(0.8, 0.8)

    # Goyangan lembut dengan animasi lebih hidup
    rotation_angle = math.sin(time * 0.03) * 0.15
    bounce_y = math.sin(time * 0.05) * 3
    ctx.rotate(rotation_angle)
    ctx.translate(0, bounce_y)
    
    # Badan dengan efek 3D
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    ctx.set_source_rgb(1,1,1); ctx.set_line_width(8); ctx.stroke()
    
    # Gradien badan dengan highlight
    grad_p = cairo.RadialGradient(-10, -20, 0, -10, -20, 50)
    grad_p.add_color_stop_rgb(0, 0.9, 0.5, 1.0)  # Highlight
    grad_p.add_color_stop_rgb(0.7, 0.8, 0.4, 0.9)  # Main color
    grad_p.add_color_stop_rgb(1, 0.5, 0.1, 0.7)   # Shadow
    
    rounded_rect(ctx, -35, -35, 70, 65, 15)
    ctx.set_source(grad_p); ctx.fill()
    
    # Mata dengan animasi berkedip
    eye_offset_x = math.sin(time * 0.05 + math.pi) * 3
    blink = abs(math.sin(time * 0.1)) > 0.7  # Kedip acak
    
    if not blink:
        ctx.translate(-15 + eye_offset_x, -10)
        # Mata putih dengan gradien
        grad_eye = cairo.RadialGradient(-3, -3, 0, 0, 0, 14)
        grad_eye.add_color_stop_rgb(0, 1, 1, 1)
        grad_eye.add_color_stop_rgb(1, 0.9, 0.9, 1)
        ctx.set_source(grad_eye); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
        
        # Pupil dengan gradien
        grad_pupil = cairo.RadialGradient(1, 1, 0, 2, 2, 4)
        grad_pupil.add_color_stop_rgb(0, 0, 0, 0)
        grad_pupil.add_color_stop_rgb(1, 0.2, 0.2, 0.3)
        ctx.set_source(grad_pupil); ctx.arc(2,2, 4, 0, 2*math.pi); ctx.fill()
        
        # Highlight mata
        ctx.set_source_rgba(1, 1, 1, 0.8); ctx.arc(0, -2, 2, 0, 2*math.pi); ctx.fill()
    
    ctx.restore()
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(0.8, 0.8)
    ctx.rotate(rotation_angle)
    ctx.translate(0, bounce_y)
    
    if not blink:
        ctx.translate(30, -10)
        # Mata kanan
        grad_eye = cairo.RadialGradient(-3, -3, 0, 0, 0, 14)
        grad_eye.add_color_stop_rgb(0, 1, 1, 1)
        grad_eye.add_color_stop_rgb(1, 0.9, 0.9, 1)
        ctx.set_source(grad_eye); ctx.arc(0,0, 14, 0, 2*math.pi); ctx.fill()
        
        grad_pupil = cairo.RadialGradient(-1, 1, 0, -2, 2, 4)
        grad_pupil.add_color_stop_rgb(0, 0, 0, 0)
        grad_pupil.add_color_stop_rgb(1, 0.2, 0.2, 0.3)
        ctx.set_source(grad_pupil); ctx.arc(-2,2, 4, 0, 2*math.pi); ctx.fill()
        
        ctx.set_source_rgba(1, 1, 1, 0.8); ctx.arc(-1, -2, 2, 0, 2*math.pi); ctx.fill()
    
    ctx.restore()

def draw_floating_islands(ctx, w, h, time=0):
    """Menggambar pulau-pulau mengambang di langit dengan efek 3D."""
    ctx.save()
    
    # Pulau besar kiri dengan efek kedalaman
    island_y_offset = math.sin(time * 0.02) * 3
    
    # Bayangan pulau (lebih gelap dan besar untuk efek 3D)
    ctx.set_source_rgba(0.2, 0.3, 0.1, 0.6)
    ctx.arc(w * 0.2 + 8, h * 0.25 + island_y_offset + 15, 85, 0, 2 * math.pi)
    ctx.fill()
    
    # Badan pulau dengan gradien
    grad_island = cairo.RadialGradient(w * 0.2 - 20, h * 0.25 - 20, 0, w * 0.2, h * 0.25, 80)
    grad_island.add_color_stop_rgb(0, 0.5, 0.8, 0.4)  # Highlight
    grad_island.add_color_stop_rgb(0.7, 0.4, 0.7, 0.3)  # Main
    grad_island.add_color_stop_rgb(1, 0.3, 0.5, 0.2)   # Shadow
    
    ctx.set_source(grad_island)
    ctx.arc(w * 0.2, h * 0.25 + island_y_offset, 80, 0, 2 * math.pi)
    ctx.fill()
    
    # Detail pepohonan di pulau
    ctx.set_source_rgb(0.3, 0.4, 0.2)
    for i in range(3):
        tree_x = w * 0.2 - 20 + i * 20
        tree_y = h * 0.25 + island_y_offset - 30
        ctx.move_to(tree_x, tree_y)
        ctx.line_to(tree_x - 8, tree_y - 25)
        ctx.line_to(tree_x + 8, tree_y - 25)
        ctx.close_path()
        ctx.fill()
    
    # Pulau kecil kanan
    island2_y_offset = math.sin(time * 0.025 + 2) * 4
    
    # Bayangan
    ctx.set_source_rgba(0.3, 0.4, 0.2, 0.5)
    ctx.arc(w * 0.85 + 5, h * 0.35 + island2_y_offset + 10, 55, 0, 2 * math.pi)
    ctx.fill()
    
    # Badan pulau kecil
    grad_island2 = cairo.RadialGradient(w * 0.85 - 10, h * 0.35 - 10, 0, w * 0.85, h * 0.35, 50)
    grad_island2.add_color_stop_rgb(0, 0.6, 0.9, 0.5)
    grad_island2.add_color_stop_rgb(1, 0.5, 0.8, 0.4)
    
    ctx.set_source(grad_island2)
    ctx.arc(w * 0.85, h * 0.35 + island2_y_offset, 50, 0, 2 * math.pi)
    ctx.fill()
    
    ctx.restore()

def draw_butterflies(ctx, w, h, time=0):
    """Menggambar kupu-kupu yang beterbangan dengan animasi sayap."""
    ctx.save()
    
    # Kupu-kupu 1 dengan animasi sayap
    butterfly_x = w * 0.3 + math.sin(time * 0.02) * 20
    butterfly_y = h * 0.4 + math.sin(time * 0.03) * 15
    wing_flap = math.sin(time * 0.2) * 0.3 + 0.7  # Animasi kepak sayap
    
    # Badan kupu-kupu
    ctx.set_source_rgb(1, 0.8, 0.9)
    ctx.arc(butterfly_x, butterfly_y, 6, 0, 2 * math.pi)
    ctx.fill()
    
    # Sayap dengan gradien dan animasi
    wing_grad = cairo.RadialGradient(butterfly_x, butterfly_y, 0, butterfly_x, butterfly_y, 15)
    wing_grad.add_color_stop_rgba(0, 1, 0.7, 0.9, 0.9)
    wing_grad.add_color_stop_rgba(1, 1, 0.6, 0.8, 0.6)
    
    ctx.set_source(wing_grad)
    # Sayap kiri
    ctx.save()
    ctx.translate(butterfly_x, butterfly_y)
    ctx.scale(1, wing_flap)
    ctx.arc(-10, 0, 12, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    
    # Sayap kanan
    ctx.save()
    ctx.translate(butterfly_x, butterfly_y)
    ctx.scale(1, wing_flap)
    ctx.arc(10, 0, 12, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    
    # Kupu-kupu 2
    butterfly_x2 = w * 0.7 + math.sin(time * 0.025 + 2) * 25
    butterfly_y2 = h * 0.5 + math.sin(time * 0.035 + 1) * 20
    wing_flap2 = math.sin(time * 0.18 + 1) * 0.3 + 0.7
    
    # Badan
    ctx.set_source_rgb(0.8, 0.9, 1)
    ctx.arc(butterfly_x2, butterfly_y2, 5, 0, 2 * math.pi)
    ctx.fill()
    
    # Sayap dengan gradien berbeda
    wing_grad2 = cairo.RadialGradient(butterfly_x2, butterfly_y2, 0, butterfly_x2, butterfly_y2, 12)
    wing_grad2.add_color_stop_rgba(0, 0.7, 0.8, 1, 0.9)
    wing_grad2.add_color_stop_rgba(1, 0.6, 0.7, 1, 0.6)
    
    ctx.set_source(wing_grad2)
    # Sayap kiri
    ctx.save()
    ctx.translate(butterfly_x2, butterfly_y2)
    ctx.scale(1, wing_flap2)
    ctx.arc(-8, 0, 10, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    
    # Sayap kanan
    ctx.save()
    ctx.translate(butterfly_x2, butterfly_y2)
    ctx.scale(1, wing_flap2)
    ctx.arc(8, 0, 10, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    
    ctx.restore()

def draw_3d_hills(ctx, w, h):
    """Menggambar bukit dengan efek 3D dan tekstur."""
    ctx.save()
    
    # Bukit belakang dengan efek kedalaman
    grad_hill_back = cairo.LinearGradient(0, h * 0.6, 0, h)
    grad_hill_back.add_color_stop_rgb(0, 0.25, 0.6, 0.15)  # Puncak
    grad_hill_back.add_color_stop_rgb(0.5, 0.3, 0.7, 0.2)   # Tengah
    grad_hill_back.add_color_stop_rgb(1, 0.4, 0.8, 0.3)    # Bawah
    
    ctx.set_source(grad_hill_back)
    ctx.move_to(0, h * 0.6)
    ctx.curve_to(w * 0.2, h * 0.5, w * 0.6, h * 0.7, w, h * 0.6)
    ctx.line_to(w, h)
    ctx.line_to(0, h)
    ctx.close_path()
    ctx.fill()
    
    # Tekstur bukit belakang (garis kontur)
    ctx.set_source_rgba(0.2, 0.5, 0.1, 0.3)
    ctx.set_line_width(2)
    for i in range(3):
        y_pos = h * 0.6 + (h * 0.4 / 4) * (i + 1)
        ctx.move_to(0, y_pos)
        ctx.curve_to(w * 0.2, y_pos - 20, w * 0.6, y_pos + 20, w, y_pos)
        ctx.stroke()
    
    # Bukit depan dengan efek 3D lebih kuat
    grad_hill_front = cairo.LinearGradient(0, h * 0.75, 0, h)
    grad_hill_front.add_color_stop_rgb(0, 0.4, 0.8, 0.25)   # Puncak (terang)
    grad_hill_front.add_color_stop_rgb(0.3, 0.5, 0.85, 0.3) # Tengah
    grad_hill_front.add_color_stop_rgb(1, 0.6, 0.9, 0.4)    # Bawah (sangat terang)
    
    ctx.set_source(grad_hill_front)
    ctx.move_to(0, h * 0.75)
    ctx.curve_to(w * 0.3, h * 0.7, w * 0.7, h * 0.9, w, h * 0.8)
    ctx.line_to(w, h)
    ctx.line_to(0, h)
    ctx.close_path()
    ctx.fill()
    
    # Highlight di puncak bukit depan
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.move_to(w * 0.3, h * 0.7)
    ctx.curve_to(w * 0.4, h * 0.68, w * 0.6, h * 0.72, w * 0.7, h * 0.75)
    ctx.stroke()
    
    ctx.restore()

def draw_sky_background(ctx, w, h, time=0):
    """Menggambar latar belakang langit dengan awan dan efek atmosfer."""
    # Gradien langit dengan multiple color stops untuk efek lebih natural
    grad_sky = cairo.LinearGradient(0, 0, 0, h)
    grad_sky.add_color_stop_rgb(0, 0.3, 0.5, 0.9)   # Biru tua di atas
    grad_sky.add_color_stop_rgb(0.3, 0.5, 0.7, 1.0) # Biru medium
    grad_sky.add_color_stop_rgb(0.7, 0.7, 0.85, 1.0) # Biru muda
    grad_sky.add_color_stop_rgb(1, 0.9, 0.95, 1.0)  # Sangat muda di horizon
    
    ctx.set_source(grad_sky)
    ctx.paint()

    # Matahari dengan glow effect
    sun_glow = cairo.RadialGradient(w * 0.15, h * 0.2, 0, w * 0.15, h * 0.2, 80)
    sun_glow.add_color_stop_rgba(0, 1, 1, 0.8, 0.8)
    sun_glow.add_color_stop_rgba(0.5, 1, 0.95, 0.6, 0.4)
    sun_glow.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
    
    ctx.set_source(sun_glow)
    ctx.arc(w * 0.15, h * 0.2, 80, 0, 2 * math.pi)
    ctx.fill()
    
    # Matahari utama
    sun_grad = cairo.RadialGradient(w * 0.15 - 10, h * 0.2 - 10, 0, w * 0.15, h * 0.2, 50)
    sun_grad.add_color_stop_rgb(0, 1, 1, 0.9)
    sun_grad.add_color_stop_rgb(1, 1, 0.8, 0.3)
    
    ctx.set_source(sun_grad)
    ctx.arc(w * 0.15, h * 0.2, 50, 0, 2 * math.pi)
    ctx.fill()

def draw_foreground_scenery(ctx, w, h, time=0):
    """Menggambar elemen pemandangan depan dengan efek 3D."""
    # Awan-awan kartun dengan animasi
    draw_cartoon_cloud(ctx, w * 0.3, h * 0.25, 1.2, time)
    draw_cartoon_cloud(ctx, w * 0.7, h * 0.15, 1.0, time)
    draw_cartoon_cloud(ctx, w * 0.9, h * 0.3, 0.8, time)
    draw_cartoon_cloud(ctx, w * 0.1, h * 0.35, 0.9, time)

    # Bukit dengan efek 3D
    draw_3d_hills(ctx, w, h)

    # Monster mengintip dari belakang bukit
    draw_map_monster(ctx, w * 0.7, h * 0.55, time)

    # Tambahkan bunga-bunga kecil di bukit depan
    ctx.set_source_rgb(1, 0.8, 0.9)
    for i in range(8):
        x = w * (0.1 + i * 0.1)
        flower_y = h * 0.76 + math.sin(x * 0.1) * 5
        ctx.arc(x, flower_y, 2 + (i % 3), 0, 2 * math.pi)
        ctx.fill()

def get_3d_path_points(points, segments=20):
    """Menghasilkan titik-titik jalur dengan efek perspektif 3D."""
    spline_points = []
    elevations = []  # Tinggi setiap titik untuk efek 3D
    
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        
        for t_int in range(segments):
            t = t_int / segments
            
            # Koordinat X, Y biasa
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t**2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t**3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t**2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t**3)
            
            # Hitung elevasi (efek bukit dan lembah)
            elevation = math.sin(i + t) * 15 + 10  # Gelombang antara 0-25 pixel
            elevations.append(elevation)
            
            spline_points.append((x, y - elevation))  # Kurangi Y untuk efek 3D
    
    spline_points.append((points[-1][0], points[-1][1] - elevations[-1] if elevations else 0))
    return spline_points, elevations

def draw_3d_winding_path(ctx, levels, time=0):
    """Menggambar jalur meliuk dengan efek 3D dan perspektif."""
    if len(levels) < 2: return

    points = [tuple(l['pos']) for l in levels]
    spline_points, elevations = get_3d_path_points(points)

    ctx.save()
    
    # Bayangan jalur dengan efek kedalaman
    ctx.set_source_rgba(0.1, 0.05, 0, 0.5)
    ctx.set_line_width(35)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    
    ctx.move_to(spline_points[0][0] + 8, spline_points[0][1] + 12)
    for i, p in enumerate(spline_points[1:]):
        shadow_offset = 8 + elevations[i] * 0.1  # Shadow mengikuti elevasi
        ctx.line_to(p[0] + shadow_offset, p[1] + shadow_offset)
    ctx.stroke()

    # Jalur utama dengan gradien 3D
    grad_path = cairo.LinearGradient(0, 0, 0, 720)
    grad_path.add_color_stop_rgb(0, 0.95, 0.9, 0.8)  # Terang di atas
    grad_path.add_color_stop_rgb(0.3, 0.9, 0.85, 0.7)
    grad_path.add_color_stop_rgb(0.7, 0.8, 0.75, 0.6)
    grad_path.add_color_stop_rgb(1, 0.7, 0.65, 0.5)   # Gelap di bawah
    
    ctx.set_source(grad_path)
    ctx.set_line_width(28)
    
    ctx.move_to(spline_points[0][0], spline_points[0][1])
    for p in spline_points[1:]:
        ctx.line_to(p[0], p[1])
    ctx.stroke()

    # Highlight di tengah jalan untuk efek 3D
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.set_line_width(8)
    
    ctx.move_to(spline_points[0][0], spline_points[0][1])
    for p in spline_points[1:]:
        ctx.line_to(p[0], p[1])
    ctx.stroke()

    # Tambahkan tekstur batu-batu dengan variasi ukuran
    ctx.set_source_rgba(1, 1, 1, 0.5)
    for i in range(0, len(spline_points), 6):
        if i < len(spline_points):
            p = spline_points[i]
            stone_size = 2 + (i % 4)  # Variasi ukuran batu
            ctx.arc(p[0], p[1], stone_size, 0, 2 * math.pi)
            ctx.fill()

    # Garis pembatas jalan (pinggiran)
    ctx.set_source_rgba(0.6, 0.5, 0.4, 0.8)
    ctx.set_line_width(3)
    
    # Pinggiran kiri
    ctx.move_to(spline_points[0][0] - 12, spline_points[0][1])
    for p in spline_points[1:]:
        ctx.line_to(p[0] - 12, p[1])
    ctx.stroke()
    
    # Pinggiran kanan
    ctx.move_to(spline_points[0][0] + 12, spline_points[0][1])
    for p in spline_points[1:]:
        ctx.line_to(p[0] + 12, p[1])
    ctx.stroke()
    
    ctx.restore()

def draw_crystal_level_node(ctx, x, y, level_id, state, is_hovered, time=0):
    """Menggambar node kristal dengan efek 3D dan animasi."""
    ctx.save()
    ctx.translate(x, y)

    # Animasi mengambang
    float_offset = math.sin(time * 0.05 + level_id) * 3
    ctx.translate(0, float_offset)

    scale = 1.4 if is_hovered and state != 'locked' else 1.0
    ctx.scale(scale, scale)

    if state == 'locked':
        draw_3d_lock_icon(ctx, -25, -25, 50, time)
        ctx.restore()
        return

    # Warna berdasarkan state dengan gradien 3D
    if state == 'unlocked':
        base_color = (0.4, 0.8, 1.0)  # Biru
        highlight_color = (0.6, 0.95, 1.0)
        shadow_color = (0.2, 0.4, 0.8)
        glow_color = (0.6, 0.9, 1.0, 0.6)
    else: # 'current'
        base_color = (1.0, 0.8, 0.0)  # Kuning
        highlight_color = (1.0, 0.95, 0.6)
        shadow_color = (0.8, 0.5, 0.0)
        glow_color = (1.0, 0.9, 0.3, 0.8)

    # Efek glow dan bayangan 3D
    if is_hovered:
        # Outer glow
        ctx.set_source_rgba(*glow_color)
        for i in range(3):
            glow_size = 40 + i * 5
            ctx.arc(0, 0, glow_size, 0, 2 * math.pi)
            ctx.fill()

    # Bayangan di bawah kristal
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.arc(4, 4, 32, 0, 2 * math.pi)
    ctx.fill()

    # Bentuk dasar kristal (octagon untuk efek lebih kristalin)
    angle_step = 2 * math.pi / 8
    points = [(math.sin(i * angle_step) * 30, -math.cos(i * angle_step) * 30) for i in range(8)]

    # Badan utama dengan gradien radial 3D
    ctx.move_to(points[-1][0], points[-1][1])
    for p in points: 
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    grad_body = cairo.RadialGradient(-10, -15, 0, 0, 0, 35)
    grad_body.add_color_stop_rgb(0, *highlight_color)
    grad_body.add_color_stop_rgb(0.6, *base_color)
    grad_body.add_color_stop_rgb(1, *shadow_color)
    
    ctx.set_source(grad_body)
    ctx.fill_preserve()
    
    # Border dengan gradien untuk efek 3D
    border_grad = cairo.LinearGradient(-30, -30, 30, 30)
    border_grad.add_color_stop_rgb(0, *[min(1, c + 0.4) for c in base_color])
    border_grad.add_color_stop_rgb(0.5, *base_color)
    border_grad.add_color_stop_rgb(1, *shadow_color)
    
    ctx.set_source(border_grad)
    ctx.set_line_width(4)
    ctx.stroke()

    # Kilau (Shine) dengan animasi
    shine_alpha = 0.7 + math.sin(time * 0.1) * 0.2
    ctx.set_source_rgba(1, 1, 1, shine_alpha)
    
    # Multiple shine spots untuk efek kristal
    ctx.move_to(-15, -20)
    ctx.curve_to(-8, -25, -3, -18, -6, -10)
    ctx.curve_to(-10, -8, -16, -12, -15, -20)
    ctx.close_path()
    ctx.fill()
    
    ctx.arc(10, -15, 8, 0, 2 * math.pi)
    ctx.fill()

    # Teks nomor level dengan efek 3D
    ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(18)
    text = str(level_id)
    ext = ctx.text_extents(text)
    
    text_x = -ext.width / 2 - ext.x_bearing
    text_y = -ext.height / 2 - ext.y_bearing
    
    # Bayangan teks untuk efek 3D
    ctx.move_to(text_x + 2, text_y + 2)
    ctx.set_source_rgba(0, 0, 0, 0.6)
    ctx.show_text(text)
    
    # Teks utama dengan gradien
    text_grad = cairo.LinearGradient(text_x, text_y, text_x, text_y + 20)
    text_grad.add_color_stop_rgb(0, 1, 1, 1)
    text_grad.add_color_stop_rgb(1, 0.9, 0.9, 0.9)
    
    ctx.move_to(text_x, text_y)
    ctx.set_source(text_grad)
    ctx.show_text(text)
    
    ctx.restore()

def draw_3d_lock_icon(ctx, x, y, size, time=0):
    """Menggambar ikon kunci dengan efek 3D."""
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    
    # Animasi bergetar untuk kunci terkunci
    shake_x = math.sin(time * 0.3) * 1 if time % 60 < 30 else 0
    
    # Bayangan kunci
    ctx.set_source_rgba(0.2, 0.2, 0.3, 0.6)
    ctx.rectangle(-12 + shake_x + 2, -8 + 2, 24, 25)
    ctx.fill()
    
    # Badan kunci dengan gradien metalik
    metal_grad = cairo.LinearGradient(-12, -8, -12, 17)
    metal_grad.add_color_stop_rgb(0, 0.7, 0.7, 0.8)  # Highlight
    metal_grad.add_color_stop_rgb(0.5, 0.5, 0.5, 0.6)  # Mid
    metal_grad.add_color_stop_rgb(1, 0.3, 0.3, 0.4)   # Shadow
    
    ctx.set_source(metal_grad)
    ctx.rectangle(-12 + shake_x, -8, 24, 25)
    ctx.fill()
    
    # Lingkaran kunci
    circle_grad = cairo.RadialGradient(-5 + shake_x, -20, 0, 0 + shake_x, -15, 10)
    circle_grad.add_color_stop_rgb(0, 0.8, 0.8, 0.9)
    circle_grad.add_color_stop_rgb(1, 0.4, 0.4, 0.5)
    
    ctx.set_source(circle_grad)
    ctx.arc(0 + shake_x, -15, 10, 0, 2 * math.pi)
    ctx.fill()
    
    # Lubang kunci
    ctx.set_source_rgb(0.2, 0.2, 0.3)
    ctx.rectangle(-4 + shake_x, -5, 8, 15)
    ctx.fill()
    
    # Kilau pada kunci
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.rectangle(-8 + shake_x, -3, 5, 2)
    ctx.fill()
    
    # Highlight lingkaran
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.arc(-3 + shake_x, -20, 3, 0, 2 * math.pi)
    ctx.fill()
    
    ctx.restore()

def draw_ui_button(ctx, x, y, width, height, text, is_hovered=False, is_pressed=False, time=0):
    """Menggambar tombol UI dengan efek 3D dan animasi."""
    ctx.save()
    
    # Animasi tombol
    pulse = math.sin(time * 0.1) * 0.05 + 1.0 if is_hovered else 1.0
    
    # Warna tombol berdasarkan state
    if is_pressed:
        base_color = (0.7, 0.4, 0.1)
        shadow_offset = 2
        bevel = -2  # Efek tekan
    elif is_hovered:
        base_color = (1.0, 0.7, 0.2)
        shadow_offset = 4
        bevel = 0
    else:
        base_color = (1.0, 0.6, 0.2)
        shadow_offset = 5
        bevel = 2
    
    # Bayangan tombol
    ctx.set_source_rgba(0.1, 0.05, 0, 0.5)
    rounded_rect(ctx, x + shadow_offset, y + shadow_offset, width, height, 15)
    ctx.fill()
    
    # Badan tombol dengan gradien 3D
    btn_grad = cairo.LinearGradient(x, y, x, y + height)
    btn_grad.add_color_stop_rgb(0, *[min(1, c + 0.3) for c in base_color])  # Top highlight
    btn_grad.add_color_stop_rgb(0.1, *[min(1, c + 0.2) for c in base_color])
    btn_grad.add_color_stop_rgb(0.5, *base_color)  # Middle
    btn_grad.add_color_stop_rgb(0.9, *[max(0, c - 0.1) for c in base_color])
    btn_grad.add_color_stop_rgb(1, *[max(0, c - 0.2) for c in base_color])  # Bottom shadow
    
    ctx.set_source(btn_grad)
    rounded_rect(ctx, x + bevel, y + bevel, width, height, 15)
    ctx.fill_preserve()
    
    # Border dengan gradien
    border_grad = cairo.LinearGradient(x, y, x, y + height)
    border_grad.add_color_stop_rgb(0, 1, 1, 1)  # Top highlight
    border_grad.add_color_stop_rgb(1, 0.7, 0.7, 0.7)  # Bottom shadow
    
    ctx.set_source(border_grad)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Efek highlight di bagian atas tombol
    highlight_grad = cairo.LinearGradient(x, y, x, y + height/3)
    highlight_grad.add_color_stop_rgba(0, 1, 1, 1, 0.4)
    highlight_grad.add_color_stop_rgba(1, 1, 1, 1, 0)
    
    ctx.set_source(highlight_grad)
    rounded_rect(ctx, x + bevel, y + bevel, width, height/2, 15)
    ctx.fill()
    
    # Teks tombol dengan efek 3D
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(18 * pulse)  # Animasi pulse saat hover
    
    # Bayangan teks
    text_extents = ctx.text_extents(text)
    text_x = x + (width - text_extents.width) / 2
    text_y = y + (height + text_extents.height) / 2 - text_extents.y_bearing
    
    ctx.move_to(text_x + 2, text_y + 2)
    ctx.set_source_rgba(0, 0, 0, 0.5)
    ctx.show_text(text)
    
    # Teks utama dengan gradien
    text_grad = cairo.LinearGradient(text_x, text_y, text_x, text_y + text_extents.height)
    text_grad.add_color_stop_rgb(0, 1, 1, 1)  # Top highlight
    text_grad.add_color_stop_rgb(1, 0.9, 0.9, 0.9)  # Bottom
    
    ctx.move_to(text_x, text_y)
    ctx.set_source(text_grad)
    ctx.show_text(text)
    
    ctx.restore()
