import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from .config import JUDUL_WINDOW, LEBAR_WINDOW, TINGGI_WINDOW

class GameWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=JUDUL_WINDOW)

        self.set_default_size(LEBAR_WINDOW, TINGGI_WINDOW)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        self.connect("destroy", Gtk.main_quit)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.main_box)

        label = Gtk.Label()
        label.set_markup(f"<span font='20' foreground='black'>Selamat Datang di <b>{JUDUL_WINDOW}</b></span>")
        self.main_box.pack_start(label, True, True, 0)

        tombol = Gtk.Button(label="Mulai")
        tombol.connect("clicked", self.on_tombol_clicked)
        self.main_box.pack_start(tombol, False, False, 20)

    def on_tombol_clicked(self, widget, data=None):
        print(f"Tombol {widget.get_label()} di klik")
        print("SIstem GTK berfungsi")