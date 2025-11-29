# src/halaman/map_scene.py
import gi
gi.require_version('Gtk', '3.0')
import math
import cairo
import json
from gi.repository import Gtk, Gdk, GLib
from ..components import komponen_map

class MapScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback
        self.difficulty = "easy" 

        self.animation_time = 0
        self.level_data = {}
        self.savegame_data = {}
        self.unlocked_level = 1

        self.buttons = []
        self.hovered_button_name = None
        self.pressed_button_name = None

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion)

        GLib.timeout_add(16, self.on_update)

    def on_update(self):
        self.animation_time += 1
        self.queue_draw()
        return True

    def load_data(self):
        try:
            with open('data/savegame.json', 'r') as f:
                self.savegame_data = json.load(f)
            self.unlocked_level = self.savegame_data.get('current_level', {}).get(self.difficulty, 1)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Savegame not found, default to level 1.")
            self.unlocked_level = 1
        
        # Buat koordinat level berdasarkan tingkat kesulitan
        self._create_levels()

    def _create_levels(self):
        """Membuat koordinat jalur yang berbeda untuk setiap difficulty."""
        self.level_data['levels'] = []
        positions = []

        if self.difficulty == 'easy':
            # Jalur S-Curve Sederhana
            positions = [
                (150, 600), (300, 550), (400, 450), (300, 350), (450, 250),
                (650, 250), (800, 350), (950, 450), (1100, 350), (1150, 210)
            ]
        elif self.difficulty == 'medium':
            # Jalur Berliku
            positions = [
                (125, 600), (250, 500), (150, 350), (350, 250), (600, 300),
                (500, 450), (750, 550), (950, 400), (850, 220), (1125, 180)
            ]
        elif self.difficulty == 'hard':
            # Jalur Zig-Zag Tajam
            positions = [
               (125, 600), (250, 500), (150, 350), (350, 250), (600, 300),
                (500, 450), (750, 550), (950, 475), (850, 425), (1100, 375)
            ]

        for i, pos in enumerate(positions):
            lvl_id = i + 1
            self.level_data['levels'].append({'id': lvl_id, 'pos': pos})

    def on_enter(self, level='easy'):
        self.difficulty = level
        print(f"Loading Map: {self.difficulty.upper()}")
        self.load_data()
        self._register_buttons(1280, 720)
        self.queue_draw()

    def on_motion(self, widget, event):
        x, y = event.x, event.y
        v_width, v_height = 1280, 720
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        vx = x / scale_x
        vy = y / scale_y

        current_hover = None
        for btn in self.buttons:
            bx, by, bw, bh = btn['v_rect']
            if bx <= vx < bx + bw and by <= vy < by + bh:
                current_hover = btn['name']
                break
        
        if not current_hover:
            levels = self.level_data.get('levels', [])
            for level in levels:
                lx, ly = level['pos']
                hitbox_radius = 35
                # Animasi naik turun mempengaruhi hitbox sedikit
                anim_offset = math.sin(self.animation_time * 0.05 + level['id']) * 4
                dist_sq = (vx - lx)**2 + (vy - (ly + anim_offset))**2
                
                if dist_sq < hitbox_radius**2: 
                    current_hover = f"level_{level['id']}"
                    break

        if self.hovered_button_name != current_hover:
            self.hovered_button_name = current_hover
            self.queue_draw()

    def on_button_press(self, widget, event):
        self.pressed_button_name = self.hovered_button_name
        self.queue_draw()
        return True

    def on_button_release(self, widget, event):
        if self.pressed_button_name and self.pressed_button_name == self.hovered_button_name:
            if self.pressed_button_name == "Kembali":
                self.change_scene("pilihan_level_scene")
            elif str(self.pressed_button_name).startswith("level_"):
                lvl_id = int(self.pressed_button_name.split("_")[1])
                
                if lvl_id <= self.unlocked_level:
                    print(f"Start Game: Level {lvl_id} [{self.difficulty}]")
                    # Pindah ke Game Scene
                    self.change_scene("game_scene", level=lvl_id, difficulty=self.difficulty) 
                else:
                    print("Level Terkunci!")

        self.pressed_button_name = None
        self.queue_draw()
        return True

    def on_draw(self, widget, ctx):
        v_width, v_height = 1280, 720
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        ctx.scale(scale_x, scale_y)

        # 1. Background
        komponen_map.draw_sky_background(ctx, v_width, v_height, self.animation_time, self.difficulty)

        # 2. Pemandangan
        komponen_map.draw_foreground_scenery(ctx, v_width, v_height, self.animation_time, self.difficulty)

        levels = self.level_data.get('levels', [])
        
        # 3. Jalur & Rumah
        komponen_map.draw_3d_winding_path(ctx, levels, self.animation_time, self.difficulty)

        # Hitung Offset Angka Tampilan (Visual Saja)
        # Easy: 1-10, Medium: 11-20, Hard: 21-30
        display_offset = 0
        if self.difficulty == 'medium':
            display_offset = 10
        elif self.difficulty == 'hard':
            display_offset = 20

        # 4. Node Level
        for level in levels:
            lvl_id = level['id'] # Ini tetap 1-10 untuk logika internal
            pos = level['pos']
            
            # Tentukan status kunci
            state = 'locked'
            if lvl_id < self.unlocked_level: 
                state = 'unlocked' # Level yang sudah lewat (bintang/hijau)
            elif lvl_id == self.unlocked_level: 
                state = 'current'  # Level saat ini (kuning/berdenyut)
            
            is_hovered = (self.hovered_button_name == f"level_{lvl_id}")
            
            # PENTING: Kita kirim (lvl_id + display_offset) ke fungsi gambar
            # supaya yang muncul di layar adalah angka 11, 12, dst.
            komponen_map.draw_crystal_level_node(
                ctx, 
                pos[0], pos[1], 
                lvl_id + display_offset, # <--- PERUBAHAN DISINI
                state, 
                is_hovered, 
                self.animation_time, 
                self.difficulty
            )

        # 5. UI & Judul
        self._draw_title(ctx, v_width)
        for btn in self.buttons:
            vx, vy, vw, vh = btn['v_rect']
            
            state = "normal"
            if btn['name'] == self.pressed_button_name:
                state = "pressed"
            elif btn['name'] == self.hovered_button_name:
                state = "hover"

            komponen_map.draw_ui_button(
                ctx, vx, vy, vw, vh, btn['name'], 
                color="ORANGE", state=state, font_size=24
            )

    def _register_buttons(self, v_width, v_height):
        self.buttons.clear()
        self.buttons.append({ 'name': "Kembali", 'v_rect': (30, v_height - 80, 150, 50) })

    def _draw_title(self, ctx, w):
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(60)
        
        if self.difficulty == 'hard':
            text = "PETA MISTERIUS"; color = (0.8, 0.2, 0.2) 
        elif self.difficulty == 'medium':
            text = "PETA PETUALANGAN"; color = (1.0, 0.9, 0.0) 
        else:
            text = "PETA PETUALANGAN"; color = (1.0, 1.0, 1.0) 

        ext = ctx.text_extents(text)
        x = (w - ext.width) / 2
        y = 80
        
        ctx.move_to(x+4, y+4); ctx.set_source_rgba(0,0,0,0.6); ctx.show_text(text)
        ctx.move_to(x, y); ctx.set_source_rgb(*color); ctx.show_text(text)
        ctx.move_to(x, y); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(2); ctx.text_path(text); ctx.stroke()