import subprocess
import sys
import os
import time
import base64
import random
from datetime import datetime
from colorama import Fore, Style, init

# Gerekli kütüphanelerin kurulumu
required_libraries = ["colorama"]
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Renkli terminal başlatma
init(autoreset=True)

# DNA haritası
DNA_MAP = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}

# Base-4’e çevirme
def to_base_4(value):
    result = ""
    while value > 0:
        result = str(value % 4) + result
        value //= 4
    return result.zfill(4)

# Anahtar üretimi
def generate_key(open_key, timestamp):
    print(f"Open Key: {open_key}")
    print(f"Timestamp: {timestamp}")
    
    # 1. Açık anahtarın ASCII değerlerini al
    ascii_values = [ord(char) for char in open_key]
    print(f"ASCII Values: {ascii_values}")
    
    # 2. Zamanı formatla
    day, month, year, hour, minute = timestamp
    formatted_time = [day, month, year % 100, year // 100, hour, minute]
    print(f"Formatted Time: {formatted_time}")
    
    # 3. ASCII ve zamanı birleştir
    combined = [
        ascii_values[i % len(ascii_values)] +
        formatted_time[i % len(formatted_time)]
        for i in range(len(ascii_values))
    ]
    print(f"Combined Values: {combined}")
    
    # 4. Base-4’e çevir
    base_4_values = [to_base_4(value) for value in combined]
    print(f"Base-4 Values: {base_4_values}")
    
    # 5. DNA harflerine çevir
    dna_sequence = ''.join(DNA_MAP[int(digit)] for value in base_4_values for digit in value)
    print(f"DNA Sequence: {dna_sequence}")
    
    # 6. Kodonlara böl
    codons = [dna_sequence[i:i+3] for i in range(0, len(dna_sequence), 3)]
    print(f"Codons: {codons}")
    
    # 7. ASCII toplamı %100 → Anahtar
    key = [sum(ord(char) for char in codon) % 100 for codon in codons]
    print(f"Generated Key: {key}")
    return key

# Rastgele IV üretimi
def generate_iv(length=16):
    iv = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=length))
    print(f"Generated IV: {iv}")
    return iv

# XOR tabanlı şifreleme
def encrypt(plaintext, key, timestamp):
    print(f"Plaintext: {plaintext}")
    iv = generate_iv(16)
    timestamp_str = ':'.join(map(str, timestamp))
    print(f"Timestamp String: {timestamp_str}")
    encrypted = ''.join(
        chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
        for i, char in enumerate(plaintext)
    )
    print(f"Encrypted Text (before encoding): {encrypted}")
    data_to_encode = f"{timestamp_str}:{iv}:{encrypted}"
    print(f"Data to Encode: {data_to_encode}")
    encoded = base64.urlsafe_b64encode(data_to_encode.encode()).decode()
    print(f"Encoded Encrypted Text: {encoded}")
    return encoded

# XOR tabanlı çözme
def decrypt(ciphertext, open_key):
    print(f"Ciphertext: {ciphertext}")
    decoded_data = base64.urlsafe_b64decode(ciphertext).decode()
    print(f"Decoded Data: {decoded_data}")
    parts = decoded_data.split(':', 6)
    timestamp_str = ':'.join(parts[:5])
    iv = parts[5]
    encrypted_text = parts[6]
    print(f"Timestamp String: {timestamp_str}")
    print(f"IV: {iv}")
    print(f"Encrypted Text: {encrypted_text}")
    timestamp = tuple(map(int, timestamp_str.split(':')))
    print(f"Timestamp: {timestamp}")
    key = generate_key(open_key, timestamp)
    decrypted = ''.join(
        chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
        for i, char in enumerate(encrypted_text)
    )
    print(f"Decrypted Text: {decrypted}")
    return decrypted

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
            encrypted_text = encrypt(plaintext, key, timestamp)
            print(Fore.LIGHTGREEN_EX + encrypted_message + encrypted_text)
        elif action == '2':
            ciphertext = input(text_decrypt_prompt)
            decrypted_text = decrypt(ciphertext, open_key)
            print(Fore.LIGHTGREEN_EX + decrypted_message + decrypted_text)

        input(Fore.LIGHTCYAN_EX + continue_prompt)

# Çalıştır
if __name__ == "__main__":
    main()
