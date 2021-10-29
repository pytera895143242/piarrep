from pyrogram import Client
from pyrogram import filters
from pyrogram import types
import sqlite3
import time
import random
import asyncio
from sqlit import bot_start,chach_actuale_date,reg_channel
from config import content,names_channels,captions,link_for_caption,avatarka_for_channel
from config import bot_id  #ID бота для управления
from config import content_channel
app = Client('my_accounts')

bot_start(chat_id = -1001781011152, invite_link = 'https://t.me/joinchat/RD8miEtPh1gwMWFi', name_channel= 'Дефолтный канал') #Для первого запуска


async def proverka():
    await asyncio.sleep(6)  # Время на запуск программы
    print('Скрипт начал свою работу')

    try:
        chat_id, number_channel, message_id, text_post, id_prok,link_chat = chach_actuale_date()  # Собирает начальные данные
        await app.edit_message_text(chat_id= int(id_prok), message_id = int(message_id), text=(text_post.format(link_chat)),parse_mode='html')  # Редактируем пост в прокладке
    except:
        pass

    while True:
        chat_id, number_channel, message_id, text_post, id_prok,invite = chach_actuale_date() #Собирает актуальные данные
        await asyncio.sleep(10)

        count_member = int((await app.get_chat(chat_id)).members_count)#Количество пользователей
        await asyncio.sleep(13)

        if count_member > 200:
            pass
        elif count_member > 190: #1 минуту
            await asyncio.sleep(60)
        elif count_member > 150: #4 минут
            await asyncio.sleep(60*4)
        elif count_member > 125: #7 минут
            await asyncio.sleep(60*7)
        elif count_member > 75: #10 минуты
            await asyncio.sleep(60*10)
        else: #15 минут
            await asyncio.sleep(60*15)

        if count_member > 200: #Если в послденем чате больше 200 человек, то создаем новый
            print(f'В чате Больше 2 человек. Нужно создать новый')
            name = names_channels[number_channel]#Достаем название

            #Работа с новым каналом
            a = await app.create_channel(title=name)#Создаем канал с названием - name
            await asyncio.sleep(10)

            link_chat = await app.export_chat_invite_link(a.id) #Генерируем новую ссылку
            await asyncio.sleep(10)

            await app.set_chat_photo(chat_id=a.id, photo=random.choice(avatarka_for_channel))  # Устанавливаем аватарку
            await app.delete_messages(chat_id=a.id,message_ids = 2)#Удаляем сообщение где установлена аватарка
            await app.promote_chat_member(chat_id=a.id, user_id=bot_id, can_manage_chat=True, can_change_info=True,
                                              can_post_messages=True, can_edit_messages=True, can_delete_messages=True,
                                              can_restrict_members=True, can_invite_users=True, can_pin_messages=True,
                                              can_manage_voice_chats=True)

            for i in range(4,22):
                await app.copy_message(chat_id=a.id, from_chat_id=content_channel, message_id=i, caption = (random.choice(captions)).format(link_for_caption),parse_mode='html')


            #Работа с прокладкой
            await app.edit_message_text(chat_id=int(id_prok), message_id=int(message_id),text = text_post.format(link_chat),parse_mode='html') #Редактируем пост в прокладке
            await asyncio.sleep(10)

            reg_channel(number_channel = number_channel, chat_id_channel = a.id,invite_link = link_chat,count_member = 1 ,name_channel = name) #Вносим данные о нровом канале, для регистрации в бд
            print('Изменения завершены')





@app.on_message(filters.text)
async def payments (client,message):
    # try:
    #     print(message.reply_to_message.photo.file_id)
    # except:
    #     pass
    #  print(message)


    if (message.text  == 'База'):
         await app.send_document(document=(open("server.db", "rb")),chat_id=message.chat.id)
