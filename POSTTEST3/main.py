# SISTEM MANAJEMEN SCRIM / TOURNAMENT PUBG MOBILE
from abc import ABC, abstractmethod


class JadwalScrim:
    """Class tambahan untuk mendemonstrasikan Komposisi pada class Scrim"""
    def __init__(self, hari, jam):
        self.hari = hari
        self.jam = jam

    def tampilkan_info(self):
        print(f"Hari: {self.hari}, Jam: {self.jam}")


# --- ABSTRACT CLASS (SUPERCLASS) ---
class Peserta(ABC):
    total_terdaftar = 0
    kategori_game = "PUBG MOBILE"

    def __init__(self, nama):
        if not self.validasi_nama(nama):
            raise ValueError("Nama tidak boleh mengandung angka")
        self._nama = nama
        Peserta.total_terdaftar += 1

    @staticmethod
    def validasi_nama(nama):
        return isinstance(nama, str) and not any(char.isdigit() for char in nama)

    # Abstract method: wajib diimplementasikan oleh setiap subclass
    @abstractmethod
    def tampilkan_aksi(self):
        pass

    @abstractmethod
    def hitung_skor(self):
        pass

    # Method konkret: dipakai bersama oleh semua subclass
    def tampilkan_info(self):
        print(f"Nama: {self._nama}")

    def jalankan(self):
        self.tampilkan_aksi()
        print(f"Skor {self._nama}: {self.hitung_skor()}")


# --- SUBCLASS 1 ---
class Pemain(Peserta):
    def __init__(self, nama, role, poin_awal=0):
        super().__init__(nama)
        self.role = role
        self.__poin_performa = max(0, poin_awal)

    @property
    def poin_performa(self):
        return self.__poin_performa

    @poin_performa.setter
    def poin_performa(self, nilai):
        # Nilai negatif akan tertahan di 0 (tidak mencetak error/ditolak)
        self.__poin_performa = max(0, nilai)

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"Role: {self.role}")
        print(f"Poin: {self.__poin_performa}")

    def bertanding(self, poin_tambahan):
        """Menambah poin pemain layaknya mengkonsumsi item."""
        self.poin_performa = self.__poin_performa + poin_tambahan
        print(f"Pemain {self._nama} mencetak kill, dan mendapatkan {poin_tambahan} poin")

    def tampilkan_aksi(self):
        """Implementasi abstract method: perilaku spesifik untuk pemain."""
        print(f"Pemain {self._nama} ({self.role}) sedang bertanding di arena")

    def hitung_skor(self):
        """Implementasi abstract method: skor pemain = poin performanya."""
        return self.__poin_performa

    @classmethod
    def dari_dict(cls, data: dict):
        """Factory method: membuat objek Pemain langsung dari dictionary data pendaftaran."""
        return cls(data["nama"], data["role"], data.get("poin", 0))

    # --- OPERATOR OVERLOADING ---
    def __str__(self):
        return f"{self._nama} ({self.role}) - {self.__poin_performa} poin"

    def __add__(self, other):
        return self.__poin_performa + other.poin_performa

    def __gt__(self, other):
        return self.__poin_performa > other.poin_performa


# --- SUBCLASS 2 ---
class Squad(Peserta):
    kapasitas_maksimal = 5

    def __init__(self, nama):
        super().__init__(nama)
        self.__dana_operasional = 0
        self.anggota = []

    @property
    def dana_operasional(self):
        return self.__dana_operasional

    @dana_operasional.setter
    def dana_operasional(self, nilai):
        self.__dana_operasional = max(0, nilai)

    def rekrut_pemain(self, pemain: Pemain):
        if len(self.anggota) >= Squad.kapasitas_maksimal:
            print(f"[GAGAL] Squad {self._nama} sudah mencapai kapasitas maksimal.")
            return
        self.anggota.append(pemain)

    def hapus_pemain_poin_kosong(self):
        self.anggota = [p for p in self.anggota if p.poin_performa > 0]

    def tampilkan_isi(self):
        for p in self.anggota:
            p.tampilkan_info()

    def tampilkan_aksi(self):
        """Implementasi abstract method: perilaku spesifik untuk squad."""
        print(f"Menurunkan Squad {self._nama} ke arena")

    def hitung_skor(self):
        """Implementasi abstract method: skor squad = total poin semua anggotanya."""
        return sum(p.poin_performa for p in self.anggota)

    # --- OPERATOR OVERLOADING ---
    def __len__(self):
        return len(self.anggota)


