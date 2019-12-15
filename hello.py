from flask import Flask, request, render_template, jsonify
# from controller import splitBook, translate
import json
# from controller.textProcessing import split_this, translate_this
from textblob import TextBlob
import string
from controller.translate import translate_this
from controller.textProcessing import clean_this, shorten_this, flatten_this, saveBook
import time

app = Flask(__name__)


@app.route('/traducir', methods=['POST'])
def traducir():
  data = json.loads(request.data.decode('utf-8'))
  tb = TextBlob(data['story'])
  book = data["book"]
  text_splat = []
  text_translated = []
  word4word_translations = []
  translations = []

  for blob in tb.sentences:
    sentence = shorten_this(blob.string)
    flattened = flatten_this(sentence)
    for sent in flattened:
      time.sleep(1)
      print('==============')
      print(sent)
      try:
        # Translate the original text & append to array to be saved
        translated_text = translate_this([sent])
        text_translated.append(translated_text)
        
        # Translated_text is to be split and translated each word individually
        # remove punctuations
        wordsToTranslate = TextBlob(translated_text.translate(str.maketrans('', '', string.punctuation))).words
        print("Translating each word individually - stripped the text")
        print("Translating this: ", wordsToTranslate) #spanish
        translation_translated = translate_this(wordsToTranslate, source_language='es-ES', target_language='en-us')
        
        literal_translations = []
        for index in range(len(wordsToTranslate)):
          
          print([wordsToTranslate[index], translation_translated[index]])

          literal_translations.append([wordsToTranslate[index], translation_translated[index]])

        # Original text that is appended to array to be saved
        print(literal_translations)

        translations.append({
          "text":translated_text,
          "translated": literal_translations
        })

        text_splat.append(sent)
        word4word_translations.append(literal_translations)
      except:
        try:
          time.sleep(5)
          text_splat.append(sent)
          text_translated.append(translate_this(sent))
        except:
          saveBook(book['title'], text_splat, translations, book['_id'])
          dataToReturn = {
            "en": text_splat,
            "es": text_translated
          }
          return jsonify(dataToReturn)

  dataToReturn = {
    "en": text_splat,
    "es": text_translated
  }
  saveBook(book['title'], text_splat, translations, book['_id'])
  return jsonify(dataToReturn)