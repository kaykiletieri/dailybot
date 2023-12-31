import discord
from discord.ext import commands, tasks
import random
import datetime
import json
import pytz

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='/', intents=intents)
channel_id = 1113433596934504579
# Kayki, David, Cesar, Vitor, Jonatas, Joao Henrique, Jessica
membros = [577980969374449684, 851799475617005608, 1009869447143620728, 737819749756698745, 1148938354793123981, 808328918603268207, 512012088013619243]
# Equipe Regulatorio, Equipe Pld
cargos = [960622553024585839, 1095062418469695488]

membros_sorteados = []
indice_frase_do_dia = 0
random.seed()

@bot.event
async def on_ready():
    print(f'{bot.user.name} está conectado! hora:{datetime.datetime.now()}')

    enviar_mensagem.start()
    channel = bot.get_channel(channel_id)

    if channel:
        # Envia a mensagem
        await channel.send(f'{bot.user.name} está online!')

@tasks.loop(minutes=1)
async def enviar_mensagem():
    global envios_realizados

    fuso_horario_sao_paulo = pytz.timezone('America/Sao_Paulo')
    agora = datetime.datetime.now(fuso_horario_sao_paulo)
    horario_envio = agora.replace(hour=8, minute=23, second=7, microsecond=7)

    # Verificar se é dia útil (segunda a sexta)
    if agora.weekday() < 5 and agora >= horario_envio and agora <= horario_envio + datetime.timedelta(minutes=1):
        channel = bot.get_channel(channel_id)

        if channel:
            mensagem = f'Bom diaaa equipe!!!\n' \
                       f'{mencionar_cargos()}\n' \
                       f'Regulatório Daily\'s Definitiva\n' \
                       f'{agora.strftime("%A, %d de %B")} · 8:30 até 8:45am\n' \
                       f'Fuso horário: America/Sao_Paulo\n' \
                       f'Como participar do Google Meet\n' \
                       f'Link da videochamada: https://meet.google.com/upf-orzm-oks\n' \
                       f'Apresentação: {sortear_proximo_membro()}\n' \
                       f'Frase do dia: {mencionar_proximo_membro_frase_do_dia()}'

            await channel.send(mensagem)

def mencionar_cargos():
    mencao_cargos = ""
    for cargo_id in cargos:
        mencao_cargos += f'<@&{cargo_id}> '
    return mencao_cargos

def mencionar_proximo_membro_frase_do_dia():
    global indice_frase_do_dia
    member_id = membros[indice_frase_do_dia]
    indice_frase_do_dia = (indice_frase_do_dia + 1) % len(membros)
    return f'<@{member_id}>'

def sortear_proximo_membro():
    global membros_sorteados
    if len(membros_sorteados) == len(membros):
        membros_sorteados.clear()

    member_id = random.choice(membros)
    while member_id in membros_sorteados:
        member_id = random.choice(membros)

    membros_sorteados.append(member_id)
    return f'<@{member_id}>'


@bot.command(name='ignorardiautil')
async def ignorar_proximo_dia_util(ctx):
    global proximo_dia_util_ignorado

    agora = datetime.datetime.now()

    # Verifica se já é sexta-feira, se sim, pula para a próxima segunda-feira
    if agora.weekday() == 4:
        agora += datetime.timedelta(days=3)
    else:
        agora += datetime.timedelta(days=1)

    # Define a próxima data de envio
    proximo_dia_util_ignorado = agora.date()

    await ctx.send(f"O próximo dia útil ({proximo_dia_util_ignorado.strftime('%d/%m/%Y')}) foi marcado como ignorado.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(config['token'])
