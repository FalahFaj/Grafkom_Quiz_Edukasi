import cairo
import math
import random
import time

# Virtual canvas
V_W, V_H = 1000, 700  # larger virtual size for more breathing room

# Default anchors (10 levels) arranged roughly vertically with S-curve
LEVEL_ANCHORS = [
    (120, 620), (240, 560), (360, 480), (420, 360),
    (520, 280), (660, 320), (760, 240), (700, 140),
    (520, 100), (280, 90)
]

NODE_RADIUS = 30
NODE_SAFE_RADIUS = 70  # radius around nodes reserved for no-decor

random.seed(987654321)

# -------------------------
# Utility
# -------------------------
def clamp(v, a, b):
    return max(a, min(b, v))

def lerp(a, b, t):
    return a + (b - a) * t

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def sample_bezier(p0, p1, p2, p3, t):
    # cubic bezier evaluation
    u = 1 - t
    x = (u**3)*p0[0] + 3*(u**2)*t*p1[0] + 3*u*(t**2)*p2[0] + (t**3)*p3[0]
    y = (u**3)*p0[1] + 3*(u**2)*t*p1[1] + 3*u*(t**2)*p2[1] + (t**3)*p3[1]
    return (x, y)

def make_segments(anchors):
    segs = []
    n = len(anchors)
    for i in range(n-1):
        p0 = anchors[i]; p3 = anchors[i+1]
        midx = (p0[0]+p3[0])/2
        offset = 80 if i%2==0 else -80
        p1 = (midx + offset, p0[1])
        p2 = (midx - offset, p3[1])
        segs.append((p0,p1,p2,p3))
    return segs

def flatten(segs, steps=48):
    pts = []
    for (p0,p1,p2,p3) in segs:
        for i in range(steps):
            t = i/float(steps)
            pts.append(sample_bezier(p0,p1,p2,p3,t))
    pts.append(segs[-1][3])
    return pts

# -------------------------
# Candy Forest assets
# -------------------------
def draw_marshmallow_cloud(ctx, x, y, scale=1.0, alpha=0.9):
    ctx.save()
    ctx.translate(x,y)
    ctx.scale(scale, scale)
    ctx.set_source_rgba(1,1,1,alpha)
    for ox, oy, r in [(-42,0,28), (-10,-14,36), (28,-8,30), (62,0,22)]:
        ctx.arc(ox, oy, r, 0, 2*math.pi); ctx.fill()
    ctx.set_source_rgba(1,1,1,0.12)
    ctx.arc(-6, -18, 14, 0, 2*math.pi); ctx.fill()
    ctx.restore()

def pastel_rgb(idx):
    # a small palette for candy forest
    palette = [
        (0.98, 0.64, 0.78),  # pink
        (0.98, 0.9, 0.6),    # yellow
        (0.6, 0.9, 0.95),    # aqua
        (0.82, 0.7, 1.0),    # lavender
        (0.9, 0.83, 0.74),   # peach
        (0.6, 0.86, 0.67),   # mint
    ]
    return palette[int(idx)%len(palette)]

def draw_lollipop_tree(ctx, x, y, scale=1.0, color_idx=0):
    ctx.save()
    ctx.translate(x,y)
    ctx.scale(scale, scale)
    # stick
    ctx.set_line_width(6)
    ctx.set_source_rgb(0.92,0.82,0.7)
    ctx.move_to(-2,28); ctx.line_to(-2,-6); ctx.stroke()
    ctx.set_source_rgb(1,1,1); ctx.move_to(6,28); ctx.line_to(6,-6); ctx.stroke()
    # candy head
    c = pastel_rgb(color_idx)
    grad = cairo.RadialGradient(-6,-8,3, 0,0,36)
    grad.add_color_stop_rgb(0, min(c[0]+0.2,1), min(c[1]+0.2,1), min(c[2]+0.2,1))
    grad.add_color_stop_rgb(1, *c)
    ctx.set_source(grad)
    ctx.arc(0,-8,36,0,2*math.pi); ctx.fill()
    # swirls
    ctx.set_source_rgba(1,1,1,0.16)
    ctx.set_line_width(3)
    ctx.arc(-2,-8,20, -1.6, 1.6); ctx.stroke()
    ctx.restore()

