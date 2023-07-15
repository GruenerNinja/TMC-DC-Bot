import discord
from discord.app import OptionType
from discord.app.commands import SlashCommand
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="list_commands",
    description="List all commands",
    guild=discord.Object(id=YourGuildID)
)
async def list_commands(ctx):
    commands_list = [cmd.name for cmd in client.commands]
    commands_str = "\n".join(commands_list)
    await ctx.send(f"Here are all the commands:\n{commands_str}")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=YourGuildID))
    print("Ready!")

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

@tree.command(
    name="reactingrole",
    description="Select an option",
    guild=discord.Object(id=YourGuildID)
)
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

@tree.command(
    name="react_role",
    description="Add or remove a role",
    guild=discord.Object(id=YourGuildID)
)
async def react_role(ctx, role: discord.Role, action: str):
    if action == "add":
        await ctx.send(f"React to this message to get the {role.mention} role!")
    elif action == "remove":
        await ctx.send(f"React to this message to remove the {role.mention} role!")
    else:
        await ctx.send("Invalid action specified.")

    message = await ctx.send("Waiting for reaction...")
    await message.add_reaction("✅")

    reaction, user = await client.wait_for(
        "reaction_add",
        check=lambda r, u: u == ctx.author and r.message == message,
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


client.run('your_bot_token')