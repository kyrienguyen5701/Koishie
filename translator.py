import googletrans

languages = googletrans.LANGUAGES
translator = googletrans.Translator()

def trans(s, to_lang):
    for abbr, lang in languages.items():
        if lang == to_lang:
            to_lang = abbr
            break
    result = translator.translate(s, dest=to_lang)
    return {
        'Text': result.text,
        'Pronunciation': result.pronunciation
    }