def draw_candy_mushroom(ctx, x, y, scale=1.0, hue=0):
    ctx.save()
    ctx.translate(x,y)
    ctx.scale(scale, scale)
    # stem
    ctx.set_source_rgb(1,0.98,0.95)
    ctx.rectangle(-6, 0, 12, 20); ctx.fill()
    # cap
    c = pastel_rgb(hue)
    ctx.set_source_rgb(*c)
    ctx.move_to(-24,0); ctx.curve_to(-18,-28,18,-28,24,0); ctx.close_path(); ctx.fill()
    # spots
    ctx.set_source_rgb(1,1,1)
    for ox,oy in [(-10,-6),(0,-12),(10,-6),(6,-2),(-6,-2)]:
        ctx.arc(ox, oy, 4.5, 0, 2*math.pi); ctx.fill()
    ctx.restore()

def draw_gumdrop(ctx, x, y, scale=1.0, color_idx=0):
    ctx.save()
    ctx.translate(x,y)
    ctx.scale(scale, scale)
    c = pastel_rgb(color_idx)
    ctx.set_source_rgb(*c)
    ctx.move_to(-18,10); ctx.curve_to(-10,-10, 10,-10, 18,10); ctx.close_path(); ctx.fill()
    ctx.set_source_rgba(1,1,1,0.08)
    ctx.move_to(-6,0); ctx.line_to(6,-4); ctx.stroke()
    ctx.restore()

def draw_flower_cluster(ctx, x, y, scale=1.0):
    for i in range(3):
        draw_candy_mushroom(ctx, x + (i-1)*10 + random.uniform(-6,6), y + random.uniform(-4,6), scale=0.5 + random.random()*0.6, hue=random.randint(0,5))

# -------------------------
# Smart decor placement
# -------------------------
def generate_decors(anchors, attempts=600, target=25):
    segs = make_segments(anchors)
    path_pts = flatten(segs, steps=30)
    placed = []
    tries = 0
    while len(placed) < target and tries < attempts:
        tries += 1
        x = random.uniform(60, V_W-60)
        y = random.uniform(220, V_H-40)
        if any(dist((x,y), a) < NODE_SAFE_RADIUS for a in anchors):
            continue
        minpd = min(dist((x,y), p) for p in path_pts)
        if minpd < 46:
            continue
        if any(dist((x,y),(px,py))<40 for (px,py, *_ ) in placed):
            continue
        r = random.random()
        if r < 0.03:
            placed.append((x,y,'tree',(lerp(0.7,1.25,random.random()), random.randint(0,5))))
        elif r < 0.04:
            placed.append((x,y,'gumdrop',(lerp(0.6,1.1,random.random()), random.randint(0,5))))
        elif r < 0.03:
            placed.append((x,y,'mush',(lerp(0.6,1.0,random.random()), random.randint(0,5))))
    return placed

