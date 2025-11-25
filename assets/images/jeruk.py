import cairo
import math

# Fungsi standar agar bisa dipanggil main.py
def gambar(ctx, width, height):
    # 1. Background Putih (Agar bersih)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    # Pindah ke tengah kanvas
    ctx.translate(width / 2, height / 2)

    # --- BAGIAN 1: BADAN JERUK ---
    ctx.save()
    
    # Sedikit gepeng biar terlihat alami (tidak bulat sempurna)
    ctx.scale(1.0, 0.95)

    # Gambar Lingkaran Dasar
    ctx.arc(0, 0, 140, 0, 2 * math.pi)

    # Pewarnaan 3D (Gradien Radial)
    # Cahaya datang dari kiri atas (-40, -40)
    gradient = cairo.RadialGradient(-40, -40, 10, 0, 0, 140)
    gradient.add_color_stop_rgb(0, 1, 0.9, 0.4)      # Highlight (Kuning Pucat)
    gradient.add_color_stop_rgb(0.2, 1, 0.6, 0.0)    # Warna Utama (Oranye Terang)
    gradient.add_color_stop_rgb(1, 0.8, 0.3, 0.0)    # Bayangan (Oranye Gelap)

    ctx.set_source(gradient)
    ctx.fill()
    ctx.restore() # Reset skala dan warna

    # --- BAGIAN 2: PORI-PORI KULIT (Tekstur) ---
    # Kita gambar bintik-bintik samar agar terlihat seperti kulit jeruk
    ctx.save()
    ctx.set_source_rgba(0.6, 0.3, 0, 0.1) # Oranye gelap transparan
    
    # Gambar beberapa titik manual (biar ringan di GTK)
    # Kita putar koordinat biar menyebar
    for i in range(0, 360, 30): 
        ctx.save()
        ctx.rotate(i * (math.pi / 180)) # Putar kertas
        ctx.arc(80, 0, 2, 0, 2 * math.pi) # Gambar titik di jarak 80
        ctx.fill()
        ctx.arc(110, 20, 1.5, 0, 2 * math.pi) # Gambar titik lain
        ctx.fill()
        ctx.restore()
    ctx.restore()

    # --- BAGIAN 3: KELOPAK (Ujung Batang) ---
    ctx.save()
    ctx.translate(0, -130) # Pindah ke atas jeruk
    
    # Gambar bintang kecil hijau tua
    ctx.set_source_rgb(0.3, 0.4, 0.2) 
    for i in range(5):
        ctx.move_to(0, 0)
        ctx.line_to(8, 0)
        ctx.rotate((2 * math.pi) / 5) # Putar 72 derajat
        ctx.stroke()
    ctx.restore()

    # --- BAGIAN 4: DAUN ---
    ctx.save()
    ctx.translate(0, -135)   # Pangkal daun di atas
    ctx.rotate(-math.pi / 4) # Miring ke kiri atas

    # Gradien Daun
    grad_leaf = cairo.LinearGradient(0, 0, 80, -20)
    grad_leaf.add_color_stop_rgb(0, 0.1, 0.5, 0.1) # Hijau Tua
    grad_leaf.add_color_stop_rgb(1, 0.4, 0.8, 0.2) # Hijau Muda

    ctx.set_source(grad_leaf)
    
    # Bentuk Daun
    ctx.move_to(0, 0)
    ctx.curve_to(30, -30, 70, -30, 100, 0)
    ctx.curve_to(70, 30, 30, 30, 0, 0)
    ctx.fill()
    
    # Tulang Daun (Garis tipis di tengah)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(2)
    ctx.move_to(0,0)
    ctx.line_to(90,0)
    ctx.stroke()

    ctx.restore()