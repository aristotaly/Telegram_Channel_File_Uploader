import os
import asyncio
import logging
from telethon import TelegramClient, types, utils, functions
import zipfile

# Configuration
api_id = '<Your Telegram API ID>'
api_hash = '<Your Telegram API HASH>'
phone = '<Your phone number>'
channel_url_pdfs = "<Your PDF Channel URL>"
channel_url_zipped = "<Your ZIP Channel URL>"
directory = "<Your Directory Path>"
zipped_directory = "<Your ZIP Directory Path>"
uploaded_files_path = "<Path to your uploaded files text file>"
max_size = 1.1 * 1024 ** 3  # Maximum size of a zip file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Ensure the Telethon client is connected
client = TelegramClient('session', api_id, api_hash)

async def get_uploaded_files():
    uploaded_files = []
    channel_pdfs = await client.get_entity(channel_url_pdfs)
    channel_zipped = await client.get_entity(channel_url_zipped)

    async for message in client.iter_messages(channel_pdfs):
        if message.document:
            for attr in message.document.attributes:
                if isinstance(attr, types.DocumentAttributeFilename):
                    uploaded_files.append(attr.file_name)

    async for message in client.iter_messages(channel_url_zipped):
        if message.document:
            for attr in message.document.attributes:
                if isinstance(attr, types.DocumentAttributeFilename):
                    uploaded_files.append(attr.file_name)

    return uploaded_files

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))

    logger.info('Connected to Telegram API')
    uploaded_files = await get_uploaded_files()

    with open(uploaded_files_path, 'w') as file:
        file.write('\n'.join(uploaded_files))

    # Start the main process
    try:
        # Your main process code here
        pass
    except Exception as e:
        logger.error('An unexpected error occurred.', exc_info=True)
    finally:
        await client.disconnect()
        logger.info('Disconnected from Telegram API')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
