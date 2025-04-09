import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() # load environment variables from .env file
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# create bot instance with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# event: bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event 
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Welcome to the server, {member.mention}!')
    print(f'{member.name} has joined the server!')

    # send a direct message to the new member
    await member.send(f'Welcome to the server, {member.name}! We hope you enjoy your stay!')

    # role = discord.utils.get(member.guild.roles, name='Member')
    # if role is not None:
    #     await member.add_roles(role)
    #     print(f'Assigned {role.name} role to {member.name}')
    # else:
    #     print(f'Role not found: Member') 
# command to customize the welcome message
@bot.command(name='set_welcome')
@commands.has_permissions(administrator=True)
async def set_welcome(ctx, *, message: str):
    global welcome_template
    welcome_template = message
    await ctx.send(f'Welcome message set to: {message}')

# command to test welcome message
@bot.command(name='testwelcome')
@commands.has_permissions(administrator=True)
async def test_welcome(ctx):
    await on_member_join(ctx.author)
    await ctx.send(f'Test welcome message sent!')

@bot.command(name='viewwelcome')
async def view_welcome(ctx):
    await ctx.send(f'Current welcome message: {welcome_template}')

@bot.command(name='resetwelcome')
@commands.has_permissions(administrator=True)
async def reset_welcome(ctx):
    global welcome_template
    welcome_template = 'Welcome to the server!'
    await ctx.send('Welcome message reset to default: Welcome to the server!')

@bot.command(name='setwelcomechannel')
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await ctx.send(f'Welcome channel set to: {channel.mention}')
    await ctx.send('Note: This is just a placeholder. You need to implement the logic to send welcome messages to this channel.')

# error handling
@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'You do not have permission to use this command.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Command not found. Use !help to see the list of available commands.')
    else:
        await ctx.send(f'An error occurred: {error}')

# Help command for welcome bot
@bot.command(name='welcomehelp')
async def welcome_help(ctx):
    help_text = """
**Welcome Bot Commands**
`!setwelcome [message]` - Set a custom welcome message (Admin only)
`!testwelcome` - Test the welcome message (Admin only)
`!viewwelcome` - View the current welcome message
`!resetwelcome` - Reset welcome message to default (Admin only)
`!setwelcomechannel [#channel]` - Set the welcome channel (Admin only)
`!welcomehelp` - Show this help message

**Tips**
- Use {member} in your welcome message to mention the new member
- Example: `!setwelcome Hello {member}! Welcome to our awesome server!`
"""
    await ctx.send(help_text)

# command to check if the bot is online
bot.run(os.getenv('DISCORD_TOKEN')) # run the bot with the token from .env file