# src/halaman/game_scene.py
import gi
gi.require_version('Gtk', '3.0')
import json
import time
import random
from gi.repository import Gtk, Gdk, GLib

# Import logika game dan komponen
from ..game_logic import QuestionGenerator
from ..components.components_menu import draw_glossy_button
from ..audio_manager import audio_manager
from ..components import component_game 

# Import gambar feedback
import assets.images.benar as img_benar
import assets.images.salah as img_salah

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
        
        # Posisi tombol pilihan jawaban
        start_y = 430 
        
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

        # Tombol Keluar (Pojok kiri bawah)
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

    def on_draw(self, widget, ctx):
        # Scale ke Virtual Resolution 800x600
        ctx.scale(self.width / 800, self.height / 600)
        
        # 1. Background Dinamis 
        component_game.draw_game_background(ctx, 800, 600, self.difficulty)
        
        # 2. HUD (Nyawa, Waktu, Info Level) 
        component_game.draw_hud(
            ctx, 800, 600, 
            self.lives, self.timer, self.difficulty, self.get_display_level()
        )

        # 3. Konten Soal (Buah, Operator, Text Soal)
        if self.current_question:
            component_game.draw_question_visuals(ctx, 800, 600, self.current_question)

        # 4. Tombol Jawaban & Navigasi
        for btn in self.buttons:
            state = "hover" if btn['name'] == self.hovered_button else "normal"
            color = "BLUE" if btn['type'] == 'answer' else "RED"
            font_s = 28 if btn['type'] == 'answer' else 18
            
            draw_glossy_button(ctx, *btn['rect'], btn['text'], color, state, font_size=font_s)

        # 5. Overlay Feedback (Benar/Salah)
        if self.show_feedback:
            ctx.save()
            # Overlay Gelap
            ctx.set_source_rgba(0, 0, 0, 0.4)
            ctx.rectangle(0, 0, 800, 600)
            ctx.fill()
            
            # Gambar Icon Benar/Salah di tengah
            ctx.translate(400, 300)
            if self.feedback_type == 'correct':
                img_benar.gambar(ctx, 0, 0)
            else:
                img_salah.gambar(ctx, 0, 0)
            ctx.restore()