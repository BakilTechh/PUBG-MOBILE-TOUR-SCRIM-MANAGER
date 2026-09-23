class Pemain:
    total_pemain_terdaftar = 0
    kategori_game = "PUBG MOBILE"
    role_tersedia = ("IGL", "Assaulter", "Support", "Sniper", "Flexer")

    def __init__(self, nama_pemain, nomor_id, role, poin_awal=0):
        self.nama_pemain = nama_pemain
        self.nomor_id = nomor_id
        self.role = role
        self.__poin_performa = 0
        self.poin_performa = poin_awal
        Pemain.total_pemain_terdaftar += 1

    def __repr__(self):
        return f"<Pemain {self.nama_pemain} | {self.role} | Poin: {self.__poin_performa}>"

    @property
    def poin_performa(self):
        return self.__poin_performa

    @poin_performa.setter
    def poin_performa(self, nilai):
        if not isinstance(nilai, (int, float)):
            raise ValueError(f"Poin performa harus berupa angka, diterima: {type(nilai).__name__}")
        if nilai < 0:
            raise ValueError("Poin performa tidak boleh bernilai negatif")
        self.__poin_performa = nilai

    def catat_hasil_pertandingan(self, jumlah_kill, damage_total):
        tambahan = (jumlah_kill * 4) + (damage_total // 100)
        self.poin_performa = self.__poin_performa + tambahan
        print(f"[LOG] {self.nama_pemain} mencatat {jumlah_kill} kill & {damage_total} dmg "
              f"-> poin performa naik jadi {self.__poin_performa}")

    @classmethod
    def buat_dari_data(cls, data: dict):
        """Factory method: membangun objek Pemain langsung dari data pendaftaran (dictionary)."""
        return cls(data["nama"], data["id"], data["role"], data.get("poin", 0))

    @staticmethod
    def cek_format_id(nomor_id):
        """Utility: ID pemain harus string angka sepanjang 8-12 digit."""
        return isinstance(nomor_id, str) and nomor_id.isdigit() and 8 <= len(nomor_id) <= 12


class Squad:
    total_squad_terdaftar = 0
    kapasitas_maksimal = 5
    region_utama = "Asia Tenggara"

    def __init__(self, nama_squad, region=None):
        self.nama_squad = nama_squad
        self.region = region if region else Squad.region_utama
        self.anggota = []
        self.__dana_operasional = 0
        Squad.total_squad_terdaftar += 1

    @property
    def dana_operasional(self):
        return self.__dana_operasional

    @dana_operasional.setter
    def dana_operasional(self, nilai):
        if not isinstance(nilai, (int, float)):
            raise ValueError(f"Dana operasional harus berupa angka, diterima: {type(nilai).__name__}")
        if nilai < 0:
            raise ValueError("Dana operasional tidak boleh bernilai negatif")
        self.__dana_operasional = nilai

    def rekrut_pemain(self, pemain: Pemain):
        if len(self.anggota) >= Squad.kapasitas_maksimal:
            print(f"[GAGAL] Squad {self.nama_squad} sudah mencapai kapasitas maksimal.")
            return False
        self.anggota.append(pemain)
        print(f"[INFO] {pemain.nama_pemain} resmi bergabung ke squad {self.nama_squad}.")
        return True

    def tampilkan_anggota(self):
        print(f"\nSquad: {self.nama_squad} ({self.region}) | Dana: {self.__dana_operasional}")
        if not self.anggota:
            print("  Belum ada anggota.")
        for p in self.anggota:
            print(" ", p)

    @classmethod
    def buat_dari_data(cls, data: dict):
        """Factory method: membangun objek Squad dari dictionary."""
        return cls(data["nama"], data.get("region"))

    @staticmethod
    def hitung_rata_rata_poin(daftar_pemain):
        """Utility: menghitung rata-rata poin performa dari sekumpulan pemain."""
        if not daftar_pemain:
            return 0
        total = sum(p.poin_performa for p in daftar_pemain)
        return round(total / len(daftar_pemain), 2)


class Scrim:
    total_scrim_dijalankan = 0
    penyelenggara = "Kampus Esports Arena"
    format_pertandingan = "Squad TPP"

    def __init__(self, judul_scrim, kuota_squad):
        self.judul_scrim = judul_scrim
        self.kuota_squad = kuota_squad
        self.daftar_squad_peserta = []
        self.__total_hadiah = 0
        Scrim.total_scrim_dijalankan += 1

    @property
    def total_hadiah(self):
        return self.__total_hadiah

    @total_hadiah.setter
    def total_hadiah(self, nilai):
        if not isinstance(nilai, (int, float)):
            raise ValueError(f"Total hadiah harus berupa angka, diterima: {type(nilai).__name__}")
        if nilai < 0:
            raise ValueError("Total hadiah tidak boleh bernilai negatif")
        self.__total_hadiah = nilai

    def undang_squad(self, squad: Squad):
        if len(self.daftar_squad_peserta) >= self.kuota_squad:
            print(f"[GAGAL] Kuota scrim {self.judul_scrim} sudah penuh.")
            return False
        self.daftar_squad_peserta.append(squad)
        print(f"[INFO] Squad {squad.nama_squad} diundang ke {self.judul_scrim}.")
        return True

    def tampilkan_papan_peringkat(self):
        print(f"\n=== PAPAN PERINGKAT {self.judul_scrim} | "
              f"Hadiah: {self.format_rupiah(self.__total_hadiah)} ===")
        if not self.daftar_squad_peserta:
            print("  Belum ada squad yang bertanding.")
            return
        peringkat = sorted(
            self.daftar_squad_peserta,
            key=lambda s: Squad.hitung_rata_rata_poin(s.anggota),
            reverse=True
        )
        for posisi, squad in enumerate(peringkat, start=1):
            rata2 = Squad.hitung_rata_rata_poin(squad.anggota)
            print(f"  #{posisi} {squad.nama_squad} - rata-rata poin: {rata2}")

    @classmethod
    def buat_dari_data(cls, data: dict):
        """Factory method: membangun objek Scrim dari dictionary."""
        return cls(data["judul"], data["kuota"])

    @staticmethod
    def format_rupiah(angka):
        """Utility: mengubah angka menjadi format mata uang Rupiah."""
        return f"Rp{angka:,.0f}".replace(",", ".")


if __name__ == "__main__":
    print("========== DEMO SISTEM SCRIM PUBG MOBILE ==========")

    print("\n[1] Membuat objek Pemain")
    pemain_a = Pemain("Baskara", "310045871", "IGL", 40)
    pemain_b = Pemain("Ryzen", "310098234", "Sniper", 35)
    pemain_c = Pemain.buat_dari_data({"nama": "Zuxxy", "id": "310077612", "role": "Assaulter", "poin": 30})

    for p in (pemain_a, pemain_b, pemain_c):
        print(" ", p)

    pemain_a.catat_hasil_pertandingan(jumlah_kill=6, damage_total=850)

    print(f"[KELAS] Total pemain terdaftar: {Pemain.total_pemain_terdaftar}")
    print("Cek format ID '310045871':", Pemain.cek_format_id("310045871"))
    print("Cek format ID 'ABC123':", Pemain.cek_format_id("ABC123"))

    print("\n[2] Membuat objek Squad")
    squad_x = Squad("Bigetron Alpha", "Asia Tenggara")
    squad_y = Squad.buat_dari_data({"nama": "Aura Esports"})

    squad_x.rekrut_pemain(pemain_a)
    squad_x.rekrut_pemain(pemain_b)
    squad_y.rekrut_pemain(pemain_c)

    squad_x.tampilkan_anggota()
    squad_y.tampilkan_anggota()

    print("Rata-rata poin Garuda Prime:", Squad.hitung_rata_rata_poin(squad_x.anggota))

    print("\n[3] Membuat objek Scrim")
    scrim_1 = Scrim("Scrim Malam Mingguan", 4)
    scrim_2 = Scrim.buat_dari_data({"judul": "Scrim Kualifikasi Kampus", "kuota": 8})

    scrim_1.total_hadiah = 1_500_000
    scrim_2.total_hadiah = 5_000_000

    scrim_1.undang_squad(squad_x)
    scrim_1.undang_squad(squad_y)

    scrim_1.tampilkan_papan_peringkat()
    print(f"[KELAS] Penyelenggara: {Scrim.penyelenggara} | "
          f"Total scrim dijalankan: {Scrim.total_scrim_dijalankan}")

    print("\n[4] Uji Validasi Setter (data valid vs tidak valid)")
    pemain_b.poin_performa = 60
    print(f"Poin performa {pemain_b.nama_pemain} (valid): {pemain_b.poin_performa}")
    try:
        pemain_b.poin_performa = -25
    except ValueError as e:
        print(f"[DITOLAK] {e}")

    squad_x.dana_operasional = 750_000
    print(f"Dana operasional {squad_x.nama_squad} (valid): {squad_x.dana_operasional}")
    try:
        squad_x.dana_operasional = -100_000
    except ValueError as e:
        print(f"[DITOLAK] {e}")

    try:
        scrim_2.total_hadiah = -1
    except ValueError as e:
        print(f"[DITOLAK] {e}")
    print(f"Total hadiah {scrim_2.judul_scrim} (tetap): {Scrim.format_rupiah(scrim_2.total_hadiah)}")

    print("\n========== SELESAI ==========")