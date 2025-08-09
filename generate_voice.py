from .kittentts import KittenTTS
m = KittenTTS("KittenML/kitten-tts-nano-0.1")

def genarate_audio(text, audio):
    audio = m.generate(text, voice=audio)
    return audio

# available_voices : [  'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f' ]

