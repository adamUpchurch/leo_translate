from flask import Flask, request, render_template, jsonify
from controller import splitBook, translate
import json


def split_this(req):
  print(req)
  print(type(req))
  if 'text_to_split' in req:
    text = req['text_to_split']
    split = splitBook.splitThis(text)
    print(split)
    return jsonify(split)
  else:
    return 'There is no text in header: text_to_split'
    
def translate_this(req):
  if 'text_to_translate' in req:
    text = req['text_to_translate']
    newText = text[1:-1].split(',')
    text_to_translate = []

    for text in newText:
      clean_text = text.strip()
      text_to_translate.append(clean_text[1:-1])

    translated_text = translate.this_text(text_to_translate)
    print(translated_text)
    return translated_text
  else:
    return translate.this_text(['Your request needs headers.'])