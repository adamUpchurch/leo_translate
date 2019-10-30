from flask import Flask, request, render_template, jsonify
# from controller import splitBook, translate
import json
# from controller.textProcessing import split_this, translate_this
from textblob import TextBlob
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
  for blob in tb.sentences:
    sentence = shorten_this(blob.string)
    flattened = flatten_this(sentence)
    for sent in flattened:
      time.sleep(.5)
      try:
        text_splat.append(sent)
        # text_translated.append(TextBlob(sent).translate(to='es').string)
      except:
        try:
          time.sleep(5)
          text_splat.append(sent)
          text_translated.append(translate_this(sent))  
        except:
          saveBook(book['title'], book['summary'], book['author'], book['cover'], text_splat, text_translated, book['_id'])
          dataToReturn = {
            "en": text_splat,
            "es": text_translated
          }
          return jsonify(dataToReturn)
        
      # try:
      #   text_translated.append(TextBlob(sent).translate(to='es').string)
      # except:

  dataToReturn = {
    "en": text_splat,
    "es": text_translated
  }
  saveBook(book['title'], book['summary'], book['author'], book['cover'], text_splat, text_translated, book['_id'])
  return jsonify(dataToReturn)