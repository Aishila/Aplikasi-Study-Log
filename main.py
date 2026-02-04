import json
import os
import datetime

catatan = []
targets = {}  # mapping 'YYYY-MM-DD' -> menit
default_target = None  # jika tidak ada target khusus untuk tanggal

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

    tanggal = datetime.date.today().isoformat()
    catatan.append({'mapel': mapel, 'topik': topik, 'durasi': durasi, 'tanggal': tanggal})
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

    # Tampilkan perbandingan dengan target hari ini jika ada
    today = datetime.date.today().isoformat()
    today_total = sum(x['durasi'] for x in catatan if x.get('tanggal') == today)
    today_target = get_target_for_date(today)
    if today_target:
        print(f"Total hari ini: {today_total} menit. Target harian: {today_target} menit.")
        if today_total >= today_target:
            print("Selamat — target harian tercapai! 🎉")
        else:
            sisa = today_target - today_total
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

def get_target_for_date(date_str):
    """Kembalikan target untuk tanggal tertentu, atau default jika tidak ada."""
    if date_str in targets:
        return targets[date_str]
    return default_target


def target_harian_menu():
    """Menu untuk set target default atau target per tanggal, dan melihat target."""
    global default_target
    print("\n=== Target Harian ===")
    print(f"Target default saat ini: {default_target if default_target else 'belum diset'}")
    print("1. Set target default (untuk semua hari)")
    print("2. Set target untuk tanggal tertentu")
    print("3. Lihat target untuk tanggal tertentu")
    print("4. Hapus target untuk tanggal tertentu")
    print("(kosong untuk kembali)")
    pilih = input("Pilihan: ").strip()
    if pilih == "":
        return
    if pilih == "1":
        inp = input("Masukkan target default (menit): ").strip()
        if inp.isdigit():
            default_target = int(inp)
            print(f"Target default disimpan: {default_target} menit")
        else:
            print("Input tidak valid.")
    elif pilih == "2":
        tanggal = input("Tanggal (YYYY-MM-DD) kosong=hari ini: ").strip()
        if tanggal == "":
            tanggal = datetime.date.today().isoformat()
        menit = input("Target (menit): ").strip()
        if menit.isdigit():
            targets[tanggal] = int(menit)
            print(f"Target untuk {tanggal} disimpan: {menit} menit")
        else:
            print("Input tidak valid.")
    elif pilih == "3":
        tanggal = input("Tanggal (YYYY-MM-DD) kosong=hari ini: ").strip()
        if tanggal == "":
            tanggal = datetime.date.today().isoformat()
        t = get_target_for_date(tanggal)
        print(f"Target untuk {tanggal}: {t if t else 'tidak diset'}")
    elif pilih == "4":
        tanggal = input("Tanggal (YYYY-MM-DD) kosong=hari ini: ").strip()
        if tanggal == "":
            tanggal = datetime.date.today().isoformat()
        if tanggal in targets:
            del targets[tanggal]
            print(f"Target untuk {tanggal} dihapus.")
        else:
            print("Tidak ada target untuk tanggal tersebut.")
    else:
        print("Pilihan tidak valid.")

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
        # Simpan state lengkap: catatan + targets + default_target
        state = {'catatan': catatan, 'targets': targets, 'default_target': default_target}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"Catatan dan target disimpan ke {path}.")
    except Exception as e:
        print("Gagal menyimpan:", e)

def muat_catatan(path='catatan.json'):
    """Muat catatan dari file JSON jika ada."""
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # dukung format lama (list) dan format state baru (dict)
        if isinstance(data, list):
            catatan.clear()
            for item in data:
                if all(k in item for k in ('mapel', 'topik', 'durasi')):
                    catatan.append({'mapel': item['mapel'], 'topik': item['topik'], 'durasi': int(item['durasi']), 'tanggal': item.get('tanggal')})
            print(f"Memuat {len(catatan)} catatan dari {path} (format lama).")
        elif isinstance(data, dict):
            catatan.clear()
            for item in data.get('catatan', []):
                if all(k in item for k in ('mapel', 'topik', 'durasi')):
                    catatan.append({'mapel': item['mapel'], 'topik': item['topik'], 'durasi': int(item['durasi']), 'tanggal': item.get('tanggal')})
            # muat targets jika ada
            global targets, default_target
            targets = {k: int(v) for k, v in data.get('targets', {}).items()}
            default_target = int(data.get('default_target')) if data.get('default_target') else None
            print(f"Memuat {len(catatan)} catatan dan {len(targets)} target dari {path}.")
    except Exception as e:
        print("Gagal memuat catatan:", e)


def ringkasan_mingguan():
    """Tampilkan ringkasan 7 hari terakhir, bandingkan dengan target tiap hari."""
    today = datetime.date.today()
    print("\n=== Ringkasan 7 Hari Terakhir ===")
    for d in range(6, -1, -1):
        day = (today - datetime.timedelta(days=d)).isoformat()
        total = sum(x['durasi'] for x in catatan if x.get('tanggal') == day)
        t = get_target_for_date(day)
        status = "-" if not t else ("Tercapai" if total >= t else f"Kurang {t-total}m")
        print(f"{day}: {total} menit | Target: {t if t else '-'} | {status}")


def check_today_target_warning():
    """Jika ada target hari ini dan belum tercapai, tampilkan peringatan singkat."""
    today = datetime.date.today().isoformat()
    t = get_target_for_date(today)
    if not t:
        return
    total = sum(x['durasi'] for x in catatan if x.get('tanggal') == today)
    if total < t:
        sisa = t - total
        print(f"Peringatan: Anda masih kurang {sisa} menit untuk mencapai target hari ini ({t} menit).")

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

# muat data saat startup (jika ada) dan periksa target hari ini
muat_catatan()
check_today_target_warning()

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