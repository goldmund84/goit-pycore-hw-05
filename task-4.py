# Декоратор для обробки типових помилок введення для команд CLI.
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            # Обробляє випадки, коли очікується ім'я користувача, але його не знайдено.
            return "Введіть ім'я користувача."
        except ValueError:
            # Обробляє випадки, коли надано недостатньо аргументів для операції.
            return "Будь ласка, введіть ім'я та номер телефону."
        except IndexError:
            # Обробляє випадки, коли індекс виходить за межі, зазвичай через відсутність аргументів.
            return "Недостатньо аргументів."
    return inner

# Додає новий контакт до словника контактів.
@input_error
def add_contact(args, contacts):
    # Викликає ValueError, якщо надано менше двох аргументів (ім'я та телефон).
    if len(args) < 2:
        raise ValueError
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Контакт додано."

# Змінює номер телефону існуючого контакту.
@input_error
def change_contact(args, contacts):
    # Викликає ValueError, якщо надано менше двох аргументів (ім'я та телефон).
    if len(args) < 2:
        raise ValueError
    name, phone = args[0], args[1]
    # Викликає KeyError, якщо ім'я контакту не існує.
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Контакт оновлено."

# Отримує номер телефону для вказаного контакту.
@input_error
def get_phone(args, contacts):
    # Викликає ValueError, якщо не надано аргументу імені.
    if len(args) < 1:
        raise ValueError
    name = args[0]
    # Викликає KeyError, якщо ім'я контакту не існує.
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"

# Відображає всі контакти у словнику.
@input_error
def show_all(args, contacts):
    # Повертає повідомлення, якщо контакти не знайдено.
    if not contacts:
        return "Контакти не знайдено."
    result = []
    # Форматує кожен контакт у рядок.
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)

# Розбирає введення користувача на команду та її аргументи.
def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    command = parts[0].lower()
    args = parts[1:]
    return command, args

# Основна функція для запуску бота контактів.
def main():
    contacts = {}  # Словник для зберігання контактів.
    # Визначає доступні команди та відповідні функції.
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "all": show_all,
        "exit": None,      # Команди для виходу з бота.
        "close": None,
        "goodbye": None,
    }

    # Основний цикл для бота.
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_command(user_input)
        # Перевіряє, чи хоче користувач вийти.
        if command in ("exit", "close", "goodbye"):
            print("До побачення!")
            break
        # Отримує функцію обробника для команди.
        handler = commands.get(command)
        if handler:
            # Виконує команду та виводить результат.
            result = handler(args, contacts)
            print(result)
        else:
            # Обробляє невідомі команди.
            print("Невідома команда.")

# Забезпечує виклик main() при виконанні скрипта.
if __name__ == "__main__":
    main()
