import cairo
import math

# Tambahkan parameter 'frame_count' untuk animasi
def gambar(ctx, width, height, frame_count):
    ctx.translate(width / 2, height / 2)

    # Hitung sudut putaran jarum (frame_count * kecepatan)
    # Ini akan membuat jarum berputar terus menerus
    angle_jarum = (frame_count % 60) * (6 * math.pi / 180) 

    # --- 1. BAYANGAN STOPWATCH (Drop Shadow) ---
    ctx.save()
    ctx.translate(0, 10)
    ctx.scale(1, 0.3)
    ctx.arc(0, 260, 60, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.fill()
    ctx.restore()

    # --- 2. TOMBOL PEMICU (Atas) ---
    ctx.save()
    ctx.translate(0, -85)
    
    # Kuping Kiri Kanan
    ctx.set_source_rgb(0.2, 0.3, 0.4)
    ctx.rectangle(-25, 10, 10, 15); ctx.fill()
    ctx.rectangle(15, 10, 10, 15); ctx.fill()
    
    # Batang Tengah
    ctx.rectangle(-10, -10, 20, 20)
    grad_btn = cairo.LinearGradient(0, -10, 0, 10)
    grad_btn.add_color_stop_rgb(0, 0.8, 0.8, 0.8) # Silver Terang
    grad_btn.add_color_stop_rgb(1, 0.4, 0.4, 0.4) # Silver Gelap
    ctx.set_source(grad_btn)
    ctx.fill()
    
    # Tombol Merah
    ctx.rectangle(-12, -18, 24, 8)
    ctx.set_source_rgb(0.9, 0.1, 0.1)
    ctx.fill()
    ctx.restore()

    # --- 3. BADAN JAM (BIRU SPORTY) ---
    ctx.save()
    ctx.arc(0, 0, 80, 0, 2 * math.pi)
    
    # Gradien Biru Keren
    grad_body = cairo.RadialGradient(-30, -30, 10, 0, 0, 80)
    grad_body.add_color_stop_rgb(0, 0.2, 0.6, 1.0)   # Biru Terang
    grad_body.add_color_stop_rgb(1, 0.0, 0.1, 0.4)   # Biru Gelap (Navy)
    
    ctx.set_source(grad_body)
    ctx.fill()
    
    # Garis pinggir tebal
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.restore()

    # --- 4. MUKA JAM (PUTIH) ---
    ctx.save()
    ctx.arc(0, 0, 65, 0, 2 * math.pi)
    ctx.set_source_rgb(0.95, 0.95, 0.95)
    ctx.fill()
    ctx.restore()

    # --- 5. ANGKA / TICK MARKS ---
    ctx.save()
    ctx.set_line_width(3)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    for i in range(12):
        ctx.save()
        rot = (i * 30) * (math.pi / 180)
        ctx.rotate(rot)
        
        # Warna selang-seling (Merah di jam 12, 3, 6, 9)
        if i % 3 == 0:
            ctx.set_source_rgb(0.8, 0.1, 0.1) # Merah
            ctx.move_to(0, -50)
            ctx.line_to(0, -60)
        else:
            ctx.set_source_rgb(0.2, 0.2, 0.3) # Hitam
            ctx.move_to(0, -55)
            ctx.line_to(0, -60)
            
        ctx.stroke()
        ctx.restore()
    ctx.restore()

    # --- 6. JARUM JAM BERGERAK (ANIMASI) ---
    ctx.save()
    
    # ROTASI JARUM BERDASARKAN FRAME!
    ctx.rotate(angle_jarum)
    
    # Bayangan Jarum (Biar melayang)
    ctx.save()
    ctx.translate(3, 3)
    ctx.move_to(0, 15); ctx.line_to(0, -50)
    ctx.set_source_rgba(0,0,0,0.3); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

    # Jarum Utama (Oranye Neon)
    ctx.set_source_rgb(1, 0.5, 0) 
    ctx.set_line_width(4)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(0, 15)   # Ekor
    ctx.line_to(0, -50)  # Ujung
    ctx.stroke()
    
    # Titik Poros
    ctx.arc(0, 0, 6, 0, 2*math.pi)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.fill()
    ctx.restore()

    # --- 7. KILAUAN KACA (GLOSSY) ---
    ctx.save()
    ctx.scale(1, 0.6)
    ctx.arc(0, -65, 55, 0, 2 * math.pi)
    
    grad_gloss = cairo.LinearGradient(0, -90, 0, -20)
    grad_gloss.add_color_stop_rgba(0, 1, 1, 1, 0.5) 
    grad_gloss.add_color_stop_rgba(1, 1, 1, 1, 0.0) 
    
    ctx.set_source(grad_gloss)
    ctx.fill()
    ctx.restore()