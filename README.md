# 🧬 Genetic Encryption Algorithm

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure and innovative encryption algorithm that combines genetic algorithms with cryptographic techniques to provide robust data protection. This project includes both a command-line interface and a modern graphical user interface.

## ✨ Features

- **DNA-based Encryption**: Utilizes a genetic-inspired approach with DNA mapping (A, C, G, T)
- **Time-based Key Generation**: Generates unique encryption keys based on system time
- **XOR-based Encryption**: Implements XOR operations for secure data transformation
- **Graphical User Interface**: Modern, user-friendly interface with real-time logging
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Lightweight**: Minimal dependencies, easy to integrate

## 📦 Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- colorama (for colored console output)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GeneticEncryptionAlgorithm.git
   cd GeneticEncryptionAlgorithm
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install them manually:
   ```bash
   pip install colorama
   ```

## 🖥️ Usage

### Command Line Interface
Run the command-line version:
```bash
python Algorithm.py
```

### Graphical User Interface
Run the GUI version:
```bash
python Algorithm_gui.py
```

### How It Works

1. **Key Generation**:
   - Converts your secret key to ASCII values
   - Combines with system timestamp
   - Transforms using DNA mapping (A, C, G, T)

2. **Encryption**:
   - Takes plaintext and secret key as input
   - Generates a unique IV (Initialization Vector)
   - Performs XOR operations with the generated key
   - Returns base64-encoded ciphertext

3. **Decryption**:
   - Takes ciphertext and secret key
   - Reverses the encryption process
   - Returns the original plaintext

## 🎨 Screenshots

*GUI Interface will be added here*

## 📝 Example

### Encryption
```python
# Using the command line
> python Algorithm.py
> Select option (1-3): 1
> Enter your secret key: MySecretKey123
> Enter text to encrypt: Hello, World!
```

### Decryption
```python
> python Algorithm.py
> Select option (1-3): 2
> Enter your secret key: MySecretKey123
> Enter ciphertext to decrypt: [base64-encoded-ciphertext]
```

## 🛡️ Security Notes

- Always keep your secret key secure and never share it
- The strength of encryption depends on the complexity of your secret key
- For production use, consider additional security measures

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/yourusername/GeneticEncryptionAlgorithm](https://github.com/yourusername/GeneticEncryptionAlgorithm)

## 🙏 Acknowledgments

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Colorama](https://pypi.org/project/colorama/)
- [Shields.io](https://shields.io/)

---

<div align="center">
  Made with ❤️ using Python
</div>