# --- CLASS UTAMA 3 ---
class Scrim:
    def __init__(self, judul):
        self.judul = judul
        self.jadwal = JadwalScrim("Minggu", "19.00")
        self.squad_unggulan = None

    def pegang_squad(self, squad: Squad):
        self.squad_unggulan = squad
        print(f"{self.judul} memegang: {squad._nama}")

    def lepas_squad(self):
        self.squad_unggulan = None
        print("Tidak ada squad yang dipegang")

    def tampilkan_info(self):
        print(f"Scrim: {self.judul}")

    def tampilkan_peringkat(self, daftar_peserta):
        """
        OCP & DIP: method ini hanya bergantung pada abstraksi Peserta
        (hitung_skor), bukan pada Pemain/Squad secara langsung. Daftar
        peserta disuntikkan dari luar, jadi subclass baru bisa langsung
        diperingkat tanpa mengubah kode Scrim.
        """
        urutan = sorted(daftar_peserta, key=lambda p: p.hitung_skor(), reverse=True)
        for no, peserta in enumerate(urutan, start=1):
            print(f"  #{no} {peserta._nama} - skor {peserta.hitung_skor()}")


# --- FUNGSI DUCK TYPING ---
def cetak_info(objek):
    """Tidak peduli tipe objeknya, asalkan punya method tampilkan_info()."""
    objek.tampilkan_info()


