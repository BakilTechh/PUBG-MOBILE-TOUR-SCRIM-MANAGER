# Sistem Manajemen Scrim / Tournament PUBG Mobile (PBO - Python)

## Daftar Isi
- Relasi UML
- Inheritance
- Penjelasan Class
  1. Peserta, Pemain, Squad
  2. JadwalScrim
  3. Scrim
- Alur Program (main)
- Panduan Pengujian
- Kesimpulan

## Relasi UML

```
Peserta <|-- Pemain
Peserta <|-- Squad

Squad  o--  Pemain        (AGREGASI)
Scrim  *--  JadwalScrim    (KOMPOSISI)
Scrim  --   Squad          (ASOSIASI)
```

### Agregasi
Squad.anggota berisi objek Pemain yang dibuat di luar Squad, lalu
direkrut lewat `rekrut_pemain()`. Objek Pemain tetap ada walau objek
Squad-nya dihapus, karena dibuat terpisah dan tidak dimiliki secara
eksklusif.

Contoh:
```python
squad_sementara = Squad("Evos Reborn")
squad_sementara.rekrut_pemain(pemain_microboy)

del squad_sementara
pemain_microboy.tampilkan_info()   # Pemain masih bisa dipakai
```

### Komposisi
Scrim.jadwal adalah objek JadwalScrim yang dibuat otomatis di dalam
`Scrim.__init__`. Objek ini tidak pernah dibuat terpisah dari Scrim
pemiliknya, dan ikut lenyap begitu objek Scrim-nya dihapus.

Contoh:
```python
scrim_kampus = Scrim("Scrim Kampus")
scrim_kampus.jadwal.tampilkan_info()

del scrim_kampus   # JadwalScrim ikut hilang bersama Scrim
```

### Asosiasi
`Scrim.squad_unggulan` cuma referensi sementara ke objek `Squad yang sudah
ada sebelumnya. Scrim tidak memiliki Squad itu secara eksklusif.

Contoh:
```python
scrim_malam.pegang_squad(squad_btr)
scrim_malam.lepas_squad()
```

## Inheritance
Peserta menjadi superclass, diturunkan ke dua subclass: Pemain dan
Squad. Keduanya memanggil `super().__init__(...)` di konstruktornya, dan
masing-masing menambahkan atribut yang unik.

Contoh:
```python
class Pemain(Peserta):
    def __init__(self, nama, role, poin_awal=0):
        super().__init__(nama)
        self.role = role
        self.__poin_performa = max(0, poin_awal)
```

Method `tampilkan_aksi()` di-override di kedua subclass dengan perilaku
berbeda.

Contoh:
```python
squad_btr.tampilkan_aksi()     # "Menurunkan Squad ... ke arena"
pemain_ryzen.tampilkan_aksi()  # "Pemain ... sedang bertanding di arena"
```

`Peserta._nama` adalah atribut protected, diakses langsung oleh subclass
tanpa lewat property.

Contoh:
```python
print(f"Poin {pemain_ryzen._nama} setelah bertanding: ...")
```

## Penjelasan Class

### 1. Peserta, Pemain, Squad
`Peserta` adalah cetak biru dasar untuk siapa pun yang terdaftar di scrim.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `total_terdaftar` | Atribut kelas (publik) | Menghitung total objek `Peserta` (termasuk subclass) yang pernah dibuat |
| `kategori_game` | Atribut kelas (publik) | Nama game, sama untuk semua peserta |
| `_nama` | Atribut instance (protected) | Divalidasi saat objek dibuat |

Static method `validasi_nama()` memastikan nama tidak mengandung angka.

Contoh:
```python
Peserta.validasi_nama("Kairi")   # True
```

`Pemain(Peserta)` menambahkan `role` dan `__poin_performa` (privat, lewat
property). Class method `dari_dict()` adalah factory method: membangun
objek `Pemain` langsung dari dictionary.

Contoh:
```python
pemain_dari_data = Pemain.dari_dict({"nama": "Kiboy", "role": "Sniper", "poin": 40})
```

`Squad(Peserta)` menambahkan `kapasitas_maksimal` (atribut kelas),
`__dana_operasional` (privat, lewat property), dan `anggota` (list berisi
objek `Pemain`).

Contoh:
```python
squad_btr.rekrut_pemain(pemain_ryzen)
squad_btr.hapus_pemain_poin_kosong()
```

### 2. JadwalScrim
Komponen internal milik `Scrim` — menyimpan hari dan jam pelaksanaan scrim.

Contoh:
```python
jadwal = JadwalScrim("Minggu", "19.00")
jadwal.tampilkan_info()
```

### 3. Scrim
Merepresentasikan satu event scrim, menyimpan jadwalnya sendiri dan bisa
memegang referensi ke satu squad unggulan.

Contoh:
```python
scrim_malam = Scrim("Scrim Malam Mingguan")
```

## Alur Program (main)
Blok `if __name__ == "__main__":` menjalankan skenario pengujian berurutan:
uji class method, uji method overriding, uji instance method (rekrut
pemain), uji asosiasi, uji agregasi, uji komposisi, uji setter (data valid
dan tidak valid), uji hapus item, dan uji static method (termasuk
menangkap `ValueError` saat nama mengandung angka).

## Panduan Pengujian

**Cara menjalankan**
```bash
python main.py
```
Menggunakan Python standar (3.10+) tanpa modul eksternal.

**Uji manual lain yang bisa dicoba**
- Rekrut lebih dari `Squad.kapasitas_maksimal` (5) pemain ke satu squad,
  pastikan pesan "sudah mencapai kapasitas maksimal" muncul saat anggota
  ke-6 ditambahkan.
- Buat objek Pemain dan Squad lalu bandingkan hasil `tampilkan_aksi()`
  keduanya untuk melihat perbedaan override secara langsung.

## Kesimpulan
Program ini menunjukkan bagaimana `Peserta` sebagai superclass diturunkan
ke Pemain dan Squad dengan method yang di-override berbeda, bagaimana
atribut privat diakses lewat `@property` dengan validasi di setiap setter,
serta bagaimana ketiga relasi UML (asosiasi, agregasi, komposisi) berbeda
perilakunya saat objek pemiliknya dihapus — Pemain pada relasi agregasi
tetap hidup, sedangkan JadwalScrim pada relasi komposisi ikut lenyap
bersama Scrim yang memilikinya. Seluruh class method, instance method, dan
static method yang diwajibkan sudah diuji di bagian main code, lengkap
dengan pengujian data valid maupun tidak valid pada setiap setter.
