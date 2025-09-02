import discord
from discord.ext import commands
import ollama
from dotenv import load_dotenv
import os
import asyncio
from functools import partial
import random

# --- Load Environment Variables ---
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
model = os.getenv('MODEL_NAME')
my_id = os.getenv('MY_ID')
lime_id = os.getenv('LiME_ID')
seemly_id = os.getenv('SEEMLY_ID')

# --- Intents & Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Bot Ready Event ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# --- Flirt Mode Toggle ---
flirt_mode = True

@bot.command()
async def enable(ctx):
    global flirt_mode
    flirt_mode = True
    await ctx.send("Functionality enabled!")

@bot.command()
async def disable(ctx):
    global flirt_mode
    flirt_mode = False
    await ctx.send("Functionality disabled!")

# --- Core Flirtify Function ---
def flirtify_sync(message):
    prompt = (
        "You are a flirty rewriting assistant. Rewrite everything the user types into a playful, flirty tone, no matter how short or unusual. "
        "Never break character, never explain, comment, or output anything else. Only flirty rewrites, every time, zero exceptions. "
        "Make it teasing, flirty, and playful. Keep rewrites about the same length as the original message."
    )
    user_message = f"Remember, you are flirty and playful. Now rewrite this: {message}"
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        )
        if "message" in response:
            return response["message"]["content"].strip()
        elif "messages" in response:
            return response["messages"][-1]["content"].strip()
    except Exception as e:
        print("Generation failed:", e)
        return message

async def flirtify(message):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(flirtify_sync, message))

# --- On Message Event ---
@bot.event
async def on_message(message):
    global flirt_mode

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
    if message.author == bot.user or message.webhook_id is not None:
        return
    if str(message.author.id) in [str(my_id), str(seemly_id)]:
        return

    if flirt_mode:
        if str(message.author.id) == str(lime_id):
            transformed = random.choice([
                "Asshole!!", "Bitch!", "Cunt", "Fuck u!!!",
                "Mother fucker.", "Nigga", "quickNutter",
                "Sex slave", "Whore.", "zesty!!"
            ])
        else:
            transformed = await flirtify(message.content)
        await message.delete()

        if message.guild:
            if message.channel.permissions_for(message.guild.me).manage_webhooks:
                webhooks = await message.channel.webhooks()
                webhook = discord.utils.get(webhooks, name="CloudNine")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name="CloudNine")
                await webhook.send(
                    content=transformed,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url
                )
        else:
            embed = discord.Embed(
                description=transformed,
                color=discord.Color.pink()
            )
            await message.channel.send(embed=embed)

# --- Run the Bot ---
bot.run(token)