from flask import Flask, request, render_template, jsonify
import json
import math
from textblob import TextBlob
from hansel import story
import string
import time

def clean_this(text):
  split_text = text[1:-1].split(',')
  text_to_return = []
  for text in split_text:
    clean_text = text.strip()
    clean_text = clean_text.replace('&quot;','"')
    clean_text = clean_text.replace('&apos;',"'")
    clean_text = clean_text.replace('&#x27;',"'")
    clean_text = clean_text.replace('&#x27;','"')
    text_to_return.append(clean_text)

  return text_to_return

def shorten_this(sentenceN):
  if (isinstance(sentenceN, str)):
    sentence = sentenceN.split(' ')
    array = []
    length = len(sentence)
    halfed = math.floor(length / 2)
    if length < 12:
      return [sentenceN]
    else:
      first = shorten_this(" ".join(sentence[:halfed]))
      second = shorten_this(" ".join(sentence[halfed:]))
      array.append(first)
      array.append(second)
      return array

  if(isinstance(sentenceN, list)):
    array = []
    for sentence in sentenceN:
      array.append(shorten_this(sentence))
    return array

def flatten_this(input_array):
    result_array = []
    for element in input_array:
        if not isinstance(element, list):
            result_array.append(element)
        elif isinstance(element, list):
            result_array += flatten_this(element)
    return result_array

def saveBook(title, text_original, translations, word4word_translations, _id=0):
    book =     {
      "title": title,
      "summary": "summary",
      "author": "author",
      "cover": "cover",
      "grade_level": "8th",
      "word_count": 0,
      "unique_words": 0,
      "index_last_read": 0,
      "hasFinished": False,
      "isLiked": False,
      "isCurrentlyReading": False,
      "_id": _id,
      "text": {
        "en": text_original,
        "esp": translations
      }
    }
    with open('books/'+ title + '.json', 'w') as file:
      json.dump(book, file, indent=2)

def updateBook(title, fileName):
  
  with open('books/'+ title + ".json", "r") as file:
    book = json.load(file)

  print(book["title"])
  # print(data)
  sentencesToRetranslate = book["text"]["esp"]
  word4word_translations = []
  translations = []

  for num, sentence in enumerate(sentencesToRetranslate, start=0):
    wordsToTranslate = TextBlob(sentence.translate(str.maketrans('', '', string.punctuation))).words
    literal_translations = []

    try:
      translation_translated = translate_this(wordsToTranslate, source_language='es-ES', target_language='en-us')
    except: 
      time.sleep(20)
      try:
        translation_translated = translate_this(wordsToTranslate, source_language='es-ES', target_language='en-us')
      except:
        break

    for index in range(len(wordsToTranslate)): 
        literal_translations.append([wordsToTranslate[index], translation_translated[index]])
    word4word_translations.append(literal_translations)
    
    translations.append({
      "text":sentence,
      "translated": literal_translations,
      "index": num
    })

    if(len(translations)%10 == 0):
      print(len(translations))

  book["text"]["esp"] =  translations

  with open('books/'+ fileName + "2.json", 'w') as file:
    json.dump(book, file, indent=1)

def traducir(storyTitle, title):
  with open('books/'+ storyTitle + ".json", "r") as file:
    book = json.load(file)
  tb = TextBlob(story)
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
          time.sleep(20)
          text_splat.append(sent)
          text_translated.append(translate_this(sent))
        except:
          saveBook(title, text_splat, translations, book['_id'])
          dataToReturn = {
            "en": text_splat,
            "es": text_translated
          }
          return jsonify(dataToReturn)

  saveBook(title, text_splat, translations, book['_id'])
  return 'Book saved!'

if __name__ == '__main__':
  from translate import translate_this
  
  t1_start = time.process_time()  
  traducir("story", 'Three Little Pigs')
  # updateBook("story", "storyTest")
  t1_stop = time.process_time()  

  print("Elapsed time minutes:", (t1_stop-t1_start)/60) 