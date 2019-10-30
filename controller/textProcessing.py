from flask import Flask, request, render_template, jsonify
import json
import math

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


def saveBook(title, summary, author, cover, text_original, text_translation, _id):
    book =     {
      "title": title,
      "summary": summary,
      "author": author,
      "cover": cover,
      "index_last_read": 0,
      "_id": _id,
      "text": {
        "en": text_original,
        "esp": text_translation
      }
    }
    with open('books/'+ title + '.json', 'w') as file:
      json.dump(book, file, indent=2)

