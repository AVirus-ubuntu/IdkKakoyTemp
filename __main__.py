import logging
import telebot # type: ignore
import sqlite3
import time as tm
import datetime as dt
from time import sleep, strftime

from __config__ import cfg # type: ignore
from __func__ import func # type: ignore
from __banners__ import banners # type: ignore


logging.basicConfig(filename='logs/info.log', level=logging.INFO)

print(f'{banners.b1}')

def pingedbot(msg):
    if msg.reply_to_message == None:
        return True
    elif msg.reply_to_message != None:
        if msg.reply_to_message.from_user.is_bot == True:
            return False
        elif msg.reply_to_message.from_user.is_bot == False:
            return True

bot = telebot.TeleBot(cfg.token)

@bot.message_handler(content_types=['text'])
def getmessage(message):
    if message.from_user.is_bot == False and pingedbot(msg=message):
        connection = sqlite3.connect(cfg.database)
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        bal1 REAL,
        bal2 REAL,
        bal3 REAL,
        username TEXT,
        banned INTEGER,
        bannedres TEXT
        )
        ''')


        ultradata = cursor.execute(f'''
        SELECT banned FROM Users WHERE id = {message.from_user.id}
        ''').fetchone()

        if ultradata == None:
            # bot.send_message(message.chat.id, f'Тип, зарегайся лучше,\nтебя нету в базе нашей\nтыкни здесь <i>/start</i>', parse_mode="html")
            info = [message.from_user.id, 0, 0, 0, message.from_user.username, 0, 'NULL']
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?);', info)
            connection.commit()
            
            ultradata = cursor.execute(f'''
            SELECT banned FROM Users WHERE id = {message.from_user.id}
            ''').fetchone()

        elif ultradata[0] == 0:
            if message.text == '/start':
                bot.send_message(message.chat.id, f'Ку, я бот который не работает!\nпиши `/help`', parse_mode="Markdown")

                cursor.execute(f'SELECT id FROM Users WHERE id = {message.from_user.id}')
                data = cursor.fetchone()
                if data is None:
                    info = [message.from_user.id, 0, 0, 0, message.from_user.username, 0, 'NULL']
                    cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?);', info)
                    connection.commit()
            
            elif message.text == '/start@MneSkusnaaaabot':
                cursor.execute(f'SELECT id FROM Users WHERE id = {message.from_user.id}')
                data = cursor.fetchone()
                if data is None:
                    info = [message.from_user.id, 0, 0, 0, message.from_user.username]
                    cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?);', info)
                    connection.commit()
                
                bot.send_message(message.chat.id, f'Ку, я бот который не работает!\nпиши `Хто я?`', parse_mode="Markdown")

            elif message.text == '/help':
                bot.send_message(message.chat.id, f'ну типа команды (клик = копи)\n\n`передать1 <скока>`, `передать2 <скока>`, `передать3 <скока>`,\n`скока у меня`', parse_mode="Markdown")
                if strftime('%m-%d') == '09-15':
                    bot.send_message(message.chat.id, f'Кстати\nТы уже поздравил этот чат с днем рождения?\nНет???\nТогда скорей беги поздравлять,\nЭтот ботик уже поздравил в другом месте :)', parse_mode="Markdown")
            
                
            elif message.text == '/help@MneSkusnaaaabot':
                bot.send_message(message.chat.id, f'ну типа команды (клик = копи)\n\n`передать1 <скока>`, `передать2 <скока>`, `передать3 <скока>`,\n`скока у меня`', parse_mode="Markdown")
                if strftime('%m-%d') == '09-15':
                    bot.send_message(message.chat.id, f'Кстати\nТы уже поздравил этот чат с днем рождения?\nНет???\nТогда скорей беги поздравлять,\nЭтот ботик уже поздравил в другом месте :)', parse_mode="Markdown")            
            
            elif message.text == '/credits':

                bot.send_message(message.chat.id, f'О, кому-то интерестно!\nНу лан кароч создатель бота [ТУТ](t.me/ANTIVIRUSNIY_GUS)', parse_mode='Markdown')
            elif message.text == '/credits@MneSkusnaaaabot':
                bot.send_message(message.chat.id, f'О, кому-то интерестно!\nНу лан кароч создатель бота [ТУТ](t.me/ANTIVIRUSNIY_GUS)', parse_mode='Markdown')

            elif message.text.lower() == 'скока у меня':
                data1 = cursor.execute(f'SELECT bal1 FROM Users WHERE id = {message.from_user.id}').fetchone()
                data2 = cursor.execute(f'SELECT bal2 FROM Users WHERE id = {message.from_user.id}').fetchone()
                data3 = cursor.execute(f'SELECT bal3 FROM Users WHERE id = {message.from_user.id}').fetchone()
                
                if data1[0] == None:
                    bot.send_message(message.chat.id, 'Ты не зареган в боте напиши /start в личку боте, так ты зарегаешься')
                if data1[0] != None:
                    bot.send_message(message.chat.id, f'ну... может...\n{data1[0]}💵, {data2[0]}💶, {data3[0]}💷')

                # message.reply_to_message
                    
            


            
            elif message.text.lower()[0:10] == 'передать1 ':
                if message.reply_to_message == None:
                    bot.send_message(message.chat.id, 'Надо кому-то передавать')
                elif message.reply_to_message != None:
                    if message.reply_to_message.from_user.is_bot:
                        bot.send_message(message.chat.id, 'Жаль что боту передать нельзя :(')
                    elif not message.reply_to_message.from_user.is_bot:
                        cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                        data = cursor.fetchone()

                        if data[0] == None:
                            bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации напишите\n/start боту в личные сообщения\n:(')
                        elif data[0] != None:
                            cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                            data = cursor.fetchone()

                            if data[0] == None:
                                bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации, попросите его написать\n/start боту в личные сообщения\n:(')
                            elif data[0] != None:
                                cursor.execute(f'SELECT bal1 FROM Users WHERE id = {message.from_user.id}')
                                data = cursor.fetchone()

                                try:
                                    if float(message.text.split(' ', maxsplit = 1)[1]) >= 0:
                                        if data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            
                                            info = [float(message.text.split(' ', maxsplit = 1)[1])]

                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal1 = bal1 + {info[0]}
                                            WHERE id = {message.reply_to_message.from_user.id};
                                            """)
                                            connection.commit()
                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal1 = bal1 - {info[0]}
                                            WHERE id = {message.from_user.id};
                                            """)
                                            connection.commit()
                                            
                                            bot.send_message(message.chat.id, f'Вроде передал, у тебя осталось: {cursor.execute(f"SELECT bal1 FROM Users WHERE id = {message.from_user.id}").fetchone()[0]}')

                                        elif not data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            bot.send_message(message.chat.id, 'Ну вроде, у тебя сток нету')
                                    elif float(message.text.split(' ', maxsplit = 1)[1]) < 0:
                                        bot.send_message(message.chat.id, 'Так низя вапщета')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float: '):
                                        bot.send_message(message.chat.id, 'Это не число)')
            elif message.text.lower()[0:10] == 'передать2 ':
                if message.reply_to_message == None:
                    bot.send_message(message.chat.id, 'Надо кому-то передавать')
                elif message.reply_to_message != None:
                    if message.reply_to_message.from_user.is_bot:
                        bot.send_message(message.chat.id, 'Жаль что боту передать нельзя :(')
                    elif not message.reply_to_message.from_user.is_bot:
                        cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                        data = cursor.fetchone()

                        if data[0] == None:
                            bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации напишите\n/start боту в личные сообщения\n:(')
                        elif data[0] != None:
                            cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                            data = cursor.fetchone()

                            if data[0] == None:
                                bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации, попросите его написать\n/start боту в личные сообщения\n:(')
                            elif data[0] != None:
                                cursor.execute(f'SELECT bal2 FROM Users WHERE id = {message.from_user.id}')
                                data = cursor.fetchone()

                                try:
                                    if float(message.text.split(' ', maxsplit = 1)[1]) >= 0:
                                        if data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            
                                            info = [float(message.text.split(' ', maxsplit = 1)[1])]

                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal2 = bal2 + {info[0]}
                                            WHERE id = {message.reply_to_message.from_user.id};
                                            """)
                                            connection.commit()
                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal2 = bal2 - {info[0]}
                                            WHERE id = {message.from_user.id};
                                            """)
                                            connection.commit()
                                            
                                            bot.send_message(message.chat.id, f'Вроде передал, у тебя осталось: {cursor.execute(f"SELECT bal2 FROM Users WHERE id = {message.from_user.id}").fetchone()[0]}')

                                        elif not data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            bot.send_message(message.chat.id, 'Ну вроде, у тебя сток нету')
                                    elif float(message.text.split(' ', maxsplit = 1)[1]) < 0:
                                        bot.send_message(message.chat.id, 'Так низя вапщета')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float: '):
                                        bot.send_message(message.chat.id, 'Это не число)')

            elif message.text.lower()[0:10] == 'передать3 ':
                if message.reply_to_message == None:
                    bot.send_message(message.chat.id, 'Надо кому-то передавать')
                elif message.reply_to_message != None:
                    if message.reply_to_message.from_user.is_bot:
                        bot.send_message(message.chat.id, 'Жаль что боту передать нельзя :(')
                    elif not message.reply_to_message.from_user.is_bot:
                        cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                        data = cursor.fetchone()

                        if data[0] == None:
                            bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации напишите\n/start боту в личные сообщения\n:(')
                        elif data[0] != None:
                            cursor.execute(f'SELECT id FROM Users WHERE id = {message.reply_to_message.from_user.id}')
                            data = cursor.fetchone()

                            if data[0] == None:
                                bot.send_message(message.chat.id, f'Бот не зарегестрирован в этом боте\nДля регистрации, попросите его написать\n/start боту в личные сообщения\n:(')
                            elif data[0] != None:
                                cursor.execute(f'SELECT bal3 FROM Users WHERE id = {message.from_user.id}')
                                data = cursor.fetchone()

                                try:
                                    if float(message.text.split(' ', maxsplit = 1)[1]) >= 0:
                                        if data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            
                                            info = [float(message.text.split(' ', maxsplit = 1)[1])]

                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal3 = bal3 + {info[0]}
                                            WHERE id = {message.reply_to_message.from_user.id};
                                            """)
                                            connection.commit()
                                            cursor.execute(f"""
                                            UPDATE Users
                                            SET bal3 = bal3 - {info[0]}
                                            WHERE id = {message.from_user.id};
                                            """)
                                            connection.commit()
                                            
                                            bot.send_message(message.chat.id, f'Вроде передал, у тебя осталось: {cursor.execute(f"SELECT bal3 FROM Users WHERE id = {message.from_user.id}").fetchone()[0]}')

                                        elif not data[0] >= float(message.text.split(' ', maxsplit = 1)[1]):
                                            bot.send_message(message.chat.id, 'Ну вроде, у тебя сток нету')
                                    elif float(message.text.split(' ', maxsplit = 1)[1]) < 0:
                                        bot.send_message(message.chat.id, 'Так низя вапщета')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float: '):
                                        bot.send_message(message.chat.id, 'Это не число)')

            elif message.text.lower()[0:14] == 'халяваbyадмин ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    try:
                        info = [float(message.text.split(' ', maxsplit = 1)[1])]
                        cursor.execute(f"""
                        UPDATE Users
                        SET bal1 = bal1 + {info[0]}
                        WHERE id = {message.from_user.id};
                        """)
                        cursor.execute(f"""
                        UPDATE Users
                        SET bal2 = bal2 + {info[0]}
                        WHERE id = {message.from_user.id};
                        """)
                        cursor.execute(f"""
                        UPDATE Users
                        SET bal3 = bal3 + {info[0]}
                        WHERE id = {message.from_user.id};
                        """)
                        connection.commit()

                        bot.send_message(message.chat.id, 'Гарри поттер наколдавал халяву!\nПолучить ее можно за актив)')
                    except Exception as e:
                        if str(e).startswith('could not convert string to float: '):
                            bot.send_message(message.chat.id, 'Это не число кста')
                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')
                

            elif message.text.lower()[0:8] == 'чеквал @':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    data1 = cursor.execute(f'SELECT bal1 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1]}"').fetchone()
                    data2 = cursor.execute(f'SELECT bal2 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1]}"').fetchone()
                    data3 = cursor.execute(f'SELECT bal3 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1]}"').fetchone()


                    if len(message.text.split(' ', maxsplit = 1)) == 2:

                        if data1[0] == None:
                            
                            bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                        elif data1[0] != None:

                            bot.send_message(message.chat.id, f'Ну типа там:\n{data1[0]}💵, {data2[0]}💶, {data3[0]}💷')
                            
                    else:
                        ...

                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')
                    
            elif message.text.lower()[0:8] == 'аддвал1 ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data1 = cursor.execute(f'SELECT bal1 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                        if c:
                            if data1 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data1[0] != None:
                                
                                try:
                                    cursor.execute(f'''
                                    UPDATE Users
                                    SET bal1 = bal1 + {float(message.text.split(' ', maxsplit = 2)[2])}
                                    WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                    ''')
                                    connection.commit()

                                    bot.send_message(message.chat.id, f'Пополнил, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')

                    else:
                        bot.send_message(message.chat.id, f'Тип че-т забыл')
                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')

            elif message.text.lower()[0:8] == 'аддвал2 ':            
                
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data2 = cursor.execute(f'SELECT bal2 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                            
                        if c:
                            if data2 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data2[0] != None:
                                
                                try:
                                    cursor.execute(f'''
                                    UPDATE Users
                                    SET bal2 = bal2 + {float(message.text.split(' ', maxsplit = 2)[2])}
                                    WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                    ''')
                                    connection.commit()

                                    bot.send_message(message.chat.id, f'Пополнил, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')

                                
                    else:
                        bot.send_message(message.chat.id, f'Тип че-т забыл')
                
                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')
            elif message.text.lower()[0:8] == 'аддвал3 ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data3 = cursor.execute(f'SELECT bal3 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                        if c:
                            if data3 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data3[0] != None:
                                
                                try:
                                    cursor.execute(f'''
                                    UPDATE Users
                                    SET bal3 = bal3 + {float(message.text.split(' ', maxsplit = 2)[2])}
                                    WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                    ''')
                                    connection.commit()

                                    bot.send_message(message.chat.id, f'Пополнил, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')

                                
                    else:
                        bot.send_message(message.chat.id, f'Тип че-т забыл')

                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')
                    
                
            elif message.text.lower()[0:8] == 'ремвал1 ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data1 = cursor.execute(f'SELECT bal1 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                        if c:
                            if data1 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data1[0] != None:
                                
                                try:
                                    data1 = cursor.execute(f'SELECT bal1 FROM Users WHERE username = "{message.text.split(" ", maxsplit = 2)[1][1:]}"').fetchone()[0]
                                    if data1 < float(message.text.split(' ', maxsplit = 2)[2]):
                                        bot.send_message(message.chat.id, 'У типа столько нету :(')
                                    elif data1 >= float(message.text.split(' ', maxsplit = 2)[2]):
                                        cursor.execute(f'''
                                        UPDATE Users
                                        SET bal1 = bal1 - {float(message.text.split(' ', maxsplit = 2)[2])}
                                        WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                        ''')
                                        connection.commit()

                                        bot.send_message(message.chat.id, f'Сп#зд#л, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')

            elif message.text.lower()[0:8] == 'ремвал2 ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data2 = cursor.execute(f'SELECT bal2 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                        if c:
                            if data2 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data2[0] != None:
                                
                                try:
                                    data2 = cursor.execute(f'SELECT bal2 FROM Users WHERE username = "{message.text.split(" ", maxsplit = 2)[1][1:]}"').fetchone()[0]
                                    if data2 < float(message.text.split(' ', maxsplit = 2)[2]):
                                        bot.send_message(message.chat.id, 'У типа столько нету :(')
                                    elif data2 >= float(message.text.split(' ', maxsplit = 2)[2]):
                                        cursor.execute(f'''
                                        UPDATE Users
                                        SET bal2 = bal2 - {float(message.text.split(' ', maxsplit = 2)[2])}
                                        WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                        ''')
                                        connection.commit()

                                        bot.send_message(message.chat.id, f'Сп#зд#л, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')
                    
            elif message.text.lower()[0:8] == 'ремвал3 ':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit = 2)) == 3:
                        c = True
                        try:
                            data3 = cursor.execute(f'SELECT bal3 FROM Users WHERE username = "{message.text.split(" @", maxsplit = 1)[1].split(" ", maxsplit=1)[0]}"').fetchone()
                        except Exception as e:
                            if str(e) == ('list index out of range'):
                                bot.send_message(message.chat.id, 'Ты забыл аргументы указать')
                                c = False
                        if c:
                            if data3 == None:
                                
                                bot.send_message(message.chat.id, f'К сожалению либо я лох либо тип в боте не зареган\n:(')

                            elif data3[0] != None:
                                
                                try:
                                    data3 = cursor.execute(f'SELECT bal3 FROM Users WHERE username = "{message.text.split(" ", maxsplit = 2)[1][1:]}"').fetchone()[0]
                                    if data3 < float(message.text.split(' ', maxsplit = 2)[2]):
                                        bot.send_message(message.chat.id, 'У типа столько нету :(')
                                    elif data3 >= float(message.text.split(' ', maxsplit = 2)[2]):
                                        cursor.execute(f'''
                                        UPDATE Users
                                        SET bal3 = bal3 - {float(message.text.split(' ', maxsplit = 2)[2])}
                                        WHERE username = "{message.text.split(' ', maxsplit = 2)[1][1:]}";
                                        ''')
                                        connection.commit()

                                        bot.send_message(message.chat.id, f'Сп#зд#л, если надо чекни')
                                except Exception as e:
                                    if str(e).startswith('could not convert string to float:'):
                                        bot.send_message(message.chat.id, 'Че-то тут не то')
                                        

                                
                    else:
                        bot.send_message(message.chat.id, f'Тип че-т забыл')
                elif not b:
                        bot.send_message(message.chat.id, 'Крыса, тебе низя')

            elif message.text.lower() == 'админкмд':
                    
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    bot.send_message(message.chat.id, 'Это список команд админов,\n$ это 1, 2, 3 - валюта,\n(клик = копи)\n\n`админкмд`, `аддвал$`, `ремвал$`, `чеквал$` `халяваbyадмин`', parse_mode='Markdown')
                    
                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')
            
            elif message.text.lower()[0:5] == 'банан':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if len(message.text.split(' ', maxsplit=1)) == 1:
                        bot.send_message(message.chat.id, 'Ну причина какааааая???')
                    elif len(message.text.split(' ', maxsplit=1)) == 2:
                        if message.reply_to_message == None:
                            bot.send_message(message.chat.id, 'Забыл типа пнуть)')
                        elif message.reply_to_message != None:
                            data0 = cursor.execute(f'SELECT banned FROM Users WHERE id = {message.reply_to_message.from_user.id}').fetchone()
                            if data0 == None:
                                bot.send_message(message.chat.id, 'Типа такого нету')
                            elif data0[0] != None:
                                if data0[0] == 0:
                                    cursor.execute(f'UPDATE Users SET banned = 1 WHERE id = {message.reply_to_message.from_user.id}')
                                    cursor.execute(f'UPDATE Users SET bannedres = "{message.text.split(" ", maxsplit=1)[1]}" WHERE id = {message.reply_to_message.from_user.id}')
                                    bot.send_message(message.chat.id, f'Тип был забанен в боте по причине\n<i>{cursor.execute(f"SELECT bannedres FROM Users WHERE id = {message.reply_to_message.from_user.id}").fetchone()[0]}</i>', parse_mode='html')
                                elif data0[0] == 1:
                                    bot.send_message(message.chat.id, f'Тип уже забанен по причине\n<i>{cursor.execute(f"SELECT bannedres FROM Users WHERE id = {message.reply_to_message.from_user.id}").fetchone()[0]}</i>', parse_mode='html')
            elif message.text.lower() == 'анбанан':
                b = False
                for x in cfg.admins:
                    if x == message.from_user.id:
                        b = True
                if b:
                    if message.reply_to_message == None:
                        bot.send_message(message.chat.id, 'Забыл типа пнуть)')
                    elif message.reply_to_message != None:
                        data0 = cursor.execute(f'SELECT banned FROM Users WHERE id = {message.reply_to_message.from_user.id}').fetchone()
                        if data0 == None:
                            bot.send_message(message.chat.id, 'Типа такого нету')
                        elif data0[0] != None:
                            if data0[0] == 1:
                                bot.send_message(message.chat.id, f'Тип был разбанен в боте по причине\n<i>{cursor.execute(f"SELECT bannedres FROM Users WHERE id = {message.reply_to_message.from_user.id}").fetchone()[0]}</i>', parse_mode='html')
                                cursor.execute(f'UPDATE Users SET banned = 0 WHERE id = {message.reply_to_message.from_user.id}')
                                cursor.execute(f'UPDATE Users SET bannedres = "NULL" WHERE id = {message.reply_to_message.from_user.id}')
                            elif data0[0] == 0:
                                bot.send_message(message.chat.id, 'Тип не забанен')

                elif not b:
                    bot.send_message(message.chat.id, 'Крыса, тебе низя')



        elif ultradata[0] == 1:
            if message.text.lower() == 'банинфо':
                bot.send_message(message.chat.id, f'Чувачок забанен\nОписание: <i>{cursor.execute(f"SELECT bannedres FROM Users WHERE id = {message.from_user.id}").fetchone()[0]}</i>', parse_mode="html")
        connection.commit()
        connection.close()

# bot.infinity_polling(none_stop=True)

while True:
    try:
        bot.infinity_polling(none_stop=True, interval=0)
    except Exception as e: ...