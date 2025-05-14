import subprocess # Note: Not directly used by GUI, but kept if core logic might need it elsewhere
import sys       # Note: Not directly used by GUI
import os        # Note: Not directly used by GUI
import base64
import random
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font as tkfont

# --- Constants for Styling ---
BG_COLOR = "#F4F4F4"  # A very light grey, almost white
TEXT_COLOR = "#333333"
ENTRY_BG_COLOR = "#FFFFFF"
BUTTON_PRIMARY_BG = "#0078D4" # A modern blue (e.g., Microsoft Fluent UI blue)
BUTTON_PRIMARY_FG = "#FFFFFF"
BUTTON_SECONDARY_BG = "#EAEAEA"
BUTTON_SECONDARY_FG = "#333333"
FONT_FAMILY_PREFERENCE = ("Segoe UI", "Calibri", "Helvetica Neue", "Helvetica", "Arial")
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 11

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
def generate_key(open_key, timestamp, log_func):
    log_func(f"Open Key: {open_key}")
    log_func(f"Timestamp: {timestamp}")
    
    ascii_values = [ord(char) for char in open_key]
    log_func(f"ASCII Values: {ascii_values}")
    
    day, month, year, hour, minute = timestamp
    formatted_time = [day, month, year % 100, year // 100, hour, minute]
    log_func(f"Formatted Time: {formatted_time}")
    
    combined = [
        ascii_values[i % len(ascii_values)] +
        formatted_time[i % len(formatted_time)]
        for i in range(len(ascii_values))
    ]
    log_func(f"Combined Values: {combined}")
    
    base_4_values = [to_base_4(value) for value in combined]
    log_func(f"Base-4 Values: {base_4_values}")
    
    dna_sequence = ''.join(DNA_MAP[int(digit)] for value in base_4_values for digit in value)
    log_func(f"DNA Sequence: {dna_sequence}")
    
    codons = [dna_sequence[i:i+3] for i in range(0, len(dna_sequence), 3)]
    log_func(f"Codons: {codons}")
    
    key = [sum(ord(char) for char in codon) % 100 for codon in codons]
    log_func(f"Generated Key: {key}")
    return key

# Rastgele IV üretimi
def generate_iv(length=16):
    iv = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=length))
    return iv

# XOR tabanlı şifreleme
def encrypt(plaintext, key, timestamp, log_func):
    log_func(f"Plaintext: {plaintext}")
    iv = generate_iv(16)
    log_func(f"Generated IV: {iv}")
    timestamp_str = ':'.join(map(str, timestamp))
    log_func(f"Timestamp String: {timestamp_str}")
    encrypted = ''.join(
        chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
        for i, char in enumerate(plaintext)
    )
    log_func(f"Encrypted Text (before encoding): {encrypted}")
    data_to_encode = f"{timestamp_str}:{iv}:{encrypted}"
    log_func(f"Data to Encode: {data_to_encode}")
    encoded = base64.urlsafe_b64encode(data_to_encode.encode()).decode()
    log_func(f"Encoded Encrypted Text: {encoded}")
    return encoded

# XOR tabanlı çözme
def decrypt(ciphertext, open_key, log_func):
    log_func(f"Ciphertext: {ciphertext}")
    try:
        decoded_data = base64.urlsafe_b64decode(ciphertext).decode()
        log_func(f"Decoded Data: {decoded_data}")
        # Split into 7 parts: 5 for timestamp, 1 for IV, 1 for encrypted text
        parts = decoded_data.split(':', 6) 
        if len(parts) < 7:
            log_func(f"Error: Decoded data '{decoded_data}' split into {len(parts)} parts, expected 7.")
            return None
            
        timestamp_str = ':'.join(parts[:5])
        iv = parts[5]
        encrypted_text = parts[6]
        
        log_func(f"Timestamp String: {timestamp_str}")
        log_func(f"IV: {iv}")
        log_func(f"Encrypted Text: {encrypted_text}")
        
        timestamp = tuple(map(int, timestamp_str.split(':')))
        log_func(f"Timestamp: {timestamp}")
        
        key = generate_key(open_key, timestamp, log_func)
        decrypted = ''.join(
            chr(ord(char) ^ key[i % len(key)] ^ ord(iv[i % len(iv)]))
            for i, char in enumerate(encrypted_text)
        )
        log_func(f"Decrypted Text: {decrypted}")
        return decrypted
    except (base64.binascii.Error, UnicodeDecodeError) as b64_err:
        log_func(f"Error decoding Base64 or UTF-8: {str(b64_err)}")
        return None
    except ValueError as ve:
        log_func(f"Error converting timestamp parts to int: {str(ve)}")
        return None
    except Exception as e:
        log_func(f"Error during decryption: {str(e)}")
        return None

# Sistem saati alma
def get_system_time():
    now = datetime.now()
    return now.day, now.month, now.year, now.hour, now.minute

