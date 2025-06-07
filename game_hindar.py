import pygame
import random

# Inisialisasi Pygame
pygame.init()

# --- Pengaturan Layar ---
LEBAR_LAYAR = 800
TINGGI_LAYAR = 600
LAYAR = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption("Game Menghindari Objek Jatuh")

# --- Warna ---
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
MERAH = (255, 0, 0)
BIRU = (0, 0, 255)

# --- Pengaturan Pemain ---
UKURAN_PEMAIN = 50
KECEPATAN_PEMAIN = 5
PEMAIN_X = (LEBAR_LAYAR - UKURAN_PEMAIN) // 2
PEMAIN_Y = TINGGI_LAYAR - UKURAN_PEMAIN - 10
pemain_rect = pygame.Rect(PEMAIN_X, PEMAIN_Y, UKURAN_PEMAIN, UKURAN_PEMAIN)

# --- Pengaturan Objek Jatuh ---
UKURAN_OBJEK = 20
KECEPATAN_OBJEK_MIN = 3
KECEPATAN_OBJEK_MAX = 7
JUMLAH_OBJEK_MAX = 10
objek_jatuh = []

# --- Skor ---
SKOR = 0
FONT = pygame.font.Font(None, 36) # Font default, ukuran 36

# --- Fungsi untuk membuat objek baru ---
def buat_objek():
    x = random.randint(0, LEBAR_LAYAR - UKURAN_OBJEK)
    y = random.randint(-50, -20) # Muncul di atas layar
    kecepatan = random.randint(KECEPATAN_OBJEK_MIN, KECEPATAN_OBJEK_MAX)
    objek_jatuh.append(pygame.Rect(x, y, UKURAN_OBJEK, UKURAN_OBJEK))
    return kecepatan

# --- Variabel game ---
game_over = False
clock = pygame.time.Clock()

# --- Loop Game Utama ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # --- Input Pemain ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and pemain_rect.left > 0:
            pemain_rect.x -= KECEPATAN_PEMAIN
        if keys[pygame.K_RIGHT] and pemain_rect.right < LEBAR_LAYAR:
            pemain_rect.x += KECEPATAN_PEMAIN

        # --- Gerakkan Objek Jatuh ---
        for i, objek in enumerate(objek_jatuh):
            objek.y += (i % (KECEPATAN_OBJEK_MAX - KECEPATAN_OBJEK_MIN + 1)) + KECEPATAN_OBJEK_MIN # Variasi kecepatan
            if objek.top > TINGGI_LAYAR:
                objek_jatuh.pop(i) # Hapus objek jika sudah keluar layar
                SKOR += 1 # Tambah skor jika berhasil menghindari

        # --- Hasilkan Objek Baru ---
        if len(objek_jatuh) < JUMLAH_OBJEK_MAX and random.randint(0, 100) < 5: # Peluang 5% setiap frame
            buat_objek()

        # --- Deteksi Tabrakan ---
        for objek in objek_jatuh:
            if pemain_rect.colliderect(objek):
                game_over = True

        # --- Gambar ke Layar ---
        LAYAR.fill(HITAM) # Isi latar belakang dengan hitam
        pygame.draw.rect(LAYAR, BIRU, pemain_rect) # Gambar pemain
        for objek in objek_jatuh:
            pygame.draw.rect(LAYAR, MERAH, objek) # Gambar objek jatuh

        # --- Tampilkan Skor ---
        teks_skor = FONT.render(f"Skor: {SKOR}", True, PUTIH)
        LAYAR.blit(teks_skor, (10, 10))

    else:
        # Layar Game Over
        teks_game_over = FONT.render("GAME OVER!", True, PUTIH)
        teks_skor_akhir = FONT.render(f"Skor Akhir: {SKOR}", True, PUTIH)
        teks_restart = FONT.render("Tekan R untuk Restart", True, PUTIH)

        LAYAR.fill(HITAM)
        LAYAR.blit(teks_game_over, (LEBAR_LAYAR // 2 - teks_game_over.get_width() // 2, TINGGI_LAYAR // 2 - 50))
        LAYAR.blit(teks_skor_akhir, (LEBAR_LAYAR // 2 - teks_skor_akhir.get_width() // 2, TINGGI_LAYAR // 2))
        LAYAR.blit(teks_restart, (LEBAR_LAYAR // 2 - teks_restart.get_width() // 2, TINGGI_LAYAR // 2 + 50))

        # Input untuk restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            SKOR = 0
            objek_jatuh = []
            pemain_rect.x = PEMAIN_X # Reset posisi pemain

    # --- Update Layar ---
    pygame.display.flip()

    # --- Batasi Frame Rate ---
    clock.tick(60) # 60 frame per detik

# --- Keluar dari Pygame ---
pygame.quit()