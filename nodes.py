class KittenTTS:
    @classmethod
    def INPUT_TYPES(cls):
        voice_list = ['expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f']
        return {
            "required": {
                "text": ("STRING",),
                "voice": (voice_list,),               
            }
        }
    
    RETURN_TYPES = ("AUDIO", )
    FUNCTION = 'apply_generate_voice'
    CATEGORY = "utils"
    def apply_generate_voice(self, text, voice):
        from .generate_voice import generate_audio
        finally_voice = generate_audio(text, voice)
        return (finally_voice, )

NODE_CLASS_MAPPINGS = {
    "KittenTTS": KittenTTS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KittenTTS": "Generate voice",
}
# class TestNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "text": ("STRING", {"default": "test"}),
#             }
#         }
    
#     RETURN_TYPES = ("STRING",)
#     FUNCTION = "process"
#     CATEGORY = "test"
    
#     def process(self, text):
#         return (f"Hello: {text}",)

# NODE_CLASS_MAPPINGS = {
#     "TestNode": TestNode,
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "TestNode": "Test Node",
# }

