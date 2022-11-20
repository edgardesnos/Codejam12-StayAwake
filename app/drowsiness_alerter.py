import pyttsx3
from multiprocessing import Process
import threading
from playsound import playsound

not_rick_roll_path = "C:\\Users\\edgar\\Desktop\\CodeJam12\\Codejam12-StayAwake\\app\\alrt_sound.mp3"
beep_sound_path = "C:\\Users\\edgar\\Desktop\\CodeJam12\\Codejam12-StayAwake\\app\\beep.mp3"
tts_message = "You seem tired, you should get some rest."


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
        self.alert_type = 0

    def should_alert(self, is_drowsy):
        if is_drowsy:
            self.drowsiness_counter += 1
        else:
            self.drowsiness_counter = 0
        if self.drowsiness_counter > 30:
            self.alert_driver()
            self.drowsiness_counter = 0

    def alert_driver(self):
        if self.alert_type == 0:
            self.tts_thread = threading.Thread(target=play_text_to_speech_message, args=(tts_message,))
            self.tts_thread.start()
        elif self.alert_type == 1:
            self.start_playsound_thread(beep_sound_path)
        elif self.alert_type == 2:
            self.start_playsound_thread(not_rick_roll_path)

    def start_playsound_thread(self, path):
        self.thread = threading.Thread(target=playsound, args=(path,))
        self.thread.start()