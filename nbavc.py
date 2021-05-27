import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY = 'tA0_xgVpoaiH'
PROJECT_TOKEN = 'tKijAox01o6c'
RUN_TOKEN = 'tJ9Vk3gTO8kM'


class Data:
    def __init__(self,api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key

        }
        self.get_data()

    def get_data(self):
        response = requests.get(f'https://parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                params={'api_key': API_KEY})

        self.data = json.loads(response.text)

    def all_teams(self):
        teamsname = self.data['team1']
        versus = []

        for content in teamsname:
            versus.append(content['team1name'])
            versus.append(content['playing'])

        return versus





data = Data(API_KEY,PROJECT_TOKEN)
print(data.data)
print(data.all_teams())
#Voice
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))
    return said.lower()


def main():
    print("Program Started")
    END_PHRASE = "stop"

    while True:
        print("Speak")
        text = get_audio()

        if text.find(END_PHRASE):
            break