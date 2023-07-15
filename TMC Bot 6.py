import discord
from discord.ext import commands
import aiohttp
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='+', intents=intents)

async def create_session():
    return aiohttp.ClientSession()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

@client.event
async def on_member_join(member):
    unverified_role = discord.utils.get(member.guild.roles, name='Unverified')
    rank_role = discord.utils.get(member.guild.roles, name='Rank')
    game_role = discord.utils.get(member.guild.roles, name='Game')
    ping_role = discord.utils.get(member.guild.roles, name='Pingrollen')
    content_creator_role = discord.utils.get(member.guild.roles, name='ContentCrator')
    prefix_rank_role = discord.utils.get(member.guild.roles, name='Prefix Rank')
    other_role = discord.utils.get(member.guild.roles, name='Other')

    await member.add_roles(unverified_role, rank_role, game_role, ping_role, content_creator_role, prefix_rank_role, other_role)

@client.command()
async def reactingrole(ctx):
    options = ['option1', 'option2', 'option3', 'option4']

    message = f"Please select an option by typing its number:\n\n"
    for i, option in enumerate(options):
        message += f"{i+1}. {option}\n"

    await ctx.send(message)
    response = await client.wait_for('message', check=lambda message: message.author == ctx.author)

    try:
        option_number = int(response.content)
        selected_option = options[option_number-1]
        await ctx.send(f"You selected: {selected_option}")
    except (ValueError, IndexError):
        await ctx.send("Invalid option selected")

@client.command()
async def react_role(ctx, role: discord.Role, action: str):
    if action == "add":
        await ctx.send(f"React to this message to get the {role.mention} role!")
    elif action == "remove":
        await ctx.send(f"React to this message to remove the {role.mention} role!")
    else:
        await ctx.send("Invalid action specified.")

    # Wait for the user to react to the message
    reaction, user = await client.wait_for(
        "reaction_add",
        check=lambda r, u: u == ctx.author and r.message.channel == ctx.channel,
    )
    if reaction.emoji == "✅":
        if action == "add":
            await user.add_roles(role)
            await ctx.send(f"{user.mention}, you now have the {role.mention} role!")
        elif action == "remove":
            await user.remove_roles(role)
            await ctx.send(f"{user.mention}, you no longer have the {role.mention} role!")
    else:
        await ctx.send("You didn't react with the checkmark emoji.")

async def start_bot():
    session = await create_session()
    client.session = session
    try:
        await client.start('your_bot_token')
    finally:
        await session.close()

asyncio.get_event_loop().run_until_complete(start_bot())
