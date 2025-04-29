import logging
import os
import sys
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message



class Reference:
    # A class to stroe previously response from the chatGPT API
    def __init__(self) -> None:
        self.response = ""

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

reference =  Reference()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Model Name
MODEL_NAME = "gpt-3.5-turbo"

# Initializing bot and dispaticher
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)



def clear_past():
    reference.response = ""

@router.message(Command("start"))
async def welcome(message: Message):
    await message.reply("Hi\n I am Aryan Bot\n I am made by Aryan. How cna i Help you?")

@router.message(Command("clear"))
async def clear(message: Message):
    clear_past()
    await message.reply("I've cleared the past conversation and context")

@router.message(Command("help"))
async def helper(message: Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by PWskills! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@router.message()
async def chatgpt(message: Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response =  client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response.choices[0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())