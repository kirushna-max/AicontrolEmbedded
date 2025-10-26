# 🎙️ Voice-Controlled Embedded System

A sophisticated voice-controlled Arduino system that uses AI for speech recognition and natural language processing. Speak commands to control LEDs, servos, and other components through an intelligent interface.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Arduino](https://img.shields.io/badge/arduino-nano%2Funo-green)
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
- **Text-to-Speech**: Audio feedback for system responses
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
            ▼ (Serial: /dev/ttyUSB0)
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
| Microphone | 1 | For voice input |

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
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space for models

### Required Software
- Python 3.10+
- Pyenv (for Python version management)
- Arduino CLI (for Arduino programming)
- Ollama (for LLM inference)
- Git (for version control)

### Python Dependencies
- `torch` - PyTorch for ML models
- `transformers` - Hugging Face Transformers (Whisper)
- `pyserial` - Serial communication
- `sounddevice` - Audio recording
- `numpy` - Numerical operations
- `keyboard` - Keyboard event handling
- `pyttsx3` - Text-to-speech
- `ollama` - Ollama client

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/voice-controlled-system.git
cd voice-controlled-system
```

### 2. Setup Python Environment

```bash
# Install and set Python version
pyenv install 3.11.9
pyenv local 3.11.9

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install PyTorch (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
pip install pyserial numpy sounddevice keyboard pyttsx3 ollama transformers

# Or use requirements.txt
pip install -r requirements.txt
```

### 4. Install Ollama

```bash
# Linux/Mac:
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com/download

# Pull the LLM model
ollama pull llama3.1
```

### 5. Install Arduino CLI

```bash
# Linux/Mac:
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Windows:
winget install ArduinoSA.Arduino-CLI

# Initialize and install cores
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli lib install "Servo"
```

### 6. Upload Arduino Sketch

```bash
# Navigate to Arduino sketch folder
cd arduino_sketch

# Compile
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old voice_control_arduino.ino

# Upload (replace /dev/ttyUSB0 with your port)
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old voice_control_arduino.ino

# Verify upload
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=9600
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

1. **Start Ollama Server** (in a separate terminal):
```bash
ollama serve
```

2. **Update Configuration**:
Edit `main.py` and update the serial port:
```python
CONFIG = {
    "serial_port": "/dev/ttyUSB0",  # Change to your port
    # ... other settings
}
```

3. **Run the Python Script**:
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

4. **Using Voice Commands**:
   - Hold `Ctrl` key to start recording
   - Speak your command clearly
   - Release `Ctrl` to stop recording
   - Wait for AI processing and response
   - Press `Esc` to exit the program

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

### Common Issues

#### 1. Serial Port Not Found
```bash
# List available ports
arduino-cli board list

# On Linux, add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

#### 2. Microphone Not Working
```bash
# Test microphone
python -c "import sounddevice as sd; print(sd.query_devices())"

# Install audio dependencies (Linux)
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### 3. Ollama Connection Failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify model is downloaded
ollama list
```

#### 4. Arduino Upload Failed
```bash
# Try with different bootloader
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328 voice_control_arduino.ino

# Check permissions (Linux)
sudo chmod 666 /dev/ttyUSB0
```

#### 5. Speech Recognition Not Working
- Ensure microphone permissions are granted
- Check if correct audio device is selected
- Speak clearly and closer to microphone
- Reduce background noise

## ⚙️ Configuration

### Python Configuration (main.py)

```python
CONFIG = {
    "whisper_model": "openai/whisper-small",  # Model size: tiny, base, small, medium
    "llm_model": "llama3.1",                   # Ollama model name
    "sample_rate": 16000,                      # Audio sample rate
    "record_key": "ctrl",                      # Recording hotkey
    "serial_port": "/dev/ttyUSB0",            # Arduino port
    "baud_rate": 9600,                         # Serial baud rate
    "response_timeout": 15,                    # LLM timeout (seconds)
}
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
├── .gitignore                   # Git ignore rules
│
├── arduino_sketch/
│   └── voice_control_arduino/
│       └── voice_control_arduino.ino  # Arduino code
│
├── docs/
│   ├── HARDWARE_SETUP.md       # Detailed hardware guide
│   ├── API_REFERENCE.md        # Code documentation
│   └── CONTRIBUTING.md         # Contribution guidelines
│
└── examples/
    ├── basic_led_control.py    # Simple LED example
    └── advanced_patterns.py    # Complex sequences
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test hardware changes before committing
- Update documentation for new features

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
- [ ] Implement gesture control alongside voice
- [ ] Add web interface for remote control
- [ ] Support for multiple language voice commands
- [ ] Add motor driver support for DC motors
- [ ] Implement feedback loop with sensors
- [ ] Create mobile app interface
- [ ] Add command history and logging

## 📊 Performance

- **Voice Recognition Latency**: ~2-3 seconds
- **LLM Response Time**: ~3-5 seconds
- **Serial Communication**: 9600 baud (adjustable)
- **Command Execution**: Real-time

## 🔒 Security Notes

- This system runs locally - no cloud dependencies
- Microphone access required for voice input
- Serial port access required for Arduino communication
- No sensitive data is transmitted externally

---

**Made with ❤️ by [Your Name]**

*Last Updated: October 2025*
