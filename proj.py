

if 'привет' in user_message.lower():
    bot_response = "Привет! Как дела?"
elif 'пока' in user_message.lower():
    bot_response = "До свидания!"
elif 'нормально' or 'хорошо' or 'шикарно' in user_message.lower():
    bot_response = "Отлично !"
else:
    bot_response = f"Вы сказали: {user_message}"