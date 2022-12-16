import keyboard
from main import *
from database import *



for event in vkinder.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            user_id = event.user_id
            message = event.text
            keyboard.sender(event.user_id, message)

            if request == "привет":
                vkinder.write_msg(user_id, f"Хай, {vkinder.get_user_name(event.user_id)}")
            elif request == 'Начать поиск':
                create_users_table()
                create_viewed_users_table()
                vkinder.pair_search(user_id)
                vkinder.write_msg(user_id, f'Привет, {vkinder.get_user_name(event.user_id)} '
                                           f'Погляди кого я для тебя нашел: {vkinder.found_person_info()}')
                vkinder.send_partner(user_id)
            elif request == 'расскажи анекдот':
                vkinder.write_msg(event.user_id, f'Три помидора идут по улице: папа-помидор, мама-помидор и'
                                                 f' сын-помидорчик. Сын-помидор начинает отставать. Папа-помидор'
                                                 f', рассердившись, подходит к сыну, давит его и говорит:'
                                                 f' «Догоняй, кетчуп!»')
            elif request == "пока":
                vkinder.write_msg(event.user_id, "Пока((")

            elif request == "в каком я городе?":
               self.write_msg(event.user_id, f' {self.get_user_name(event.user_id)}\
               ты в {self.get_user_city(event.user_id)}, дурашка =)')
            else:
                vkinder.write_msg(event.user_id, "Не поняла вашего ответа...")
