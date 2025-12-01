
# Grafkom_Quiz_Edukasi

Grafkom_Quiz_Edukasi adalah game kuis edukasi matematika yang dirancang untuk anak-anak. Game ini dibangun menggunakan Python dengan library GTK3 untuk antarmuka pengguna dan Cairo untuk rendering grafis 2D.

## Fitur

- **Kuis Matematika Interaktif**: Soal-soal matematika dasar (penjumlahan, pengurangan, perkalian, pembagian) yang disajikan secara visual.
- **Visualisasi dengan Buah**: Angka-angka dalam soal direpresentasikan dengan gambar buah (apel dan jeruk) untuk membuat pembelajaran lebih menarik.
- **Tiga Tingkat Kesulitan**: 
    - **Easy**: Latar belakang siang hari.
    - **Medium**: Latar belakang sore hari.
    - **Hard**: Latar belakang malam hari dengan bintang dan bulan.
- **Peta Level**: Kemajuan pemain ditampilkan dalam sebuah peta level yang dapat dijelajahi.
- **Sistem Nyawa dan Waktu**: Setiap level memiliki batas waktu dan pemain memiliki 3 nyawa.
- **Penyimpanan Progres**: Progres permainan (level yang terbuka) disimpan secara otomatis.
- **Audio**: Dilengkapi dengan musik latar dan efek suara untuk jawaban benar atau salah.

## Prasyarat dan Instalasi

Pastikan Anda memiliki Python 3 dan GTK3 terinstal di sistem Anda.

1.  **Instalasi dependensi Python:**
    Game ini memerlukan `PyGObject` untuk menggunakan GTK. Instalasi bisa berbeda tergantung sistem operasi Anda.

    **Untuk Windows:**
    Ikuti petunjuk instalasi dari [MSYS2](https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started) untuk menginstal GTK3 dan PyGObject.

    ```bash
    # Setelah setup MSYS2 dan MinGW64
    pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject
    ```

    **Untuk Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
    ```


## Cara Menjalankan

Untuk memulai game, jalankan file `main.py`:

```bash
python main.py
```

## Struktur Proyek

```
Grafkom_Quiz_Edukasi/
├── main.py                # Titik masuk utama aplikasi
├── data/
│   ├── level.json         # Konfigurasi posisi level di peta
│   └── savegame.json      # Menyimpan progres pemain
├── assets/
│   ├── images/            # Modul Python untuk menggambar aset (buah, ikon, dll)
│   └── sounds/            # File musik dan suara
└── src/
    ├── __init__.py
    ├── audio_manager.py   # Mengelola pemutaran musik dan suara
    ├── config.py          # Konfigurasi global (judul window, dll)
    ├── game_logic.py      # Logika untuk menghasilkan soal kuis
    ├── window.py          # Konfigurasi window utama GTK dan manajer scene
    ├── components/        # Komponen UI yang dapat digunakan kembali (tombol, dll)
    └── halaman/           # Modul untuk setiap scene/halaman (menu, game, peta, dll)
```
