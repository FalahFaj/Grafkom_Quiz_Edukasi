import cairo
import math

# --- Helper functions (bisa dipindahkan ke file utilitas nanti) ---

def rounded_rect(ctx, x, y, w, h, r):
    """Helper untuk menggambar kotak dengan sudut tumpul."""
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()

def draw_lock_icon(ctx, x, y, size):
    """Menggambar ikon gembok sederhana di tengah koordinat x, y."""
    ctx.save()
    ctx.translate(x - size / 2, y - size / 2) # Pusatkan ikon

    # Warna dasar gembok
    body_color = (0.3, 0.3, 0.3)
    shackle_color = (0.5, 0.5, 0.5)
    
    body_w = size * 0.7
    body_h = size * 0.6
    body_x = (size - body_w) / 2
    body_y = size * 0.4
    
    # Badan Gembok
    rounded_rect(ctx, body_x, body_y, body_w, body_h, 3)
    ctx.set_source_rgb(*body_color)
    ctx.fill()
    
    # Gagang Gembok
    ctx.set_line_width(size * 0.12)
    ctx.set_source_rgb(*shackle_color)
    
    radius = body_w * 0.4
    center_x = size / 2
    center_y = body_y
    
    ctx.new_sub_path()
    ctx.arc(center_x, center_y, radius, math.pi, 0)
    ctx.stroke()
    ctx.restore()

# --- Komponen Utama ---

def draw_level_card(ctx, x, y, w, h, title, subtitle, color, state="normal", locked=False):
    """
    Menggambar kartu pilihan level yang interaktif.
    - state: "normal", "hover", "pressed"
    - locked: True/False
    """
    ctx.save()
    
    press_offset = 2 if state == "pressed" and not locked else 0
    ctx.translate(x, y + press_offset)
    
    # Tentukan warna dasar
    colors = {
        "GREEN": ((0.5, 0.8, 0.1), (0.3, 0.6, 0.0)),
        "BLUE": ((0.1, 0.5, 0.8), (0.0, 0.3, 0.6)),
        "RED": ((0.9, 0.3, 0.2), (0.7, 0.1, 0.1))
    }
    top_col, bot_col = colors.get(color, colors["GREEN"])

    # Penyesuaian state
    if locked:
        top_col = (0.5, 0.5, 0.5)
        bot_col = (0.3, 0.3, 0.3)
    elif state == "hover":
        top_col = tuple(min(1.0, c + 0.15) for c in top_col)
    elif state == "pressed":
        top_col = tuple(max(0.0, c - 0.2) for c in top_col)

    # Gambar kartu
    r = 25
    shadow_offset = 4 if state == "pressed" else 8
    
    # Drop shadow
    if not locked:
        ctx.set_source_rgba(0, 0, 0, 0.3)
        rounded_rect(ctx, 0, shadow_offset, w, h, r); ctx.fill()

    # Badan Kartu
    grad = cairo.LinearGradient(0, 0, 0, h)
    grad.add_color_stop_rgb(0, *top_col)
    grad.add_color_stop_rgb(1, *bot_col)
    rounded_rect(ctx, 0, 0, w, h, r)
    ctx.set_source(grad); ctx.fill()
    
    # Border
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(5)
    rounded_rect(ctx, 0, 0, w, h, r); ctx.stroke()

    # Teks Judul (e.g., "MUDAH")
    ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(h * 0.15)
    ext = ctx.text_extents(title)
    
    text_color = (1, 1, 1) if not locked else (0.7, 0.7, 0.7)
    
    ctx.set_source_rgb(*text_color)
    ctx.move_to(w/2 - ext.width/2, h * 0.45 + ext.height/2)
    ctx.show_text(title)
    
    # Teks Subjudul (e.g., "Level 1-10")
    ctx.set_font_size(h * 0.1)
    ext_sub = ctx.text_extents(subtitle)
    ctx.set_source_rgba(*text_color, 0.8 if not locked else 0.6)
    ctx.move_to(w/2 - ext_sub.width/2, h * 0.7 + ext_sub.height/2)
    ctx.show_text(subtitle)
    
    # Ikon gembok jika terkunci
    if locked:
        ctx.set_source_rgba(0, 0, 0, 0.4) # Lapisan gelap
        rounded_rect(ctx, 0, 0, w, h, r); ctx.fill()
        draw_lock_icon(ctx, w / 2, h / 2, h * 0.5)
        
    ctx.restore()
