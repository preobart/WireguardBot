LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Start bot',
    '/clients': 'List all clients',
    '/create': 'Create a new user',
    '/revoke': 'Revoke existing user',
    '/config': 'Get user config',
    '/help': 'Help on how the bot works',
}

LEXICON: dict[str, str] = {
    "start": "Добро пожаловать! Я ваш бот для управления пользователями Wireguard.\n\nДля списка доступных команд нажмите /help",
    "help": "Список доступных команд:\n"
            "/clients - Показать список пользователей\n"
            "/create - Добавить нового пользователя\n"
            "/revoke - Удалить пользователя\n"
            "/config - Получить конфигурацию пользователя\n"
            "/help - Показать это сообщение",
    "no_clients": "В настоящий момент у вас нет пользователей, для того чтобы добавить используйте /create",
    "no_user": "Пользователя {username} не существует",
    "clients": "Текущий список пользователей:\n{clients}",
    "create_prompt": "Введите имя нового пользователя:",
    "create_invalid": "Попробуйте другое имя.",
    "create_success": "Пользователь {username} успешно добавлен. Вот его конфигурация:",
    "revoke_prompt": "Выберите пользователя для удаления:",
    "revoke_success": "Пользователь {username} успешно удален.",
    "config_prompt": "Выберите пользователя для получения конфига:",
    "config_received": "Ваш конфиг:"
}