# GUI sınıfı
class EncryptionApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Genetic Encryption Algorithm")
        self.root.geometry("800x700") # Adjusted size
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(700, 600)

        self.language = "en"
        self.active_font_family = self._get_active_font_family()
        self.font_normal = (self.active_font_family, FONT_SIZE_NORMAL)
        self.font_large_bold = (self.active_font_family, FONT_SIZE_LARGE, "bold")
        
        self.configure_styles()
        self.create_widgets()
        self.update_language() # Initialize texts

    def _get_active_font_family(self):
        available_fonts = tkfont.families(self.root)
        for family in FONT_FAMILY_PREFERENCE:
            if family in available_fonts:
                return family
        return "TkDefaultFont" # Fallback

    def configure_styles(self):
        style = ttk.Style(self.root)
        
        # Attempt to use a modern theme like 'clam' or 'alt', fallback to default
        # Some themes might ignore certain configurations if not fully compatible
        try:
            style.theme_use('clam') 
        except tk.TclError:
            try:
                style.theme_use('alt')
            except tk.TclError:
                pass # Use default theme

        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=self.font_normal)
        
        style.configure("TLabelframe", background=BG_COLOR, borderwidth=1, relief="groove")
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=TEXT_COLOR, font=self.font_large_bold)
        
        style.configure("TEntry", font=self.font_normal, padding=6, fieldbackground=ENTRY_BG_COLOR)
        
        style.configure("TCombobox", font=self.font_normal, padding=(6,6,6,6)) # More padding for combobox
        style.map("TCombobox", fieldbackground=[('readonly', ENTRY_BG_COLOR)])
        
        # Primary Buttons (Encrypt, Decrypt)
        style.configure("Primary.TButton", font=self.font_normal, padding=(12, 8), 
                        background=BUTTON_PRIMARY_BG, foreground=BUTTON_PRIMARY_FG)
        style.map("Primary.TButton",
                  background=[('active', '#0056b3'), ('disabled', '#B0B0B0')], # Darker blue on active, grey on disabled
                  foreground=[('disabled', '#707070')])

        # Secondary Button (Clear)
        style.configure("Secondary.TButton", font=self.font_normal, padding=(12, 8),
                        background=BUTTON_SECONDARY_BG, foreground=BUTTON_SECONDARY_FG)
        style.map("Secondary.TButton",
                  background=[('active', '#D0D0D0'), ('disabled', '#B0B0B0')],
                  foreground=[('disabled', '#707070')])
        
    def create_widgets(self):
        # Main container frame with padding
        container = ttk.Frame(self.root, padding="20 20 20 20")
        container.pack(fill=tk.BOTH, expand=True)

        # Configure grid column weights for responsiveness
        container.columnconfigure(0, weight=1) # Allow the single column to expand

        # --- Language Selection ---
        # Placed at the top right using grid's sticky option
        lang_outer_frame = ttk.Frame(container) # Extra frame for better positioning control
        lang_outer_frame.grid(row=0, column=0, sticky="ne", pady=(0, 10))

        self.lang_select_label = ttk.Label(lang_outer_frame, text="Language:") # Text set by update_language
        self.lang_select_label.pack(side="left", padx=(0,5))
        
        self.lang_var = tk.StringVar(value="en")
        lang_combo = ttk.Combobox(lang_outer_frame, textvariable=self.lang_var, values=["en", "tr"], 
                                  width=5, state="readonly", font=self.font_normal)
        lang_combo.pack(side="left")
        lang_combo.bind("<<ComboboxSelected>>", self.update_language)
        
        # --- Open Key ---
        self.key_labelframe = ttk.LabelFrame(container, text="Open Key") # Text set by update_language
        self.key_labelframe.grid(row=1, column=0, sticky="ew", pady=10)
        self.key_labelframe.columnconfigure(0, weight=1) # Make entry expand

        self.key_entry = ttk.Entry(self.key_labelframe, width=70)
        self.key_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # --- Text Input ---
        self.input_labelframe = ttk.LabelFrame(container, text="Input Text") # Text set by update_language
        self.input_labelframe.grid(row=2, column=0, sticky="nsew", pady=10)
        self.input_labelframe.columnconfigure(0, weight=1)
        self.input_labelframe.rowconfigure(0, weight=1) # Allow text area to expand vertically

        self.input_text = scrolledtext.ScrolledText(self.input_labelframe, height=6, width=70, 
                                                    font=self.font_normal, relief="solid", borderwidth=1,
                                                    bg=ENTRY_BG_COLOR, fg=TEXT_COLOR, wrap=tk.WORD)
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        container.rowconfigure(2, weight=1) # Make this section expandable

        # --- Buttons ---
        button_frame = ttk.Frame(container) # Frame to center buttons
        button_frame.grid(row=3, column=0, pady=(15,15)) # Increased vertical padding
        
        self.encrypt_button = ttk.Button(button_frame, text="Encrypt", command=self.encrypt_action, style="Primary.TButton")
        self.encrypt_button.pack(side="left", padx=8)
        
        self.decrypt_button = ttk.Button(button_frame, text="Decrypt", command=self.decrypt_action, style="Primary.TButton")
        self.decrypt_button.pack(side="left", padx=8)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields, style="Secondary.TButton")
        self.clear_button.pack(side="left", padx=8)
        
        # --- Output Area ---
        self.output_labelframe = ttk.LabelFrame(container, text="Output / Log") # Text set by update_language
        self.output_labelframe.grid(row=4, column=0, sticky="nsew", pady=10)
        self.output_labelframe.columnconfigure(0, weight=1)
        self.output_labelframe.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(self.output_labelframe, height=12, width=70, 
                                                     font=self.font_normal, relief="solid", borderwidth=1,
                                                     bg=ENTRY_BG_COLOR, fg=TEXT_COLOR, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.output_text.config(state="disabled")
        container.rowconfigure(4, weight=2) # Make output area more expandable

    def update_language(self, event=None):
        self.language = self.lang_var.get()
        if self.language == "en":
            self.root.title("Genetic Encryption Algorithm")
            self.lang_select_label.config(text="Language:")
            self.key_labelframe.config(text="Open Key")
            self.input_labelframe.config(text="Text to Encrypt/Decrypt")
            self.encrypt_button.config(text="Encrypt")
            self.decrypt_button.config(text="Decrypt")
            self.clear_button.config(text="Clear")
            self.output_labelframe.config(text="Output / Log")
        else: # tr
            self.root.title("Genetik Şifreleme Algoritması")
            self.lang_select_label.config(text="Dil:")
            self.key_labelframe.config(text="Açık Anahtar")
            self.input_labelframe.config(text="Şifrelenecek/Çözülecek Metin")
            self.encrypt_button.config(text="Şifrele")
            self.decrypt_button.config(text="Çöz")
            self.clear_button.config(text="Temizle")
            self.output_labelframe.config(text="Çıktı / Günlük")
    
    def log_to_output(self, message):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
    
    def _common_action_prep(self):
        open_key = self.key_entry.get().strip()
        text_content = self.input_text.get("1.0", tk.END).strip()
        
        if not open_key or not text_content:
            messagebox.showerror(
                "Error" if self.language == "en" else "Hata",
                "Open key and text cannot be empty!" if self.language == "en" else "Açık anahtar ve metin boş olamaz!"
            )
            return None, None
        
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        # Do not disable here, log_to_output will handle it
        return open_key, text_content

    def encrypt_action(self):
        open_key, plaintext = self._common_action_prep()
        if open_key is None: # Error occurred
            self.output_text.config(state="disabled") # Ensure it's disabled if prep failed
            return

        try:
            timestamp = get_system_time()
            key = generate_key(open_key, timestamp, self.log_to_output)
            encrypted_text = encrypt(plaintext, key, timestamp, self.log_to_output)
            
            self.log_to_output(f"\n--- {'Encrypted Text' if self.language == 'en' else 'Şifrelenmiş Metin'} ---")
            self.log_to_output(encrypted_text)
        except Exception as e:
            self.log_to_output(f"CRITICAL ENCRYPTION ERROR: {str(e)}")
            messagebox.showerror("Error" if self.language == "en" else "Hata",
                                 f"{'Encryption failed unexpectedly!' if self.language == 'en' else 'Şifreleme beklenmedik bir şekilde başarısız oldu!'}\n{str(e)}")
        finally:
            self.output_text.config(state="disabled")

    def decrypt_action(self):
        open_key, ciphertext = self._common_action_prep()
        if open_key is None: # Error occurred
            self.output_text.config(state="disabled") # Ensure it's disabled if prep failed
            return

        try:
            decrypted_text = decrypt(ciphertext, open_key, self.log_to_output)
            
            if decrypted_text is not None:
                self.log_to_output(f"\n--- {'Decrypted Text' if self.language == 'en' else 'Çözülen Metin'} ---")
                self.log_to_output(decrypted_text)
            else:
                # Error message already logged by decrypt function or due to its preconditions
                messagebox.showerror(
                    "Error" if self.language == "en" else "Hata",
                    "Decryption failed. Check the log, ciphertext, and open key." if self.language == "en" else "Çözme başarısız. Günlüğü, şifreli metni ve açık anahtarı kontrol edin."
                )
        except Exception as e: # Catch-all for unexpected issues during the process
            self.log_to_output(f"CRITICAL DECRYPTION ERROR: {str(e)}")
            messagebox.showerror("Error" if self.language == "en" else "Hata",
                                 f"{'Decryption failed unexpectedly!' if self.language == 'en' else 'Çözme beklenmedik bir şekilde başarısız oldu!'}\n{str(e)}")
        finally:
            self.output_text.config(state="disabled")
            
    def clear_fields(self):
        self.key_entry.delete(0, tk.END)
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

# Ana uygulama
if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
