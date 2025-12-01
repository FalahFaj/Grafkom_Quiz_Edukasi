# src/audio_manager.py
import pygame
import os

class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            try:
                pygame.mixer.init()
                cls._instance.is_initialized = True
                print("AudioManager: Pygame mixer initialized successfully.")
            except pygame.error as e:
                cls._instance.is_initialized = False
                print(f"AudioManager Error: Failed to initialize mixer. {e}")
                print("Audio akan dinonaktifkan.")
            
            cls._instance.current_song_name = None
            cls._instance.user_selected_song = "Lagu 1"  # Default user song
            cls._instance.songs = {
                "Lagu 1": "assets/sounds/lagupagi.mp3",
                "Lagu 2": "assets/sounds/lagusore.mp3",
                "Lagu 3": "assets/sounds/lagumalam.mp3"
            }
            # Set default song
            if cls._instance.is_initialized:
                cls._instance.current_song_name = "Lagu 1"


        return cls._instance

    def play_song_by_name(self, name, loops=-1, is_level_specific=False):
        """Memuat dan memutar lagu berdasarkan nama dari daftar lagu."""
        if not self.is_initialized:
            return

        file_path = self.songs.get(name)
        if file_path is None:
            print(f"AudioManager Error: Nama lagu '{name}' tidak ditemukan.")
            return

        if not os.path.exists(file_path):
            print(f"AudioManager Error: File musik tidak ditemukan di '{file_path}'")
            # Coba putar lagu default jika ada
            if name != self.user_selected_song:
                self.play_song_by_name(self.user_selected_song, loops)
            return

        try:
            # Don't reload if the same song is already playing
            if self.current_song_name == name and pygame.mixer.music.get_busy():
                return

            pygame.mixer.music.load(file_path)
            # Ambil volume yang sudah ada sebelumnya
            current_vol = self.get_volume()
            pygame.mixer.music.set_volume(current_vol)
            pygame.mixer.music.play(loops=loops)
            self.current_song_name = name

            if not is_level_specific:
                self.user_selected_song = name

            print(f"AudioManager: Memutar '{name}' dari file '{file_path}'.")
        except pygame.error as e:
            print(f"AudioManager Error: Gagal memutar musik. {e}")
            self.current_song_name = None

    def resume_user_song(self, loops=-1):
        """Resume playing the user's chosen song."""
        if self.current_song_name != self.user_selected_song:
            self.play_song_by_name(self.user_selected_song, loops)

    def stop_music(self):
        if not self.is_initialized: return
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        if not self.is_initialized: return
        vol = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(vol)
        self.current_volume = vol
        # Tidak perlu print di sini agar tidak spam console saat slider digeser

    def get_volume(self):
        if not self.is_initialized: return 0.0
        return getattr(self, 'current_volume', 0.5)

    def get_current_song_name(self):
        return self.current_song_name

# Buat satu instance global
audio_manager = AudioManager()