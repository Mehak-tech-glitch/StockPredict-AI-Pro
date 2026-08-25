
from pathlib import Path
import tempfile

def make_voice(text, language="English"):
    try:
        from gtts import gTTS
        codes = {"English":"en","Hindi":"hi","Bengali":"bn","Gujarati":"gu",
                 "Marathi":"mr","Tamil":"ta","Telugu":"te","Kannada":"kn",
                 "Malayalam":"ml","Punjabi":"pa","Urdu":"ur","French":"fr",
                 "German":"de","Spanish":"es","Portuguese":"pt","Arabic":"ar",
                 "Japanese":"ja","Korean":"ko","Chinese":"zh-cn","Russian":"ru",
                 "Italian":"it","Dutch":"nl"}
        path = Path(tempfile.gettempdir()) / "stockpredict_reply.mp3"
        gTTS(text=text, lang=codes.get(language,"en")).save(str(path))
        return str(path)
    except Exception:
        return None
