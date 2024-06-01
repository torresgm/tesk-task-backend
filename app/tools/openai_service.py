from openai import AsyncOpenAI
from starlette.config import Config

config = Config(".env")

OPENAI_API_MODEL = config("OPENAI_API_MODEL")
OPENAI_API_KEY = config("OPENAI_API_KEY")


class OpenAIService:
    def __init__(self, logger):
        # Note: timeout set to 90 to fix Request Timeout Error (shows frequently only when running in Docker)
        self.client = AsyncOpenAI(
            api_key=OPENAI_API_KEY, timeout=90
        )
        self.logger = logger

    async def summarize_text(self, text):
        try:
            completion = await self.client.chat.completions.create(
                model=OPENAI_API_MODEL,
                messages=[
                    {"role": "user", "content": f"Summarize this: ${text}"}
                ]
            )
            return completion.choices[0].message
        except Exception as e:
            self.logger.error(f"OpenAIError: {str(e)}")
            raise Exception('OpenAI Library Error')
