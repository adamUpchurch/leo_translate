from google.cloud import translate_v3beta1 as translate
from flask import jsonify

import os


GOOGLE_APPLICATION_CREDENTIALS="/Users/AdamMacPro/startUp_athon/translate/leo-ios-244300-ca1482078257.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

def this_text(text, source_language='en-us', target_language='es-ES', location='global', project_id = 'leo-ios-244300'):
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
        translations.append(translation.translated_text)

    return jsonify(translations)

if __name__ == '__main__':
    translating_text('Hello')