#
#     elif (message.text[0:3] =='Инф' and message.from_user.id == my_id):
#         q = (await app.get_chat(chat_one_id)).members_count
#         print(q)
#
#     elif (message.text[0:3] == 'Соз' and message.from_user.id == my_id):
#         number_name = len(list_chat)
#         print(number_name)
#         a = await app.create_channel(title=name_channel[number_name])
#
#     elif (message.text[0:3] == 'Чат' and message.from_user.id == my_id):
#         print(' ')
#         print('Актуальный список чатов:')
#         for c in list_chat:
#             print(f'Канал: {c[1]}, количество участников: {(await app.get_chat(c[0])).members_count}')
#             await asyncio.sleep(5)
#
#
#
# if (message.text[0:2] =='Рекдавтирую' and message.from_user.id == my_id):
#         if message.text[0:18] == 'Добавь прокладку @':
#             id_user = message.chat.id
#             user_channel = message.text[19:]
#
#             try:
#                 a = await app.create_channel(title=message.chat.first_name)
#                 await app.send_message(chat_id=a.id, text=f"""<b>Фильмы 2021 скрыты от посторонних глаз. И доступны на приватном канале по ссылке ниже. Заходи и следуй инструкции</b>
#
# <a href = https://t.me/MovieAndSerialsBot?start={user_channel}>🍿НАЧАТЬ СМОТРЕТЬ🍿</a>""")
#
#                 await app.add_chat_members(chat_id=a.id, user_ids=id_user)
#                 await app.promote_chat_member(chat_id=a.id, user_id=id_user, can_manage_chat=True, can_change_info=True,
#                                               can_post_messages=True, can_edit_messages=True, can_delete_messages=True,
#                                               can_restrict_members=True, can_invite_users=True, can_pin_messages=True,
#                                               can_manage_voice_chats=True)
#
#                 url = await app.export_chat_invite_link(chat_id=a.id)
#                 await asyncio.sleep(3)
#
#                 await app.send_message(chat_id=message.chat.id, text=f"""Это прокладка:
# {url}
#
# В дальнейшем используешь только эту ссылку. Ты админ в этом канале, поменяй аву и имя канала. Имя используй такое же как и в основном тг канале с фильмами.""")
#
#             except:
#                 await app.send_message(chat_id=message.chat.id, text="""Не могу создать тебе прокладку и добавить тебя туда.
#
# Что бы это исправить переходи в настройки, нажимай
#
#     - Конфидециальность
#     - Группы и каналы
# И добавь меня в список тех, кто тебя может приглашать в группы
#
# После этого напиши мне и мы повторим попытку""")
#         else:
#             try:
#                 id_user = message.chat.id
#                 user_channel = message.text[4:]
#
#
#                 a = await app.create_channel(title=message.chat.first_name)
#                 await app.send_message(chat_id=a.id,text=f"""<b>Фильмы 2021 скрыты от посторонних глаз. И доступны на приватном канале по ссылке ниже. Заходи и следуй инструкции</b>
#
#     <a href = https://t.me/MovieAndSerialsBot?start={user_channel}>🍿НАЧАТЬ СМОТРЕТЬ🍿</a>""",disable_web_page_preview=True)
#
#                 await app.add_chat_members(chat_id=a.id,user_ids= id_user)
#                 await app.promote_chat_member(chat_id=a.id,user_id=id_user,can_manage_chat= True,can_change_info= True,can_post_messages = True, can_edit_messages= True, can_delete_messages = True, can_restrict_members= True,can_invite_users = True, can_pin_messages = True,can_manage_voice_chats = True)
#
#                 url = await app.export_chat_invite_link(chat_id=a.id)
#                 await asyncio.sleep(3)
#
#                 await app.send_message(chat_id=message.chat.id,text=f"""Это прокладка:\n{url}
#
# В дальнейшем используешь только эту ссылку. Ты админ в этом канале, поменяй аву и имя канала. Имя используй такое же как и в основном тг канале с фильмами.""")
#
#             except:
#                 await app.send_message(chat_id=message.chat.id,text="""Не могу создать тебе прокладку и добавить тебя туда.
#
# Что бы это исправить переходи в настройки, нажимай
#
#     - Конфидециальность
#     - Группы и каналы
# И добавь меня в список тех, кто тебя может приглашать в группы
#
# После этого напиши мне и мы повторим попытку""")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(proverka())
    app.run()