# MAIN CODE / PENGUJIAN PROGRAM
if __name__ == "__main__":

    squad_btr = Squad("Bigetron Alpha")
    pemain_ryzen = Pemain("Ryzen", "Rusher", 0)
    pemain_zuxxy = Pemain("Zuxxy", "IGL", 50)
    scrim_malam = Scrim("Scrim Malam Mingguan")

    print("UJI CLASS METHOD")
    pemain_dari_data = Pemain.dari_dict({"nama": "Kiboy", "role": "Sniper", "poin": 40})
    print(f"Pemain berhasil dibuat lewat class method: {pemain_dari_data._nama}")

    print("\nUJI METHOD OVERRIDING")
    squad_btr.tampilkan_aksi()
    pemain_ryzen.bertanding(50)
    print(f"Poin {pemain_ryzen._nama} setelah bertanding: {pemain_ryzen.poin_performa}")

    print("\nUJI INSTANCE METHOD")
    print("Daftar Anggota Sebelum:\n")
    squad_btr.tampilkan_isi()

    squad_btr.rekrut_pemain(pemain_ryzen)
    print("Daftar Anggota Sesudah:")
    squad_btr.tampilkan_isi()
    print()

    squad_btr.rekrut_pemain(pemain_zuxxy)
    print(f"Daftar Anggota Sesudah Ditambah Lagi ({pemain_zuxxy._nama}, formasi digabung):")
    squad_btr.tampilkan_isi()

    print("\nUJI ABSTRAKSI (ABSTRACT CLASS)")
    print("Mencoba membuat objek langsung dari Peserta (abstract class)...")
    try:
        peserta_langsung = Peserta("Anonim")
    except TypeError as e:
        print(f"TypeError tertangkap: {e}")

    print("\nMethod konkret jalankan() dipakai bersama oleh semua subclass:")
    pemain_zuxxy.jalankan()
    squad_btr.jalankan()

    print("\nUJI POLIMORFISME (PEWARISAN)")
    for peserta in [pemain_ryzen, squad_btr, pemain_zuxxy]:
        peserta.tampilkan_aksi()
        print(f"  Skor: {peserta.hitung_skor()}")

    print("\nUJI DUCK TYPING")
    jadwal_uji = JadwalScrim("Sabtu", "20.00")
    for objek in (jadwal_uji, scrim_malam):
        cetak_info(objek)

    print("\nUJI OPERATOR OVERLOADING")
    print(f"__str__ : {pemain_ryzen}")
    print(f"__add__ : {pemain_ryzen._nama} + {pemain_zuxxy._nama} = {pemain_ryzen + pemain_zuxxy} poin")
    print(f"__gt__  : {pemain_ryzen._nama} > {pemain_dari_data._nama} ? {pemain_ryzen > pemain_dari_data}")
    print(f"__len__ : jumlah anggota {squad_btr._nama} = {len(squad_btr)}")

    print("\nUJI ASOSIASI")
    scrim_malam.pegang_squad(squad_btr)
    squad_btr.tampilkan_aksi()
    scrim_malam.lepas_squad()

    print("\nUJI AGREGASI (Squad dihapus, Pemain tetap ada)")
    pemain_microboy = Pemain("Microboy", "Support", 30)
    squad_sementara = Squad("Evos Reborn")
    squad_sementara.rekrut_pemain(pemain_microboy)
    print("Squad berisi:")
    squad_sementara.tampilkan_isi()

    del squad_sementara
    print("\nSquad dihapus. Pemain Microboy masih ada:")
    pemain_microboy.tampilkan_info()

    print("\nUJI KOMPOSISI (Scrim dihapus, Jadwal ikut hilang)")
    scrim_kampus = Scrim("Scrim Kampus")
    print(f"Jadwal milik {scrim_kampus.judul}:")
    scrim_kampus.jadwal.tampilkan_info()

    del scrim_kampus
    print("\nScrim dihapus, Jadwal nya juga akan ikut hilang")

    print("\nUJI SOLID (OCP & DIP)")
    squad_alter = Squad("Alter Ego")
    squad_alter.rekrut_pemain(pemain_microboy)
    squad_alter.rekrut_pemain(pemain_dari_data)

    print("Peringkat Pemain:")
    scrim_malam.tampilkan_peringkat([pemain_ryzen, pemain_zuxxy, pemain_dari_data, pemain_microboy])
    print("Peringkat Squad (kode Scrim tidak diubah sama sekali):")
    scrim_malam.tampilkan_peringkat([squad_btr, squad_alter])

    print("\nUJI SETTER")
    squad_btr.dana_operasional = 100
    pemain_ryzen.poin_performa = 6
    print(f"Dana Operasional {squad_btr._nama} (Valid): {squad_btr.dana_operasional}")
    print(f"Poin Performa {pemain_ryzen._nama} (Valid): {pemain_ryzen.poin_performa}")

    squad_btr.dana_operasional = -500
    pemain_ryzen.poin_performa = -10
    print(f"Dana Operasional {squad_btr._nama} (Tidak Valid -500): {squad_btr.dana_operasional} (Tertahan di 0)")
    print(f"Poin Performa {pemain_ryzen._nama} (Tidak Valid -10): {pemain_ryzen.poin_performa} (Tertahan di 0)")

    print("\nUJI HAPUS ITEM (INSTANCE METHOD)")
    pemain_ryzen.poin_performa = 0
    print("Daftar Anggota Sebelum Dihapus:")
    squad_btr.tampilkan_isi()

    squad_btr.hapus_pemain_poin_kosong()

    print("\nDaftar Anggota Sesudah Dihapus:")
    squad_btr.tampilkan_isi()

    print("\nUJI STATIC METHOD")
    uji_nama = Peserta.validasi_nama("Kairi")
    print(f"Hasil static method untuk 'Kairi': {uji_nama}")

    print("Uji coba membuat peserta dengan angka (Kairikumar777)...")
    try:
        pemain_error = Pemain("Kairikumar777", "Support")
    except ValueError as e:
        print(f"Error tertangkap: {e}")