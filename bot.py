import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

# --- Load Environment Variables ---
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
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
copy_mode = True

@bot.command()
async def enable(ctx):
    global copy_mode
    copy_mode = True
    await ctx.send("Functionality enabled!")

@bot.command()
async def disable(ctx):
    global copy_mode
    copy_mode = False
    await ctx.send("Functionality disabled!")

# --- On Message Event ---
@bot.event
async def on_message(message):
    global copy_mode

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
    if message.author == bot.user or message.webhook_id is not None:
        return
    if str(message.author.id) in [str(my_id), str(seemly_id)]:
        return

    if copy_mode:
        if str(message.author.id) == str(lime_id):
            new_message = random.choice([
                "Asshole!!", "Bitch!", "Cunt", "Fuck u!!!",
                "Mother fucker.", "Nigga", "quickNutter",
                "Sex slave", "Whore.", "zesty!!"
            ])
            await message.delete()
        else:
            new_message = message.content

        if message.guild:
            if message.channel.permissions_for(message.guild.me).manage_webhooks:
                webhooks = await message.channel.webhooks()
                webhook = discord.utils.get(webhooks, name="CloudNine")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name="CloudNine")
                await webhook.send(
                    content=new_message,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url
                )
        else:
            embed = discord.Embed(
                description=new_message,
                color=discord.Color.pink()
            )
            await message.channel.send(embed=embed)

# --- Run the Bot ---
bot.run(token)