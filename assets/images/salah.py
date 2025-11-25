import cairo
import math

def gambar(ctx, width, height):
    # Pindah ke tengah
    ctx.translate(width / 2, height / 2)

    # --- 1. BAYANGAN TOMBOL ---
    ctx.save()
    ctx.translate(0, 5)
    ctx.arc(0, 0, 70, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.fill()
    ctx.restore()

    # --- 2. LINGKARAN DASAR (MERAH) ---
    ctx.save()
    # Gradien Merah Mewah
    gradient = cairo.RadialGradient(-30, -30, 10, 0, 0, 90)
    gradient.add_color_stop_rgb(0, 1.0, 0.4, 0.4)   # Merah Pink (Highlight)
    gradient.add_color_stop_rgb(0.5, 0.9, 0.0, 0.0) # Merah Utama
    gradient.add_color_stop_rgb(1, 0.5, 0.0, 0.0)   # Merah Maroon (Pinggir)
    
    ctx.arc(0, 0, 70, 0, 2 * math.pi)
    ctx.set_source(gradient)
    ctx.fill()
    
    # Ring Putih Tipis
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(3)
    ctx.arc(0, 0, 65, 0, 2 * math.pi)
    ctx.stroke()
    ctx.restore()

    # --- 3. IKON SILANG (CROSS) ---
    
    def path_silang():
        # Garis 1 (\)
        ctx.move_to(-25, -25)
        ctx.line_to(25, 25)
        # Garis 2 (/)
        ctx.move_to(25, -25)
        ctx.line_to(-25, 25)

    # A. Bayangan Ikon
    ctx.save()
    ctx.translate(3, 3)
    path_silang()
    ctx.set_line_width(18)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(0.3, 0, 0, 0.4) # Bayangan merah tua gelap
    ctx.stroke()
    ctx.restore()

    # B. Ikon Utama (Putih)
    ctx.save()
    path_silang()
    ctx.set_line_width(18)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke()
    ctx.restore()

    # --- 4. EFEK KILAUAN KACA (GLOSS) ---
    ctx.save()
    ctx.scale(1, 0.6) 
    ctx.arc(0, -60, 50, 0, 2 * math.pi)
    
    grad_gloss = cairo.LinearGradient(0, -90, 0, -20)
    grad_gloss.add_color_stop_rgba(0, 1, 1, 1, 0.7)
    grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    
    ctx.set_source(grad_gloss)
    ctx.fill()
    ctx.restore()