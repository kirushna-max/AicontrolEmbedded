import serial
import time
import queue
import threading
import numpy as np
import sounddevice as sd
import torch
import keyboard
import pyttsx3
import ollama
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Configuration
CONFIG = {
    "whisper_model": "openai/whisper-small",
    "llm_model": "llama3.1",
    "sample_rate": 16000,
    "record_key": "ctrl",
    "serial_port": "COM12",
    "baud_rate": 9600,
    "response_timeout": 15,  # Timeout for LLM response in seconds
}

# Global variables
recording = False
should_exit = False
speech_queue = queue.Queue()
tts_queue = queue.Queue()  # Queue for text-to-speech requests
ser = None
processor = None
model = None
engine = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# System prompt for LLM
SYSTEM_PROMPT = """
You are an AI assistant controlling an Embedded System. The System can receive the following commands:
- 'U': GLOW white LED
- 'D': GLOW Red LED
- 'R': Turn the Servo 90 degrees
- 'S': Stop

You should respond with a sequence of timed commands to execute. Format your response as follows:
1. First, acknowledge the user's request in a brief, conversational manner.
2. Then on a new line, write "COMMANDS:" followed by a sequence of commands with durations.

Command format: [LETTER]:[SECONDS];
For example:
- "U:3;" means exedcute the maneuvre for 3 seconds
- "R:1.5;S:0.5;" means Glow white LED for 1.5 seconds, stop for 0.5 seconds, then Beep the Buzzer for 2 seconds

When the user says something like "glow Randomly" or "start executing", create a sequence of 3-6 commands that would make the car move in an interesting pattern.

Examples:
User: "Blink the LED and then stop"
Response: I'll make the white LED glow and then stop.
COMMANDS: U:3;S:1;

User: "Operate the Components in a random pattern"
Response: I'll Operate these components a random sequence
COMMANDS: R:2;S:0.5;R:1;U:2;R:1;U:2;R:1;U:2;R:1;S:1;
"""

