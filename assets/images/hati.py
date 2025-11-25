import cairo
import math

def gambar(ctx, width, height):
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    ctx.translate(width / 2, height / 2)
    ctx.save() 
    ctx.move_to(0, -50)
    ctx.curve_to(-110, -130, -220, 40, 0, 170)
    ctx.curve_to(220, 40, 110, -130, 0, -50)
    ctx.close_path()
    
    gradient = cairo.RadialGradient(-30, -50, 20, 0, 20, 200)
    gradient.add_color_stop_rgb(0, 1, 0.2, 0.2)     
    gradient.add_color_stop_rgb(0.4, 0.9, 0.0, 0.0) 
    gradient.add_color_stop_rgb(1, 0.4, 0.0, 0.0)   
    
    ctx.set_source(gradient)
    ctx.fill()
    ctx.restore()
    ctx.save() 
    ctx.translate(-70, -70)
    ctx.rotate(-0.3)  
    ctx.scale(1.0, 0.6)

    ctx.arc(0, 0, 35, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 0.4) 
    ctx.fill()
    ctx.restore()