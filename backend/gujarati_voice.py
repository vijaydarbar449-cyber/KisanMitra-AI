from gtts import gTTS

text = "નમસ્તે ખેડૂત મિત્રો! કિસાનમિત્ર એઆઈમાં આપનું સ્વાગત છે."

tts = gTTS(text=text, lang="gu")
tts.save("gujarati_voice.mp3")

print("Gujarati Voice Created Successfully!")