import discord
import os
from dotenv import load_dotenv
from groq_llama import process_query_with_groq
from zohodesk import create_ticket

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

user_ticket_map = {}

@client.event
async def on_ready():
    print(f'🤖 Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    user_name = str(message.author.name)

    if user_id in user_ticket_map:
        await message.channel.send(f"You already have a ticket open: #{user_ticket_map[user_id]}")
        return

    await message.channel.send("Let me look into that...")

    try:
        response = process_query_with_groq(message.content)
        if "create ticket" in response.lower():
            ticket_id = create_ticket(user_name, "Washing Machine Issue", message.content)
            user_ticket_map[user_id] = ticket_id
            await message.channel.send(f"Ticket created ✅: #{ticket_id}")
        else:
            await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"⚠️ Error: {str(e)}")

client.run(TOKEN)
