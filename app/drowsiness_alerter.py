import pyttsx3
import threading
from playsound import playsound
from pathlib import Path

SOUNDS_PATH = str(Path.cwd())[:-3] + "sounds\\"

NOT_RICK_ROLL_PATH = SOUNDS_PATH + "alrt_sound.mp3"
BEEP_SOUND_PATH = SOUNDS_PATH + "beep.mp3"
TTS_MESSAGE = "You seem tired, you should get some rest."


engine = pyttsx3.init()
engine.setProperty("rate", 150)

def play_text_to_speech_message(message):
    engine.say(message)
    engine.runAndWait()

class DrowsinessAlerter:

    def __init__(self):
        self.drowsiness_counter = 0

        # Alert types: 
        #   0 -> Text to speech asks to wake up
        #   1 -> Beep sound
        #   2 -> Definitely not a Rick Roll
        self.alert_type = 1

    def should_alert(self, is_drowsy):
        if is_drowsy:
            self.drowsiness_counter += 1
        else:
            self.drowsiness_counter = 0
        if self.drowsiness_counter > 20:
            self.alert_driver()
            self.drowsiness_counter = 0
            return True
        return False 

    def alert_driver(self):
        if self.alert_type == 0:
            self.tts_thread = threading.Thread(target=play_text_to_speech_message, args=(TTS_MESSAGE,))
            self.tts_thread.start()
        elif self.alert_type == 1:
            self.start_playsound_thread(BEEP_SOUND_PATH)
        elif self.alert_type == 2:
            self.start_playsound_thread(NOT_RICK_ROLL_PATH)

    def start_playsound_thread(self, path):
        self.thread = threading.Thread(target=playsound, args=(path,))
        self.thread.start()