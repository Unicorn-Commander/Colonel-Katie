import pyttsx3
import requests
import os

class TTSService:
    def __init__(self, elevenlabs_api_key=None):
        try:
            self.engine = pyttsx3.init()
            self.tts_available = True
            print("✅ TTS engine initialized")
        except Exception as e:
            print(f"⚠️  TTS unavailable: {e}")
            print("   (TTS features disabled - install espeak if needed)")
            self.engine = None
            self.tts_available = False
            
        self.elevenlabs_api_key = elevenlabs_api_key
        self.elevenlabs_base_url = "https://api.elevenlabs.io/v1"

        self.voices = {
            "colonel_katie": {"pyttsx3": None, "elevenlabs_id": "21m00TNDk4Z8WGF7bQnE", "description": "Military-professional voice"},
            "default_male": {"pyttsx3": None, "elevenlabs_id": "pNInz6obpgDQGXGNvn6X", "description": "Standard male voice"},
            "default_female": {"pyttsx3": None, "elevenlabs_id": "EXAVITQu4vr4xnSDxMaL", "description": "Standard female voice"},
        }
        self.active_voice_profile = "colonel_katie"

        # Attempt to set pyttsx3 voices if available
        if self.tts_available and self.engine:
            pyttsx3_voices = self.engine.getProperty('voices')
            for voice in pyttsx3_voices:
                if "english" in voice.languages:
                    if "male" in voice.name.lower() or "david" in voice.name.lower():
                        self.voices["default_male"]["pyttsx3"] = voice.id
                    elif "female" in voice.name.lower() or "zira" in voice.name.lower():
                        self.voices["default_female"]["pyttsx3"] = voice.id
                    # Assign a default pyttsx3 voice for Colonel Katie if a suitable one is found
                    if "zira" in voice.name.lower() or "female" in voice.name.lower(): # Example: using a female voice for Katie
                        self.voices["colonel_katie"]["pyttsx3"] = voice.id

    def set_voice_profile(self, profile_name):
        if profile_name in self.voices:
            self.active_voice_profile = profile_name
            print(f"Active voice profile set to: {profile_name}")
            return True
        else:
            print(f"Voice profile '{profile_name}' not found.")
            return False

    def get_available_voice_profiles(self):
        return list(self.voices.keys())

    def speak_pyttsx3(self, text, speed=1.0, pitch=1.0):
        """Uses pyttsx3 for local text-to-speech."""
        if not self.tts_available or not self.engine:
            print("⚠️  TTS not available - text would be spoken:", text[:50])
            return
            
        voice_id = self.voices[self.active_voice_profile]["pyttsx3"]
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        
        # Adjust speed and pitch
        self.engine.setProperty('rate', int(self.engine.getProperty('rate') * speed))
        # pyttsx3 doesn't have a direct pitch control, but rate affects it slightly.
        # For more advanced pitch control, external libraries or different TTS engines are needed.

        self.engine.say(text)
        self.engine.runAndWait()

    def speak_elevenlabs(self, text, model_id="eleven_monolingual_v1", speed=1.0, pitch=1.0):
        """Uses ElevenLabs API for premium text-to-speech."""
        voice_id = self.voices[self.active_voice_profile]["elevenlabs_id"]
        if not voice_id:
            print(f"No ElevenLabs voice ID configured for {self.active_voice_profile} profile.")
            return

        if not self.elevenlabs_api_key:
            print("ElevenLabs API key not set. Cannot use ElevenLabs TTS.")
            return

        url = f"{self.elevenlabs_base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            # Save the audio to a temporary file and play it
            with open("elevenlabs_output.mp3", "wb") as f:
                f.write(response.content)
            os.system("mpg123 elevenlabs_output.mp3") # Requires mpg123 to be installed
            os.remove("elevenlabs_output.mp3")

        except requests.exceptions.RequestException as e:
            print(f"Error with ElevenLabs API: {e}")
        except Exception as e:
            print(f"Error playing ElevenLabs audio: {e}")

    def speak(self, text, use_elevenlabs=False, tts_enabled=True, speed=1.0, pitch=1.0, **kwargs):
        """Main speak method, chooses between pyttsx3 and ElevenLabs."""
        if not tts_enabled:
            print("TTS is disabled.")
            return

        if use_elevenlabs:
            self.speak_elevenlabs(text, speed=speed, pitch=pitch, **kwargs)
        else:
            self.speak_pyttsx3(text, speed=speed, pitch=pitch)

    def handle_ssml(self, ssml_text):
        """Placeholder for SSML handling. Pyttsx3 has limited SSML support.
        ElevenLabs might support it depending on the model."""
        print(f"Attempting to handle SSML: {ssml_text}")
        # For pyttsx3, you might need to strip SSML tags or use a library
        # to convert SSML to plain text if full SSML rendering isn't supported.
        # For ElevenLabs, check their API documentation for SSML support.
        self.speak(ssml_text) # For now, just speak the raw SSML text
