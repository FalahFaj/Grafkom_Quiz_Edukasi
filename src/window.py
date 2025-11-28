import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from .config import JUDUL_WINDOW

# Impor semua scene/halaman yang ada
from .halaman.menu import MenuScene
from .halaman.pilihan_level import PilihanLevelScene
from .halaman.options import OptionsScene
from .halaman.map_scene import MapScene
from .halaman.credit_scene import CreditScene

# Impor audio manager
from .audio_manager import audio_manager

class GameWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=JUDUL_WINDOW)
        
        screen = self.get_screen()
        self.lebar_layar = screen.get_width()
        self.tinggi_layar = screen.get_height()

        self.set_default_size(self.lebar_layar, self.tinggi_layar)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
        self.fullscreen()

        # Mulai musik latar belakang dari lagu default
        audio_manager.play_song_by_name("Lagu 1", loops=-1)

        # Container utama untuk scene
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        # "Scene Manager" sederhana
        self.scenes = {
            "menu_scene": MenuScene(self.lebar_layar, self.tinggi_layar, self.change_scene),
            "pilihan_level_scene": PilihanLevelScene(self.lebar_layar, self.tinggi_layar, self.change_scene),
            "options_scene": OptionsScene(self.lebar_layar, self.tinggi_layar, self.change_scene),
            "map_scene": MapScene(self.lebar_layar, self.tinggi_layar, self.change_scene),
            "credit_scene": CreditScene(self.lebar_layar, self.tinggi_layar, self.change_scene)
        }
        
        self.current_scene = None
        self.change_scene("menu_scene") # Mulai dari menu

    def change_scene(self, scene_name, **kwargs):
        """Fungsi sentral untuk mengganti halaman/scene."""
        print(f"Berpindah ke scene: {scene_name}")
        
        if self.current_scene:
            self.main_box.remove(self.current_scene)
            
        new_scene = self.scenes.get(scene_name)
        
        if new_scene:
            self.current_scene = new_scene
            self.main_box.pack_start(self.current_scene, True, True, 0)
            
            # Panggil on_enter jika ada, untuk inisialisasi/refresh data
            if hasattr(self.current_scene, 'on_enter'):
                self.current_scene.on_enter(**kwargs)

            self.show_all()
        else:
            print(f"Error: Scene '{scene_name}' tidak ditemukan!")
            # Fallback ke menu jika scene tidak ada
            if self.current_scene is None:
                 self.change_scene("menu_scene")
