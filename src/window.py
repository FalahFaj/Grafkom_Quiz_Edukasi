import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from .config import JUDUL_WINDOW, LEBAR_WINDOW, TINGGI_WINDOW
from .scene.menu import MenuScene

class GameWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=JUDUL_WINDOW)

        self.set_default_size(LEBAR_WINDOW, TINGGI_WINDOW)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)

        self.connect("destroy", Gtk.main_quit)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        self.show_menu_scene()
    def on_tombol_clicked(self, widget, data=None):
        print(f"Tombol {widget.get_label()} di klik")
        print("SIstem GTK berfungsi")

    def change_scene(self, scene_name):
        """Fungsi sentral untuk mengganti halaman"""
        print(f"Berpindah ke scene: {scene_name}")
        
        # Hapus scene lama
        for child in self.main_box.get_children():
            self.main_box.remove(child)
            
        if scene_name == "map_scene":
            # Nanti kita buat MapScene, sementara label dulu
            label = Gtk.Label(label="INI HALAMAN PETA LEVEL (Next Step)")
            self.main_box.pack_start(label, True, True, 0)
        
        elif scene_name == "menu":
            self.show_menu_scene()
            
        self.show_all()

    def show_menu_scene(self):
        # Buat instance MenuScene dan berikan fungsi callback change_scene
        menu = MenuScene(LEBAR_WINDOW, TINGGI_WINDOW, self.change_scene)
        self.main_box.pack_start(menu, True, True, 0)