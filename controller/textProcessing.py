from flask import Flask, request, render_template, jsonify
import json
import math
from translate import translate_this
from textblob import TextBlob
import string

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
      "grade_level": 0,
      "word_count": 0,
      "unique_words": 0,
      "index_last_read": 0,
      "_id": _id,
      "text": {
        "en": text_original,
        "esp": translations
      }
    }
    with open('books/'+ title + '.json', 'w') as file:
      json.dump(book, file, indent=2)


def updateBook(title):
  
  with open('../books/'+ title + '.json', "r") as file:
    book = json.load(file)

  # print(data)
  sentencesToRetranslate = book["text"]["esp"]
  word4word_translations = []
  translations = []

  for sentence in sentencesToRetranslate:
    wordsToTranslate = TextBlob(sentence.translate(str.maketrans('', '', string.punctuation))).words
    translation_translated = translate_this(wordsToTranslate, source_language='es-ES', target_language='en-us')
    literal_translations = []

    for index in range(len(wordsToTranslate)):    
        literal_translations.append([wordsToTranslate[index], translation_translated[index]])
    word4word_translations.append(literal_translations)
    
    translations.append({
      "text":sentence,
      "translated": literal_translations
    })

  book["text"]["esp"] =  translations

  with open('../books/'+ title + '.json', 'w') as file:
    json.dump(book, file, indent=1)