# -------------------------
# Nodes (candy-styled)
# -------------------------
def draw_node(ctx, x, y, num, status, tnow):
    ctx.save()
    ctx.translate(x,y)
    # shadow
    ctx.save()
    ctx.translate(0,8); ctx.scale(1.0,0.45)
    ctx.set_source_rgba(0,0,0,0.16)
    ctx.arc(0,0,NODE_RADIUS+8,0,2*math.pi); ctx.fill()
    ctx.restore()
    # halo
    if status=='CURRENT':
        pulse = 1.0 + 0.08*math.sin(tnow*3.2)
        ctx.set_source_rgba(1,1,1,0.12)
        ctx.arc(0,0,(NODE_RADIUS+14)*pulse,0,2*math.pi); ctx.fill()
    # base
    if status=='PASSED':
        base=(1,0.52,0.78)
    elif status=='CURRENT':
        base=(1,0.88,0.36)
    else:
        base=(0.86,0.86,0.92)
    grad=cairo.RadialGradient(-8,-10,3,0,0,NODE_RADIUS+6)
    grad.add_color_stop_rgb(0,min(base[0]+0.28,1),min(base[1]+0.28,1),min(base[2]+0.28,1))
    grad.add_color_stop_rgb(1,*base)
    ctx.set_source(grad)
    ctx.arc(0,0,NODE_RADIUS,0,2*math.pi); ctx.fill()
    # glossy
    ctx.set_source_rgba(1,1,1,0.14)
    ctx.arc(-8,-12,NODE_RADIUS*0.6,0,2*math.pi); ctx.fill()
    # ring
    ctx.set_line_width(3); ctx.set_source_rgba(1,1,1,0.95); ctx.stroke_preserve(); ctx.fill()
    # content
    if status=='LOCKED':
        ctx.set_source_rgb(0.18,0.18,0.2)
        ctx.rectangle(-8,-6,16,12); ctx.fill()
        ctx.arc(0,-6,6,math.pi,0); ctx.stroke()
    else:
        ctx.set_source_rgb(1,1,1)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(18)
        ext = ctx.text_extents(str(num))
        ctx.move_to(-ext.width/2 - ext.x_bearing, ext.height/2); ctx.show_text(str(num))
    # passed stars
    if status=='PASSED':
        ctx.save()
        ctx.set_source_rgb(1,0.96,0.18)
        for i,(ox,oy) in enumerate([(-16,-28),(0,-34),(16,-28)]):
            ctx.save()
            ctx.translate(ox,oy); ctx.scale(0.22,0.22)
            ctx.move_to(0,-12)
            for k in range(1,10):
                ang=k*math.pi*2/10; r=12*(0.4 if k%2 else 1)
                ctx.line_to(math.sin(ang)*r, -math.cos(ang)*r)
            ctx.close_path(); ctx.fill(); ctx.restore()
        ctx.restore()
    ctx.restore()

# -------------------------
# candy castle
# -------------------------
def draw_castle(ctx, x, y, scale=1.0):
    ctx.save()
    ctx.translate(x,y); ctx.scale(scale,scale)
    ctx.set_source_rgb(0.98,0.88,0.97)
    ctx.rectangle(-48,-72,36,72); ctx.fill()
    ctx.rectangle(12,-72,36,72); ctx.fill()
    ctx.rectangle(-18,-48,36,48); ctx.fill()
    ctx.set_source_rgb(0.96,0.46,0.8)
    ctx.move_to(-48,-72); ctx.line_to(-26,-112); ctx.line_to(-4,-72); ctx.fill()
    ctx.move_to(12,-72); ctx.line_to(34,-112); ctx.line_to(56,-72); ctx.fill()
    ctx.set_source_rgb(0.12,0.08,0.18)
    for wx in (-36,-20,-4,12,28):
        ctx.rectangle(wx,-40,10,12); ctx.fill()
    ctx.rectangle(-10,-8,20,28); ctx.fill()
    ctx.set_source_rgb(1.0,0.78,0.95)
    ctx.set_line_width(2); ctx.move_to(0,-112); ctx.line_to(0,-132); ctx.stroke()
    ctx.move_to(2,-132); ctx.line_to(20,-124); ctx.line_to(2,-116); ctx.close_path(); ctx.fill()
    ctx.restore()

# -------------------------
# Particles sparkles
# -------------------------
_particles = []
_last_spawn = 0.0

def spawn_sparkles(now):
    global _last_spawn, _particles
    if now - _last_spawn < 0.07:
        return
    _last_spawn = now
    for _ in range(3):
        _particles.append({
            "x": random.uniform(60,V_W-60),
            "y": random.uniform(40,200),
            "vx": random.uniform(-10,10),
            "vy": random.uniform(-8,-1),
            "life": random.uniform(0.9,2.2),
            "size": random.uniform(1.0,3.2),
            "alpha": random.uniform(0.06,0.16)
        })

