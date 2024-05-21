import os
import json
from flask import Flask, render_template, request
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import speech_recognition as sr


app = Flask(__name__)

# Chatbot'u oluştur
chatbot = ChatBot("MyChatBot", read_only=False,
                  logic_adapters=[
                      {
                          "import_path": "chatterbot.logic.BestMatch",
                          "default_response": "Üzgünüm dediğinize cevap veremiyorum",
                          "maximum_similarity_threshold": 0.9
                      }
                  ])

# JSON dosyasını oku
with open(os.path.join(app.root_path, 'templates', 'soru_komut.json'), 'r', encoding='utf-8') as file:
    training_data = json.load(file)

# Veriyi liste olarak dönüştür
training_data_list = []
for qa_pair in training_data:
    training_data_list.append(qa_pair['kullanici'])
    training_data_list.append(qa_pair['cevap'])

# Trainer'ı oluştur ve eğit
trainer = ListTrainer(chatbot)
trainer.train(training_data_list)


@app.route("/")
def main():
    return render_template("chatbotv01.html")


@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    response = str(chatbot.get_response(userText))


    return response




@app.route("/speech_recognition", methods=["POST"])
def speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)  # 5 saniye boyunca ses kaydı yap

    userText = ""
    try:
        userText = r.recognize_google(audio_data, language="tr-TR")  # Ses dosyasını metne çevir
    except sr.UnknownValueError:
        userText = "Anlayamadım, lütfen tekrar deneyin"
    except sr.RequestError:
        userText = "Bağlantı hatası, lütfen internet bağlantınızı kontrol edin"

    return userText


if __name__ == "__main__":
    app.run(debug=True)
