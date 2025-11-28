# src/halaman/credit_scene.py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
from ..components import components_credit
from ..components.components_menu import draw_glossy_button

class CreditScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback

        # State
        self.animation_time = 0
        self.scroll_y = 0
        self.scroll_speed = 0.9 
        
        self.buttons = []
        self.hovered_button_name = None
        self.pressed_button_name = None

        self.credits_data = [
            {'role': 'Kelompok', 'name': 'Kelompok 9'},
            {'role': 'Pertama', 'name': 'Muhammad Fajrul Falah'},
            {'role': 'Art & Animation', 'name': 'Falah'},
            {'role': 'Sound Design', 'name': 'Falah'},
            {'role': 'Special Thanks', 'name': 'Allah SWT'},
            {'role': 'Special Thanks', 'name': 'Orang Tua'},
            {'role': 'Special Thanks', 'name': 'Diri Sendiri'},
            {'role': 'Special Thanks', 'name': 'Teman-Teman'},
            {'role': 'Terima Kasih Telah Bermain!', 'name': ''},
        ]

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion)

        self._register_buttons(800, 600)
        GLib.timeout_add(16, self.on_update)

    def on_enter(self):
        """Dipanggil saat scene ini ditampilkan."""
        self.scroll_y = 0 # Reset scroll setiap kali masuk scene
        self.queue_draw()

    def on_update(self):
        """Update animasi dan scroll."""
        self.animation_time += 1
        self.scroll_y += self.scroll_speed
        
        # Reset scroll jika sudah selesai
        total_height = len(self.credits_data) * 110
        if self.scroll_y > total_height + self.height:
            self.scroll_y = 0
            
        self.queue_draw()
        return True

    def on_draw(self, widget, ctx):
        v_width, v_height = 800, 600
        
        # Scaling agar konsisten di berbagai resolusi
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        ctx.scale(scale_x, scale_y)

        # Gambar elemen dari components_credit
        components_credit.draw_starry_background(ctx, v_width, v_height, self.animation_time)
        components_credit.draw_credit_title(ctx, v_width)
        components_credit.draw_scrolling_credits(ctx, v_width, v_height, self.scroll_y, self.credits_data)
        
        # Gambar tombol
        self._draw_buttons(ctx)

    def _register_buttons(self, v_width, v_height):
        """Mendaftarkan tombol kembali."""
        self.buttons.clear()
        # Tombol kembali di pojok kiri bawah
        self.buttons.append({
            'rect': (30, v_height - 80, 150, 50),
            'name': "Kembali",
            'color': "PURPLE"
        })

    def _draw_buttons(self, ctx):
        """Menggambar semua tombol terdaftar."""
        for btn in self.buttons:
            x, y, w, h = btn['rect']
            state = "normal"
            if btn['name'] == self.pressed_button_name:
                state = "pressed"
            elif btn['name'] == self.hovered_button_name:
                state = "hover"
            
            draw_glossy_button(ctx, x, y, w, h, btn['name'], btn['color'], state, font_size=20)

    def on_motion(self, widget, event):
        """Mendeteksi hover pada tombol."""
        v_width, v_height = 800, 600
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        
        vx = event.x / scale_x
        vy = event.y / scale_y

        current_hover = None
        for btn in self.buttons:
            bx, by, bw, bh = btn['rect']
            if bx <= vx < bx + bw and by <= vy < by + bh:
                current_hover = btn['name']
                break
        
        if self.hovered_button_name != current_hover:
            self.hovered_button_name = current_hover
            self.queue_draw()

    def on_button_press(self, widget, event):
        """Menangani event tombol ditekan."""
        self.pressed_button_name = self.hovered_button_name
        self.queue_draw()
        return True

    def on_button_release(self, widget, event):
        """Menangani event tombol dilepas."""
        if self.pressed_button_name and self.pressed_button_name == self.hovered_button_name:
            if self.pressed_button_name == "Kembali":
                self.change_scene("menu_scene")
        
        self.pressed_button_name = None
        self.queue_draw()
        return True
