# src/components/component_options.py
import cairo
import math

def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

def draw_slider(ctx, x, y, w, h, percentage, state="normal"):
    """
    Menggambar komponen slider custom.
    - percentage: 0.0 sampai 1.0
    - state: "normal" atau "dragging"
    """
    ctx.save()
    ctx.translate(x, y)

    # Warna
    track_color = (0.2, 0.2, 0.2)
    fill_color = (0.2, 0.8, 1.0) # Biru cerah
    handle_color_top = (1, 1, 1)
    handle_color_bot = (0.8, 0.8, 0.8)
    handle_border_color = (0.1, 0.1, 0.1)

    # 1. Gambar 'rel' slider
    track_height = h * 0.25
    track_y = (h - track_height) / 2
    rounded_rect(ctx, 0, track_y, w, track_height, track_height / 2)
    ctx.set_source_rgba(0, 0, 0, 0.5)
    ctx.fill() # Bayangan rel

    rounded_rect(ctx, 0, track_y - 2, w, track_height, track_height / 2)
    ctx.set_source_rgb(*track_color)
    ctx.fill()

    # 2. Gambar 'isian' slider sesuai persentase
    fill_width = w * percentage
    if fill_width > 0:
        rounded_rect(ctx, 0, track_y - 2, fill_width, track_height, track_height / 2)
        ctx.set_source_rgb(*fill_color)
        ctx.fill()

    # 3. Gambar 'handle' atau 'kenop' slider
    handle_x = w * percentage
    handle_radius = h / 2
    
    # Efek saat di-drag
    if state == "dragging":
        handle_radius *= 1.1
        ctx.set_source_rgba(0.2, 0.8, 1.0, 0.3)
        ctx.arc(handle_x, h/2, handle_radius * 1.5, 0, 2 * math.pi)
        ctx.fill()
    
    # Bayangan handle
    ctx.set_source_rgba(0,0,0,0.4)
    ctx.arc(handle_x, h/2 + 3, handle_radius, 0, 2*math.pi)
    ctx.fill()

    # Badan handle
    grad = cairo.LinearGradient(handle_x, h/2 - handle_radius, handle_x, h/2 + handle_radius)
    grad.add_color_stop_rgb(0, *handle_color_top)
    grad.add_color_stop_rgb(1, *handle_color_bot)
    ctx.set_source(grad)
    ctx.arc(handle_x, h/2, handle_radius, 0, 2*math.pi)
    ctx.fill()
    
    # Border handle
    ctx.set_source_rgb(*handle_border_color)
    ctx.set_line_width(2)
    ctx.arc(handle_x, h/2, handle_radius, 0, 2*math.pi)
    ctx.stroke()
    
    ctx.restore()
