#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
import math
import time
import random

class EduQuizGame(Gtk.Window):
    def __init__(self):
        super().__init__(title="EduQuiz")
        
        # Set fullscreen
        self.fullscreen()
        
        # Game state
        self.current_page = "menu"
        self.sound_enabled = True
        
        # Animation variables
        self.animation_time = 0
        self.stars = []
        self.particles = []
        self.hovered_button = None
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Initialize stars for background
        for i in range(50):
            self.stars.append({
                'x': random.uniform(0, 1),
                'y': random.uniform(0, 1),
                'size': random.uniform(1, 4),
                'speed': random.uniform(0.0001, 0.0005),
                'opacity': random.uniform(0.3, 1.0),
                'twinkle_speed': random.uniform(0.5, 2.0)
            })
        
        # Create drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)
        
        # Mouse events
        self.drawing_area.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK | 
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.drawing_area.connect("button-press-event", self.on_mouse_click)
        self.drawing_area.connect("motion-notify-event", self.on_mouse_move)
        
        # Keyboard events
        self.connect("key-press-event", self.on_key_press)
        
        # Button positions
        self.buttons = []
        
        # Start animation loop
        GLib.timeout_add(16, self.update_animation)  # ~60 FPS
        
        self.show_all()
    
    def update_animation(self):
        self.animation_time += 0.016
        
        # Update particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # gravity
            particle['life'] -= 0.02
            particle['opacity'] = particle['life']
        
        self.drawing_area.queue_draw()
        return True
    
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            if self.current_page == "menu":
                Gtk.main_quit()
            else:
                self.current_page = "menu"
                self.hovered_button = None
                self.drawing_area.queue_draw()
    
    def on_mouse_move(self, widget, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
        # Check hover state
        old_hover = self.hovered_button
        self.hovered_button = None
        
        for i, btn in enumerate(self.buttons):
            if btn["x"] <= event.x <= btn["x"] + btn["width"] and \
               btn["y"] <= event.y <= btn["y"] + btn["height"]:
                self.hovered_button = i
                break
        
        if old_hover != self.hovered_button:
            self.drawing_area.queue_draw()
    
    def on_mouse_click(self, widget, event):
        x, y = event.x, event.y
        
        # Create click particles
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'opacity': 1.0,
                'color': (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
            })
        
        # Check button clicks
        for btn in self.buttons:
            if btn["x"] <= x <= btn["x"] + btn["width"] and \
               btn["y"] <= y <= btn["y"] + btn["height"]:
                self.handle_button_click(btn["action"])
                break
    
    def handle_button_click(self, action):
        if action == "play":
            self.current_page = "level"
        elif action == "option":
            self.current_page = "option"
        elif action == "credit":
            self.current_page = "credit"
        elif action == "quit":
            Gtk.main_quit()
        elif action == "back":
            self.current_page = "menu"
        elif action == "toggle_sound":
            self.sound_enabled = not self.sound_enabled
        
        self.drawing_area.queue_draw()
    
    def draw_button(self, cr, x, y, width, height, text, action, index):
        is_hovered = (self.hovered_button == index)
        
        # Store button position
        self.buttons.append({
            "x": x, "y": y, "width": width, "height": height, "action": action
        })
        
        # Hover effect - scale and glow
        if is_hovered:
            scale = 1.05
            glow_size = 8
            offset_x = width * (scale - 1) / 2
            offset_y = height * (scale - 1) / 2
            
            # Glow effect
            cr.set_source_rgba(0.3, 0.6, 1.0, 0.3)
            self.draw_rounded_rect(cr, x - offset_x - glow_size, y - offset_y - glow_size, 
                                 width * scale + glow_size * 2, height * scale + glow_size * 2, 20)
            cr.fill()
            
            x -= offset_x
            y -= offset_y
            width *= scale
            height *= scale
        
        # Animated gradient
        pulse = math.sin(self.animation_time * 2) * 0.1 + 0.9
        gradient = cairo.LinearGradient(x, y, x, y + height)
        
        if is_hovered:
            gradient.add_color_stop_rgb(0, 0.4 * pulse, 0.7 * pulse, 1.0 * pulse)
            gradient.add_color_stop_rgb(1, 0.3 * pulse, 0.5 * pulse, 0.9 * pulse)
        else:
            gradient.add_color_stop_rgb(0, 0.3, 0.6, 0.9)
            gradient.add_color_stop_rgb(1, 0.2, 0.4, 0.7)
        
        cr.set_source(gradient)
        self.draw_rounded_rect(cr, x, y, width, height, 15)
        cr.fill()
        
        # Shine effect
        shine = cairo.LinearGradient(x, y, x, y + height * 0.5)
        shine.add_color_stop_rgba(0, 1, 1, 1, 0.3)
        shine.add_color_stop_rgba(1, 1, 1, 1, 0)
        cr.set_source(shine)
        self.draw_rounded_rect(cr, x, y, width, height * 0.5, 15)
        cr.fill()
        
        # Border with glow
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(3 if is_hovered else 2)
        self.draw_rounded_rect(cr, x, y, width, height, 15)
        cr.stroke()
        
        # Text with shadow
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        font_size = 32 if is_hovered else 28
        cr.set_font_size(font_size)
        
        extents = cr.text_extents(text)
        text_x = x + (width - extents.width) / 2
        text_y = y + (height + extents.height) / 2
        
        # Shadow
        cr.move_to(text_x + 2, text_y + 2)
        cr.show_text(text)
        
        # Actual text
        cr.set_source_rgb(1, 1, 1)
        cr.move_to(text_x, text_y)
        cr.show_text(text)
    
    def draw_rounded_rect(self, cr, x, y, width, height, radius):
        cr.arc(x + radius, y + radius, radius, math.pi, 3 * math.pi / 2)
        cr.arc(x + width - radius, y + radius, radius, 3 * math.pi / 2, 0)
        cr.arc(x + width - radius, y + height - radius, radius, 0, math.pi / 2)
        cr.arc(x + radius, y + height - radius, radius, math.pi / 2, math.pi)
        cr.close_path()
    
    def draw_particles(self, cr):
        for particle in self.particles:
            cr.set_source_rgba(*particle['color'], particle['opacity'])
            cr.arc(particle['x'], particle['y'], 3, 0, 2 * math.pi)
            cr.fill()
    
    def draw_animated_stars(self, cr, width, height):
        for star in self.stars:
            # Update position
            star['y'] += star['speed']
            if star['y'] > 1:
                star['y'] = 0
                star['x'] = random.uniform(0, 1)
            
            # Twinkle effect
            twinkle = abs(math.sin(self.animation_time * star['twinkle_speed']))
            opacity = star['opacity'] * twinkle
            
            x = star['x'] * width
            y = star['y'] * height
            
            # Draw star with glow
            cr.set_source_rgba(1, 1, 1, opacity * 0.3)
            cr.arc(x, y, star['size'] * 2, 0, 2 * math.pi)
            cr.fill()
            
            cr.set_source_rgba(1, 1, 0.8, opacity)
            cr.arc(x, y, star['size'], 0, 2 * math.pi)
            cr.fill()
    
    def draw_menu(self, cr, width, height):
        self.buttons = []
        
        # Animated background gradient
        wave = math.sin(self.animation_time * 0.5) * 0.1
        gradient = cairo.LinearGradient(0, 0, 0, height)
        gradient.add_color_stop_rgb(0, 0.1 + wave, 0.2 + wave, 0.4 + wave)
        gradient.add_color_stop_rgb(0.5, 0.15 + wave, 0.25 + wave, 0.45 + wave)
        gradient.add_color_stop_rgb(1, 0.2 + wave, 0.3 + wave, 0.5 + wave)
        cr.set_source(gradient)
        cr.paint()
        
        # Animated stars
        self.draw_animated_stars(cr, width, height)
        
        # Animated title with glow
        bounce = math.sin(self.animation_time * 2) * 10
        
        # Title glow
        cr.set_source_rgba(1, 1, 0.3, 0.5)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(85)
        text = "EDUQUIZ"
        extents = cr.text_extents(text)
        title_x = (width - extents.width) / 2
        title_y = 150 + bounce
        
        for i in range(3):
            cr.move_to(title_x, title_y)
            cr.text_path(text)
            cr.set_line_width(8 - i * 2)
            cr.stroke()
        
        # Main title
        gradient_text = cairo.LinearGradient(0, title_y - 50, 0, title_y + 50)
        gradient_text.add_color_stop_rgb(0, 1, 1, 0.5)
        gradient_text.add_color_stop_rgb(0.5, 1, 0.9, 0.3)
        gradient_text.add_color_stop_rgb(1, 1, 0.8, 0.2)
        cr.set_source(gradient_text)
        cr.set_font_size(80)
        cr.move_to(title_x, title_y)
        cr.show_text(text)
        
        # Animated subtitle
        color_shift = abs(math.sin(self.animation_time))
        cr.set_source_rgb(0.7 + color_shift * 0.3, 0.7 + color_shift * 0.3, 1)
        cr.set_font_size(32)
        text = "Educational Quiz Game"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, 210 + bounce)
        cr.show_text(text)
        
        # Decorative rotating circles
        for i in range(5):
            angle = self.animation_time + i * (2 * math.pi / 5)
            radius = 100
            circle_x = width / 2 + math.cos(angle) * radius
            circle_y = 180 + math.sin(angle) * radius
            
            cr.set_source_rgba(1, 1, 0, 0.3)
            cr.arc(circle_x, circle_y, 8, 0, 2 * math.pi)
            cr.fill()
        
        # Menu buttons with animation
        button_width = 300
        button_height = 60
        button_x = (width - button_width) / 2
        start_y = 320
        spacing = 80
        
        buttons = [
            ("PLAY", "play"),
            ("OPTIONS", "option"),
            ("CREDITS", "credit"),
            ("QUIT", "quit")
        ]
        
        for i, (text, action) in enumerate(buttons):
            # Staggered entrance animation (optional)
            y = start_y + i * spacing
            self.draw_button(cr, button_x, y, button_width, button_height, text, action, i)
        
        # Draw particles
        self.draw_particles(cr)
    
    def draw_level_page(self, cr, width, height):
        self.buttons = []
        
        # Background
        gradient = cairo.LinearGradient(0, 0, 0, height)
        gradient.add_color_stop_rgb(0, 0.1, 0.2, 0.3)
        gradient.add_color_stop_rgb(1, 0.2, 0.3, 0.4)
        cr.set_source(gradient)
        cr.paint()
        
        self.draw_animated_stars(cr, width, height)
        
        # Title
        cr.set_source_rgb(1, 1, 0.3)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(60)
        text = "SELECT LEVEL"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, 100)
        cr.show_text(text)
        
        # Level grid (placeholder with hover effect)
        levels = ["Easy", "Medium", "Hard", "Expert"]
        grid_start_x = width / 2 - 400
        grid_start_y = height / 2 - 100
        
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(28)
        
        for i, level in enumerate(levels):
            x = grid_start_x + (i % 2) * 400
            y = grid_start_y + (i // 2) * 150
            
            # Level box
            cr.set_source_rgba(0.3, 0.5, 0.7, 0.5)
            self.draw_rounded_rect(cr, x, y, 300, 100, 15)
            cr.fill()
            
            cr.set_source_rgb(1, 1, 1)
            extents = cr.text_extents(level)
            cr.move_to(x + (300 - extents.width) / 2, y + (100 + extents.height) / 2)
            cr.show_text(level)
        
        # Back button
        self.draw_button(cr, 50, height - 100, 200, 50, "BACK", "back", len(self.buttons))
        
        self.draw_particles(cr)
    
    def draw_option_page(self, cr, width, height):
        self.buttons = []
        
        # Background
        gradient = cairo.LinearGradient(0, 0, 0, height)
        gradient.add_color_stop_rgb(0, 0.1, 0.2, 0.3)
        gradient.add_color_stop_rgb(1, 0.2, 0.3, 0.4)
        cr.set_source(gradient)
        cr.paint()
        
        self.draw_animated_stars(cr, width, height)
        
        # Title
        cr.set_source_rgb(1, 1, 0.3)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(60)
        text = "OPTIONS"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, 100)
        cr.show_text(text)
        
        # Sound option
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(36)
        text = "Sound:"
        cr.move_to(width / 2 - 250, height / 2 - 50)
        cr.show_text(text)
        
        # Animated toggle button
        sound_status = "ON" if self.sound_enabled else "OFF"
        button_color = (0.2, 0.8, 0.2) if self.sound_enabled else (0.8, 0.2, 0.2)
        
        btn_x = width / 2 + 50
        btn_y = height / 2 - 85
        btn_width = 180
        btn_height = 60
        
        self.buttons.append({
            "x": btn_x, "y": btn_y, "width": btn_width, "height": btn_height, 
            "action": "toggle_sound"
        })
        
        # Button with glow
        pulse = abs(math.sin(self.animation_time * 3))
        cr.set_source_rgba(*button_color, 0.3)
        self.draw_rounded_rect(cr, btn_x - 5, btn_y - 5, btn_width + 10, btn_height + 10, 12)
        cr.fill()
        
        cr.set_source_rgb(*button_color)
        self.draw_rounded_rect(cr, btn_x, btn_y, btn_width, btn_height, 10)
        cr.fill()
        
        # Border
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(2)
        self.draw_rounded_rect(cr, btn_x, btn_y, btn_width, btn_height, 10)
        cr.stroke()
        
        cr.set_font_size(32)
        extents = cr.text_extents(sound_status)
        cr.move_to(btn_x + (btn_width - extents.width) / 2, 
                   btn_y + (btn_height + extents.height) / 2)
        cr.show_text(sound_status)
        
        # Back button
        self.draw_button(cr, 50, height - 100, 200, 50, "BACK", "back", len(self.buttons))
        
        self.draw_particles(cr)
    
    def draw_credit_page(self, cr, width, height):
        self.buttons = []
        
        # Background
        gradient = cairo.LinearGradient(0, 0, 0, height)
        gradient.add_color_stop_rgb(0, 0.1, 0.15, 0.25)
        gradient.add_color_stop_rgb(1, 0.15, 0.2, 0.3)
        cr.set_source(gradient)
        cr.paint()
        
        self.draw_animated_stars(cr, width, height)
        
        # Title
        cr.set_source_rgb(1, 1, 0.3)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(60)
        text = "CREDITS"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, 100)
        cr.show_text(text)
        
        # "Created by" with animation
        wave = math.sin(self.animation_time * 2) * 0.2
        cr.set_source_rgb(0.8 + wave, 0.8 + wave, 1)
        cr.set_font_size(32)
        text = "Created by:"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, 200)
        cr.show_text(text)
        
        # Creators with staggered animation
        creators = [
            "Agung Kurniawan",
            "Muhammad Fajrul Falah",
            "Muhamad Rizqi Ramadhani"
        ]
        
        cr.set_font_size(40)
        start_y = 280
        for i, creator in enumerate(creators):
            color_wave = math.sin(self.animation_time * 2 + i * 0.5)
            cr.set_source_rgb(0.7 + color_wave * 0.3, 0.7 + color_wave * 0.3, 1)
            extents = cr.text_extents(creator)
            offset = math.sin(self.animation_time + i) * 5
            cr.move_to((width - extents.width) / 2 + offset, start_y + i * 70)
            cr.show_text(creator)
        
        # Tech info
        cr.set_source_rgb(0.6, 0.8, 1)
        cr.set_font_size(24)
        text = "Built with Python, PyCairo & GTK3"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, height / 2 + 180)
        cr.show_text(text)
        
        # Year
        cr.set_font_size(20)
        text = "© 2024"
        extents = cr.text_extents(text)
        cr.move_to((width - extents.width) / 2, height / 2 + 220)
        cr.show_text(text)
        
        # Back button
        self.draw_button(cr, 50, height - 100, 200, 50, "BACK", "back", len(self.buttons))
        
        self.draw_particles(cr)
    
    def on_draw(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        
        if self.current_page == "menu":
            self.draw_menu(cr, width, height)
        elif self.current_page == "level":
            self.draw_level_page(cr, width, height)
        elif self.current_page == "option":
            self.draw_option_page(cr, width, height)
        elif self.current_page == "credit":
            self.draw_credit_page(cr, width, height)

def main():
    game = EduQuizGame()
    game.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()