# Initialize system components
def initialize_system():
    global ser, processor, model, engine
    
    # Initialize serial connection
    try:
        ser = serial.Serial(CONFIG["serial_port"], CONFIG["baud_rate"], timeout=1)
        print(f"Connected to {CONFIG['serial_port']}")
        # Ensure the connection is established
        time.sleep(2)
        # Send stop command to ensure car is in known state
        ser.write(b'S')
        ser.flush()
    except Exception as e:
        print(f"Serial connection error: {str(e)}")
        return False
    
    # Initialize speech recognition
    try:
        processor = WhisperProcessor.from_pretrained(CONFIG["whisper_model"])
        model = WhisperForConditionalGeneration.from_pretrained(CONFIG["whisper_model"]).to(device)
        print("Whisper model loaded")
    except Exception as e:
        print(f"Speech recognition initialization error: {str(e)}")
        if ser:
            ser.close()
        return False
    
    # Initialize LLM - Test connection
    try:
        # Simple test to verify Ollama is running
        test_response = ollama.chat(
            model=CONFIG["llm_model"],
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(f"LLM: {CONFIG['llm_model']} - Connection successful")
    except Exception as e:
        print(f"LLM initialization error: {str(e)}")
        print("Make sure Ollama server is running and the model is available")
        if ser:
            ser.close()
        return False
    
    # Initialize text-to-speech
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        print("Text-to-speech initialized")
    except Exception as e:
        print(f"Text-to-speech initialization error: {str(e)}")
        if ser:
            ser.close()
        return False
    
    return True

# Recording functions
def toggle_recording(e):
    global recording
    if e.event_type == keyboard.KEY_DOWN and not recording:
        recording = True
        print("Recording...")
        threading.Thread(target=record_audio, daemon=True).start()
    elif e.event_type == keyboard.KEY_UP and recording:
        recording = False
        print("Stopped recording")

def record_audio():
    global recording
    audio_chunks = []
    
    try:
        while recording:
            chunk = sd.rec(int(CONFIG["sample_rate"] * 0.5), samplerate=CONFIG["sample_rate"], channels=1, dtype='float32')
            sd.wait()
            audio_chunks.append(chunk)
        
        if not audio_chunks:
            return
            
        full_recording = np.vstack(audio_chunks)
        print("Processing speech...")
        
        input_features = processor(full_recording.squeeze(), sampling_rate=CONFIG["sample_rate"], return_tensors="pt").input_features.to(device)
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()
        
        if transcription:
            print(f"You said: {transcription}")
            speech_queue.put(transcription)
        else:
            print("No speech detected")
    except Exception as e:
        print(f"Speech recognition error: {str(e)}")

# Text-to-speech thread function
def tts_thread_function():
    global should_exit, engine
    
    while not should_exit:
        try:
            # Get text from queue with timeout to check should_exit periodically
            text = tts_queue.get(block=True, timeout=0.5)
            
            # Process the text-to-speech in the same thread
            if text:
                engine.say(text)
                engine.runAndWait()
                
        except queue.Empty:
            # Queue is empty, continue checking
            continue
        except Exception as e:
            print(f"Error in TTS thread: {str(e)}")

# Process speech and control the car
def process_speech(text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    
    try:
        # Call Ollama directly
        response = ollama.chat(
            model=CONFIG["llm_model"],
            messages=messages
        )
        
        response_text = response["message"]["content"].strip()
        print(f"AI response: {response_text}")
        
        # Extract commands and speech part from the response
        speech_text = response_text
        if "COMMANDS:" in response_text:
            parts = response_text.split("COMMANDS:", 1)
            speech_text = parts[0].strip()
            commands_text = parts[1].strip()
            
            # Only try to execute if we have commands
            if commands_text:
                # Run command execution in a separate thread to avoid blocking
                cmd_thread = threading.Thread(
                    target=execute_commands, 
                    args=(commands_text,),
                    daemon=True
                )
                cmd_thread.start()
        
        # Send the speech to the TTS queue instead of speaking directly
        if speech_text:
            tts_queue.put(speech_text)
            
    except Exception as e:
        print(f"Error communicating with AI: {str(e)}")
        # Send error message to TTS queue
        error_msg = "Sorry, I couldn't process your request. Please try again."
        tts_queue.put(error_msg)

def execute_commands(commands_text):
    # Parse commands like "U:3;R:1.5;S:0.5;"
    commands = commands_text.split(';')
    
    for cmd in commands:
        if not cmd.strip():
            continue
            
        try:
            if ':' not in cmd:
                print(f"Invalid command format (missing colon): {cmd}")
                continue
                
            action, duration = cmd.split(':', 1)
            action = action.strip().upper()
            duration = float(duration.strip())
            
            if action in "UDLRS":
                print(f"Executing: {action} for {duration} seconds")
                ser.write(action.encode())
                ser.flush()  # Ensure command is sent immediately
                time.sleep(duration)
            else:
                print(f"Unknown command: {action}")
                
        except ValueError as ve:
            print(f"Invalid command format: {cmd} - {str(ve)}")
        except Exception as e:
            print(f"Error exarduino-cli lib install "Servo"ecuting command: {str(e)}")
    
    # Stop the car at the end of all commands
    try:
        ser.write(b'S')
        ser.flush()
        print("Commands completed")
    except Exception as e:
        print(f"Error stopping: {str(e)}")

# Speech processing thread function
def speech_processor_thread():
    global should_exit
    
    while not should_exit:
        try:
            # Use a timeout to allow checking the should_exit flag periodically
            user_input = speech_queue.get(block=True, timeout=0.5)
            # Process in yet another thread to ensure queue can continue to be processed
            threading.Thread(target=process_speech, args=(user_input,), daemon=True).start()
        except queue.Empty:
            # Queue is empty, continue checking
            continue
        except Exception as e:
            print(f"Error in speech processor thread: {str(e)}")

# Main function

def main():
    global should_exit
    
    print("Initializing system...")
    if not initialize_system():
        print("Initialization failed. Exiting.")
        return
    
    print("System initialized successfully!")
    
    # Start speech processing thread
    speech_thread = threading.Thread(target=speech_processor_thread, daemon=True)
    speech_thread.start()
    
    # Start text-to-speech thread
    tts_thread = threading.Thread(target=tts_thread_function, daemon=True)
    tts_thread.start()
        
    keyboard.hook_key(CONFIG["record_key"], toggle_recording)
    print(f"\nSystem ready!")
    print(f"Hold {CONFIG['record_key']} to record your voice command.")
    print("Press Esc to exit.")
    
    # Main loop - keep program running until Esc is pressed
    try:
        keyboard.wait('esc')
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
    finally:
        # Clean up
        should_exit = True
        print("\nShutting down...")
        
        try:
            # Stop the car
            if ser and ser.is_open:
                ser.write(b'S')
                ser.flush()
                ser.close()
                print("Serial connection closed.")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        
        print("System shut down. Goodbye!")

if __name__ == "__main__":
    main()
