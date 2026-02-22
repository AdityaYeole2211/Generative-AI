import speech_recognition as sr

def main():
    r = sr.Recognizer() ## on device speech to text

    with sr.Microphone() as source: #gain access of microphone
        r.adjust_for_ambient_noise(source) #reduce bg noise if there
        r.pause_threshold = 2 #if user does not speak for  2 secs , start trancribing 

        print("🎙️Speak Something.....")
        audio = r.listen(source) 

        print("Processing audio....")
        stt = r.recognize_google(audio) #on device

        print("You said: \n", stt)

main()