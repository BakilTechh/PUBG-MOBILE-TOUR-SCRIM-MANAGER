# Sistem Manajemen Scrim / Tournament PUBG Mobile (PBO - Python)

Program sederhana berbasis **Pemrograman Berorientasi Objek (PBO)** menggunakan
Python untuk merepresentasikan manajemen pemain, tim (roster), dan tournament
scrim PUBG Mobile.

## Cara Menjalankan

```bash
python main.py
```

Program akan langsung menjalankan demonstrasi (main code) di bagian bawah file:
membuat beberapa objek, memanggil seluruh jenis method, lalu menguji validasi
setter dengan data valid dan tidak valid.

---

## Struktur Class

Program terdiri dari 4 class yang saling berinteraksi (tanpa inheritance):

```
Pemain  ---->  RosterSlot  ---->  Tim  ---->  Tournament
(dipakai)      (dipakai)          (dipakai)
```

- `RosterSlot` menyimpan sebuah objek `Pemain`.
- `Tim` menyimpan banyak objek `RosterSlot` (roster).
- `Tournament` menyimpan banyak objek `Tim` yang terdaftar.

### 1. `Pemain`
Merepresentasikan satu pemain PUBG Mobile.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `total_pemain` | Menghitung total pemain yang pernah dibuat |
| Atribut kelas (private) | `__base_rating` | Nilai dasar rating yang berlaku untuk semua pemain baru |
| Atribut instance (public) | `nama` | Nama pemain |
| Atribut instance (private) | `__rating` | Rating pemain, hanya bisa diakses lewat `property` |
| Instance method | `__str__()` | Menampilkan nama & rating pemain |
| Class method | `ubah_base_rating(cls, value)` | Mengubah `__base_rating` untuk semua pemain berikutnya |
| Property (getter) | `rating` | Mengembalikan nilai `__rating` |
| Property (setter) | `rating` | Menambah/mengurangi rating, **tidak boleh negatif** (ditahan di 0 dengan `max(0, ...)`) |

### 2. `RosterSlot`
Menghubungkan satu `Pemain` dengan jumlah pertandingan yang sudah dimainkan
(mirip "stack" pada inventaris).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut instance (public) | `pemain` | Objek `Pemain` yang dipegang slot ini |
| Atribut instance (private) | `__jumlah_main` | Jumlah match yang sudah dimainkan pemain di tim ini |
| Instance method | `__str__()` | Menampilkan info pemain + jumlah main |
| Property (getter/setter) | `jumlah_main` | Setter memakai `max(0, ...)` agar tidak pernah negatif |

### 3. `Tim`
Merepresentasikan satu tim/roster scrim.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `max_slot` | Batas maksimal jumlah pemain dalam satu tim (5) |
| Atribut instance (public) | `nama_tim`, `daftar_roster` | Nama tim dan daftar `RosterSlot` |
| Atribut instance (private) | `__slot` | Salinan `max_slot` per objek tim |
| Instance method | `tambah_roster()` | Menambahkan `RosterSlot`; jika penuh, mencetak peringatan |
| Instance method | `hapus_pemain_nonaktif()` | Menghapus pemain yang jumlah mainnya 0 dari roster |
| Instance method | `tampilkan_roster()` | Mencetak seluruh isi roster tim |

### 4. `Tournament`
Merepresentasikan satu event scrim/turnamen.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut instance (public) | `nama_tournament`, `daftar_tim` | Nama turnamen dan daftar tim yang terdaftar |
| Atribut instance (private) | `__hadiah` | Total hadiah turnamen, hanya lewat `property` |
| Instance method | `daftarkan_tim()` | Mendaftarkan objek `Tim` ke turnamen |
| Property (getter/setter) | `hadiah` | Setter memakai `max(0, ...)` agar hadiah tidak pernah negatif |
| Static method | `validasi_nama(nama)` | Mengecek nama turnamen tidak boleh mengandung angka |
| Validasi di `__init__` | — | Jika `validasi_nama()` gagal, langsung `raise ValueError` |

---

## Pemetaan ke Syarat Tugas

| Syarat | Bukti di Kode |
|---|---|
| Minimal 3 class utama, tidak wajib inheritance | `Pemain`, `RosterSlot`, `Tim`, `Tournament` — berdiri sendiri, saling berinteraksi lewat objek |
| Minimal 3 atribut kelas | `Pemain.total_pemain`, `Pemain.__base_rating`, `Tim.max_slot` |
| Atribut instance lewat `__init__` + `self` | Semua atribut instance di tiap class (`self.nama`, `self.nama_tim`, dll) |
| Atribut public & minimal 1 private | Public: `nama`, `nama_tim`, `nama_tournament`, `daftar_roster`, `daftar_tim`. Private: `__rating`, `__jumlah_main`, `__hadiah`, `__base_rating`, `__slot` |
| Instance method | `tambah_roster()`, `hapus_pemain_nonaktif()`, `tampilkan_roster()`, `daftarkan_tim()`, `__str__()` |
| Class method (`@classmethod`, pakai `cls`) | `Pemain.ubah_base_rating()` |
| Static method (`@staticmethod`, tanpa `self`/`cls`) | `Tournament.validasi_nama()` |
| `@property` sebagai getter | `rating`, `jumlah_main`, `hadiah` |
| `@<nama>.setter` dengan nama fungsi sama persis | `@rating.setter`, `@jumlah_main.setter`, `@hadiah.setter` |
| Validasi data di setter | Nilai negatif ditahan di 0 lewat `max(0, ...)`; nama turnamen dengan angka ditolak lewat `raise ValueError` di `__init__` |
| Minimal 2 objek per class | `pemain1`, `pemain2`; `roster1`, `roster2` (Tim & Tournament didemonstrasikan 1 objek untuk fokus pada interaksi antar objek — tinggal duplikasi baris jika dosen ingin tegas 2 objek juga untuk `Tim`/`Tournament`) |
| Panggil semua jenis method di main code | Instance, class, dan static method semuanya dipanggil di bagian `if __name__ == "__main__":` |
| Uji setter valid vs tidak valid | Diuji untuk `rating`, `jumlah_main`, `hadiah`, plus uji `ValueError` saat membuat `Tournament` dengan nama mengandung angka |

---
