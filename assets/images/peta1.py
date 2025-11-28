# draw_level_map.py
# Gambarkan peta jalur 1..10 menggunakan pycairo
# Output: level_map_1_10.png

import math
import cairo

W, H = 800, 1200
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)

def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

def draw_shadowed_circle(ctx, cx, cy, radius, fill_rgb, border_rgb):
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.arc(cx+6, cy+6, radius, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgb(*fill_rgb)
    ctx.arc(cx, cy, radius, 0, 2*math.pi)
    ctx.fill_preserve()
    ctx.set_line_width(6)
    ctx.set_source_rgb(*border_rgb)
    ctx.stroke()

# ---- Background sky gradient ----
lin = cairo.LinearGradient(0, 0, 0, H)
lin.add_color_stop_rgb(0, 0.18, 0.7, 0.9)   # top
lin.add_color_stop_rgb(1, 0.26, 0.86, 0.96)  # bottom
ctx.rectangle(0, 0, W, H)
ctx.set_source(lin)
ctx.fill()

# subtle rays (very transparent)
ctx.save()
ctx.translate(W/2, 120)
for i in range(20):
    ctx.rotate(2*math.pi/20)
    ctx.move_to(0, 30)
    ctx.line_to(0, 520)
ctx.set_line_width(60)
ctx.set_source_rgba(1,1,1,0.03)
ctx.stroke()
ctx.restore()

# ---- Grass area ----
ctx.set_source_rgb(0.22, 0.72, 0.22)
ctx.rectangle(0, 280, W, H-280)
ctx.fill()

# ---- Winding path points (10 nodes) ----
path_pts = [
    (W*0.5, H-120),
    (W*0.45, H-260),
    (W*0.55, H-380),
    (W*0.38, H-520),
    (W*0.6, H-640),
    (W*0.5, H-780),
    (W*0.68, H-900),
    (W*0.45, H-1000),
    (W*0.3, H-860),
    (W*0.2, H-720)
]

# draw thick sand path
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)
ctx.set_line_width(120)
ctx.set_source_rgb(0.97, 0.90, 0.75)
ctx.move_to(*path_pts[0])
for (x,y) in path_pts[1:]:
    ctx.line_to(x,y)
ctx.stroke()

# inner edge to add depth
ctx.set_line_width(6)
ctx.set_source_rgba(0.88, 0.78, 0.6, 0.9)
ctx.move_to(*path_pts[0])
for (x,y) in path_pts[1:]:
    ctx.line_to(x,y)
ctx.stroke()

# ---- Decorative bushes function ----
def draw_bush(ctx, x, y, scale=1.0):
    ctx.set_source_rgb(0.15,0.6,0.15)
    for dx,dy,r in [(-40,0,36),(0,-20,44),(40,0,36),(15,18,30),(-15,18,30)]:
        ctx.arc(x+dx*scale, y+dy*scale, r*scale, 0, 2*math.pi)
        ctx.fill()
    ctx.set_source_rgba(1,1,1,0.12)
    ctx.arc(x-10*scale, y-20*scale, 25*scale, 0, 2*math.pi)
    ctx.fill()

draw_bush(ctx, 140, 880, 1.4)
draw_bush(ctx, 680, 940, 1.2)
draw_bush(ctx, 720, 720, 0.9)
draw_bush(ctx, 90, 620, 1.0)
draw_bush(ctx, 500, 520, 1.1)

# ---- Draw node stones with numbers 1..10 ----
node_radius = 46
for i, (x,y) in enumerate(path_pts, start=1):
    # stone base shadow + body
    draw_shadowed_circle(ctx, x, y, node_radius+6, (0.2,0.12,0.08), (0.05,0.03,0.02))
    draw_shadowed_circle(ctx, x, y-6, node_radius, (0.85,0.85,0.9), (0.12,0.09,0.08))
    # inner (white) circle
    ctx.set_source_rgb(0.98,0.98,0.98)
    ctx.arc(x, y-6, node_radius-12, 0, 2*math.pi)
    ctx.fill()
    # number
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(36)
    txt = str(i)
    xb, yb, tw, th, xa, ya = ctx.text_extents(txt)
    ctx.set_source_rgb(0.15,0.15,0.18)
    ctx.move_to(x - tw/2 - xb, y-6 + th/2)
    ctx.show_text(txt)

# ---- Start/End labels ----
ctx.set_font_size(28)
ctx.set_source_rgb(1,1,1)
sx, sy = path_pts[0]
ctx.move_to(sx-60, sy+90)
ctx.show_text("Start")
ex, ey = path_pts[-1]
ctx.move_to(ex-20, ey-90)
ctx.show_text("Level 10")

# ---- Bottom water strip ----
ctx.set_source_rgb(0.08,0.48,0.79)
ctx.rectangle(0, H-60, W, 60)
ctx.fill()

# ---- Header title ----
ctx.set_font_size(72)
txt = "Eduiz - Mudah"
xb,yb,tw,th,_,_ = ctx.text_extents(txt)
ctx.set_source_rgb(1,0.9,0.2)
ctx.move_to((W-tw)/2 - xb, 60)
ctx.show_text(txt)
surface.write_to_png("level_map_1_10.png")