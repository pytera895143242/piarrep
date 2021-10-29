import sqlite3
import time

def bot_start(chat_id,invite_link,name_channel):

    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_to200 (
        number_channel,
        chat_id_channel,
        invite_link,
        count_member,
        name_channel
        ) """)
    db.commit()

    sql.execute(f"SELECT chat_id_channel FROM channel_to200 WHERE chat_id_channel = {chat_id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_to200 VALUES (?,?,?,?,?)", (1,chat_id,invite_link,1,name_channel)) #Добавили дефолтный канал
        db.commit()

    # Теперь создаем таблицу list_settings - с общими настройками бота
    sql.execute(""" CREATE TABLE IF NOT EXISTS list_settings (
            name_function,
            value_function
            ) """)

    # Записываем базовые настройки скрипта
    sql.execute(f"SELECT name_function FROM list_settings WHERE name_function ='id_prok'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO list_settings VALUES (?,?)",('id_prok','-1001522287903')) #Id прокладки (куда гоним траф)
        sql.execute(f"INSERT INTO list_settings VALUES (?,?)",('message_post_id', '53'))  #id редактируемого поста
        sql.execute(f"INSERT INTO list_settings VALUES (?,?)", ('my_id', '1913298990'))  # Мой id
        sql.execute(f"INSERT INTO list_settings VALUES (?,?)", ('text_post', '<b>ФУЛЛ С РЕКЛАМЫ ТУТ👇</b>\n\n{}'))  # Текст рекламного поста
        db.commit()

    db.commit()


def chach_actuale_date():
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    #Собираем актуальные данные
    chat_id = (sql.execute(f"SELECT chat_id_channel FROM channel_to200").fetchall())[-1][0] #Актуальный заливной чат
    number_channel = (sql.execute(f"SELECT number_channel FROM channel_to200").fetchall())[-1][0] #Номер заливного чата
    invite_link = (sql.execute(f"SELECT invite_link FROM channel_to200").fetchall())[-1][0]  #Ссылка на заливной чат

    message_id = (sql.execute(f"SELECT value_function FROM list_settings WHERE name_function = 'message_post_id'").fetchall())[0][0] # Номер Поста для редактирования
    text_post = (sql.execute(f"SELECT value_function FROM list_settings WHERE name_function = 'text_post'").fetchall())[0][0] #Текст поста для редактирования
    id_prok = (sql.execute(f"SELECT value_function FROM list_settings WHERE name_function = 'id_prok'").fetchall())[0][0] #Id прокладки (куда гоним траф)

    return [chat_id,number_channel,message_id,text_post,id_prok,invite_link]

def reg_channel(number_channel,chat_id_channel,invite_link,count_member,name_channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT chat_id_channel FROM channel_to200 WHERE chat_id_channel = {chat_id_channel}")
    if sql.fetchone() is None: #Защита от повторной регистрации
        sql.execute(f"INSERT INTO channel_to200 VALUES (?,?,?,?,?)",(number_channel+1, chat_id_channel, invite_link, 1, name_channel))  # Добавиляем новый канал в базу данный
        db.commit()