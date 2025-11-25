import cairo
import math

def gambar(ctx, width, height):
    # Pindah ke tengah
    ctx.translate(width / 2, height / 2)

    # --- 1. BAYANGAN TOMBOL (Di bawah lingkaran hijau) ---
    ctx.save()
    ctx.translate(0, 5) # Geser ke bawah sedikit
    ctx.arc(0, 0, 70, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.3) # Hitam transparan
    ctx.fill()
    ctx.restore()

    # --- 2. LINGKARAN DASAR (HIJAU) ---
    ctx.save()
    # Gradien Hijau Mewah
    # Pusat cahaya di atas (-30, -30)
    gradient = cairo.RadialGradient(-30, -30, 10, 0, 0, 90)
    gradient.add_color_stop_rgb(0, 0.2, 0.9, 0.4)   # Hijau Neon (Highlight)
    gradient.add_color_stop_rgb(0.5, 0.0, 0.7, 0.0) # Hijau Utama
    gradient.add_color_stop_rgb(1, 0.0, 0.4, 0.0)   # Hijau Gelap (Pinggir)
    
    ctx.arc(0, 0, 70, 0, 2 * math.pi)
    ctx.set_source(gradient)
    ctx.fill()
    
    # Ring Putih Tipis di dalam (Agar terlihat tajam)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(3)
    ctx.arc(0, 0, 65, 0, 2 * math.pi)
    ctx.stroke()
    ctx.restore()

    # --- 3. IKON CENTANG (CHECKMARK) ---
    
    # Fungsi pembantu untuk menggambar jalur centang
    def path_centang():
        ctx.move_to(-35, 0)
        ctx.line_to(-10, 25)
        ctx.line_to(35, -25)

    # A. Bayangan Ikon (Hitam Transparan)
    ctx.save()
    ctx.translate(3, 3) # Geser bayangan
    path_centang()
    ctx.set_line_width(18)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(0, 0.2, 0, 0.4) # Bayangan hijau tua gelap
    ctx.stroke()
    ctx.restore()

    # B. Ikon Utama (Putih Tebal)
    ctx.save()
    path_centang()
    ctx.set_line_width(18) # Tebal dan gagah
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(1, 1, 1) # Putih Bersih
    ctx.stroke()
    ctx.restore()

    # --- 4. EFEK KILAUAN KACA (GLOSS) ---
    ctx.save()
    # Gambar oval putih transparan di bagian atas
    ctx.scale(1, 0.6) # Gepengkan
    ctx.arc(0, -60, 50, 0, 2 * math.pi)
    
    grad_gloss = cairo.LinearGradient(0, -90, 0, -20)
    grad_gloss.add_color_stop_rgba(0, 1, 1, 1, 0.7) # Putih terang atas
    grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.0) # Transparan bawah
    
    ctx.set_source(grad_gloss)
    ctx.fill()
    ctx.restore()