import openai
import pyaudio
import wave
import os
import numpy as np
from scipy.signal import butter, lfilter

class STTService:
    def __init__(self, api_key=None):
        # Only initialize OpenAI client if API key is provided
        self.client = None
        if api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
        else:
            # Get API key from environment if available
            env_api_key = os.getenv("OPENAI_API_KEY")
            if env_api_key:
                try:
                    self.client = openai.OpenAI(api_key=env_api_key)
                except Exception as e:
                    print(f"Warning: Failed to initialize OpenAI client with env key: {e}")
            else:
                print("Info: STTService initialized without OpenAI API key - transcription features disabled")
        
        # Initialize audio components (these work without API key)
        try:
            self.audio = pyaudio.PyAudio()
        except Exception as e:
            print(f"Warning: Failed to initialize audio: {e}")
            self.audio = None
            
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.wake_word_enabled = False # New attribute for wake word status

        # Audio recording parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # Sample rate for Whisper
        self.CHUNK = 1024
        self.input_device_index = None # Default to system default

        # Noise reduction parameters (simple high-pass filter)
        self.CUTOFF_FREQ = 100  # Hz
        self.FILTER_ORDER = 5

    def start_wake_word_detection(self):
        print("Starting wake word detection (placeholder).")
        self.wake_word_enabled = True

    def stop_wake_word_detection(self):
        print("Stopping wake word detection (placeholder).")
        self.wake_word_enabled = False

    def _butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def _highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self._butter_highpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def get_input_devices(self):
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        devices = []
        for i in range(0, num_devices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices.append({
                    "name": self.audio.get_device_info_by_host_api_device_index(0, i).get('name'),
                    "index": i
                })
        return devices

    def set_input_device(self, device_index):
        if device_index is not None:
            try:
                device_info = self.audio.get_device_info_by_index(device_index)
                if device_info['maxInputChannels'] > 0:
                    self.input_device_index = device_index
                    print(f"Input device set to: {device_info['name']}")
                else:
                    print(f"Device {device_index} has no input channels.")
            except IOError:
                print(f"Invalid input device index: {device_index}")
        else:
            self.input_device_index = None
            print("Input device set to system default.")

    def start_recording(self):
        if self.is_recording:
            print("Already recording.")
            return

        self.frames = []
        self.stream = self.audio.open(format=self.FORMAT,
                                       channels=self.CHANNELS,
                                       rate=self.RATE,
                                       input=True,
                                       frames_per_buffer=self.CHUNK,
                                       input_device_index=self.input_device_index,
                                       stream_callback=self._record_callback)
        self.is_recording = True
        self.stream.start_stream()
        print("Recording started...")

    def _record_callback(self, in_data, frame_count, time_info, status):
        # Apply high-pass filter
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        filtered_data = self._highpass_filter(audio_data, self.CUTOFF_FREQ, self.RATE)
        self.frames.append(filtered_data.astype(np.int16).tobytes())
        return (in_data, pyaudio.paContinue)

    def stop_recording(self):
        if not self.is_recording:
            print("Not recording.")
            return None

        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped.")

        # Save recorded audio to a temporary WAV file
        temp_audio_path = "temp_audio.wav"
        wf = wave.open(temp_audio_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        return temp_audio_path

    def transcribe_audio(self, audio_file_path, language=None):
        if not self.client:
            print("Error: OpenAI client not initialized. Please set OPENAI_API_KEY to use transcription features.")
            # Clean up the temporary audio file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            return "Transcription unavailable - OpenAI API key required"
            
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            # Clean up the temporary audio file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

    def __del__(self):
        if self.audio:
            self.audio.terminate()
