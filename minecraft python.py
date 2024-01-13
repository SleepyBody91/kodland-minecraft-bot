import sys, re
from javascript import require, On, Once, console
import time
mineflayer = require("mineflayer", "latest")
Vec3 = require("vec3").Vec3


host = input("введите id мира:")
port = input("введите порт:")
username = input("введите имя бота:")

bot = mineflayer.createBot({
    "host": host,
    "port": port,
    "username": username,
    "port": port
})

Item = require("prismarine-item")(bot.registry)


@On(bot, "chat")
def handle(this, username, message, *args):
    if username == bot.username:
        return

    if message.startswith("can see"):
        try:
            x, y, z = map(lambda v: int(v), message.split("see")[1].replace(",", " ").split())
        except Exception:
            bot.chat("Bad syntax")
            #команды
    elif message.startswith("pos"):
        say_position(username)
    elif message.startswith("wearing"):   
        say_equipment(username)
    elif message.startswith("block"):
        say_block_under()
    elif message.startswith("spawn"):
        say_spawn()
    elif message.startswith("quit"):
        quit_game(username)
    else:
        bot.chat("Пон")


def can_see(pos):
    block = bot.blockAt(pos)
    canSee = bot.canSeeBlock(block)

    if canSee:
        time.sleep(2)
        bot.chat(f"Я вижу этот блок на {block.displayName} в {pos}")
    else:
        time.sleep(2)
        bot.chat(f"Я не вижу этот блок на {block.displayName} в {pos}")


def say_position(username):
    p = bot.entity.position
    bot.chat(f"I am at {p.toString()}")
    if username in bot.players:
        p = bot.players[username].entity.position
        bot.chat(f"Ты на {p.toString()}")

def say_equipment(username):
    eq = bot.players[username].entity.equipment
    eqText = []
    if eq[0]:
        eqText.append(f"{eq[0].displayName}")
    if eq[1]:
        eqText.append(f"{eq[1].displayName} на твоих ступнях")
    if eq[2]:
        eqText.append(f"{eq[2].displayName} на твоих ногах")
    if eq[3]:
        eqText.append(f"{eq[3].displayName} на твоем торсе")
    if eq[4]:
        eqText.append(f" {eq[4].displayName} на твоей голове")
    if len(eqText):
        time.sleep(2)
        bot.chat(f"Ты {', '.join(eqText)}.")
    else:
        time.sleep(2)
        bot.chat("Ты без брони")


def say_spawn():
    time.sleep(2)
    bot.chat(f"Я заспавнился в {bot.spawnPoint.toString()}")


def say_block_under():
    block = bot.blockAt(bot.players[username].entity.position.offset(0, -1, 0))
    time.sleep(2)
    bot.chat(f"Блок под тобой - {block.displayName} в {block.biome.name} биоме")
    print(block)


def quit_game(username):
    time.sleep(2)
    bot.quit(f"{username} сказал мне")


def say_nick():
    time.sleep(2)
    bot.chat(f"Меня зовут - {bot.player.displayName}")


@On(bot, "whisper")
def whisper(this, username, message, rawMessage, *a):
    console.log(f"Я получил сообщение от {username}: {message}")
    time.sleep(2)
    bot.whisper(username, "Я тоже могу хранить секреты")


@On(bot, "login")
def login(this):
    time.sleep(2)
    bot.chat("Всем привет!")


@On(bot, "spawn")
def spawn(this):
    time.sleep(2)
    bot.chat("Я родился")


@On(bot, "spawnReset")
def spawnReset(this, message):
    time.sleep(2)
    bot.chat("Кто то сломал мою кровать")


@On(bot, "forcedMove")
def forcedMove(this):
    p = bot.entity.position
    time.sleep(2)
    bot.chat(f"Я был вынужден пойти  в {p.toString()}")


@On(bot, "health")
def health(this):
    time.sleep(2)
    bot.chat(f"У меня {bot.health} здоровья и {bot.food} голод")


@On(bot, "death")
def death(this):
    time.sleep(2)
    bot.chat("я умер:( )")


@On(bot, "kicked")
def kicked(this, reason, *a):
    print("Бота кикнули", reason, a)
    console.log(f"Я был исключен из мира по причине: {reason}")


#@On(bot, "time")
#def time(this):
#    bot.chat(f"Хм, я посмотрел на время, время: " + str(bot.time.timeOfDay))
#    time.sleep(10)


