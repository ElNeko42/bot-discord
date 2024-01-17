import discord
import aiohttp
from flask import Flask
from threading import Thread
import random

app = Flask('')


@app.route('/')
def home():
  return "¡Estoy vivo!"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Diccionario para llevar el conteo de comandos utilizados por usuario
command_usage = {}
command_list = {
    '$juegosgratis':
    'Muestra una lista de juegos gratis disponibles en diferentes plataformas.',
    '$pajagrupal': 'Inicia una cuenta atrás para una paja grupal.',
    '$gay': 'Analiza tu porcentaje de homosexualidad que tienes.',
    '$banana': 'Digo el tamaño de tu banana.',
    # Añade aquí otros comandos que tengas
}


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


async def fetch_free_games(session, url):
  async with session.get(url) as response:
    if response.status == 200:
      return await response.json()
    return None


@client.event
async def on_message(message):
  global command_usage

  if message.author == client.user:
    return

  if message.content.startswith('$juegosgratis'):
    urls = [
        "https://www.gamerpower.com/api/giveaways?platform=epic-games-store&type=game",
        "https://www.gamerpower.com/api/giveaways?platform=steam&type=game",
        "https://www.gamerpower.com/api/giveaways?platform=gog&type=game"
    ]
    response_message = "Juegos gratis en Epic, Steam y GOG:\n"
    async with aiohttp.ClientSession() as session:
      for url in urls:
        games = await fetch_free_games(session, url)
        if games:
          for game in games:
            title = game['title']
            worth = game['worth']
            description = game['description']
            link = game['open_giveaway_url']
            new_message = f"**{title}** - Valor: {worth}\n{description}\nLink: {link}\n\n"
            if len(response_message) + len(new_message) > 2000:
              await message.channel.send(response_message)
              response_message = new_message
            else:
              response_message += new_message
        else:
          response_message += "No se encontraron juegos gratis en una de las plataformas.\n\n"
      if response_message:
        await message.channel.send(response_message)

  elif message.content.startswith('$pajagrupal'):
    user = message.author

    # Incrementar el conteo para el usuario
    if user in command_usage:
      command_usage[user] += 1
    else:
      command_usage[user] = 1

    user_display_name = user.display_name

    # Enviar mensaje con el conteo
    await message.channel.send(
        f"{user_display_name}, ha iniciado una paja grupal en 5 minutos ,esto no es un simulacro ,\n la duración será de 30 minutos lleven vaselina y galletas ,\n repito paja grupal en 5 minutos esto no es un simulacro ,\n la duración será de 30 minutos lleven vaselina y disfruten .\n\n Te has masturbado con tus panas  {command_usage[user]} veces."
    )

  elif message.content.startswith('$gay'):
    user = message.author
    user_display_name = user.display_name

    random_number = random.randint(0, 100)
    await message.channel.send(
        f"Tu porcentaje de homosexualidad es : {random_number}%")

  elif message.content.startswith('$banana'):
    random_number = random.randint(5, 30)
    await message.channel.send(f"Tu Banana mide {random_number}cm")

  elif message.content.startswith('$comandos'):
    commands_description = "Lista de comandos disponibles:\n"
    for command, description in command_list.items():
      commands_description += f"**{command}**: {description}\n"
    await message.channel.send(commands_description)


keep_alive()
client.run('TOKEN')
