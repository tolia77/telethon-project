from random import randint, shuffle, choice
from time import sleep
import warnings
from sys import stdout
from colorama import Fore, init
from telethon import TelegramClient as TelegramClientAsync
from telethon.tl.functions.messages import GetAllStickersRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
from function_telethon import *
from phrases import *
warnings.filterwarnings("ignore")
init(convert=True)
while True:
    stdout.write(Fore.GREEN + """           МЕНЮ
1. ВСТУПИТЬ В КАНАЛ
2. ВЫЙТИ ИЗ КАНАЛА
3. ВСТУПИТЬ В КАНАЛ + КОММЕНТАРИЙ ПОД ПОСТ
4. СООБЩЕНИЕ
5. ДОБАВИТЬ АККАУНТ
6. ОТКРЫТЫЕ СЕССИИ
7. ПЕРЕМЕШАТЬ СЕССИИ
8. ВСТУПИТЬ В ЧАТ И ОТПРАВИТЬ СООБЩЕНИЕ
9. ДЕЙСТВИЯ НАД СЕССИЯМИ
0. ВСТУПИТЬ В КАНАЛ + КОММЕНТАРИЙ ПОД ПОСТ""" + Fore.RED + " (!!!АСИНХРОННО!!!)\n" +
             Fore.GREEN + "00. ВСТУПИТЬ В КАНАЛ + АНИМИРОВАННЫЙ СТИКЕР ПОД ПОСТ" + Fore.RED + " (!!!АСИНХРОННО!!!)\n")
    action = input(Fore.YELLOW + "ВЫБЕРИТЕ ДЕЙСТВИЕ: ")
    match action:
        case "1":
            invite_link = input("Ссылка на канал: ")
            while True:
                interval = input("Задержка (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            sessions = [session for session in load_sessions() if session["isActive"]]
            for session in sessions:
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    if "+" in invite_link:
                        with client:
                            join_private_channel(client, invite_link)
                    else:
                        with client:
                            join_public_channel(client, invite_link)
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ В КАНАЛ - УСПЕШНО")
                except Exception:
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ В КАНАЛ - ОШИБКА")
                pause = randint(min_s, max_s)
                sleep(pause)
        case "2":
            invite_link = input("Ссылка на канал: ")
            while True:
                interval = input("Задержка (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            sessions = [session for session in load_sessions() if session["isActive"]]
            for session in sessions:
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    if "+" in invite_link:
                        with client:
                            leave_private_channel(client, invite_link)
                    else:
                        with client:
                            leave_public_channel(client, invite_link)
                    print(f"{session['USERNAME']}: ВЫХОД ИЗ КАНАЛА - УСПЕШНО")
                except Exception:
                    print(f"{session['USERNAME']}: ВЫХОД ИЗ КАНАЛА - ОШИБКА!")
                pause = randint(min_s, max_s)
                sleep(pause)
        case "3":
            post_link = input("Введите ссылку на пост: ")
            message = input(
                """Введите текст сообщения (Пустая строка - рандом из списка
                        # - ввести от каждого аккаунта вручную
                        * - отправить юзернейм аккаунта
                        d - отправить шаблон done
                        w - отправить кошелёк
                        n - отправить рандомное число от 1 до 150
                        p - отправить фразу
                        w+ - интегрировать кошелёк в сообщение) : """)
            while True:
                interval = input("Задержка (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            sessions = [session for session in load_sessions() if session["isActive"]]
            used_numbers = []
            if message == "w+":
                extra_text = input("Введите сообщение: ")
            for session in sessions:
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    if message == "":
                        message = choice(("*", "d"))
                    if message == "#":
                        message_unique = input("Введите сообщение: ")
                        join_and_comment_post(client, post_link, message_unique)
                    elif message == "*":
                        join_and_comment_post(client, post_link, "@" + client.get_me().username)
                    elif message == "d":
                        join_and_comment_post(client, post_link, choice(done_templates))
                    elif message == "w":
                        join_and_comment_post(client, post_link, session["doneTemplate"])
                    elif message == "p":
                        join_and_comment_post(client, post_link, choice(phrases))
                    elif message == "n":
                        number = randint(1, 150)
                        while number in used_numbers:
                            number = randint(1, 150)
                        join_and_comment_post(client, post_link, str(number))
                        used_numbers.append(number)
                    elif message == "w+":
                        join_and_comment_post(client, post_link, session["doneTemplate"] + " " + extra_text)
                    else:
                        join_and_comment_post(client, post_link, message)
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ + КОММЕНТАРИЙ - УСПЕШНО")
                except Exception as ex:
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ + КОММЕНТАРИЙ - ОШИБКА!")
                    print(ex)
                pause = randint(min_s, max_s)
                sleep(pause)
        case "4":
            username = input("Имя пользователя: ")
            message = input(
                """Введите текст сообщения (Пустая строка - рандом из списка
                        # - ввести от каждого аккаунта вручную
                        * - отправить юзернейм аккаунта
                        d - отправить шаблон done
                        w - отправить кошелёк
                        n - отправить рандомное число от 1 до 150
                        p - отправить фразу
                        w+ - интегрировать кошелёк в сообщение) : """)
            while True:
                interval = input("Задержка (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            sessions = [session for session in load_sessions() if session["isActive"]]
            used_numbers = []
            if message == "w+":
                extra_text = input("Введите сообщение: ")
            for session in sessions:
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    if message == "":
                        message = choice(("*", "d"))
                    if message == "#":
                        message_unique = input("Введите сообщение: ")
                        client.send_message(username, message_unique)
                    elif message == "*":
                        client.send_message(username, "@" + client.get_me().username)
                    elif message == "d":
                        client.send_message(username, choice(done_templates))
                    elif message == "w":
                        client.send_message(username, session["doneTemplate"])
                    elif message == "p":
                        client.send_message(username, choice(phrases))
                    elif message == "n":
                        number = randint(1, 150)
                        while number in used_numbers:
                            number = randint(1, 150)
                        client.send_message(username, str(number))
                        used_numbers.append(number)
                    elif message == "w+":
                        client.send_message(username, session["doneTemplate"] + " " + extra_text)
                    elif message == "s":
                        ...; ...; ...; ...; ...; ...
                    else:
                        client.send_message(username, message)
                    print(f"{session['USERNAME']}: ОТПРАВКА СООБЩЕНИЯ - УСПЕШНО")
                except Exception as ex:
                    print(f"{session['USERNAME']}: ОТПРАВКА СООБЩЕНИЯ - ОШИБКА!")
                pause = randint(min_s, max_s)
                sleep(pause)
        case "5":
            print(Fore.BLUE + "АВТОРИЗАЦИЯ")
            while True:
                api_id = input("Введите api_id (! - выход из режима регистрации): ")
                if api_id != "!":
                    try:
                        api_id = int(api_id)
                        break
                    except ValueError:
                        print("Введите число!")
                else:
                    break
            if api_id != "!":
                api_hash = input("Введите api_hash: ")
                done_template = input("Введите шаблон done: ")
                try:
                    add_account(api_id, api_hash, done_template)
                except Exception:
                    print("ДОБАВЛЕНИЕ АККАУНТА - ОШИБКА")
        case "6":
            with open("active_sessions.json", "r") as file:
                data_loaded = loads(file.read())
            print(Fore.BLUE + "Подключенные пользователи")
            for session in data_loaded:
                print(
                    f"{Fore.BLUE}Запрос пользователя {session['USERNAME']}", end=" " * (30 - len(session["USERNAME"])))
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    if client.get_me() is None:
                        delete_account(session["ID_SESSION"])
                        print("ОШИБКА")
                        api_id = input("Введите api_id (! - выход из режима регистрации): ")
                        if api_id != "!":
                            while True:
                                try:
                                    api_id = int(api_id)
                                    break
                                except ValueError:
                                    print("Введите число!")
                            api_hash = input("Введите api_hash: ")
                            done_template = input("Введите шаблон done: ")
                            try:
                                add_account(api_id, api_hash, done_template)
                            except Exception as ex:
                                print(ex)
                    else:
                        username = session["USERNAME"]
                        phone_number = client.get_me().phone
                        print(Fore.GREEN + "+" + phone_number)
                except Exception as ex:
                    print(ex)
        case "7":
            with open("active_sessions.json", "r") as file:
                data_loaded = loads(file.read())
            shuffle(data_loaded)
            with open("active_sessions.json", "w") as file:
                file.write(dumps(data_loaded, sort_keys=True, indent=4))
            print(Fore.GREEN + "Порядок сессий изменён")
        case "8":
            chat_link = input("Введите ссылку на чат: ")
            message = input(
                """Введите текст сообщения (Пустая строка - рандом из списка
                        # - ввести от каждого аккаунта вручную
                        * - отправить юзернейм аккаунта
                        d - отправить шаблон done
                        w - отправить кошелёк
                        n - отправить рандомное число от 1 до 150
                        p - отправить фразу
                        w+ - интегрировать кошелёк в сообщение) : """)
            while True:
                interval = input("Задержка (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            sessions = [session for session in load_sessions() if session["isActive"]]
            used_numbers = []
            if message == "w+":
                extra_text = input("Введите сообщение: ")
            for session in sessions:
                try:
                    client = TelegramClient(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    client.connect()
                    chat = client.get_entity(chat_link)
                    join_public_channel(client, chat_link)
                    if message == "":
                        message = choice(("*", "d"))
                    if message == "#":
                        message_unique = input("Введите сообщение: ")
                        client.send_message(chat, message_unique)
                    elif message == "*":
                        client.send_message(chat, "@" + client.get_me().username)
                    elif message == "d":
                        client.send_message(chat, choice(done_templates))
                    elif message == "w":
                        client.send_message(chat, session["doneTemplate"])
                    elif message == "p":
                        client.send_message(chat, choice(phrases))
                    elif message == "n":
                        number = randint(1, 150)
                        while number in used_numbers:
                            number = randint(1, 150)
                        client.send_message(chat, str(number))
                        used_numbers.append(number)
                    elif message == "w+":
                        client.send_message(chat, session["doneTemplate"] + " " + extra_text)
                    else:
                        client.send_message(chat, message)
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ + СООБЩЕНИЕ - УСПЕШНО")
                except Exception as ex:
                    print(f"{session['USERNAME']}: ВСТУПЛЕНИЕ + СООБЩЕНИЕ - ОШИБКА!")
                    print(ex)
                pause = randint(min_s, max_s)
                sleep(pause)
        case "9":
            with open("active_sessions.json", "r") as file:
                data_loaded = loads(file.read())
            for index, session in enumerate(data_loaded, start=1):
                print(Fore.RESET + str(index), end=". ")
                if session["isActive"]:
                    print(Fore.GREEN + "АКТИВЕН", end=Fore.RESET + " Имя пользователя: ")
                else:
                    print(Fore.RED + "НЕ АКТИВЕН", end=Fore.RESET + " Имя пользователя: ")
                print(session["USERNAME"])
            while True:
                try:
                    session_index = int(input(Fore.BLUE + "Выберите номер аккаунта для взаимодействия: ")) - 1
                    session = data_loaded[session_index]
                    break
                except ValueError:
                    print("Введите число!")
            while True:
                action = input(
                    f"Выбран аккаунт: {session['USERNAME']}\n" + Fore.GREEN + "Меню:\n1.Установить шаблон done\n2.Удалить сессию\n3.Отключить сессию\n4.Включить сессию\nВыберите действие: "
                )
                if action == "1":
                    done_template = input("Введите шаблон done: ")
                    session["doneTemplate"] = done_template
                    data_loaded[session_index] = session
                    with open("active_sessions.json", "w") as file:
                        file.write(dumps(data_loaded, sort_keys=True, indent=4))
                    break
                elif action == "2":
                    data_loaded.pop(session_index)
                    with open("active_sessions.json", "w") as file:
                        file.write(dumps(data_loaded, sort_keys=True, indent=4))
                    break
                elif action == "3":
                    session["isActive"] = False
                    data_loaded[session_index] = session
                    with open("active_sessions.json", "w") as file:
                        file.write(dumps(data_loaded, sort_keys=True, indent=4))
                    break
                elif action == "4":
                    session["isActive"] = True
                    data_loaded[session_index] = session
                    with open("active_sessions.json", "w") as file:
                        file.write(dumps(data_loaded, sort_keys=True, indent=4))
                    break
        case "0":
            post_link = input("Введите ссылку на пост: ")
            message = input(
                """Введите текст сообщения (Пустая строка - рандом из списка
                        # - ввести от каждого аккаунта вручную
                        * - отправить юзернейм аккаунта
                        d - отправить шаблон done
                        w - отправить кошелёк
                        n - отправить рандомное число от 1 до 150
                        p - отправить фразу
                        w+ - интегрировать кошелёк в сообщение) : """)
            sessions = [session for session in load_sessions() if session["isActive"]]
            tasks = []
            used_numbers = []
            if message == "w+":
                extra_text = input("Введите сообщение: ")
            for session in sessions:
                try:
                    client = TelegramClientAsync(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"]
                    )
                    if message == "":
                        message = choice(("*", "d"))
                    if message == "#":
                        message_unique = input("Введите сообщение: ")
                        tasks.append(join_and_comment_post_async(client, post_link, message_unique))
                    elif message == "*":
                        tasks.append(join_and_comment_post_async(client, post_link, session["USERNAME"]))
                    elif message == "d":
                        tasks.append(join_and_comment_post_async(client, post_link, choice(done_templates)))
                    elif message == "w":
                        tasks.append(join_and_comment_post_async(client, post_link, session["doneTemplate"]))
                    elif message == "p":
                        tasks.append(join_and_comment_post_async(client, post_link, choice(phrases)))
                    elif message == "n":
                        number = randint(1, 150)
                        while number in used_numbers:
                            number = randint(1, 150)
                        tasks.append(join_and_comment_post_async(client, post_link, str(number)))
                        used_numbers.append(number)
                    elif message == "w+":
                        tasks.append(join_and_comment_post_async(client, post_link, session["doneTemplate"] + " " + extra_text))
                    else:
                        tasks.append(join_and_comment_post_async(client, post_link, message))
                except Exception:
                    print("ВСТУПЛЕНИЕ + КОММЕНТАРИЙ - ОШИБКА!")
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(gather_loop(tasks))
            except Exception:
                print("ВСТУПЛЕНИЕ + КОММЕНТАРИЙ - ОШИБКА!")
        case "00":
            while True:
                interval = input("Задержка между сообщениями (сек) (! - установить интервал): ")
                if interval == "!":
                    try:
                        min_s = int(input("Нижний порог: "))
                        max_s = int(input("Верхний порог: "))
                        break
                    except ValueError:
                        print("Введите число!")
                elif interval == "":
                    interval = 0
                    min_s = max_s = interval
                    break
                else:
                    try:
                        interval = int(interval)
                        min_s = max_s = interval
                        break
                    except ValueError:
                        print("Введите число!")
            while True:
                stickers_count = input("Количество стикеров: ")
                if stickers_count == "":
                    stickers_count = 1
                    break
                else:
                    try:
                        stickers_count = int(stickers_count)
                        break
                    except ValueError:
                        print("Введите число!")
            while True:
                sticker = input("""Вид стикера (Пустая строка - слоты
            1 - кубик
            2 - баскетбол
            3 - боулинг
            4 - футбол
            5 - дартс): """)
                stickers_dict = {
                    "": "🎰",
                    "1": "🎲",
                    "2": "🏀",
                    "3": "🎳",
                    "4": "⚽",
                    "5": "🎯"
                }
                if sticker in stickers_dict:
                    break
            post_link = input("Ссылка на пост: ")
            sessions = [session for session in load_sessions() if session["isActive"]]
            tasks = []
            for session in sessions:
                try:
                    client = TelegramClientAsync(
                        StringSession(session["ID_SESSION"]), session["API_ID"], session["API_HASH"])
                    tasks.append(join_and_send_sticker(
                        client, post_link, stickers_dict[sticker], stickers_count, interval
                    ))
                except Exception:
                    pass
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(gather_loop(tasks))
            except Exception as ex:
                print("ВСТУПЛЕНИЕ + СТИКЕР - ОШИБКА!")
