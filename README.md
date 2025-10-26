# 🎙️ Voice-Controlled Embedded System (Windows)

A sophisticated voice-controlled Arduino system that uses AI for speech recognition and natural language processing. Speak commands to control LEDs, servos, and other components through an intelligent interface.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Arduino](https://img.shields.io/badge/arduino-nano%2Funo-green)
![Windows](https://img.shields.io/badge/platform-windows-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Troubleshooting](#troubleshooting)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Voice Recognition**: Real-time speech-to-text using OpenAI's Whisper model
- **Natural Language Processing**: AI-powered command interpretation using Llama 3.1
- **Text-to-Speech**: Audio feedback for system responses using Windows TTS
- **Multi-threaded Architecture**: Responsive UI with parallel processing
- **Sequential Command Execution**: Execute complex command sequences
- **Hardware Control**: 
  - LED control (white and red)
  - Servo motor control
  - Easily extensible for additional components

## 🏗️ System Architecture

```
┌─────────────┐
│   User      │
│  (Voice)    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Python Control System           │
│  ┌────────────────────────────┐    │
│  │  Speech Recognition        │    │
│  │  (Whisper Model)           │    │
│  └────────┬───────────────────┘    │
│           │                         │
│           ▼                         │
│  ┌────────────────────────────┐    │
│  │  Natural Language          │    │
│  │  Processing (Llama 3.1)    │    │
│  └────────┬───────────────────┘    │
│           │                         │
│           ▼                         │
│  ┌────────────────────────────┐    │
│  │  Command Parser            │    │
│  └────────┬───────────────────┘    │
│           │                         │
│           ▼                         │
│  ┌────────────────────────────┐    │
│  │  Serial Communication      │    │
│  └────────┬───────────────────┘    │
└───────────┼─────────────────────────┘
            │
            ▼ (Serial: COM12)
┌─────────────────────────────────────┐
│      Arduino Nano/Uno               │
│  ┌────────────────────────────┐    │
│  │  Command Interpreter       │    │
│  └────────┬───────────────────┘    │
│           │                         │
│           ▼                         │
│  ┌────────────────────────────┐    │
│  │  Hardware Controllers      │    │
│  │  - LEDs                    │    │
│  │  - Servo Motor             │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
```

## 🛠️ Hardware Requirements

### Required Components

| Component | Quantity | Specifications |
|-----------|----------|----------------|
| Arduino Nano/Uno | 1 | ATmega328P |
| White LED | 1 | 5mm, with 220Ω resistor |
| Red LED | 1 | 5mm, with 220Ω resistor |
| Servo Motor | 1 | SG90 or similar (0-180°) |
| Breadboard | 1 | Standard size |
| Jumper Wires | 10+ | Male-to-male |
| USB Cable | 1 | Arduino compatible |
| Microphone | 1 | For voice input (built-in or USB) |

### Pin Configuration

```
Arduino Pin  →  Component
─────────────────────────────
Pin 9        →  White LED (+) → 220Ω Resistor → GND
Pin 10       →  Red LED (+) → 220Ω Resistor → GND
Pin 11       →  Servo Signal (Orange/Yellow)
5V           →  Servo Power (Red)
GND          →  Servo Ground (Brown/Black)
```

## 💻 Software Requirements

### System Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.10 or 3.11
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space for models
- **GPU**: Optional (NVIDIA with CUDA for faster processing)

### Required Software
- Python 3.10+ (from python.org or Microsoft Store)
- Pyenv-win (for Python version management)
- Arduino CLI (for Arduino programming)
- Ollama (for LLM inference)
- Git for Windows

### Python Dependencies
- `torch` - PyTorch for ML models
- `transformers` - Hugging Face Transformers (Whisper)
- `pyserial` - Serial communication
- `sounddevice` - Audio recording
- `numpy` - Numerical operations
- `keyboard` - Keyboard event handling (requires admin rights)
- `pyttsx3` - Text-to-speech (uses Windows SAPI)
- `ollama` - Ollama client

## 📦 Installation

### 1. Install Prerequisites

#### Install Python
```powershell
# Option 1: Download from python.org
# Visit https://www.python.org/downloads/ and install Python 3.11

# Option 2: Using winget (Windows Package Manager)
winget install Python.Python.3.11

# Verify installation
python --version
```

#### Install Git
```powershell
winget install Git.Git
```

#### Install Pyenv-win (Optional - for managing Python versions)
```powershell
# Using PowerShell (Run as Administrator)
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# Add to PATH (if not automatically added)
# Add these to System Environment Variables:
# %USERPROFILE%\.pyenv\pyenv-win\bin
# %USERPROFILE%\.pyenv\pyenv-win\shims
```

#### Install Arduino CLI
```powershell
# Using winget
winget install ArduinoSA.Arduino-CLI

# Verify installation
arduino-cli version
```

#### Install Ollama
```powershell
# Download and install from https://ollama.com/download/windows
# Or use winget:
winget install Ollama.Ollama

# After installation, pull the model
ollama pull llama3.1
```

### 2. Clone the Repository

```powershell
# Open PowerShell or Command Prompt
git clone https://github.com/YOUR_USERNAME/voice-controlled-system.git
cd voice-controlled-system
```

### 3. Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

### 4. Install Python Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install PyTorch (CPU version - recommended for most users)
pip install torch torchvision torchaudio

# For NVIDIA GPU users (faster processing):
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install pyserial numpy sounddevice keyboard pyttsx3 ollama transformers

# Or use requirements.txt
pip install -r requirements.txt
```

### 5. Setup Arduino CLI

```powershell
# Initialize Arduino CLI
arduino-cli config init

# Update core index
arduino-cli core update-index

# Install Arduino AVR core
arduino-cli core install arduino:avr

# Install Servo library
arduino-cli lib install "Servo"
```

### 6. Find Your Arduino Port

```powershell
# List connected Arduino boards
arduino-cli board list

# Output will look like:
# Port         Protocol Type              Board Name FQBN
# COM3         serial   Serial Port (USB) Arduino Nano arduino:avr:nano
# COM12        serial   Serial Port (USB) Arduino Uno arduino:avr:uno

# Note your COM port (e.g., COM3, COM12, etc.)
```

### 7. Upload Arduino Sketch

```powershell
# Navigate to Arduino sketch folder
cd arduino_sketch\voice_control_arduino

# Compile for Arduino Nano (Old Bootloader - most common for clones)
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old voice_control_arduino.ino

# Upload (replace COM3 with your port)
arduino-cli upload -p COM3 --fqbn arduino:avr:nano:cpu=atmega328old voice_control_arduino.ino

# For Arduino Uno, use:
# arduino-cli compile --fqbn arduino:avr:uno voice_control_arduino.ino
# arduino-cli upload -p COM3 --fqbn arduino:avr:uno voice_control_arduino.ino

# Verify upload with serial monitor
arduino-cli monitor -p COM3 -c baudrate=9600
# Press Ctrl+C to exit monitor
```

## 🔌 Hardware Setup

### Circuit Diagram

```
                    Arduino Nano
                   ┌─────────────┐
                   │             │
   White LED ──────┤ D9      VIN │
   Red LED ────────┤ D10     GND ├──── GND Rail
   Servo Signal ───┤ D11      5V ├──── Power Rail
                   │             │
                   │         RST │
                   │             │
                   │         GND ├──── GND Rail
                   └─────────────┘
```

### Step-by-Step Wiring

1. **White LED (Pin 9)**:
   - Connect longer leg (anode) → 220Ω resistor → Arduino Pin 9
   - Connect shorter leg (cathode) → GND

2. **Red LED (Pin 10)**:
   - Connect longer leg (anode) → 220Ω resistor → Arduino Pin 10
   - Connect shorter leg (cathode) → GND

3. **Servo Motor (Pin 11)**:
   - Brown/Black wire → GND
   - Red wire → 5V
   - Orange/Yellow wire → Pin 11

4. **Power**:
   - Connect Arduino to computer via USB

## 🚀 Usage

### Starting the System

**Method 1: Using PowerShell (Recommended)**

```powershell
# Step 1: Start Ollama (in a separate PowerShell window)
ollama serve

# Step 2: Navigate to project folder
cd C:\path\to\voice-controlled-system

# Step 3: Activate virtual environment
.\venv\Scripts\activate

# Step 4: Update serial port in main.py (if needed)
# Open main.py and change COM port:
#   "serial_port": "COM3",  # Change to your COM port

# Step 5: Run the application (requires Administrator privileges)
# Right-click PowerShell and "Run as Administrator"
python main.py
```

**Method 2: Using Batch Script (Easy Method)**

Create a file named `run.bat`:
```batch
@echo off
echo Starting Voice-Controlled System...
echo.

REM Start Ollama in background
start /B ollama serve

REM Wait for Ollama to start
timeout /t 3 /nobreak > nul

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python main.py

pause
```

Then simply double-click `run.bat` to start the system.

### Using Voice Commands

1. **Start Recording**: Hold the `Ctrl` key
2. **Speak Clearly**: Give your command while holding Ctrl
3. **Stop Recording**: Release the `Ctrl` key
4. **Wait for Response**: The AI will process and respond
5. **Exit Program**: Press `Esc`

### Example Voice Commands

```
"Turn on the white LED"
→ AI Response: "I'll turn on the white LED for you."
→ Executes: U:3;S:1;

"Blink the red LED and rotate the servo"
→ AI Response: "I'll blink the red LED and rotate the servo."
→ Executes: D:2;S:0.5;D:2;S:0.5;R:2;S:1;

"Operate the components randomly"
→ AI Response: "I'll operate these components in a random sequence."
→ Executes: R:2;S:0.5;U:1;D:2;R:1;U:2;S:1;

"Stop everything"
→ AI Response: "Stopping all operations."
→ Executes: S:1;
```

## 📖 Command Reference

### Arduino Commands

| Command | Description | Duration |
|---------|-------------|----------|
| `U` | Turn ON white LED | User-defined |
| `D` | Turn ON red LED | User-defined |
| `R` | Rotate servo to 90° | User-defined |
| `S` | Stop all (LEDs off, servo to 0°) | N/A |

### Command Format

Commands are sent as timed sequences:
```
FORMAT: [COMMAND]:[DURATION];
EXAMPLE: U:3;S:0.5;D:2;
```

This means:
- `U:3;` → White LED ON for 3 seconds
- `S:0.5;` → Stop for 0.5 seconds
- `D:2;` → Red LED ON for 2 seconds

## 🐛 Troubleshooting

### Common Issues (Windows Specific)

#### 1. "Access is denied" when running main.py
**Solution**: Run PowerShell or Command Prompt as Administrator
```powershell
# Right-click PowerShell → "Run as Administrator"
cd C:\path\to\voice-controlled-system
.\venv\Scripts\activate
python main.py
```

#### 2. Serial Port Access Denied
**Solution**: Close Arduino IDE, Serial Monitor, or any program using the COM port
```powershell
# Check which program is using the port
# Close Arduino IDE and other serial programs
# Then try again
```

#### 3. Arduino Not Detected
```powershell
# Install CH340 drivers (for Arduino clones)
# Download from: http://www.wch.cn/downloads/CH341SER_ZIP.html

# Check Device Manager
# Look for "Ports (COM & LPT)"
# Your Arduino should appear as "USB-SERIAL CH340 (COMX)"
```

#### 4. Microphone Not Working
```powershell
# Check Windows microphone permissions
# Settings → Privacy → Microphone → Allow apps to access microphone

# Test microphone in Python
python -c "import sounddevice as sd; print(sd.query_devices())"

# If microphone still doesn't work, install audio backend:
pip install pyaudio
```

#### 5. Ollama Not Starting
```powershell
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve

# In another window, verify model is installed:
ollama list

# If model not installed:
ollama pull llama3.1
```

#### 6. "pyttsx3" TTS Not Working
```powershell
# Reinstall pyttsx3
pip uninstall pyttsx3
pip install pyttsx3

# Check Windows Speech settings
# Settings → Time & Language → Speech → Make sure a voice is selected
```

#### 7. PyTorch CUDA Issues (GPU Users)
```powershell
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA support:
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA installation
nvidia-smi
```

#### 8. Virtual Environment Activation Issues
```powershell
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.\venv\Scripts\activate
```

#### 9. Arduino Upload Failed (Wrong Bootloader)
```powershell
# Try new bootloader instead of old:
arduino-cli upload -p COM3 --fqbn arduino:avr:nano:cpu=atmega328 voice_control_arduino.ino

# Or for Uno:
arduino-cli upload -p COM3 --fqbn arduino:avr:uno voice_control_arduino.ino
```

## ⚙️ Configuration

### Python Configuration (main.py)

```python
CONFIG = {
    "whisper_model": "openai/whisper-small",  # Model size: tiny, base, small, medium
    "llm_model": "llama3.1",                   # Ollama model name
    "sample_rate": 16000,                      # Audio sample rate
    "record_key": "ctrl",                      # Recording hotkey
    "serial_port": "COM3",                     # Arduino COM port (CHANGE THIS!)
    "baud_rate": 9600,                         # Serial baud rate
    "response_timeout": 15,                    # LLM timeout (seconds)
}
```

### Finding Your COM Port

```powershell
# Method 1: Arduino CLI
arduino-cli board list

# Method 2: Device Manager
# Windows Key → Type "Device Manager"
# Expand "Ports (COM & LPT)"
# Look for Arduino device (shows COM number)

# Method 3: Python
python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
```

### Customizing Voice Commands

Edit the `SYSTEM_PROMPT` in `main.py` to modify AI behavior:

```python
SYSTEM_PROMPT = """
You are an AI assistant controlling an Embedded System...
[Modify this to change AI's understanding and responses]
"""
```

### Hardware Pin Configuration (Arduino)

Edit pin definitions in `voice_control_arduino.ino`:

```cpp
const int WHITE_LED_PIN = 9;   // Change to your pin
const int RED_LED_PIN = 10;    // Change to your pin
const int SERVO_PIN = 11;      // Change to your pin
```

## 📁 Project Structure

```
voice-controlled-system/
│
├── main.py                      # Main Python application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── run.bat                      # Windows batch script to run
├── .gitignore                   # Git ignore rules
│
├── arduino_sketch/
│   └── voice_control_arduino/
│       └── voice_control_arduino.ino  # Arduino code
│
├── venv/                        # Virtual environment (created during setup)
│
└── docs/
    ├── WINDOWS_SETUP.md        # Detailed Windows setup guide
    └── TROUBLESHOOTING.md      # Extended troubleshooting
```

## 🎯 Quick Start Checklist

- [ ] Install Python 3.10 or 3.11
- [ ] Install Git for Windows
- [ ] Install Arduino CLI
- [ ] Install Ollama and download llama3.1 model
- [ ] Clone the repository
- [ ] Create virtual environment
- [ ] Install Python dependencies
- [ ] Wire up Arduino components
- [ ] Upload Arduino sketch
- [ ] Update COM port in main.py
- [ ] Run as Administrator
- [ ] Test with voice commands

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition model
- **Meta Llama** - Language model
- **Ollama** - Local LLM inference
- **Arduino Community** - Hardware platform and libraries

## 📧 Contact

Project Link: [https://github.com/YOUR_USERNAME/voice-controlled-system](https://github.com/YOUR_USERNAME/voice-controlled-system)

## 🗺️ Roadmap

- [ ] Add support for more Arduino boards (ESP32, Mega)
- [ ] Create Windows installer (.exe)
- [ ] Add GUI interface with PyQt
- [ ] Support for multiple language voice commands
- [ ] Add motor driver support for DC motors
- [ ] Implement web interface for remote control
- [ ] Add command history and logging
- [ ] Create mobile app interface

## 📊 Performance (Windows)

- **Voice Recognition Latency**: ~2-3 seconds (CPU) / ~1-2 seconds (GPU)
- **LLM Response Time**: ~3-5 seconds
- **Serial Communication**: 9600 baud (adjustable)
- **Command Execution**: Real-time
- **RAM Usage**: ~1-2GB (with models loaded)

## 🔒 Security Notes

- This system runs locally - no cloud dependencies
- Requires Administrator privileges for keyboard monitoring
- Microphone access required for voice input
- Serial port access required for Arduino communication
- No sensitive data is transmitted externally
- Windows Defender may flag keyboard library (false positive)

## 💡 Windows-Specific Tips

1. **Run as Administrator**: Required for keyboard library to work
2. **Disable Antivirus temporarily**: If it blocks keyboard library
3. **Use PowerShell ISE**: Better for debugging
4. **Check Windows Updates**: Ensure latest drivers are installed
5. **Use USB 2.0 ports**: More stable for Arduino connection
6. **Close Arduino IDE**: Before running the Python script
7. **Install Visual C++ Redistributable**: If you get DLL errors

---

**Made with ❤️ for Windows Users**

*Last Updated: October 2025*
