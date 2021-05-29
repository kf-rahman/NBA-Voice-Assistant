import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

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
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                params={'api_key': API_KEY})

        data = json.loads(response.text)
        return data

    def all_teams(self):#list of all the teams that are playing
        teamsname = self.data['team1']
        versus = []

        for content in teamsname:
            versus.append(content['team1name'])
            versus.append(content['playing'])

        return versus

    def update_data(self):
        response = requests.post(f'https://parsehub.com/api/v2/projects/{self.project_token}/run',params = self.params)



        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data Updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()






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
    data = Data(API_KEY, PROJECT_TOKEN)
    print("Program Started")
    END_PHRASE ='stop'
    result = None

    TOTAL_PATTERNS = {re.compile("[\w\s]+ teams [\w\s]+playing"):data.all_teams,re.compile("[\w\s]+playing"): data.all_teams
    }


    UPDATE_COMMAND = "update"
    while True:
        print("Speak")
        text = get_audio()
        print(text)

        for pattern,func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
        if text ==  UPDATE_COMMAND:
            result = "Data is being updated"
            data.update_data()

        if result:
            print(result)
            speak(result)

        if text.find(END_PHRASE):
            break


main()
