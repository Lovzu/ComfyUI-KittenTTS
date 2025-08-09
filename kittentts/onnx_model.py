import numpy as np
import espeakng  # py-espeak-ng
import soundfile as sf
import onnxruntime as ort
import re


def basic_english_tokenize(text):
    return re.findall(r"\w+|[^\w\s]", text)


class TextCleaner:
    def __init__(self, dummy=None):
        _pad = "$"
        _punctuation = ';:,.!?¡¿—…"«»"" '
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        _letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"

        symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)
        self.word_index_dictionary = {sym: i for i, sym in enumerate(symbols)}

    def __call__(self, text):
        return [self.word_index_dictionary[char] for char in text if char in self.word_index_dictionary]


class KittenTTS_1_Onnx:
    def __init__(self, model_path="kitten_tts_nano_preview.onnx", voices_path="voices.npz"):
        self.model_path = model_path
        self.voices = np.load(voices_path)
        self.session = ort.InferenceSession(model_path)

        # Настройки для espeak-ng
        self.espeak_kwargs = {
            "voice": "en-us",
            "encoding": "ipa",
            "preserve_punctuation": True,
            "with_stress": True,
            "options": espeakng.Options.STDOUT | espeakng.Options.Phonemes
        }

        self.text_cleaner = TextCleaner()

        self.available_voices = [
            'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',
            'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'
        ]

    def _prepare_inputs(self, text: str, voice: str, speed: float = 1.0) -> dict:
        if voice not in self.available_voices:
            raise ValueError(f"Voice '{voice}' not available. Choose from: {self.available_voices}")

        # Фонетизация через py-espeak-ng
        phonemes = espeakng.phonemes(text, **self.espeak_kwargs)

        # Токенизация
        tokens = basic_english_tokenize(phonemes)
        tokens = ' '.join(tokens)
        token_ids = self.text_cleaner(tokens)

        # Добавляем start/end токены
        token_ids.insert(0, 0)
        token_ids.append(0)

        input_ids = np.array([token_ids], dtype=np.int64)
        ref_s = self.voices[voice]

        return {
            "input_ids": input_ids,
            "style": ref_s,
            "speed": np.array([speed], dtype=np.float32),
        }

    def generate(self, text: str, voice: str = "expr-voice-5-m", speed: float = 1.0) -> np.ndarray:
        inputs = self._prepare_inputs(text, voice, speed)
        outputs = self.session.run(None, inputs)
        audio = outputs[0][5000:-10000]
        return audio

    def generate_to_file(self, text: str, output_path: str, voice: str = "expr-voice-5-m",
                         speed: float = 1.0, sample_rate: int = 24000) -> None:
        audio = self.generate(text, voice, speed)
        sf.write(output_path, audio, sample_rate)
        print(f"Audio saved to {output_path}")