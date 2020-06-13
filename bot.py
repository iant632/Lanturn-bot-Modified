import discord
from discord.ext import commands
import asyncio
import sys

TOKEN = 'Your Token Here'

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

extensions = ['RaidCommands']

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	channel = message.channel
	if message.guild is None:
		await message.channel.send("I can't help you in here :(")
	else:
	    await client.process_commands(message)

#Command used for bot admin to turn their bot off
#Please put the admin's discord ID where indicated
		
#Sends greet command
@client.command()
async def greet(ctx):
	await ctx.send("Hello everyone! I am <placeholder> and I'm here to assist you :)")

@client.command()
async def load(extension):
	try:
		client.load_extension(extension)
		print('Loaded {}'.format(extension))
	except Exception as error:
		print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def unload(extension):
	try:
		client.unload_extension(extension)
		print('Unloaded {}'.format(extension))
	except Exception as error:
		print('{} cannot be unloaded. [{}]'.format(extension, error))

async def test():
	while True:
		print("Hello!")
		await asyncio.sleep(1)

if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded. [{}]'.format(extension, error))

	#client.loop.create_task(test())
	client.run(TOKEN)
