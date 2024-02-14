import telebot


class IsPouria(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_pouria'

    @staticmethod
    def check(message: telebot.types.Message):
        return message.chat.first_name == 'Pouria'
