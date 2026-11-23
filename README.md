# Jelajah Alam Bengkulu Selatan 🌿🌊

Game petualangan dan eksplorasi 2D interaktif berbasis **Pygame** yang mengangkat keindahan alam serta potensi wisata di **Kabupaten Bengkulu Selatan**.

Proyek ini juga mendukung build berbasis web via **Pygbag** (WebAssembly), sehingga dapat dimainkan langsung di peramban web.

---

## 📍 Destinasi & Zona Wisata

Game ini menampilkan berbagai spot ikonik Bengkulu Selatan:
1. **Pantai Pasar Bawah (Kota Manna)** - Pesisir berombak Samudra Hindia dengan panorama perahu nelayan tradisional.
2. **Pantai Bengkenang** - Hamparan pesisir berpasir luas dengan deretan cemara laut dan satwa pesisir.
3. **Sungai Air Manna** - Aliran sungai jernih pegunungan dengan kearifan lokal lubuk larangan.
4. **Air Terjun Geluguran (Ulu Manna)** - Gugusan air terjun megah di kaki Bukit Barisan.
5. **Hutan Rafflesia (Bukit Barisan)** - Zona hutan hujan tropis kaya biodiversitas dan habitat flora langka *Rafflesia arnoldii*.

---

## 🎮 Kontrol Permainan

| Tombol / Aksi | Fungsi |
|---|---|
| `A` / `D` atau `←` / `→` | Bergerak ke kiri / kanan |
| `W` / `Spasi` / `↑` | Melompat |
| `E` atau Klik Kiri Mouse | Membuka / mengamati kartu informasi spot wisata |
| `1` | Suasana Pagi hari |
| `2` | Suasana Senja hari |
| `3` | Suasana Malam hari |
| `X` / Tombol Navigasi Card | Menutup atau melihat spot sebelumnya / berikutnya |

---

## 🚀 Cara Menjalankan

### 1. Menjalankan di Komputer Lokal (Desktop)

Pastikan Python 3.8+ sudah terpasang di komputer Anda.

```bash
# Clone repository
git clone https://github.com/PebiHeriansyah/jelajah-alam-bengkulu-selatan.git
cd jelajah-alam-bengkulu-selatan

# Buat virtual environment (opsional tapi disarankan)
python -m venv .venv

# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependensi
pip install -r requirements.txt

# Jalankan game
python main.py
```

### 2. Menjalankan Versi Web (Pygbag)

Game ini dapat dijalankan di web browser menggunakan `pygbag`:

```bash
# Jalankan development server pygbag
pygbag .
```
Akses di browser melalui: `http://localhost:8000`

Hasil build web statis siap saji juga tersedia di dalam direktori `build/web/` (`index.html`).

### 3. Deploy ke Netlify

Repository ini sudah dilengkapi file konfigurasi `netlify.toml` dengan target publish: `build/web`.
Ketika dihubungkan ke Netlify, Netlify akan langsung men-deploy file web statis tanpa perlu build command tambahan.

---

## 🛠️ Lisensi & Kontribusi

Dibuat untuk mempromosikan keindahan alam dan pariwisata Bengkulu Selatan. Terbuka untuk kontribusi, saran, dan pengembangan lebih lanjut!
