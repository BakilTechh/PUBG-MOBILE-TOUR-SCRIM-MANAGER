# Sistem Manajemen Scrim / Tournament PUBG Mobile (PBO - Python)

Program Python sederhana yang mensimulasikan sistem pemain, squad, dan scrim
ala manajemen tim PUBG Mobile. Program ini dibuat untuk memenuhi tugas OOP
(Object-Oriented Programming) di Python, mencakup materi Class & Object,
Atribut & Method, serta Encapsulation & Property.

## Daftar Isi
- Struktur File
- Penjelasan Class
  1. Pemain
  2. Squad
  3. Scrim
- Alur Program (main)
- Panduan Pengujian
- Kesesuaian dengan Syarat Tugas

## Struktur File
```
.
└── main.py   # Berisi semua class dan blok pengujian (if __name__ == "__main__")
```

## Penjelasan Class

### 1. Pemain
Cetak biru untuk satu pemain PUBG Mobile.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `total_pemain_terdaftar` | Atribut kelas (publik) | Menghitung total objek `Pemain` yang pernah dibuat |
| `kategori_game`, `role_tersedia` | Atribut kelas (publik) | Data yang sama untuk semua pemain (nama game & daftar role yang tersedia) |
| `nama_pemain`, `nomor_id`, `role` | Atribut instance | Diisi lewat `__init__`, unik untuk tiap pemain |
| `__poin_performa` | Atribut instance (privat) | Poin performa pemain, hanya bisa diubah lewat property |

Konstruktor `__init__(self, nama_pemain, nomor_id, role, poin_awal=0)` menyimpan
data dasar pemain lalu mengisi `poin_performa` lewat setter (agar tetap
tervalidasi sejak awal objek dibuat).

Property `poin_performa` — getter mengembalikan `__poin_performa`; setter
menolak nilai yang bukan angka atau negatif dengan `raise ValueError`.

Instance method `catat_hasil_pertandingan(jumlah_kill, damage_total)`
menghitung tambahan poin dari kombinasi kill dan damage, lalu menambahkannya
ke poin performa yang sudah ada.

Class method `buat_dari_data(cls, data)` adalah factory method: membangun
objek `Pemain` langsung dari `dict` data pendaftaran.

Static method `cek_format_id(nomor_id)` memvalidasi apakah ID pemain berupa
string angka sepanjang 8–12 digit.

### 2. Squad
Mengelola kumpulan objek `Pemain` yang tergabung dalam satu tim.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `kapasitas_maksimal` | Atribut kelas | Batas maksimal anggota per squad (5), sama untuk semua objek `Squad` |
| `total_squad_terdaftar`, `region_utama` | Atribut kelas | Data bersama lainnya |
| `nama_squad`, `region`, `anggota` | Atribut instance | `anggota` adalah list berisi objek `Pemain` |
| `__dana_operasional` | Atribut instance (privat) | Dana tim, hanya bisa diubah lewat property |

`rekrut_pemain(self, pemain)` menambahkan objek `Pemain` ke `anggota` jika
kapasitas masih tersedia; jika penuh, mencetak pesan penolakan.

`tampilkan_anggota(self)` mencetak seluruh anggota squad beserta poin
performa masing-masing.

Property `dana_operasional` — setter menolak nilai negatif dengan
`raise ValueError`, sama seperti pola pada `Pemain`.

Class method `buat_dari_data(cls, data)` — factory method dari `dict`.

Static method `hitung_rata_rata_poin(daftar_pemain)` menghitung rata-rata
poin performa dari sekumpulan pemain (dipakai juga oleh class `Scrim` untuk
mengurutkan peringkat).

### 3. Scrim
Merepresentasikan satu event scrim yang diikuti beberapa squad.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `penyelenggara`, `format_pertandingan` | Atribut kelas | Data bersama semua scrim |
| `total_scrim_dijalankan` | Atribut kelas | Menghitung total objek `Scrim` yang pernah dibuat |
| `judul_scrim`, `kuota_squad`, `daftar_squad_peserta` | Atribut instance | `daftar_squad_peserta` berisi objek `Squad` yang sudah diundang |
| `__total_hadiah` | Atribut instance (privat) | Hadiah total, hanya bisa diubah lewat property |

`undang_squad(self, squad)` mendaftarkan objek `Squad` ke scrim selama kuota
masih tersedia.

`tampilkan_papan_peringkat(self)` mengurutkan squad berdasarkan rata-rata
poin performa anggotanya (memanggil `Squad.hitung_rata_rata_poin`), lalu
mencetak peringkatnya.

Property `total_hadiah` — setter menolak nilai negatif dengan
`raise ValueError`.

Class method `buat_dari_data(cls, data)` — factory method dari `dict`.

Static method `format_rupiah(angka)` mengubah angka menjadi format mata uang
Rupiah untuk ditampilkan di papan peringkat.

## Alur Program (main)
Blok `if __name__ == "__main__":` menjalankan skenario pengujian berurutan:

1. **Membuat objek Pemain** — tiga pemain dibuat (dua lewat konstruktor
   biasa, satu lewat `Pemain.buat_dari_data`), lalu salah satunya diuji
   `catat_hasil_pertandingan()` dan dicek dengan `cek_format_id()`.
2. **Membuat objek Squad** — dua squad dibuat, pemain-pemain di atas direkrut
   ke dalamnya, lalu ditampilkan dan dihitung rata-rata poinnya.
3. **Membuat objek Scrim** — dua scrim dibuat, kedua squad diundang ke salah
   satunya, lalu papan peringkat ditampilkan.
4. **Uji validasi setter** — `poin_performa`, `dana_operasional`, dan
   `total_hadiah` masing-masing diisi nilai valid lalu nilai negatif, untuk
   membuktikan `ValueError` benar-benar tertangkap dan data tidak berubah.

## Panduan Pengujian

**Cara menjalankan**
```bash
python main.py
```

**Uji manual lain yang bisa dicoba**
- Rekrut lebih dari 5 pemain ke satu squad, pastikan pesan "sudah mencapai
  kapasitas maksimal" muncul saat anggota ke-6 ditambahkan.
- Undang squad melebihi `kuota_squad` pada satu scrim, pastikan pesan
  "Kuota scrim ... sudah penuh" muncul.
- Isi `poin_performa` dengan tipe data selain angka (misal string), pastikan
  `ValueError` juga tertangkap.
4. **Getter, Setter, Validasi** — akses ke atribut private semuanya lewat
   `@property` dan `@<nama>.setter` dengan nama fungsi yang sama persis;
   setiap setter menolak input tidak valid dengan `raise ValueError`.
5. **Pengujian** — di bagian main code dibuat minimal 2 objek per class,
   seluruh jenis method dipanggil, dan setter diuji dengan data valid maupun
   tidak valid.
