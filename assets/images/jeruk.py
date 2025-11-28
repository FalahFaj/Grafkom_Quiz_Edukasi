import cairo
import math

def gambar(ctx, width, height):
    # HAPUS BARIS INI: ctx.set_source_rgb(1, 1, 1); ctx.paint()
    
    ctx.save() # Simpan state
    
    # Badan Jeruk (Gunakan scale agar sedikit gepeng alami)
    ctx.save()
    ctx.scale(1.0, 0.95)
    ctx.arc(0, 0, 140, 0, 2 * math.pi)
    
    gradient = cairo.RadialGradient(-40, -40, 10, 0, 0, 140)
    gradient.add_color_stop_rgb(0, 1, 0.9, 0.4)
    gradient.add_color_stop_rgb(0.2, 1, 0.6, 0.0)
    gradient.add_color_stop_rgb(1, 0.8, 0.3, 0.0)
    ctx.set_source(gradient)
    ctx.fill()
    ctx.restore()

    # Pori-pori (Opsional, disederhanakan agar performa ringan)
    ctx.save()
    ctx.set_source_rgba(0.6, 0.3, 0, 0.1)
    for i in range(0, 360, 45): 
        ctx.save()
        ctx.rotate(i * (math.pi / 180))
        ctx.arc(80, 0, 2, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()
    ctx.restore()

    # Kelopak
    ctx.save()
    ctx.translate(0, -130)
    ctx.set_source_rgb(0.3, 0.4, 0.2) 
    for i in range(5):
        ctx.move_to(0, 0); ctx.line_to(8, 0)
        ctx.rotate((2 * math.pi) / 5); ctx.stroke()
    ctx.restore()

    # Daun
    ctx.save()
    ctx.translate(0, -135)
    ctx.rotate(-math.pi / 4)
    grad_leaf = cairo.LinearGradient(0, 0, 80, -20)
    grad_leaf.add_color_stop_rgb(0, 0.1, 0.5, 0.1)
    grad_leaf.add_color_stop_rgb(1, 0.4, 0.8, 0.2)
    ctx.set_source(grad_leaf)
    ctx.move_to(0, 0)
    ctx.curve_to(30, -30, 70, -30, 100, 0)
    ctx.curve_to(70, 30, 30, 30, 0, 0)
    ctx.fill()
    ctx.restore()
    
    ctx.restore() # Restore state awal