# src/halaman/options.py
import gi
gi.require_version('Gtk', '3.0')
import cairo
import math
from gi.repository import Gtk, Gdk, GLib
from ..audio_manager import audio_manager
from ..components.components_menu import draw_glossy_button
from ..components.component_options import draw_slider

class OptionsScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback

        self.buttons = []
        self.hovered_button_name = None
        self.pressed_button_name = None
        self.is_dragging_slider = False

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

        GLib.timeout_add(32, self.queue_draw) # Cukup update seperlunya

    def on_enter(self):
        self._register_controls(800, 600)
        self.queue_draw()

    def on_configure(self, widget, event):
        self.width = widget.get_allocated_width()
        self.height = widget.get_allocated_height()
        self._register_controls(800, 600)
        return False

    def on_motion(self, widget, event):
        x, y = event.x, event.y
        
        # Logika untuk menggeser slider volume
        if self.is_dragging_slider:
            slider = next((b for b in self.buttons if b['name'] == 'volume_slider'), None)
            if slider:
                sx, sy, sw, sh = slider['rect']
                # Hitung persentase volume berdasarkan posisi mouse
                percentage = (x - sx) / sw
                percentage = max(0.0, min(1.0, percentage))
                audio_manager.set_volume(percentage)
                self.queue_draw() # PERBAIKAN: Paksa redraw saat slider digeser
            return

        # Logika untuk hover tombol biasa
        current_hover = None
        for btn in self.buttons:
            bx, by, bw, bh = btn['rect']
            if bx <= x < bx + bw and by <= y < by + bh:
                current_hover = btn['name']
                break
        
        if self.hovered_button_name != current_hover:
            self.hovered_button_name = current_hover
            self.queue_draw() 

    def on_button_press(self, widget, event):
        self.pressed_button_name = self.hovered_button_name
        if self.pressed_button_name == 'volume_slider':
            self.is_dragging_slider = True
            self.on_motion(widget, event)
        return True

    def on_button_release(self, widget, event):
        if self.is_dragging_slider:
            self.is_dragging_slider = False
            self.pressed_button_name = None
            return

        if self.pressed_button_name and self.pressed_button_name == self.hovered_button_name:
            name = self.pressed_button_name
            print(f"Tombol '{name}' dieksekusi!")
            if name == "Kembali":
                self.change_scene("menu_scene")
            elif "song" in name:
                song_name = name.split('_')[1] # e.g., "Lagu 1"
                audio_manager.play_song_by_name(song_name)
        
        self.pressed_button_name = None
        return True

    def on_draw(self, widget, ctx):
        v_width, v_height = 800, 600
        ctx.scale(self.width / v_width, self.height / v_height)
        
        self._draw_background(ctx, v_width, v_height)
        self._draw_title(ctx, v_width)
        self._draw_controls(ctx)

    def _register_controls(self, v_width, v_height):
        self.buttons.clear()
        scale_x = self.width / v_width
        scale_y = self.height / v_height

        v_defs = {
            "volume_slider": {'v_rect': (270, 170, 300, 40)},
            "song_Lagu 1": {'v_rect': (150, 300, 150, 60)},
            "song_Lagu 2": {'v_rect': (325, 300, 150, 60)},
            "song_Lagu 3": {'v_rect': (500, 300, 150, 60)},
            "Kembali": {'v_rect': (325, 450, 150, 60)}
        }

        for name, data in v_defs.items():
            vx, vy, vw, vh = data['v_rect']
            real_rect = (vx * scale_x, vy * scale_y, vw * scale_x, vh * scale_y)
            self.buttons.append({'name': name, 'rect': real_rect, 'v_rect': (vx, vy, vw, vh)})

    def _draw_title(self, ctx, w):
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(70)
        text = "Pengaturan"
        ext = ctx.text_extents(text)
        
        ctx.move_to(w/2 - ext.width/2 + 3, 80 + 3); ctx.set_source_rgb(0.2, 0.1, 0); ctx.show_text(text)
        ctx.move_to(w/2 - ext.width/2, 80); ctx.set_source_rgb(1, 1, 1); ctx.show_text(text)

    def _draw_controls(self, ctx):
        # Gambar label
        ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(24); ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(150, 195); ctx.show_text("Volume")
        ctx.move_to(150, 270); ctx.show_text("Pilih Lagu")

        # Gambar semua tombol dan slider
        for btn in self.buttons:
            vx, vy, vw, vh = btn['v_rect']
            name = btn['name']
            state = "normal"
            if name == self.pressed_button_name or (name == 'volume_slider' and self.is_dragging_slider): state = "pressed"
            elif name == self.hovered_button_name: state = "hover"

            if name == 'volume_slider':
                slider_state = "dragging" if self.is_dragging_slider else "normal"
                draw_slider(ctx, vx, vy, vw, vh, audio_manager.get_volume(), slider_state)
            
            elif "song" in name:
                song_name = name.split('_')[1]
                is_active = (song_name == audio_manager.get_current_song_name())
                color = "GREEN" if is_active else "ORANGE"
                draw_glossy_button(ctx, vx, vy, vw, vh, song_name, color, state, font_size=20)

            elif name == "Kembali":
                draw_glossy_button(ctx, vx, vy, vw, vh, name, "ORANGE", state, font_size=25)

    def _draw_background(self, ctx, w, h):
        grad_sky = cairo.LinearGradient(0, 0, 0, h); grad_sky.add_color_stop_rgb(0, 0.4, 0.2, 0.5); grad_sky.add_color_stop_rgb(1, 0.1, 0.0, 0.2)
        ctx.set_source(grad_sky); ctx.paint()
