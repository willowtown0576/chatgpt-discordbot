import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


class OpenAiClient:

    SPEECH_FILENAME = "reply_voice.wav"

    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GPT_MODEL = os.getenv("GPT_MODEL")
        self.GPT_ROLE = os.getenv("GPT_ROLE")
        self.GPT_TTS_MODEL = os.getenv("GPT_TTS_MODEL")
        self.GPT_VOICE = os.getenv("GPT_VOICE")
        self.GPT_STT_MODEL = os.getenv("GPT_STT_MODEL")
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.user_conversations = {}

    def send_message(self, user_id: int, prompt_text: str) -> str:
        if user_id not in self.user_conversations:
            self.user_conversations[user_id] = []

        self.user_conversations[user_id].append(
            {"role": "user", "content": prompt_text}
        )
        response = self.client.chat.completions.create(
            model=self.GPT_MODEL,
            messages=[
                {"role": "system", "content": self.GPT_ROLE},
                *self.user_conversations[user_id],
            ],
        )
        reply_message = response.choices[0].message.content
        self.user_conversations[user_id].append(
            {"role": "assistant", "content": reply_message}
        )

        return reply_message

    def text_to_speech(self, text: str) -> str:
        speech_file_path = Path(__file__).parent / OpenAiClient.SPEECH_FILENAME
        response = self.client.audio.speech.create(
            model=self.GPT_TTS_MODEL,
            voice=self.GPT_VOICE,
            response_format="wav",
            input=text,
        )
        response.stream_to_file(speech_file_path)
        return OpenAiClient.SPEECH_FILENAME

    def speech_to_text(self, audio_filename: str) -> str:
        audio_file = open(audio_filename, "rb")
        transcription = self.client.audio.transcriptions.create(
            model=self.GPT_STT_MODEL, file=audio_file
        )
        return transcription.text
