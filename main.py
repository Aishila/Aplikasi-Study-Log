import json
import os

catatan = []
target_harian = None

def tambah_catatan():
    """Minta input pengguna dan simpan catatan ke list `catatan`.

    Struktur catatan adalah dict sederhana: {'mapel', 'topik', 'durasi'}
    """
    mapel = input("Mapel: ").strip()
    topik = input("Topik: ").strip()

    while True:
        durasi_input = input("Durasi belajar (menit): ").strip()
        if durasi_input.isdigit():
            durasi = int(durasi_input)
            break
        else:
            print("Masukkan angka durasi dalam menit.")

    catatan.append({'mapel': mapel, 'topik': topik, 'durasi': durasi})
    print("Catatan tersimpan.")

def lihat_catatan():
    """Tampilkan semua catatan secara rapi.

    Jika belum ada catatan, tampilkan pesan yang sesuai.
    """
    if not catatan:
        print("Belum ada catatan. Tambah catatan terlebih dahulu.")
        return

    print("\n=== Daftar Catatan Belajar ===")
    for i, c in enumerate(catatan, start=1):
        print(f"{i}. Mapel: {c['mapel']} | Topik: {c['topik']} | Durasi: {c['durasi']} menit")
    print("------------------------------")

    if target_harian:
        total = sum(x['durasi'] for x in catatan)
        print(f"Total hari ini: {total} menit. Target harian: {target_harian} menit.")
        if total >= target_harian:
            print("Selamat — target harian tercapai! 🎉")
        else:
            sisa = target_harian - total
            print(f"Belum mencapai target. Sisa: {sisa} menit.")

def total_waktu():
    """Hitung dan tampilkan total durasi dari semua catatan."""
    total = sum(c['durasi'] for c in catatan)
    if total == 0:
        print("Belum ada durasi tercatat.")
        return

    jam = total // 60
    menit = total % 60
    print(f"Total waktu belajar: {total} menit ({jam} jam {menit} menit)")

def target_harian_menu():
    """Menu sederhana untuk set / lihat target harian."""
    global target_harian
    print("\n=== Target Harian ===")
    if target_harian:
        print(f"Target saat ini: {target_harian} menit")
    else:
        print("Belum ada target harian.")

    inp = input("Masukkan target harian baru dalam menit (kosong untuk batal): ").strip()
    if inp == "":
        print("Batal mengubah target.")
        return
    if inp.isdigit():
        target_harian = int(inp)
        print(f"Target harian disimpan: {target_harian} menit")
    else:
        print("Input tidak valid. Gunakan angka dalam menit.")

def hapus_catatan():
    """Hapus catatan berdasarkan nomor yang ditampilkan."""
    if not catatan:
        print("Belum ada catatan untuk dihapus.")
        return

    lihat_catatan()
    idx = input("Masukkan nomor catatan yang akan dihapus (kosong untuk batal): ").strip()
    if idx == "":
        print("Batal menghapus.")
        return
    if not idx.isdigit():
        print("Input tidak valid.")
        return
    i = int(idx) - 1
    if 0 <= i < len(catatan):
        removed = catatan.pop(i)
        print(f"Terhapus: {removed['mapel']} - {removed['topik']} ({removed['durasi']} menit)")
    else:
        print("Nomor catatan tidak ditemukan.")

def cari_catatan():
    """Cari catatan berdasarkan nama mapel (case-insensitive)."""
    if not catatan:
        print("Belum ada catatan.")
        return
    q = input("Cari mapel: ").strip().lower()
    if not q:
        print("Kata kunci kosong.")
        return
    hasil = [c for c in catatan if q in c['mapel'].lower()]
    if not hasil:
        print("Tidak ditemukan catatan untuk mapel tersebut.")
        return
    print("\n=== Hasil Pencarian ===")
    for i, c in enumerate(hasil, start=1):
        print(f"{i}. Mapel: {c['mapel']} | Topik: {c['topik']} | Durasi: {c['durasi']} menit")

def simpan_catatan(path='catatan.json'):
    """Simpan list `catatan` ke file JSON."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(catatan, f, ensure_ascii=False, indent=2)
        print(f"Catatan disimpan ke {path}.")
    except Exception as e:
        print("Gagal menyimpan:", e)

def muat_catatan(path='catatan.json'):
    """Muat catatan dari file JSON jika ada."""
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            catatan.clear()
            for item in data:
                # validasi ringan
                if all(k in item for k in ('mapel', 'topik', 'durasi')):
                    catatan.append({'mapel': item['mapel'], 'topik': item['topik'], 'durasi': int(item['durasi'])})
        print(f"Memuat {len(catatan)} catatan dari {path}.")
    except Exception as e:
        print("Gagal memuat catatan:", e)

def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Keluar")
    print("5. Target harian (set/view)")
    print("6. Hapus catatan")
    print("7. Cari catatan (berdasarkan mapel)")
    print("8. Simpan catatan ke file / Muat dari file")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        total_waktu()
    elif pilihan == "4":
        print("Terima kasih, terus semangat belajar!")
        break
    elif pilihan == "5":
        target_harian_menu()
    elif pilihan == "6":
        hapus_catatan()
    elif pilihan == "7":
        cari_catatan()
    elif pilihan == "8":
        sub = input("Ketik 's' untuk simpan, 'm' untuk muat: ").strip().lower()
        if sub == 's':
            simpan_catatan()
        elif sub == 'm':
            muat_catatan()
        else:
            print("Pilihan tidak dikenali.")
    else:
        print("Pilihan tidak valid")