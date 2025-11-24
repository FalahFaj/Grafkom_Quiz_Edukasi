import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.window import GameWindow

def main():
    app = GameWindow()

    app.show_all()
    Gtk.main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Aplikasi ditutup")
