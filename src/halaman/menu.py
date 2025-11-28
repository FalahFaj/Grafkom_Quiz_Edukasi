# src/scenes/menu_scene.py
import gi
gi.require_version('Gtk', '3.0')
import cairo
import math
import random
from gi.repository import Gtk, Gdk, GLib
from ..components.components_menu import draw_glossy_button, draw_logo_monster, draw_cloud

class MenuScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback

        # --- State untuk Interaksi dan Animasi ---
        self.buttons = []
        self.hovered_button_name = None
        self.pressed_button_name = None
        self.animation_time = 0

        # Inisialisasi properti awan untuk animasi berayun
        self.clouds = [
            {'x0': 150, 'y': 80, 'scale': 1.2, 'amp': 10, 'freq': 0.01},
            {'x0': 100, 'y': 200, 'scale': 0.8, 'amp': 5,  'freq': 0.008},
            {'x0': 700, 'y': 120, 'scale': 1.1, 'amp': 12, 'freq': 0.012}
        ]

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

        self._register_buttons(800, 600)
        GLib.timeout_add(16, self.on_update)

    def on_update(self):
        """Fungsi yang dipanggil berulang kali untuk semua animasi."""
        self.animation_time += 1
        
        # Minta GTK untuk menggambar ulang canvas. Perhitungan animasi
        # akan dilakukan langsung di dalam fungsi draw masing-masing.
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
            if self.pressed_button_name == "Play":
                self.change_scene("pilihan_level_scene")
            elif self.pressed_button_name == "Options":
                self.change_scene("options_scene")
            elif self.pressed_button_name == "Credit":
                self.change_scene("credit_scene")
            elif self.pressed_button_name == "Quit":
                Gtk.main_quit()
        
        self.pressed_button_name = None # Reset status press setelah dilepas

    def on_draw(self, widget, ctx):
        v_width, v_height = 800, 600
        ctx.scale(self.width / v_width, self.height / v_height)
        
        self._draw_background(ctx, v_width, v_height)
        self._draw_menu_assets(ctx, v_width, v_height)

    def _register_buttons(self, v_width, v_height):
        self.buttons.clear()
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        
        self.buttons.append({'rect': (275 * scale_x, 250 * scale_y, 250 * scale_x, 70 * scale_y), 'name': "Play", 'color': "GREEN"})
        self.buttons.append({'rect': (275 * scale_x, 330 * scale_y, 250 * scale_x, 60 * scale_y), 'name': "Options", 'color': "ORANGE"})
        self.buttons.append({'rect': (275 * scale_x, 400 * scale_y, 250 * scale_x, 60 * scale_y), 'name': "Credit", 'color': "ORANGE"})
        self.buttons.append({'rect': (275 * scale_x, 470 * scale_y, 250 * scale_x, 60 * scale_y), 'name': "Quit", 'color': "ORANGE"})

    def _draw_background(self, ctx, w, h):
        grad_sky = cairo.LinearGradient(0, 0, 0, h)
        grad_sky.add_color_stop_rgb(0, 0.0, 0.6, 0.95)
        grad_sky.add_color_stop_rgb(1, 0.2, 0.7, 1.0)
        ctx.set_source(grad_sky)
        ctx.paint()
        self._draw_sunburst(ctx, w, h)
        self._draw_pattern_hill(ctx, -80, 500, 350, 250, (0.5, 0.3, 0.6), "STRIPE")
        self._draw_pattern_hill(ctx, 580, 520, 300, 250, (0.5, 0.3, 0.6), "STAR")
        self._draw_pattern_hill(ctx, 80, 600, 250, 180, (1.0, 0.6, 0.2), "STAR")
        self._draw_pattern_hill(ctx, 500, 620, 280, 200, (0.5, 0.7, 0.2), "DOT")
        ctx.save()
        ctx.translate(180, 550)
        ctx.move_to(0, 200); ctx.curve_to(100, -50, 350, -50, 450, 200)
        ctx.set_source_rgb(0.9, 0.8, 0.1); ctx.fill()
        ctx.save(); ctx.clip()
        ctx.set_source_rgba(1, 1, 1, 0.15)
        for i in range(0, 450, 20):
            if (i//20)%2==0: ctx.rectangle(i, -50, 20, 250); ctx.fill()
        ctx.restore()
        ctx.set_source_rgb(1,1,1); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()
        self._draw_wood_frame(ctx, w, h)

    def _draw_menu_assets(self, ctx, w, h):
        # Awan berayun sesuai state animasi
        for cloud in self.clouds:
            sway = math.sin(self.animation_time * cloud['freq']) * cloud['amp']
            draw_cloud(ctx, cloud['x0'] + sway, cloud['y'], cloud['scale'])

        # Logo dengan monster yang beranimasi
        draw_logo_monster(ctx, 400, 130, time=self.animation_time)

        # Gambar tombol dengan state interaktif
        for btn_info in self.buttons:
            # Mengambil posisi dari data tombol yang sudah diskalakan
            v_x, v_y, v_w, v_h = btn_info['rect']
            # Konversi kembali ke virtual coordinates untuk drawing function
            v_x /= (self.width / 800)
            v_y /= (self.height / 600)
            v_w /= (self.width / 800)
            v_h /= (self.height / 600)

            state = "normal"
            if btn_info['name'] == self.pressed_button_name:
                state = "pressed"
            elif btn_info['name'] == self.hovered_button_name:
                state = "hover"
            
            draw_glossy_button(ctx, v_x, v_y, v_w, v_h, btn_info['name'], btn_info['color'], state)

    def _draw_sunburst(self, ctx, w, h):
        """Efek sinar matahari berputar perlahan."""
        ctx.save()
        ctx.translate(w / 2, h / 2)
        ctx.set_source_rgba(1, 1, 1, 0.1)
        # Tambahkan rotasi berdasarkan waktu animasi
        rotation_offset = self.animation_time * 0.001
        for i in range(0, 360, 15):
            ctx.save()
            ctx.rotate((i * math.pi / 180) + rotation_offset)
            ctx.move_to(0, 0)
            ctx.line_to(w, -50)
            ctx.line_to(w, 50)
            ctx.close_path()
            ctx.fill()
            ctx.restore()
        ctx.restore()

    def _draw_wood_frame(self, ctx, w, h):
        """Bingkai Kayu dengan tekstur"""
        border = 35
        # (Implementasi bingkai kayu bisa ditambahkan di sini jika ada)

    def _draw_pattern_hill(self, ctx, x, y, w, h, color, pattern):
        """Menggambar bukit berpola."""
        # (Implementasi bukit berpola bisa ditambahkan di sini jika ada)