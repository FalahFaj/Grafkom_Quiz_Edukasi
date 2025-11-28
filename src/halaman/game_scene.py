# src/halaman/game_scene.py
import gi
gi.require_version('Gtk', '3.0')
import cairo
import math
import json
import time
import random
from gi.repository import Gtk, Gdk, GLib

from ..game_logic import QuestionGenerator
from ..components.components_menu import draw_glossy_button
from ..audio_manager import audio_manager

import assets.images.apel as img_apel
import assets.images.jeruk as img_jeruk
import assets.images.hati as img_hati
import assets.images.benar as img_benar
import assets.images.salah as img_salah
import assets.images.jam as img_jam

class GameScene(Gtk.DrawingArea):
    def __init__(self, window_width, window_height, change_scene_callback):
        super().__init__()
        self.width = window_width
        self.height = window_height
        self.change_scene = change_scene_callback
        
        self.generator = QuestionGenerator()
        
        self.level = 1
        self.difficulty = "easy"
        self.lives = 3
        self.timer = 60
        
        self.current_question = None
        self.buttons = []
        self.hovered_button = None
        
        self.show_feedback = False
        self.feedback_type = None
        self.feedback_timer = 0

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_click)
        self.connect("motion-notify-event", self.on_motion)
        
        GLib.timeout_add_seconds(1, self.update_timer)
        GLib.timeout_add(16, self.on_animate)

    def on_enter(self, level=1, difficulty="easy"):
        random.seed(time.time())
        self.level = level
        self.difficulty = difficulty
        self.lives = 3
        self.load_new_question()

    def get_display_level(self):
        """Menghitung nomor level untuk tampilan (continue 1-30)"""
        offset = 0
        if self.difficulty == "medium":
            offset = 10
        elif self.difficulty == "hard":
            offset = 20
        return self.level + offset

    def load_new_question(self):
        self.timer = 60 
        self.current_question = self.generator.generate(self.difficulty, self.level)
        self._register_buttons()
        self.show_feedback = False
        self.queue_draw()

    def update_timer(self):
        if not self.show_feedback and self.timer > 0:
            self.timer -= 1
            if self.timer <= 0:
                self.handle_wrong_answer()
            self.queue_draw()
        return True

    def on_animate(self):
        if self.show_feedback:
            self.feedback_timer += 1
            if self.feedback_timer > 90:
                self.process_next_step()
        self.queue_draw()
        return True

    def _register_buttons(self):
        self.buttons = []
        if not self.current_question: return
        
        choices = self.current_question['choices']
        w, h = 160, 55 
        gap_x = 40
        gap_y = 20
        
        total_w = 2 * w + gap_x
        start_x = (800 - total_w) / 2
        
        # DIGESER KE ATAS (Sebelumnya 480)
        start_y = 420 
        
        for i, ans in enumerate(choices):
            col = i % 2
            row = i // 2
            x = start_x + col * (w + gap_x)
            y = start_y + row * (h + gap_y)
            
            self.buttons.append({
                'rect': (x, y, w, h),
                'text': str(ans),
                'val': ans,
                'name': f"ans_{i}",
                'type': 'answer'
            })

        # Tombol Keluar (Tetap di pojok kiri bawah)
        self.buttons.append({
            'rect': (20, 540, 100, 40), 
            'text': "Keluar", 
            'val': "back", 
            'name': "back", 
            'type': 'nav'
        })

    def on_click(self, widget, event):
        if self.show_feedback: return
        mx = event.x * (800 / self.width)
        my = event.y * (600 / self.height)

        for btn in self.buttons:
            bx, by, bw, bh = btn['rect']
            if bx <= mx <= bx+bw and by <= my <= by+bh:
                if btn['type'] == 'nav':
                    self.change_scene("map_scene", level=self.difficulty)
                else:
                    self.check_answer(btn['val'])
                break

    def check_answer(self, value):
        correct = self.current_question['ans']
        self.feedback_timer = 0
        self.show_feedback = True
        
        if value == correct:
            self.feedback_type = 'correct'
            print("Benar!")
        else:
            self.feedback_type = 'wrong'
            print("Salah!")

    def handle_wrong_answer(self):
        self.feedback_timer = 0
        self.show_feedback = True
        self.feedback_type = 'wrong'

    def process_next_step(self):
        self.show_feedback = False
        
        if self.feedback_type == 'correct':
            self.level += 1
            if self.level > 10:
                self.update_save_data(level=10, unlock_next=True)
                self.change_scene("map_scene", level=self.difficulty)
            else:
                self.update_save_data(level=self.level)
                self.load_new_question() 
        else:
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over. Reset ke Level 1.")
                self.update_save_data(level=1)
                self.change_scene("map_scene", level=self.difficulty)
            else:
                self.load_new_question() 

    def update_save_data(self, level, unlock_next=False):
        try:
            with open('data/savegame.json', 'r') as f:
                data = json.load(f)
            
            data['current_level'][self.difficulty] = level
            
            if unlock_next:
                if self.difficulty == 'easy' and 'medium' not in data['unlocked_levels']:
                    data['unlocked_levels'].append('medium')
                elif self.difficulty == 'medium' and 'hard' not in data['unlocked_levels']:
                    data['unlocked_levels'].append('hard')
            
            with open('data/savegame.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Save error: {e}")

    def on_motion(self, widget, event):
        mx = event.x * (800 / self.width)
        my = event.y * (600 / self.height)
        self.hovered_button = None
        for btn in self.buttons:
            bx, by, bw, bh = btn['rect']
            if bx <= mx <= bx+bw and by <= my <= by+bh:
                self.hovered_button = btn['name']
        self.queue_draw()

    # --- DRAWING VISUALS ---

    def draw_bg_dynamic(self, ctx):
        """Menggambar background berdasarkan difficulty"""
        if self.difficulty == "easy":
            # --- PAGI (Biru Cerah) ---
            pat = cairo.LinearGradient(0, 0, 0, 600)
            pat.add_color_stop_rgb(0, 0.4, 0.8, 1.0) # Langit Biru
            pat.add_color_stop_rgb(1, 0.6, 0.9, 1.0)
            ctx.set_source(pat); ctx.paint()

            # Matahari Kuning Cerah
            ctx.save(); ctx.translate(100, 100)
            ctx.set_source_rgb(1, 0.9, 0.2)
            ctx.arc(0, 0, 50, 0, 2*math.pi); ctx.fill()
            ctx.restore()
            
            # Bukit Hijau Segar
            ctx.set_source_rgb(0.3, 0.8, 0.3)
            
        elif self.difficulty == "medium":
            # --- SORE (Oranye/Ungu) ---
            pat = cairo.LinearGradient(0, 0, 0, 600)
            pat.add_color_stop_rgb(0, 0.2, 0.1, 0.4) # Ungu Tua Atas
            pat.add_color_stop_rgb(0.6, 0.8, 0.4, 0.2) # Pink/Oranye
            pat.add_color_stop_rgb(1, 1.0, 0.7, 0.3) # Kuning Bawah
            ctx.set_source(pat); ctx.paint()

            # Matahari Terbenam (Oren Kemerahan)
            ctx.save(); ctx.translate(400, 450)
            ctx.set_source_rgba(1, 0.5, 0.1, 0.8)
            ctx.arc(0, 0, 100, 0, 2*math.pi); ctx.fill()
            ctx.restore()

            # Bukit Lebih Gelap/Kecoklatan
            ctx.set_source_rgb(0.4, 0.5, 0.2)

        else: # hard
            # --- MALAM (Biru Gelap) ---
            pat = cairo.LinearGradient(0, 0, 0, 600)
            pat.add_color_stop_rgb(0, 0.05, 0.05, 0.2) # Biru Gelap
            pat.add_color_stop_rgb(1, 0.1, 0.1, 0.3)
            ctx.set_source(pat); ctx.paint()

            # Bulan Sabit
            ctx.save(); ctx.translate(700, 100)
            ctx.set_source_rgb(0.9, 0.9, 1.0)
            ctx.arc(0, 0, 40, 0, 2*math.pi); ctx.fill()
            ctx.set_source_rgb(0.05, 0.05, 0.2) # Timpa dengan warna langit
            ctx.arc(-20, 0, 40, 0, 2*math.pi); ctx.fill()
            ctx.restore()

            # Bintang-bintang
            random.seed(42) # Seed statis biar bintang ga kedip aneh
            ctx.set_source_rgba(1, 1, 1, 0.6)
            for _ in range(30):
                bx = random.randint(0, 800)
                by = random.randint(0, 400)
                ctx.arc(bx, by, random.randint(1, 3), 0, 2*math.pi)
                ctx.fill()
            random.seed(time.time()) # Balikin random

            # Bukit Gelap
            ctx.set_source_rgb(0.1, 0.2, 0.1)

        # Gambar Bukit (Bentuk sama, warna beda sesuai set_source_rgb diatas)
        ctx.move_to(0, 600)
        ctx.line_to(0, 500)
        ctx.curve_to(200, 450, 600, 550, 800, 480)
        ctx.line_to(800, 600)
        ctx.close_path()
        ctx.fill()

    def draw_rounded_rect(self, ctx, x, y, w, h, r):
        ctx.new_path()
        ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        ctx.arc(x + w - r, y + r, r, 3 * math.pi / 2, 0)
        ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        ctx.close_path()

    def draw_fruit_group(self, ctx, count, fruit_type, center_x, center_y):
        renderer = img_apel if fruit_type == "apel" else img_jeruk
        
        # Grid layout
        cols = 4
        rows = math.ceil(count / cols)
        size = 45 
        
        # Hitung Ukuran Kontainer Background
        total_w = min(count, cols) * size
        total_h = rows * size
        padding = 15

        # 1. Gambar Background Kontainer Buah (Transparan Putih)
        ctx.save()
        ctx.translate(center_x, center_y)
        ctx.set_source_rgba(1, 1, 1, 0.3) # Putih transparan
        # Pusatkan rect
        self.draw_rounded_rect(ctx, -total_w/2 - padding, -total_h/2 - padding, 
                               total_w + padding*2, total_h + padding*2, 15)
        ctx.fill()
        # Border tipis
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.restore()

        # 2. Gambar Buah
        ctx.save()
        ctx.translate(center_x, center_y)
        
        start_x = -((min(count, cols) * size) / 2) + size/2
        start_y = -((rows * size) / 2) + size/2
        
        for i in range(count):
            c = i % cols
            r = i // cols
            ctx.save()
            ctx.translate(start_x + c*size, start_y + r*size)
            ctx.scale(0.12, 0.12)
            renderer.gambar(ctx, 0, 0)
            ctx.restore()
        ctx.restore()

    def on_draw(self, widget, ctx):
        ctx.scale(self.width / 800, self.height / 600)
        
        # BACKGROUND DINAMIS
        self.draw_bg_dynamic(ctx)
        
        # --- 1. HUD ---
        # Nyawa (Kiri Atas) - DIRENGGANGKAN
        ctx.save(); ctx.translate(30, 30)
        for i in range(self.lives):
            ctx.save()
            ctx.translate(i * 55, 0) # Jarak diperlebar (40 -> 55)
            ctx.scale(0.25, 0.25)
            img_hati.gambar(ctx, 0, 0)
            ctx.restore()
        ctx.restore()

        # Timer (Kanan Atas)
        ctx.save(); ctx.translate(720, 40)
        ctx.save(); ctx.scale(0.3, 0.3); img_jam.gambar(ctx, 0, 0, 0); ctx.restore()
        ctx.set_font_size(24)
        ctx.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb(1, 1, 1) if self.timer > 10 else ctx.set_source_rgb(1, 0, 0)
        ctx.move_to(-15, 45); ctx.show_text(f"{self.timer}s")
        ctx.restore()

        # Info Level (Tengah Atas)
        # Warna teks disesuaikan background
        if self.difficulty == "hard":
            ctx.set_source_rgb(1, 1, 1) # Putih di malam
        else:
            ctx.set_source_rgb(0, 0.3, 0.6) # Biru di siang/sore

        ctx.set_font_size(30)
        # Menampilkan Level Kontinu (11, 21, dst)
        display_level = self.get_display_level()
        label = f"LEVEL {display_level}"
        ext = ctx.text_extents(label)
        ctx.move_to((800 - ext.width)/2, 50)
        ctx.show_text(label)

        # --- 2. KONTEN SOAL ---
        if self.current_question:
            q = self.current_question
            
            # Koordinat Baru (Buah & Operator Naik Sedikit)
            y_visual = 200 # Posisi tengah buah
            y_soal = 350   # Posisi teks soal
            
            x_left = 220
            x_right = 580
            x_mid = 400 
            
            op_char = "+"
            if q['op'] == "x": op_char = "×"
            elif q['op'] == ":": op_char = "÷"
            elif q['op'] == "-": op_char = "-"

            # A. VISUAL BUAH & OPERATOR (Di Tengah)
            self.draw_fruit_group(ctx, q['a'], q['fruit'], x_left, y_visual)
            
            # Operator di Tengah
            ctx.set_font_size(70)
            ctx.set_source_rgb(1, 1, 1) # Putih
            # Shadow
            ctx.move_to(x_mid - 20 + 3, y_visual + 20 + 3)
            ctx.set_source_rgba(0,0,0,0.5); ctx.show_text(op_char)
            # Utama
            ctx.move_to(x_mid - 20, y_visual + 20)
            ctx.set_source_rgb(1, 1, 1); ctx.show_text(op_char)
            
            self.draw_fruit_group(ctx, q['b'], q['fruit'], x_right, y_visual)

            # B. SOAL LENGKAP (Di Bawah Buah)
            # Format: "4 + 2 = ?"
            full_q = f"{q['a']}  {op_char}  {q['b']}  =  ?"
            
            # Box background soal biar kebaca
            ctx.set_font_size(50)
            ext_q = ctx.text_extents(full_q)
            q_x = (800 - ext_q.width)/2
            
            ctx.set_source_rgba(1, 1, 1, 0.6)
            self.draw_rounded_rect(ctx, q_x - 20, y_soal - 50, ext_q.width + 40, 70, 10)
            ctx.fill()

            ctx.set_source_rgb(0, 0, 0.4) 
            ctx.move_to(q_x, y_soal)
            ctx.show_text(full_q)

        # --- 3. TOMBOL (Sudah digeser ke atas di _register_buttons) ---
        for btn in self.buttons:
            state = "hover" if btn['name'] == self.hovered_button else "normal"
            color = "BLUE" if btn['type'] == 'answer' else "RED"
            font_s = 28 if btn['type'] == 'answer' else 18
            draw_glossy_button(ctx, *btn['rect'], btn['text'], color, state, font_size=font_s)

        # --- 4. FEEDBACK ---
        if self.show_feedback:
            ctx.save()
            ctx.set_source_rgba(0, 0, 0, 0.4)
            ctx.rectangle(0, 0, 800, 600)
            ctx.fill()
            ctx.translate(400, 300)
            if self.feedback_type == 'correct':
                img_benar.gambar(ctx, 0, 0)
            else:
                img_salah.gambar(ctx, 0, 0)
            ctx.restore()