@On(bot, "rain")
def rain(this):
    if bot.isRaining:
        time.sleep(2)
        bot.chat("Дождь начался")
    else:
        time.sleep(2)
        bot.chat("Дождь закончился")


@On(bot, "noteHeard")
def noteHeard(this, block, instrument, pitch):
    time.sleep(2)
    bot.chat(f"Я слышу музыку, похоже сейчас играет - {instrument.name}")


@On(bot, "chestLidMove")
def chestLidMove(this, block, isOpen, *a):
    action = "open" if isOpen else "close"
    time.sleep(2)
    bot.chat(f"сундук был {action}")


@On(bot, "pistonMove")
def pistonMove(this, block, isPulling, direction):
    action = "pulling" if isPulling else "pushing"
    time.sleep(2)
    bot.chat(f"Рядом со мной {action}  поршень, я его слышу.")


@On(bot, "playerJoined")
def playerJoined(this, player):
    print("joined / зашел ", player)
    if player["username"] != bot.username:
        time.sleep(2)
        bot.chat(f"Привет, {player['username']}! Добро пожаловать в мир.")


@On(bot, "playerLeft")
def playerLeft(this, player):
    if player["username"] == bot.username:
        return
    time.sleep(2)    
    bot.chat(f"Пока ${player.username}")


@On(bot, "playerCollect")
def playerCollect(this, collector, collected):
    if collector.type == "player" and collected.type == "object":
        raw_item = collected.metadata[10]
        item = Item.fromNotch(raw_item)
        header = ("Я так хочу " + collector.username) if (
            collector.username != bot.username) else "I "
        bot.chat(f"{header} собрал {item.count} {item.displayName}")


@On(bot, "entitySpawn")
def entitySpawn(this, entity):
    if entity.type == "mob":
        p = entity.position
        console.log(f"Смотрите!  {entity.displayName} заспавнился в {p.toString()}")
    elif entity.type == "player":
        time.sleep(2)
        bot.chat(f"{entity.username} - появился ")
    elif entity.type == "object":
        p = entity.position
        console.log(f"Здесь {entity.displayName} в {p.toString()}")
    elif entity.type == "global":
        time.sleep(2)
        bot.chat("Ой блин! Молния")
    elif entity.type == "orb":
        time.sleep(2)
        bot.chat("Я чувствою опыт")


@On(bot, "entityHurt")
def entityHurt(this, entity):
    if entity.type == "mob":
        time.sleep(2)
        bot.chat(f" Моб ${entity.displayName} получил урон")
    elif entity.type == "player":
        if entity.username in bot.players:
            ping = bot.players[entity.username].ping
            time.sleep(2)
            bot.chat(f"ОЙ, похоже {entity.username} получил урон. ")


@On(bot, "entitySwingArm")
def entitySwingArm(this, entity):
    time.sleep(1)
    bot.chat(f"{entity.username} - использует руку прямо сейчас")


@On(bot, "entityCrouch")
def entityCrouch(this, entity):
    time.sleep(1)
    bot.chat(f"${entity.username} - присел .")


@On(bot, "entityUncrouch")
def entityUncrouch(this, entity):
    time.sleep(1)
    bot.chat(f"{entity.username} снова встал на ноги.")


@On(bot, "entitySleep")
def entitySleep(this, entity):
    bot.chat(f"Удачной ночи, {entity.username}")


@On(bot, "entityWake")
def entityWake(this, entity):
    bot.chat(f"С добрым утром, {entity.username}")


@On(bot, "entityEat")
def entityEat(this, entity):
    time.sleep(2)
    bot.chat(f"похоже {entity.username} прямо сейчас кушает.")


@On(bot, "entityAttach")
def entityAttach(this, entity, vehicle):
    if entity.type == "player" and vehicle.type == "object":
        print(f"Опа, {entity.username} ездиет на {vehicle.displayName}")


@On(bot, "entityDetach")
def entityDetach(this, entity, vehicle):
    if entity.type == "player" and vehicle.type == "object":
        print(f"{entity.username} перестал кататься на {vehicle.displayName}")


@On(bot, "entityEquipmentChange")
def entityEquipmentChange(this, entity):
    print("entityEquipmentChange", entity)


@On(bot, "entityEffect")
def entityEffect(this, entity, effect):
    print("entityEffect", entity, effect)


@On(bot, "entityEffectEnd")
def entityEffectEnd(this, entity, effect):
    print("entityEffectEnd", entity, effect)