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

def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Keluar")
    print("5. Target harian (set/view)")

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
    else:
        print("Pilihan tidak valid")