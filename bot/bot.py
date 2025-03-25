import time
from aiogram import Bot, Dispatcher, executor, types
import logging
import requests
import json


TOKEN = "5972829355:AAELHvOhYhBO5KdjVHS3V4rcWNwtQMhaLRs"
MSG = "My first message в Telegram"

ID_LEON = '1048545758'
ID_ADMIN = '511147194'
ID_MICHAEL = '1157778380'
ID_ALEXANDER = '494845629'

REQ_PARAM = 'http://185.38.84.19/tele'
 
   #  работаем с Telegram ботом
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f'Привет от бота, дорогой {user_full_name}, id={user_id} !')

    # for i in range(10):
    #     time.sleep(2)
    #     await bot.send_message(user_id,MSG.format(user_full_name))

@dp.message_handler(commands=['mes'])
async def start_handler(message: types.Message):
    #await message.answer(chat_id=int(ID_LEON), text = 'Leons message!')
    await bot.send_message(f'{ID_LEON}', 'Message from bot Elgusto11',)
 #   await bot.send_message(f'{int(ID_ADMIN)}', 'Message from bot Elgusto11 to Admin')

@dp.message_handler(commands=['req'])
async def start_handler(message: types.Message):
    # делаю запрос на сайт django
    
    for i in range(10000):
        time.sleep(900)   #через 900 секунд

        response = requests.get(REQ_PARAM)
        dt = response.json()
        print(response.status_code)
        #dt=json.loads(response.content)
        print(dt)
        j=0
        st=""

        # for i in dt["table"]:        
        #     print(i["clist"])
        #     for k in i["task_exe"]:
        #         print ("    " + k["task"] + " время: " + k["time_control"])

        for i in dt["table"]:        
            st+="\n"
            st+="\n"        
        
            st+=str(i["clist"])
            st+="\n"
            st+="------------------------------\n"

            for k in i["task_exe"]:
                s= "  " + str(k["task"]) + " время: " + str(k["time_control"]) + "\n"
                st+=s
                j=1

        if j>0:
            await bot.send_message(f'{ID_LEON}', st)
            await bot.send_message(f'{ID_ALEXANDER}', st)
            await bot.send_message(f'{ID_MICHAEL}', st)
            await bot.send_message(f'{ID_ADMIN}', st)

@dp.message_handler(commands=['run'])
async def start_handler(message: types.Message):

        response = requests.get(REQ_PARAM)
        dt = response.json()
        print(response.status_code)
        #dt=json.loads(response.content)
        print(dt)
        j=0
        st=""

        # for i in dt["table"]:        
        #     print(i["clist"])
        #     for k in i["task_exe"]:
        #         print ("    " + k["task"] + " время: " + k["time_control"])

        for i in dt["table"]:        
            st+="\n"
            st+="\n"        
        
            st+=str(i["clist"])
            st+="\n"
            st+="------------------------------\n"

            for k in i["task_exe"]:
                s= "  " + str(k["task"]) + " время: " + str(k["time_control"]) + "\n"
                st+=s
                j=1

        if j>0:
            await bot.send_message(f'{ID_LEON}', st)
            #await bot.send_message(f'{ID_ALEXANDER}', st)
            #await bot.send_message(f'{ID_MICHAEL}', st)


if __name__ == '__main__':
    executor.start_polling(dp)