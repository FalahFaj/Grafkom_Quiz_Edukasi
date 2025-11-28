import gi
gi.require_version('Gtk', '3.0')
import math
import cairo
import json
from gi.repository import Gtk, Gdk, GLib
from ..components import komponen_map  # Import renderer baru

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

        # Mulai animation loop
        GLib.timeout_add(16, self.on_update) # 60 FPS untuk animasi lebih smooth

    def on_update(self):
        """Dipanggil secara berkala untuk update animasi."""
        self.animation_time += 1
        self.queue_draw()
        return True

    def load_data(self):
        try:
            # Coba load dari file JSON
            with open('data/level.json', 'r') as f:
                self.level_data = json.load(f)
            with open('data/savegame.json', 'r') as f:
                self.savegame_data = json.load(f)
            
            self.unlocked_level = self.savegame_data.get('current_level', {}).get(self.difficulty, 1)

            # FALLBACK: Jika JSON kosong atau posisi belum diatur, 
            # gunakan posisi hardcoded agar terlihat bagus (Winding Path)
            if not self.level_data.get('levels'):
                self._create_default_winding_levels()

        except (FileNotFoundError, json.JSONDecodeError):
            print("Warning: Data files not found. Using default layout.")
            self.savegame_data = {}
            self.unlocked_level = 1
            self._create_default_winding_levels()

    def _create_default_winding_levels(self):
        """Membuat data level default dengan posisi melengkung seperti gambar"""
        self.level_data['levels'] = []
        # Koordinat hardcoded untuk membentuk jalur 3D yang menarik
        positions = [
            (100, 520),  # 1 - Start lebih rendah
            (220, 470),  # 2 - Naik perlahan
            (340, 500),  # 3 - Turun sedikit
            (460, 570),  # 4 - Turun lebih dalam
            (580, 520),  # 5 - Naik
            (700, 400),  # 6 - Naik tajam
            (820, 340),  # 7 - Puncak
            (940, 400),  # 8 - Turun
            (1060, 500), # 9 - Turun landai
            (1150, 470), # 10 - Naik sedikit
            (1220, 370)  # 11 - Finish di ketinggian
        ]
        
        for i, pos in enumerate(positions):
            lvl_id = i + 1
            self.level_data['levels'].append({
                'id': lvl_id,
                'pos': pos,
                'next_level': lvl_id + 1 if lvl_id < len(positions) else None
            })

    def on_enter(self, level='easy'):
        self.difficulty = level
        self.load_data()
        self._register_buttons(1280, 720)
        self.queue_draw()

    def on_motion(self, widget, event):
        x, y = event.x, event.y
        v_width, v_height = 1280, 720

        # Transformasi koordinat mouse ke virtual coordinates
        scale_x = self.width / v_width
        scale_y = self.height / v_height

        vx = x / scale_x
        vy = y / scale_y

        current_hover = None
        
        # 1. Cek tombol UI
        for btn in self.buttons:
            bx, by, bw, bh = btn['v_rect']
            if bx <= vx < bx + bw and by <= vy < by + bh:
                current_hover = btn['name']
                break
        
        # 2. Cek node Level dengan hitbox yang lebih akurat
        if not current_hover:
            levels = self.level_data.get('levels', [])
            for level in levels:
                lx, ly = level['pos']
                # Hitung jarak dengan pertimbangan animasi mengambang
                hitbox_radius = 45  # Sedikit lebih besar untuk mengakomodasi animasi
                dist_sq = (vx - lx)**2 + (vy - (ly + math.sin(self.animation_time * 0.05 + level['id']) * 3))**2
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
                    print(f"Masuk ke level {lvl_id} (Difficulty: {self.difficulty})")
                    # self.change_scene("game_scene", level=lvl_id, difficulty=self.difficulty)
                else:
                    print("Level terkunci!")

        self.pressed_button_name = None
        self.queue_draw()
        return True

    def on_draw(self, widget, ctx):
        v_width, v_height = 1280, 720
        
        # 1. Gambar latar belakang langit dengan efek atmosfer
        komponen_map.draw_sky_background(ctx, self.width, self.height, self.animation_time)

        # Scaling untuk virtual coordinates
        scale_x = self.width / v_width
        scale_y = self.height / v_height
        
        ctx.save()
        ctx.scale(scale_x, scale_y)

        # 2. Gambar pemandangan dengan efek 3D
        komponen_map.draw_foreground_scenery(ctx, v_width, v_height, self.animation_time)

        levels = self.level_data.get('levels', [])
        
        # 3. Gambar jalur dengan efek 3D
        komponen_map.draw_3d_winding_path(ctx, levels, self.animation_time)

        # 4. Gambar elemen UI
        self._draw_title(ctx, v_width)

        # 5. Gambar node level dengan efek 3D
        for level in levels:
            lvl_id = level['id']
            pos = level['pos']
            state = 'locked'
            if lvl_id < self.unlocked_level: 
                state = 'unlocked'
            elif lvl_id == self.unlocked_level: 
                state = 'current'
            
            is_hovered = (self.hovered_button_name == f"level_{lvl_id}")
            komponen_map.draw_crystal_level_node(ctx, pos[0], pos[1], lvl_id, state, is_hovered, self.animation_time)

        # 6. Gambar tombol UI dengan efek 3D
        self._draw_ui_buttons(ctx)

        # 7. Gambar progress indicator
        self._draw_progress_indicator(ctx, v_width, v_height)

        ctx.restore()

    def _register_buttons(self, v_width, v_height):
        """Mendaftarkan tombol dengan virtual coordinates."""
        self.buttons.clear()
        
        v_defs = { 
            "Kembali": {'v_rect': (30, v_height - 80, 150, 50)},
        }

        for name, data in v_defs.items():
            self.buttons.append({ 'name': name, 'v_rect': data['v_rect'] })

    def _draw_title(self, ctx, w):
        """Menggambar judul dengan efek 3D dan animasi."""
        ctx.select_font_face("Comic Sans MS", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(65)
        text = "PETA PETUALANGAN"
        ext = ctx.text_extents(text)
        
        x_pos = w/2 - ext.width/2
        y_pos = 100

        # Efek bayangan bertingkat untuk 3D
        for i in range(5, 0, -1):
            ctx.move_to(x_pos + i, y_pos + i)
            ctx.set_source_rgba(0, 0, 0, 0.1 * i)
            ctx.show_text(text)

        # Outline teks
        ctx.move_to(x_pos, y_pos)
        ctx.set_source_rgb(0.1, 0.05, 0.2)
        ctx.set_line_width(8)
        ctx.text_path(text)
        ctx.stroke()

        # Gradien teks utama
        text_grad = cairo.LinearGradient(x_pos, y_pos, x_pos, y_pos + 70)
        text_grad.add_color_stop_rgb(0, 1, 0.95, 0.7)    # Kuning terang
        text_grad.add_color_stop_rgb(0.5, 1, 0.8, 0.4)   # Kuning medium
        text_grad.add_color_stop_rgb(1, 1, 0.7, 0.2)     # Kuning gelap
        
        ctx.move_to(x_pos, y_pos)
        ctx.set_source(text_grad)
        ctx.show_text(text)

        # Highlight di atas teks
        ctx.move_to(x_pos, y_pos)
        ctx.set_source_rgba(1, 1, 1, 0.3)
        ctx.set_line_width(2)
        ctx.text_path(text)
        ctx.stroke()

    def _draw_ui_buttons(self, ctx):
        """Menggambar tombol UI dengan efek 3D."""
        for btn in self.buttons:
            vx, vy, vw, vh = btn['v_rect']
            is_hover = (btn['name'] == self.hovered_button_name)
            is_pressed = (btn['name'] == self.pressed_button_name)
            
            komponen_map.draw_ui_button(ctx, vx, vy, vw, vh, btn['name'], is_hover, is_pressed, self.animation_time)

    def _draw_progress_indicator(self, ctx, w, h):
        """Menggambar indikator progress dengan efek 3D."""
        ctx.save()
        
        total_levels = len(self.level_data.get('levels', []))
        if total_levels == 0:
            ctx.restore()
            return
            
        progress = min(self.unlocked_level / total_levels, 1.0)
        
        # Background progress bar dengan efek 3D
        bar_width = 350
        bar_height = 25
        bar_x = w/2 - bar_width/2
        bar_y = h - 45
        
        # Bayangan progress bar
        ctx.set_source_rgba(0, 0, 0, 0.5)
        komponen_map.rounded_rect(ctx, bar_x + 4, bar_y + 4, bar_width, bar_height, 12)
        ctx.fill()
        
        # Background bar
        bg_grad = cairo.LinearGradient(bar_x, bar_y, bar_x, bar_y + bar_height)
        bg_grad.add_color_stop_rgb(0, 0.3, 0.3, 0.4)
        bg_grad.add_color_stop_rgb(1, 0.2, 0.2, 0.3)
        
        ctx.set_source(bg_grad)
        komponen_map.rounded_rect(ctx, bar_x, bar_y, bar_width, bar_height, 12)
        ctx.fill()
        
        # Progress fill dengan gradien 3D
        fill_width = max(25, bar_width * progress)
        fill_grad = cairo.LinearGradient(bar_x, bar_y, bar_x, bar_y + bar_height)
        
        if progress < 0.33:
            fill_grad.add_color_stop_rgb(0, 1, 0.6, 0.6)  # Merah terang
            fill_grad.add_color_stop_rgb(0.5, 1, 0.4, 0.4)  # Merah medium
            fill_grad.add_color_stop_rgb(1, 0.8, 0.2, 0.2)  # Merah gelap
        elif progress < 0.66:
            fill_grad.add_color_stop_rgb(0, 1, 1, 0.6)    # Kuning terang
            fill_grad.add_color_stop_rgb(0.5, 1, 0.9, 0.4) # Kuning medium
            fill_grad.add_color_stop_rgb(1, 0.9, 0.7, 0.2) # Kuning gelap
        else:
            fill_grad.add_color_stop_rgb(0, 0.6, 1, 0.6)  # Hijau terang
            fill_grad.add_color_stop_rgb(0.5, 0.4, 0.9, 0.4) # Hijau medium
            fill_grad.add_color_stop_rgb(1, 0.2, 0.8, 0.2)  # Hijau gelap
        
        ctx.set_source(fill_grad)
        komponen_map.rounded_rect(ctx, bar_x, bar_y, fill_width, bar_height, 12)
        ctx.fill()
        
        # Highlight di atas progress bar
        highlight_grad = cairo.LinearGradient(bar_x, bar_y, bar_x, bar_y + bar_height/2)
        highlight_grad.add_color_stop_rgba(0, 1, 1, 1, 0.3)
        highlight_grad.add_color_stop_rgba(1, 1, 1, 1, 0)
        
        ctx.set_source(highlight_grad)
        komponen_map.rounded_rect(ctx, bar_x, bar_y, fill_width, bar_height/2, 12)
        ctx.fill()
        
        # Border progress bar
        ctx.set_source_rgba(1, 1, 1, 0.8)
        komponen_map.rounded_rect(ctx, bar_x, bar_y, bar_width, bar_height, 12)
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Teks progress dengan efek 3D
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(16)
        progress_text = f"PROGRESS: {self.unlocked_level}/{total_levels} • {int(progress * 100)}%"
        text_extents = ctx.text_extents(progress_text)
        
        text_x = w/2 - text_extents.width/2
        text_y = bar_y - 15
        
        # Bayangan teks
        ctx.move_to(text_x + 2, text_y + 2)
        ctx.set_source_rgba(0, 0, 0, 0.6)
        ctx.show_text(progress_text)
        
        # Teks utama dengan gradien
        text_grad = cairo.LinearGradient(text_x, text_y, text_x, text_y + 20)
        text_grad.add_color_stop_rgb(0, 1, 1, 1)
        text_grad.add_color_stop_rgb(1, 0.8, 0.8, 0.8)
        
        ctx.move_to(text_x, text_y)
        ctx.set_source(text_grad)
        ctx.show_text(progress_text)
        
        ctx.restore()