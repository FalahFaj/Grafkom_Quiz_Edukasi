import cairo
import math

def gambar(ctx, width, height):
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    ctx.translate(width / 2, height / 2)
    ctx.save()
    ctx.move_to(0, -70) 

    ctx.curve_to(60, -100, 130, -50, 130, 20)  
    ctx.curve_to(130, 100, 50, 140, 0, 140)    

    ctx.curve_to(-50, 140, -130, 100, -130, 20) 
    ctx.curve_to(-130, -50, -60, -100, 0, -70)  

    gradient = cairo.RadialGradient(-40, -40, 10, 0, 0, 140)
    gradient.add_color_stop_rgb(0, 1, 0.5, 0.5)   
    gradient.add_color_stop_rgb(0.3, 0.9, 0.1, 0.1) 
    gradient.add_color_stop_rgb(1, 0.4, 0, 0)       
    
    ctx.set_source(gradient)
    ctx.fill()
    ctx.restore()
    ctx.save()
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(0.4, 0.25, 0.1)
    
    ctx.move_to(0, -65) 
    ctx.curve_to(0, -85, 5, -110, 25, -135) 
    ctx.stroke()
    ctx.restore()

    ctx.save()
    ctx.translate(5, -85)
    ctx.rotate(-math.pi / 3) 

    ctx.set_source_rgb(0.2, 0.6, 0.2) 

    ctx.move_to(0, 0)
    ctx.curve_to(25, -20, 50, -20, 80, 0) 
    ctx.curve_to(50, 20, 25, 20, 0, 0)    
    
    ctx.fill()
    ctx.restore()