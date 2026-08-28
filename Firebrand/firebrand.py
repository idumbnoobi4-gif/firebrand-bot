import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
# Put the ID of the channel you want to monitor here.
# Example: 1496438616203853824
AUTO_BAN_CHANNEL_ID = 1496438616203853824

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Auto-ban system is active!")


@bot.event
async def on_message(message):

    # Ignore messages from bots
    if message.author.bot:
        return

    # Only activate in the specific channel
    if message.channel.id == AUTO_BAN_CHANNEL_ID:

        # Don't ban administrators/moderators
        if message.author.guild_permissions.administrator:
            return

        # Delete the message immediately
        try:
            await message.delete()
        except discord.Forbidden:
            print("I don't have permission to delete messages.")
        except discord.HTTPException:
            pass

        # Ban the member
        try:
            await message.guild.ban(
                message.author,
                reason="Sent a message in the restricted channel"
            )

            print(
                f"Banned {message.author} "
                f"for speaking in #{message.channel.name}"
            )

        except discord.Forbidden:
            print(
                "I don't have permission to ban this member. "
                "Check my role position and permissions."
            )

        except discord.HTTPException as e:
            print(f"Discord error while banning: {e}")

        return

    # Allow normal commands everywhere else
    await bot.process_commands(message)


bot.run(TOKEN)