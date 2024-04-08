import discord
from discord.ext import commands, tasks
import random
import datetime
import json
import pytz

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='/', intents=intents)
channel_id = 1113433596934504579
# Kayki, David, Cesar, Vitor, Jonatas, Joao Henrique, Jessica, Matheus
membros = [577980969374449684, 851799475617005608, 1009869447143620728, 737819749756698745, 1148938354793123981, 808328918603268207, 512012088013619243, 339537391834628096]
# Equipe Regulatorio, Equipe Pld
cargos = [960622553024585839, 1095062418469695488]

aniversarios_da_equipe = [
    {'nome': 'KAYKI', 'mes': 7, 'dia': 10, 'id': 512012088013619243},
    {'nome': 'ZÉ LEO', 'mes': 9, 'dia': 5, 'id': 805782737692393492},
    {'nome': 'DAVID MEU BROTHER', 'mes': 10, 'dia': 12, 'id': 577980969374449684},
    {'nome': 'CESINHA FOX', 'mes': 5, 'dia': 21, 'id': 214478481608671233},
    {'nome': 'THEUZIN', 'mes': 7, 'dia': 13, 'id': 339537391834628096},
    {'nome': 'JONATAS ESTAGIÁRIO', 'mes': 10, 'dia': 15, 'id': 737819749756698745},
    {'nome': 'JÃO HENRIQUE', 'mes': 6, 'dia': 9, 'id': 1148938354793123981},
    {'nome': 'JESSÍCA', 'mes': 12, 'dia': 9, 'id': 808328918603268207},
    {'nome': 'VITÃO', 'mes': 9, 'dia': 17, 'id': 1009869447143620728}
]

link_meet = 'https://teams.microsoft.com/l/meetup-join/19%3Ameeting_Y2QxMzYzYTAtMTNhZS00OTBkLWIwMmUtZTBkMzkxMzYyOWUy%40thread.v2/0?context=%7B"Tid"%3A"d1927cad-e5bc-49ce-b46a-f9ed29711647"%2C"Oid"%3A"547705cd-3081-4f8a-beb4-ece69ddc836d"%7D'

membros_sorteados = []
indice_frase_do_dia = 0
random.seed()

def determinar_titulo(agora):

    if agora.month == 7 and agora.day == 10:
        return "FELIZ ANIVERSÁRIO GÊNIO INCOMPREENDIDO!!!"
        
    if agora.weekday() == 4:
        return "SEXTOU EQUIPE!!!"

    return "BOM DIA EQUIPE!!!"

@bot.event
async def on_ready():
    print(f'{bot.user.name} está conectado! hora:{datetime.datetime.now()}')

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s): {datetime.datetime.now()}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

    enviar_mensagem.start()
    channel = bot.get_channel(channel_id)

    if channel:
        # Envia a mensagem
        await channel.send(f'{bot.user.name} está online!')

registro_aniversarios = {pessoa['nome']: None for pessoa in aniversarios_da_equipe}

@tasks.loop(minutes=1)
async def enviar_mensagem():
    global envios_realizados

    fuso_horario_sao_paulo = pytz.timezone('America/Sao_Paulo')
    agora = datetime.datetime.now(fuso_horario_sao_paulo)
    horario_envio = agora.replace(hour=8, minute=57, second=7, microsecond=7)

    # Verificar se é o aniversário de alguém
    for pessoa in aniversarios_da_equipe:
        if agora.month == pessoa['mes'] and agora.day == pessoa['dia']:
            nome_pessoa = pessoa['nome']
            id_pessoa = pessoa["id"]
            if registro_aniversarios[nome_pessoa] != agora.date():
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f'**FELIZ ANIVERSÁRIO, {nome_pessoa}**! <@{id_pessoa}> @here 🎉🎉🎉')
                    registro_aniversarios[nome_pessoa] = agora.date()


    # Verificar se é dia útil (segunda a sexta)
    if agora.weekday() < 5 and agora >= horario_envio and agora <= horario_envio + datetime.timedelta(minutes=1):
        channel = bot.get_channel(channel_id)

        if channel:
            mensagem = f'{mencionar_cargos()}\n' \
                       f'Regulatório Daily\'s Definitiva\n' \
                       f'{agora.strftime("%A, %d de %B")} · 9:00 até 9:15am\n' \
                       f'[Link da videochamada]({link_meet})\n' \
                       f'Apresentação: {sortear_proximo_membro()}\n' \
                       f'Frase do dia: {mencionar_proximo_membro_frase_do_dia()}'
            
            embed = discord.Embed(
                title=determinar_titulo(agora),
                description=mensagem,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1152019240652640298/1212380497884221501/GaivotadasnotC3ADcias.png?ex=65f1a053&is=65df2b53&hm=6eb20c1a21b6ad6ac8f90a714a0b40ddacebeeacb6f55f8df7539176e8051dc5&=&format=webp&quality=lossless")

            await channel.send(embed=embed)

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


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello world!")

@bot.tree.command(name="mostrar_hora")
async def mostrar_hora(interaction: discord.Interaction):
    agora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    await interaction.response.send_message(f'Agora são {agora.strftime("%H:%M:%S")}')

@bot.tree.command(name="trocar_link_meet")
async def trocar_link_meet(interaction: discord.Interaction):
    global link_meet
    link_meet = interaction.data['options'][0]['value']
    await interaction.response.send_message(f'Link do Google Meet alterado para {link_meet}')

@bot.tree.command(name="adicionar_membro")
async def adicionar_membro(interaction: discord.Interaction):
    global membros
    membros.append(int(interaction.data['options'][0]['value']))
    await interaction.response.send_message(f'Membro adicionado com sucesso!')

@bot.tree.command(name="remover_membro")
async def remover_membro(interaction: discord.Interaction):
    global membros
    membros.remove(int(interaction.data['options'][0]['value']))
    await interaction.response.send_message(f'Membro removido com sucesso!')

@bot.tree.command(name='ordem_frase_do_dia')
async def ordem_frase_do_dia(interaction: discord.Interaction):
    global membros, indice_frase_do_dia

    lista_ordem = '\n'.join([f"{i+1}. <@{membro_id}>" for i, membro_id in enumerate(membros)])

    await interaction.response.send(f"A ordem para a frase do dia é:\n{lista_ordem}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(config['token'])
