import cairo

def gambar(ctx, width, height, text_string, head_index, trail_length):
    ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(50)

    total_text_width = 0
    for char in text_string:
        extents = ctx.text_extents(char)
        total_text_width = total_text_width + extents.x_advance

    start_x = (width - total_text_width) / 2
    start_y = (height / 2) + (50 / 3)

    current_x = start_x
    
    for i, char in enumerate(text_string):
        distance = head_index - i
        alpha = 0.05

        if distance >= 0 and distance < trail_length:
            alpha = 1.0 - (distance / trail_length)
        
        ctx.set_source_rgba(0.2, 1, 0.8, alpha)
        
        ctx.move_to(current_x, start_y)
        ctx.show_text(char)
        
        extents = ctx.text_extents(char)
        current_x = current_x + extents.x_advance
