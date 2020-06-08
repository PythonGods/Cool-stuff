from googletrans import Translator
print("What is the staring language?")
start_lang=input()
print("What is the final language?")
final_lang=input()
print("What is the sentance?")
sent=input()

translator=Translator()
trans_sent=translator.translate(sent, src=start_lang, dest=final_lang)
print(trans_sent.text)