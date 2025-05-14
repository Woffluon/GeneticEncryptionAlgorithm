import subprocess
import sys
import os
import time
import base64
import random
from datetime import datetime
from colorama import Fore, Style, init
from sympy import symbols

# Gerekli kütüphanelerin kurulumu
required_libraries = ["colorama", "sympy"]
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Renkli terminal başlatma
init(autoreset=True)

# DNA haritası
DNA_MAP = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}

# Belirtilen seed'e göre polinom üretimi
def polynomial_iteration(seed, degree=3):
    x = symbols('x')
    return [x**i + seed for i in range(degree)]

# Lagrange enterpolasyon fonksiyonu
def lagrange_interpolation(points):
    x = symbols('x')
    n = len(points)
    polynomial = 0
    for i in range(n):
        xi, yi = points[i]
        term = yi
        for j in range(n):
            if i != j:
                xj = points[j][0]
                term *= (x - xj) / (xi - xj)
        polynomial += term
    return polynomial

# Base-4’e çevirme
def to_base_4(value):
    result = ""
    while value > 0:
        result = str(value % 4) + result
        value //= 4
    return result.zfill(4)

# Anahtar üretimi (polinom ve lagrange katkılı)
def generate_key(open_key, timestamp):
    # 1. Seed hesapla
    seed = sum(ord(char) for char in open_key) + sum(timestamp)

    # 2. Polinomlar ve enterpolasyon
    polynomials = polynomial_iteration(seed)
    points = [(i, p.subs('x', i)) for i, p in enumerate(polynomials)]
    interpolation_poly = lagrange_interpolation(points)

    # 3. Zamanı formatla
    day, month, year, hour, minute = timestamp
    formatted_time = [day, month, year % 100, year // 100, hour, minute]

    # 4. ASCII değerleri al
    ascii_values = [ord(char) for char in open_key]

    # 5. Lagrange katkısı: pozisyona göre hesapla
    lagrange_modifiers = [int(interpolation_poly.subs('x', i)) % 50 for i in range(len(ascii_values))]

    # 6. Üçlü birleşim: ASCII + zaman + lagrange
    combined = [
        ascii_values[i % len(ascii_values)] +
        formatted_time[i % len(formatted_time)] +
        lagrange_modifiers[i % len(lagrange_modifiers)]
        for i in range(len(ascii_values))
    ]

    # 7. Base-4 çevir
    base_4_values = [to_base_4(value) for value in combined]

    # 8. DNA harflerine çevir
    dna_sequence = ''.join(DNA_MAP[int(digit)] for value in base_4_values for digit in value)

    # 9. Kodonlara böl
    codons = [dna_sequence[i:i+3] for i in range(0, len(dna_sequence), 3)]

    # 10. ASCII toplamı %100 → Anahtar
    return [sum(ord(char) for char in codon) % 100 for codon in codons]

# Rastgele IV üretimi
def generate_iv(length=16):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=length))

# XOR tabanlı şifreleme
def encrypt(plaintext, key):
    iv = generate_iv(16)
    encrypted = ''.join(
        chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
        for i, char in enumerate(plaintext)
    )
    return base64.urlsafe_b64encode(f"{iv}:{encrypted}".encode()).decode()

# XOR tabanlı çözme
def decrypt(ciphertext, key):
    decoded_data = base64.urlsafe_b64decode(ciphertext).decode()
    iv, encrypted_text = decoded_data.split(':', 1)
    return ''.join(
        chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
        for i, char in enumerate(encrypted_text)
    )

# Konsol temizleme
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Karşılama ekranı
def welcome_screen(language):
    clear_console()
    if language == "en":
        print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}" + "-"*50)
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}       GENETIC ENCRYPTION ALGORITHM")
        print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}" + "-"*50)
    else:
        print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}" + "-"*50)
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}         GENETİK ŞİFRELEME ALGORİTMASI")
        print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}" + "-"*50)

# Sistem saati alma
def get_system_time():
    now = datetime.now()
    return now.day, now.month, now.year, now.hour, now.minute

# Ana uygulama
def main():
    print("1: English")
    print("2: Türkçe")
    language = input("Select Language / Dil Seçin (1/2): ").strip()
    if language == "1":
        language = "en"
    elif language == "2":
        language = "tr"
    else:
        print("Invalid choice, defaulting to English")
        language = "en"

    while True:
        welcome_screen(language)
        if language == "en":
            print("1: Encrypt")
            print("2: Decrypt")
            action_prompt = "Choose an action (1/2): "
            key_prompt = "Enter Open Key: "
            text_encrypt_prompt = "Enter text to encrypt: "
            text_decrypt_prompt = "Enter text to decrypt: "
            encrypted_message = "Encrypted Text: "
            decrypted_message = "Decrypted Text: "
            continue_prompt = "Press ENTER to continue..."
        else:
            print("1: Şifrelemek için")
            print("2: Çözmek için")
            action_prompt = "Bir işlem seçin (1/2): "
            key_prompt = "Açık Anahtar Girin: "
            text_encrypt_prompt = "Şifrelenecek metni girin: "
            text_decrypt_prompt = "Çözülecek metni girin: "
            encrypted_message = "Şifrelenmiş Metin: "
            decrypted_message = "Çözülen Metin: "
            continue_prompt = "Devam etmek için ENTER'a basın..."

        action = input(action_prompt).strip()
        if action not in ['1', '2']:
            print(Fore.RED + "Invalid action. Please choose 1 or 2." if language == "en" else "Geçersiz işlem seçimi. Lütfen 1 veya 2 yazın.")
            continue

        open_key = input(key_prompt).strip()
        timestamp = get_system_time()
        key = generate_key(open_key, timestamp)

        if action == '1':
            plaintext = input(text_encrypt_prompt)
            encrypted_text = encrypt(plaintext, key)
            print(Fore.LIGHTGREEN_EX + encrypted_message + encrypted_text)
        elif action == '2':
            ciphertext = input(text_decrypt_prompt)
            decrypted_text = decrypt(ciphertext, key)
            print(Fore.LIGHTGREEN_EX + decrypted_message + decrypted_text)

        input(Fore.LIGHTCYAN_EX + continue_prompt)

# Çalıştır
if __name__ == "__main__":
    main()
