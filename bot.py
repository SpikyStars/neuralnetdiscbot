import colorsys
import math
import os.path
import sys
import discord
from datetime import datetime
import util
from classifier import classify_image

client = discord.Bot()


# assumes each individual guild id is on its own line
def load_guild_ids():
    if os.path.isfile("guild_ids.txt"):
        f_guilds = open("guild_ids.txt", "r")
        return [int(line.rstrip()) for line in f_guilds.readlines()]


guilds = load_guild_ids()


def launch_bot():
    if os.path.isfile("token.txt"):
        token = open("token.txt", "r")
        try:
            client.run(token.read())
        except discord.HTTPException:
            sys.exit("The bot token you provided is invalid!")
    else:
        sys.exit("You need to create a token.txt file containing your bot token!")


@client.event
async def on_ready():
    print("Bot has connected!")


@client.slash_command(guild_ids=guilds, description="Ping the bot")
async def ping(ctx):
    cur_time = datetime.now()
    await ctx.respond("Pong!")
    new_time = datetime.now()
    time_diff = str((new_time - cur_time).microseconds / 1000) + "ms"
    await ctx.edit(content=f"Pong! {time_diff}")


@client.slash_command(guild_ids=guilds,
                      description="Classify an image")
async def classify(ctx, image_link: str):
    # acknowledge the request
    await ctx.defer()
    try:
        image = util.read_image(image_link)
        results = classify_image(image)
        response = display_results(results, image_link)
        await ctx.respond(embed=response)
    except util.InputException as e:
        await ctx.respond(e.message)


def display_results(results, image_link):
    embed = discord.Embed()
    result_printout = [f"{result[0]}, {display_pct(result[1])}\n" for result in results]
    # Using the percentage of the very first result, calculate colour
    embed.colour = get_embed_color(results[0][1])
    embed.add_field(name="Results", value="".join(result_printout))
    embed.set_image(url=image_link)
    return embed


def display_pct(pct):
    return str(pct) + "%"


def get_embed_color(pct):
    # HSV values are between 0 and 1, and we want colors ranging from red to green
    # (which are approximately 1/3rd of the hue values)
    hue = pct * 0.003
    rgb = colorsys.hsv_to_rgb(hue, 1, 0.8)
    # Convert the rgb tuple into a hexadecimal representation
    return int("".join([f"{math.ceil(v * 255):02x}" for v in rgb]), 16)


if __name__ == '__main__':
    launch_bot()
