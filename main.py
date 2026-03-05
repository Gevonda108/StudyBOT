import discord
from discord.ext import commands
from db import setup_db, add_flashcard, get_flashcards, get_all_subjects


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online: {bot.user}")


@bot.command()
async def addcard(ctx, subject, *, content):

    parts = content.split('" "')
    if len(parts) != 2:
        await ctx.send('Format: !addcard subject "question" "answer"')
        return
    
    question = parts[0].replace('"', '')
    answer = parts[1].replace('"', '')
    
    add_flashcard(subject, question, answer)
    await ctx.send(f"Added to {subject}!")

@bot.command()
async def study(ctx, subject):
    cards = get_flashcards(subject)
    
    if not cards:
        await ctx.send(f"No cards for {subject}")
        return
    
    for i, card in enumerate(cards):

        await ctx.send(f"**Card {i+1}/{len(cards)}: {card['q']}**")
        await ctx.send("Reply with anything to see the answer!")
        

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            await bot.wait_for('message', check=check, timeout=30)
        except:
            await ctx.send("No response, skipping...")
            continue
        

        await ctx.send(f"✅ Answer: {card['a']}")
        await ctx.send("---")

@bot.command()
async def subjects(ctx):
    all_subs = get_all_subjects()
    if not all_subs:
        await ctx.send("No subjects yet!")
    else:
        await ctx.send("Subjects: " + ", ".join(all_subs))

@bot.command(name="cmds")
async def cmds(ctx):
    await ctx.send('''!addcard subject "question" "answer"
!study subject
!subjects''')


setup_db()
token = token
bot.run(token)
