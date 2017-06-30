# -*- coding: utf-8 -*-
from datetime import date, timedelta
import config
import telebot
from SQLlighter import SQLlighter
from telebot import types
import updatedatabase
import threading
bot = telebot.TeleBot(config.token)


groups1 = ['111', '121', '122', '131', '132', '141', '151', '161', '171', '172', '173', '181', '192', '193']
groups2 = ['211', '221', '231', '232', '241', '251', '261', '271', '272',
          '273', '281', '291', '292']
groups3 = ['311', '321', '331', '332', '341', '351', '361', '381', '392']
groups4 = ['411', '421', '431', '432', '441', '451', '461']
groups5 = ['531', '532']

courses = ['1', '2', '3', '4', '5']

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('📚 Узнать расписание')
    markup.row('📝 Сменить группу')
    bot.send_message(message.chat.id, 'Привет. '
    'Это бот, который поможет узнать свое расписание. Он создан для студентов дневного отделения факультета КНИИТ.'
                                      ' Введите /help для получения информации о боте.'
    , reply_markup=markup)
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    y =[]
    for i in courses:
        y.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))

    keyboard.add(*y)
    bot.send_message(message.chat.id, "Выберите свой курс:", reply_markup=keyboard)

@bot.message_handler(regexp='^📚 Узнать расписание$')
def send_msg(message):
    db = SQLlighter(config.database_name)
    if not db.check_user(message.chat.id):
        bot.send_message(message.chat.id, 'Я еще не знаю номер вашей группы.\nНажмите на кнопку "📝 Сменить группу", чтобы задать его.')
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        today = types.InlineKeyboardButton(text="Сегодня", callback_data="today")
        yesterday = types.InlineKeyboardButton(text="Вчера", callback_data="yesterday")
        tomorrow = types.InlineKeyboardButton(text="Завтра", callback_data="tomorrow")
        anotherdayweek = types.InlineKeyboardButton(text="День недели", callback_data="dayweek")
        keyboard.add(today, yesterday, tomorrow, anotherdayweek)
        bot.send_message(message.chat.id, "Выберите день, расписание которого надо узнать:", reply_markup=keyboard)



@bot.message_handler(regexp='^📝 Сменить группу$')
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    y = []

    for i in courses:
        y.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))

    keyboard.add(*y)
    bot.send_message(message.chat.id, "Выберите курс:", reply_markup=keyboard)

@bot.message_handler(commands=["help"])
@bot.message_handler(content_types='text')
def any_msg(message):
    bot.send_message(message.chat.id, u'Этот бот поможет вам узнать ваше расписание.\n'
                                      u'Чтобы узнать расписание, нажмите "📚 Узнать расписание" и выберите нужную дату.\n'
                                      u'Вы можете сменить группу, нажав "📝 Сменить группу" и выбрав свой курс и свою группу.')


@bot.callback_query_handler(func=lambda msg: msg.data in (*groups1, *groups2, *groups3, *groups4, *groups5, *courses))
def callback_inline(call):
    if call.data == '1':
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k = []
        for i in groups1:
            k.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите группу:")

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
    elif call.data == '2':
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k = []
        for i in groups2:
            k.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите группу:")

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
    elif call.data == '3':
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k = []
        for i in groups3:
            k.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите группу:")

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
    elif call.data == '4':
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k = []
        for i in groups4:
            k.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите группу:")

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    elif call.data == '5':
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k = []
        for i in groups5:
            k.append(types.InlineKeyboardButton(text="{}".format(i), callback_data="{}".format(i)))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите группу:")

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
    else:
        s = SQLlighter(config.database_name)
        if s.check_user(call.message.chat.id):
            s.update_schedule(call.message.chat.id, call.data)
        else:
            s.insert_schedule(call.message.chat.id, call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Готово! Ваша группа - {}.".format(call.data))

@bot.callback_query_handler(func=lambda msg: msg.data in ('today','yesterday','tomorrow',
                                                          'dayweek','monday','tuesday','wednesday','thursday','friday','saturday','sunday'))
def callback_date(call):
    dayweeks = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'}
    dayweeks_number_eng = {0 :'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
    dayweeks_eng_number = {'monday': 0, 'tuesday': 1, 'wednesday' : 2, 'thursday': 3, 'friday':4, 'saturday':5, 'sunday':6}
    dayweeks_eng_rus = {'monday': 'понедельник', 'tuesday': 'вторник',
                    'wednesday': 'среду', 'thursday': 'четверг', 'friday': 'пятницу', 'saturday': 'субботу', 'sunday': 'воскресенье'}
    db = SQLlighter(config.database_name)
    if call.data == 'today':
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text =
                         '*Сегодня {0}, {1}.\n\nТекущая неделя – {2}.\n\n*Ваше расписание:\n\n'.format(
                             date.today().strftime('%d-%m-%Y'),
                             dayweeks[date.today().weekday()],
                             'знаменатель' if date.today().isocalendar()[1] % 2 == 0
                             else 'числитель')
                         + db.get_schedule(call.message.chat.id, date.today().weekday())[0][0],
                         parse_mode='Markdown')
    elif call.data == 'yesterday':
        yesterday = date.today() + timedelta(days=-1)
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text =
                         '*Вчерашний день: {1}, {0}.\n\nНеделя – {2}.\n\n*Расписание:\n\n'.format(
                             yesterday.strftime('%d-%m-%Y'),
                             dayweeks[yesterday.weekday()],
                             'знаменатель' if yesterday.isocalendar()[1] % 2 == 0
                             else 'числитель')
                         + db.get_schedule(call.message.chat.id, yesterday.weekday())[0][0],
                         parse_mode='Markdown')
    elif call.data == 'tomorrow':
        tomorrow = date.today() + timedelta(days=1)
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text =
                         '*Завтра: {1}, {0}.\n\nНеделя – {2}.\n\n*Расписание:\n\n'.format(
                             tomorrow.strftime('%d-%m-%Y'),
                             dayweeks[tomorrow.weekday()],
                             'знаменатель' if tomorrow.isocalendar()[1] % 2 == 0
                             else 'числитель')
                         + db.get_schedule(call.message.chat.id, tomorrow.weekday())[0][0],
                         parse_mode='Markdown')
    elif call.data == 'dayweek':
        dayweeks_number_eng = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday',
                               6: 'sunday'}
        dayweeks_eng_number = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                               'sunday': 6}
        dayweeks_eng_rus = {'monday': 'понедельник', 'tuesday': 'вторник',
                            'wednesday': 'среду', 'thursday': 'четверг', 'friday': 'пятницу', 'saturday': 'субботу',
                            'sunday': 'воскресенье'}
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        k = []
        for i in dayweeks.keys():
            k.append(types.InlineKeyboardButton(text="{}".format(dayweeks[i].capitalize()), callback_data=dayweeks_number_eng[i]))
        keyboard.add(*k)
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text =
                         'Выберите день недели:',
                         parse_mode='Markdown')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)


    elif call.data in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text =
                         'Расписание на {}:\n\n'.format(dayweeks_eng_rus[call.data])
                         + db.get_schedule(call.message.chat.id, dayweeks_eng_number[call.data])[0][0],
                         parse_mode='Markdown')



if __name__ == '__main__':
    threading.Thread(target=updatedatabase.sched).start()
    threading.Thread(target=bot.polling, kwargs={'none_stop':True}).start()
