from flask import Flask, request, render_template, jsonify
from controller import splitBook, translate
import json
from controller.textProcessing import split_this, translate_this

app = Flask(__name__)

@app.route('/split', methods=['POST'])
def splitting():
  print('==============================')
  data = json.loads(request.data.decode('utf-8'))
  return split_this(data)

@app.route('/translate', methods=['POST'])
def translating():
  data = json.loads(request.data.decode('utf-8'))
  return translate_this(data)

# incomes = [
#   { 'description': 'salary', 'amount': 5000 }
# ]

# @app.route('/split')
# def split():
#   split = splitBook.splitThis(text)
#   print(split)
#   return jsonify(split)

# @app.route('/translate')
# def translateThis():
#   if 'text_to_translate' in request.headers:
#     text = request.headers['text_to_translate']
#     newText = text[1:-1].split(',')
#     text_to_translate = []

#     for text in newText:
#       clean_text = text.strip()
#       text_to_translate.append(clean_text[1:-1])

#     translated_text = translate.this_text(text_to_translate)
#     print(translated_text)
#     return translated_text
#   else:
#     return translate.this_text(['Your request needs headers.'])
#   return jsonify(text_to_translate)
    

# @app.route('/income', methods=['POST'])
# def add_income():
#   incomes.append(request.get_json())
#   return '', 204

# @app.route('/<city>')
# def hello_nashville(city):
#     return 'Hello, %s!' % city.capitalize()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'Logging in'
#     else:
#         return 'Login / Signup'