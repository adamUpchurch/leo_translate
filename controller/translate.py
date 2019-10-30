from google.cloud import translate_v3beta1 as translate
from flask import jsonify

import os


def translate_this(text, source_language='en-us', target_language='es-ES', location='global', project_id = 'leo-ios-244300', GOOGLE_APPLICATION_CREDENTIALS="/Users/adam/Code/leo-web/leo_translate/leo-ios-244300-ca1482078257.json"):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS
    client = translate.TranslationServiceClient()
    parent = client.location_path(project_id, location)
    response = client.translate_text(
        parent=parent,
        contents=text,
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code=source_language,
        target_language_code=target_language)
    translations = []
    for translation in response.translations:
        print(translation.translated_text)
        translations.append(translation.translated_text)

    return translations[0]

if __name__ == '__main__':
    translate_this(['Hello, my name is Adam.', 'Hello, my name is Adam.', 'Hello, my name is Adam.', 'Hello, my name is Adam.', 'Hello, my name is Adam.', 'Hello, my name is Adam.'])
