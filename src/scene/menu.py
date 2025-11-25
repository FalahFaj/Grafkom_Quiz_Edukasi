# src/scenes/menu_scene.py
import gi
gi.require_version('Gtk', '3.0')
import cairo
import math
import random
from gi.repository import Gtk, Gdk
from src.components import draw_glossy_button
# Kita juga perlu logo dan awan dari components
from src.components import draw_logo_monster, draw_cloud

# --- Kelas MenuScene ---
class MenuScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        # Hapus inisialisasi ukuran tetap, kita akan mendapatkannya dari event
        self.width = 1 
        self.height = 1

        self.change_scene = change_scene_callback # Fungsi untuk pindah level
        
        # Area tombol (untuk deteksi klik). Format: (x, y, w, h, nama)
        # Skala virtual 800x600
        scale_x = self.width / 800
        scale_y = self.height / 600
        
        self.buttons = [] 
        
        # Aktifkan deteksi mouse
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("configure-event", self.on_configure) # <-- TAMBAHKAN INI
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_click)

    def on_configure(self, widget, event):
        """Dipanggil saat ukuran widget berubah (responsif)."""
        # Dapatkan ukuran baru dari alokasi widget
        new_width = widget.get_allocated_width()
        new_height = widget.get_allocated_height()
        self.width = new_width
        self.height = new_height
        return False # Lanjutkan propagasi event

    def on_click(self, widget, event):
        """Dipanggil saat mouse diklik di area gambar."""
        click_x, click_y = event.x, event.y
        
        # Periksa apakah klik mengenai salah satu tombol
        for x, y, w, h, name in self.buttons:
            if x <= click_x < x + w and y <= click_y < y + h:
                print(f"Tombol '{name}' diklik!")
                if name == "Play":
                    # Panggil callback untuk pindah ke scene peta level
                    self.change_scene("map_scene")
                # Tambahkan logika untuk tombol lain jika perlu
                break

    def on_draw(self, widget, ctx):
        """Fungsi utama untuk menggambar semua elemen di menu."""
        # Skala ke kanvas virtual 800x600 agar gambar konsisten
        ctx.scale(self.width / 800, self.height / 600)
        
        # 1. Gambar Latar Belakang (dari Menu_bg.py)
        self._draw_background(ctx, 800, 600)
        
        # 2. Gambar Aset Menu (dari components.py/Menu_assets.py)
        self._draw_menu_assets(ctx, 800, 600)
        
        # Kosongkan daftar tombol lama dan buat yang baru
        self.buttons.clear()
        self._register_buttons(800, 600)

    def _register_buttons(self, v_width, v_height):
        """Mendaftarkan area tombol untuk deteksi klik."""
        # Koordinat tombol disesuaikan dengan skala window
        scale_x = self.width / v_width
        scale_y = self.height / v_height

        # Tombol Play
        self.buttons.append((250 * scale_x, 250 * scale_y, 300 * scale_x, 80 * scale_y, "Play"))
        # Tombol Options
        self.buttons.append((250 * scale_x, 345 * scale_y, 300 * scale_x, 70 * scale_y, "Options"))
        # Tombol Help
        self.buttons.append((250 * scale_x, 430 * scale_y, 300 * scale_x, 70 * scale_y, "Help"))

    # --- Fungsi-fungsi Helper untuk Menggambar ---

    def _draw_background(self, ctx, w, h):
        """Menggambar semua elemen latar belakang: langit, bukit, bingkai."""
        # Langit Biru Cerah
        grad_sky = cairo.LinearGradient(0, 0, 0, h)
        grad_sky.add_color_stop_rgb(0, 0.0, 0.6, 0.95)
        grad_sky.add_color_stop_rgb(1, 0.2, 0.7, 1.0)
        ctx.set_source(grad_sky)
        ctx.paint()
        
        # Efek Sunburst
        self._draw_sunburst(ctx, w, h)

        # Bukit-Bukit
        self._draw_pattern_hill(ctx, -80, 500, 350, 250, (0.5, 0.3, 0.6), "STRIPE")
        self._draw_pattern_hill(ctx, 580, 520, 300, 250, (0.5, 0.3, 0.6), "STAR")
        self._draw_pattern_hill(ctx, 80, 600, 250, 180, (1.0, 0.6, 0.2), "STAR")
        self._draw_pattern_hill(ctx, 500, 620, 280, 200, (0.5, 0.7, 0.2), "DOT")
        
        # Bukit Kuning di tengah
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

        # Bingkai Kayu
        self._draw_wood_frame(ctx, w, h)

    def _draw_menu_assets(self, ctx, w, h):
        """Menggambar aset utama menu: awan, logo, dan tombol."""
        # Awan Gantung
        draw_cloud(ctx, 150, 80, 1.2)
        draw_cloud(ctx, 100, 200, 0.8)
        draw_cloud(ctx, 700, 120, 1.1)

        # Logo Utama
        draw_logo_monster(ctx, 400, 130)

        # Tombol-tombol
        draw_glossy_button(ctx, 250, 250, 300, 80, "Play", "GREEN")
        draw_glossy_button(ctx, 250, 345, 300, 70, "Options", "ORANGE")
        draw_glossy_button(ctx, 250, 430, 300, 70, "Help", "ORANGE")

    def _draw_sunburst(self, ctx, w, h):
        """Efek sinar matahari berputar samar di latar belakang"""
        ctx.save()
        ctx.translate(w/2, h/2)
        ctx.set_source_rgba(1, 1, 1, 0.1)
        for i in range(0, 360, 15):
            ctx.save()
            ctx.rotate(i * math.pi / 180)
            ctx.move_to(0, 0); ctx.line_to(w, -50); ctx.line_to(w, 50); ctx.close_path(); ctx.fill()
            ctx.restore()
        ctx.restore()

    def _draw_wood_frame(self, ctx, w, h):
        """Bingkai Kayu dengan tekstur"""
        border = 35
        # ... (Implementasi bingkai kayu tetap sama, hanya dipindahkan)

    def _draw_pattern_hill(self, ctx, x, y, w, h, color, pattern):
        """Menggambar bukit berpola."""
        # ... (Implementasi bukit tetap sama, hanya dipindahkan)