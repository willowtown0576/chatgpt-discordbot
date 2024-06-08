import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


class OpenAiClient:
    """
    OpenAIのサービス（テキスト生成、テキストから音声、音声からテキストへの変換）とやり取りを行うクライアント。
    """

    SPEECH_FILENAME = "reply_voice.wav"
    IMAGE_FILE_SIZE = "1024x1024"

    def __init__(self):
        """
        環境変数からAPIキーとモデル設定を読み込んでOpenAiClientを初期化します。
        """
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GPT_MODEL = os.getenv("GPT_MODEL")
        self.GPT_ROLE = os.getenv("GPT_ROLE")
        self.GPT_TTS_MODEL = os.getenv("GPT_TTS_MODEL")
        self.GPT_VOICE = os.getenv("GPT_VOICE")
        self.GPT_STT_MODEL = os.getenv("GPT_STT_MODEL")
        self.GPT_IMAGE_MODEL = os.getenv("GPT_IMAGE_MODEL")
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.user_conversations = {}

    def send_message(self, user_id: int, prompt_text: str) -> str:
        """
        OpenAI GPTモデルにメッセージを送信し、応答を返します。

        Args:
            user_id (int): メッセージを送信するユーザーのID。
            prompt_text (str): GPTモデルに送信するテキストプロンプト。

        Returns:
            str: GPTモデルからの応答。
        """
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
        """
        テキストを音声に変換し、音声ファイルを保存します。

        Args:
            text (str): 音声に変換するテキスト。

        Returns:
            str: 保存された音声ファイルのファイル名。
        """
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
        """
        音声ファイルから音声をテキストに変換します。

        Args:
            audio_filename (str): テキストに書き起こす音声ファイルのファイル名。

        Returns:
            str: 書き起こされたテキスト。
        """
        with open(audio_filename, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=self.GPT_STT_MODEL, file=audio_file
            )
        return transcription.text
    
    def generate_image(self, prompt: str) -> str:
        """
        受け取ったプロンプトから画像を生成し、そのURLを返します。

        Args:
            prompt (str): 画像生成の際に使用するプロンプト

        Returns:
            str: 画像のURL
        """
        response = self.client.images.generate(
            model = self.GPT_IMAGE_MODEL,
            prompt = prompt,
            size = OpenAiClient.IMAGE_FILE_SIZE,
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url