def update_draw_particles(ctx, dt):
    global _particles
    alive=[]
    for p in _particles:
        p["x"] += p["vx"]*dt*30
        p["y"] += p["vy"]*dt*30
        p["life"] -= dt
        if p["life"]>0:
            alive.append(p)
            a = clamp(p["life"]/2.2,0,1)
            ctx.set_source_rgba(1,1,1,p["alpha"]*a)
            ctx.arc(p["x"], p["y"], p["size"]*(1+(1-a)), 0, 2*math.pi); ctx.fill()
    _particles = alive

# -------------------------
# Hit test for levels
# -------------------------
def hit_test_level(px, py, width, height):
    sx = width/float(V_W)
    sy = height/float(V_H)
    tx = px/sx; ty = py/sy
    for i,(lx,ly) in enumerate(LEVEL_ANCHORS):
        if dist((tx,ty),(lx,ly)) <= NODE_RADIUS+8:
            return i+1
    return None

# -------------------------
# Cached decor for determinism
# -------------------------
_cached = None
_cached_key = None

# -------------------------
# Main draw function
# -------------------------
def gambar(ctx, width, height, current_level=5, tnow=None):
    global _cached, _cached_key
    if tnow is None:
        tnow = time.time()
    # scale context to virtual canvas (use non-uniform scale to fill area but keep ratio)
    sx = width/float(V_W)
    sy = height/float(V_H)
    ctx.save()
    ctx.scale(sx, sy)

    # background gradient candy forest
    grad = cairo.LinearGradient(0,0,0,V_H)
    grad.add_color_stop_rgb(0.0, 0.98, 0.95, 1.0)
    grad.add_color_stop_rgb(0.5, 0.96, 0.92, 0.98)
    grad.add_color_stop_rgb(1.0, 0.95, 0.86, 0.9)
    ctx.set_source(grad); ctx.rectangle(0,0,V_W,V_H); ctx.fill()

    # soft hills layers
    ctx.save()
    ctx.set_source_rgba(0.6,0.78,0.62,0.85)
    ctx.move_to(-50,480); ctx.curve_to(180,380,420,560,1060,480); ctx.line_to(1060,V_H); ctx.line_to(-50,V_H); ctx.fill()
    ctx.restore()

    ctx.save()
    ctx.set_source_rgba(0.72,0.88,0.7,0.9)
    ctx.move_to(-50,540); ctx.curve_to(160,420,420,600,1060,520); ctx.line_to(1060,V_H); ctx.line_to(-50,V_H); ctx.fill()
    ctx.restore()

    # marshmallow clouds
    draw_marshmallow_cloud(ctx, 120, 120, scale=1.2, alpha=0.95)
    draw_marshmallow_cloud(ctx, 620, 80, scale=0.9, alpha=0.9)
    draw_marshmallow_cloud(ctx, 380, 170, scale=0.6, alpha=0.8)

    # pastel distant hills (decorative)
    ctx.save()
    ctx.set_source_rgba(0.8,0.7,0.95,0.22)
    ctx.move_to(-100,360); ctx.curve_to(120,240,420,420,1100,360); ctx.line_to(1100,V_H); ctx.line_to(-100,V_H); ctx.fill()
    ctx.restore()

    # path
    anchors = LEVEL_ANCHORS
    segs = make_segments(anchors)
    path_pts = flatten(segs, steps=36)

    # cache decor per anchors
    key = tuple(anchors)
    if _cached is None or _cached_key != key:
        _cached = generate_decors(anchors, attempts=1200, target=100)
        _cached_key = key

    # draw decor behind path
    for (dx,dy,typ,param) in _cached:
        if typ=='tree':
            scale,color_idx = param
            draw_lollipop_tree(ctx, dx, dy, scale=scale, color_idx=color_idx)
        elif typ=='gumdrop':
            scale,color_idx = param
            draw_gumdrop(ctx, dx, dy, scale=scale, color_idx=color_idx)
        else:
            scale,hue = param
            draw_candy_mushroom(ctx, dx, dy, scale=scale, hue=hue)

    # draw path glow
    ctx.save()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(1,1,1,0.16); ctx.set_line_width(36)
    ctx.move_to(*anchors[0])
    for (p0,p1,p2,p3) in segs:
        ctx.curve_to(p1[0],p1[1], p2[0],p2[1], p3[0], p3[1])
    ctx.stroke()
    ctx.restore()

    # main path
    ctx.save()
    ctx.set_source_rgb(1,1,1); ctx.set_line_width(14)
    ctx.move_to(*anchors[0])
    for (p0,p1,p2,p3) in segs:
        ctx.curve_to(p1[0],p1[1], p2[0],p2[1], p3[0], p3[1])
    ctx.stroke()
    ctx.restore()

    # center dashed stripe
    ctx.save()
    ctx.set_dash([12,10]); ctx.set_line_width(5)
    ctx.set_source_rgba(0.96,0.88,0.92,0.9)
    ctx.move_to(*anchors[0])
    for (p0,p1,p2,p3) in segs:
        ctx.curve_to(p1[0],p1[1], p2[0],p2[1], p3[0], p3[1])
    ctx.stroke(); ctx.set_dash([])
    ctx.restore()

    # rocks beside path
    for i in range(18):
        t = i/18.0
        seg_i = int(t*(len(segs)-1))
        sub = (t*(len(segs)-1)) - seg_i
        p0,p1,p2,p3 = segs[seg_i]
        px,py = sample_bezier(p0,p1,p2,p3,sub)
        t2 = clamp(sub+0.01, 0, 1)
        x2,y2 = sample_bezier(p0,p1,p2,p3,t2)
        dx = x2-px; dy = y2-py
        ln = math.hypot(dx,dy) or 1.0
        nx = -dy/ln; ny = dx/ln
        side = -1 if i%2==0 else 1
        sx = px + nx*(18+random.random()*10)*side
        sy = py + ny*(8+random.random()*8)
        draw_gumdrop(ctx, sx, sy, 0.5+random.random()*0.6, color_idx=random.randint(0,5))

    # node shadows
    for ax,ay in anchors:
        ctx.save()
        ctx.translate(ax,ay+10); ctx.scale(1.0,0.46)
        ctx.set_source_rgba(0,0,0,0.12); ctx.arc(0,0,NODE_RADIUS+10,0,2*math.pi); ctx.fill()
        ctx.restore()

    # draw nodes
    for i,(ax,ay) in enumerate(anchors):
        idx = i+1
        if idx < current_level:
            status='PASSED'
        elif idx==current_level:
            status='CURRENT'
        else:
            status='LOCKED'
        draw_node(ctx, ax, ay, idx, status, tnow)

    # castle
    fx,fy = anchors[-1]
    draw_castle(ctx, fx, fy-80, scale=0.95)

    # foreground flowers near nodes
    for i,(ax,ay) in enumerate(anchors):
        side = -1 if i%2==0 else 1
        ox = ax + side*44
        oy = ay + random.randint(18,40)
        if i < current_level-1:
            draw_flower_cluster(ctx, ox, oy, scale=0.6)
        elif i == current_level-1:
            draw_gumdrop(ctx, ox, oy, 0.9, color_idx=random.randint(0,5))

    # sparkles
    spawn_sparkles(tnow)
    update_draw_particles(ctx, dt=0.016)

    # title
    ctx.save()
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(26)
    ctx.set_source_rgba(0.12,0.12,0.18,0.95)
    ctx.move_to(30,38); 
    ctx.restore()
    ctx.restore()