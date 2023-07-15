import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

intents = discord.Intents.default()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@slash.slash(name="list_commands", description="List all commands")
async def list_commands(ctx: SlashContext):
    commands_list = [cmd.name for cmd in slash.commands]
    commands_str = "\n".join(commands_list)
    await ctx.send(f"Here are all the commands:\n{commands_str}")

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

@slash.slash(
    name="reactingrole",
    description="Select an option",
    options=[
        create_option(
            name="option",
            description="Select an option",
            option_type=OptionType.INTEGER,
            choices=[
                create_option(
                    name="Option 1",
                    value=1
                ),
                create_option(
                    name="Option 2",
                    value=2
                ),
                create_option(
                    name="Option 3",
                    value=3
                ),
                create_option(
                    name="Option 4",
                    value=4
                )
            ]
        )
    ]
)
async def reactingrole(ctx: SlashContext, option: int):
    options = ['option1', 'option2', 'option3', 'option4']

    if option > 0 and option <= len(options):
        selected_option = options[option-1]
        await ctx.send(f"You selected: {selected_option}")
    else:
        await ctx.send("Invalid option selected")

@slash.slash(
    name="react_role",
    description="Add or remove a role",
    options=[
        create_option(
            name="role",
            description="Select a role",
            option_type=OptionType.ROLE,
            required=True
        ),
        create_option(
            name="action",
            description="Specify the action",
            option_type=OptionType.STRING,
            choices=[
                create_option(
                    name="Add",
                    value="add"
                ),
                create_option(
                    name="Remove",
                    value="remove"
                )
            ],
            required=True
        )
    ]
)
async def react_role(ctx: SlashContext, role: discord.Role, action: str):
    if action == "add":
        await ctx.send(f"React to this message to get the {role.mention} role!")
    elif action == "remove":
        await ctx.send(f"React to this message to remove the {role.mention} role!")
    else:
        await ctx.send("Invalid action specified.")

    message = await ctx.send("Waiting for reaction...")
    await message.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except TimeoutError:
        await ctx.send("You didn't react with the checkmark emoji within 60 seconds.")
    else:
        if action == "add":
            await user.add_roles(role)
            await ctx.send(f"{user.mention}, you now have the {role.mention} role!")
        elif action == "remove":
            await user.remove_roles(role)
            await ctx.send(f"{user.mention}, you no longer have the {role.mention} role!")

client.run('your_bot_token')
