# src/halaman/pilihan_level.py
import gi
gi.require_version('Gtk', '3.0')
import cairo
import math
import json
from gi.repository import Gtk, Gdk, GLib
from ..components.component_pilih_level import draw_level_card
from ..components.components_menu import draw_glossy_button

class PilihanLevelScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback

        self.animation_time = 0
        self.buttons = []
        self.hovered_button_name = None
        self.pressed_button_name = None

        self.load_save_data()

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.connect("configure-event", self.on_configure)
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion)

        GLib.timeout_add(16, self.on_update)

    def load_save_data(self):
        try:
            with open('data/savegame.json', 'r') as f:
                save_data = json.load(f)
                self.unlocked_levels = save_data.get("unlocked_levels", ["easy"])
        except (FileNotFoundError, json.JSONDecodeError):
            self.unlocked_levels = ["easy"]

    def on_enter(self):
        self.load_save_data()
        self._register_buttons(800, 600)
        self.queue_draw()

    def on_update(self):
        self.animation_time += 1
        self.queue_draw()
        return True

    def on_configure(self, widget, event):
        self.width = widget.get_allocated_width()
        self.height = widget.get_allocated_height()
        self._register_buttons(800, 600)
        return False

    def on_motion(self, widget, event):
        x, y = event.x, event.y
        current_hover = None
        for btn in self.buttons:
            is_locked = btn.get('locked', False)
            if is_locked: continue

            # Gunakan rect (real coordinates) untuk deteksi hover
            bx, by, bw, bh = btn['rect']
            if bx <= x < bx + bw and by <= y < by + bh:
                current_hover = btn['name']
                break
        
        if self.hovered_button_name != current_hover:
            self.hovered_button_name = current_hover
        
        if self.pressed_button_name and self.hovered_button_name != self.pressed_button_name:
            self.pressed_button_name = None

    def on_button_press(self, widget, event):
        self.pressed_button_name = self.hovered_button_name
        return True

    def on_button_release(self, widget, event):
        if self.pressed_button_name and self.pressed_button_name == self.hovered_button_name:
            print(f"Tombol '{self.pressed_button_name}' dieksekusi!")
            if self.pressed_button_name == "Kembali":
                self.change_scene("menu_scene")
            elif "level" in self.pressed_button_name:
                level_type = self.pressed_button_name.split('_')[1]
                self.change_scene("map_scene", level=level_type)

        self.pressed_button_name = None
        return True

    def on_draw(self, widget, ctx):
        v_width, v_height = 800, 600
        # Terapkan scaling SEKALI di sini
        ctx.scale(self.width / v_width, self.height / v_height)
        
        # Semua fungsi drawing sekarang harus menggunakan VIRTUAL COORDINATES
        self._draw_background(ctx, v_width, v_height)
        self._draw_title(ctx, v_width)
        self._draw_level_cards(ctx)
        self._draw_buttons(ctx)

    def _register_buttons(self, v_width, v_height):
        """
        Mendaftarkan DUA set koordinat:
        - 'rect': Koordinat asli layar untuk deteksi mouse (di-scale).
        - 'v_rect': Koordinat virtual 800x600 untuk menggambar.
        """
        self.buttons.clear()
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        
        # Definisikan semua dalam VIRTUAL COORDINATES dulu
        v_card_w, v_card_h = 200, 250
        v_gap = (v_width - 3 * v_card_w) / 4
        v_y = 180

        v_defs = {
            "level_easy": {'v_rect': (v_gap, v_y, v_card_w, v_card_h)},
            "level_medium": {'v_rect': (v_gap * 2 + v_card_w, v_y, v_card_w, v_card_h)},
            "level_hard": {'v_rect': (v_gap * 3 + v_card_w * 2, v_y, v_card_w, v_card_h)},
            "Kembali": {'v_rect': (30, v_height - 80, 150, 50)}
        }

        for name, data in v_defs.items():
            vx, vy, vw, vh = data['v_rect']
            
            # Buat rect asli untuk deteksi mouse
            real_rect = (vx * scale_x, vy * scale_y, vw * scale_x, vh * scale_y)
            
            # Tentukan status lock
            is_locked = False
            if "level" in name:
                is_locked = name.split('_')[1] not in self.unlocked_levels

            self.buttons.append({
                'name': name,
                'rect': real_rect,
                'v_rect': data['v_rect'], # Simpan virtual rect untuk drawing
                'locked': is_locked
            })

    def _draw_title(self, ctx, w):
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(70)
        text = "Pilih Level"
        ext = ctx.text_extents(text)
        
        ctx.move_to(w/2 - ext.width/2 + 3, 80 + 3); ctx.set_source_rgb(0.2, 0.1, 0); ctx.show_text(text)
        ctx.move_to(w/2 - ext.width/2, 80); ctx.set_source_rgb(1, 1, 1); ctx.show_text(text)

    def _draw_level_cards(self, ctx):
        card_defs = {
            "level_easy": ("MUDAH", "Level 1-10", "GREEN"),
            "level_medium": ("SEDANG", "Level 11-20", "BLUE"),
            "level_hard": ("SULIT", "Level 21-30", "RED")
        }
        for btn in self.buttons:
            if "level" in btn['name']:
                # Gunakan VIRTUAL rect untuk menggambar
                vx, vy, vw, vh = btn['v_rect']
                title, subtitle, color = card_defs[btn['name']]
                
                state = "normal"
                if btn['name'] == self.pressed_button_name: state = "pressed"
                elif btn['name'] == self.hovered_button_name: state = "hover"
                
                draw_level_card(ctx, vx, vy, vw, vh, title, subtitle, color, state, btn['locked'])
    
    def _draw_buttons(self, ctx):
        for btn in self.buttons:
            if btn['name'] == "Kembali":
                # Gunakan VIRTUAL rect untuk menggambar
                vx, vy, vw, vh = btn['v_rect']
                
                state = "normal"
                if btn['name'] == self.pressed_button_name: state = "pressed"
                elif btn['name'] == self.hovered_button_name: state = "hover"

                draw_glossy_button(ctx, vx, vy, vw, vh, "Kembali", "ORANGE", state, font_size=25)

    def _draw_background(self, ctx, w, h):
        grad_sky = cairo.LinearGradient(0, 0, 0, h); grad_sky.add_color_stop_rgb(0, 0.0, 0.6, 0.95); grad_sky.add_color_stop_rgb(1, 0.2, 0.7, 1.0)
        ctx.set_source(grad_sky); ctx.paint()
        self._draw_sunburst(ctx, w, h)
    
    def _draw_sunburst(self, ctx, w, h):
        ctx.save()
        ctx.translate(w / 2, h / 2); ctx.set_source_rgba(1, 1, 1, 0.08)
        rotation_offset = self.animation_time * 0.001
        for i in range(0, 360, 15):
            ctx.save(); ctx.rotate((i * math.pi / 180) + rotation_offset); ctx.move_to(0, 0); ctx.line_to(w, -50); ctx.line_to(w, 50); ctx.close_path(); ctx.fill(); ctx.restore()
        ctx.restore()