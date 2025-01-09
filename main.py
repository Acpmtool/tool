import random
import Termuxtool

from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from pyfiglet import figlet_format  # Не забудьте добавить это в начало вашего файла


def signal_handler(sig, frame):
    print("\n Пока...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Убедитесь, что индекс в пределах допустимого диапазона
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text



def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name = figlet_format('FATOOL', font='drpepper')
    console.print(f"[bold red]{brand_name}[/bold red]", "\n")  # Вставляем название в баннер
    console.print("[bold green][*] Добро пожаловать![/bold green]: Спасибо за покупку")
    console.print(f"[bold green][*] Telegram[/bold green]: [bold blue]@здесь будет канал[/bold blue].")  # Заменено, предполагая, что это декодированная строка
    console.print("[bold red]==================================================[/bold red]")
    console.print("[bold yellow][!] предупреждение[/bold yellow]: Перед тем как вписать свои данные, выйдите из аккаунта в Кар Паркине", end="\n\n")
# Пример использования:
console = Console()
banner(console)

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
            console.print("[bold][blue]========[/blue][ Данные об аккаунте][blue]========[/blue][/bold]")
            console.print(f"[bold green]Имя   [/bold green]: {(data.get('Name') if 'Name' in data else 'UNDEFINED')}.")
            console.print(f"[bold green]ID[/bold green]     : {(data.get('localID') if 'localID' in data else 'UNDEFINED')}.")
            console.print(f"[bold green]Деньги  [/bold green]: {(data.get('money') if 'money' in data else 'UNDEFINED')}.")
            console.print(f"[bold green]Монеты  [/bold green]: {(data.get('coin') if 'coin' in data else 'UNDEFINED')}.", end="\n\n")
        else:
            console.print("[bold red]! ОШИБКА[/bold red]: новые аккаунты должны войти в игру хотя бы один раз!")
            exit(1)
    else:
        console.print("[bold red]! ОШИБКА[/bold red]: похоже, что ваш логин неправильно настроен!")
        exit(1)

def load_key_data(cpm):
    data = cpm.get_key_data()
    console.print("[bold][red]========[/red][ ДЕТАЛИ ДОСТУПНОГО КЛЮЧА ][red]========[/red][/bold]")
    console.print(f"[bold green]Доступный ключ [/bold green]: {data.get('access_key')}.")
    console.print(f"[bold green]Telegram ID[/bold green]: {data.get('telegram_id')}.")
    console.print(f"[bold green]Подписка    [/bold green]: {(data.get('coins') if not data.get('is_unlimited') else 'Пожизненная')}.", end="\n\n")

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(f"{tag} не может быть пустым или содержать только пробелы. Пожалуйста, попробуйте снова.")
        else:
            return value

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] Электронная почта аккаунта[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] Пароль аккаунта[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Доступный ключ[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Пытаемся войти[/bold cyan]: ", end=None)
        cpm = Termuxtool.CPMNuker(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]АККАУНТ НЕ НАЙДЕН (✘)[/bold red].")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold red]НЕПРАВИЛЬНЫЙ ПАРОЛЬ (✘)[/bold red].")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold red]НЕДОПУСТИМЫЙ ДОСТУПНЫЙ КЛЮЧ (✘)[/bold red].")
                sleep(2)
                continue
            else:
                console.print("[bold red]ПОПРОБУЙТЕ СНОВА (✘)[/bold red].")
                console.print("[bold yellow]! Заметка:[/bold yellow]: убедитесь, что вы заполнили поля !.")
                sleep(2)
                continue
        else:
            console.print("[bold green]УСПЕШНО (✔)[/bold green].")
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
           "10", "11", "12", "13", "14", "15", "16", "17", 
           "18", "19", "20", "21", "22"]

            # Вывод меню действий без указания цен
            console.print("[bold cyan](01): Увеличить деньги[/bold cyan]")
            console.print("[bold cyan](02): Увеличить монеты[/bold cyan]")
            console.print("[bold cyan](03): Королевский ранг[/bold cyan]")
            console.print("[bold cyan](04): Изменить ID[/bold cyan]")
            console.print("[bold cyan](05): Изменить имя[/bold cyan]")
            console.print("[bold cyan](06): Изменить имя (Радуга)[/bold cyan]")
            console.print("[bold cyan](07): Удалить аккаунт [/bold cyan]")
            console.print("[bold cyan](08): Зарегистрировать аккаунт [/bold cyan]")
            console.print("[bold cyan](09): Удалить друзей[/bold cyan]")
            console.print("[bold cyan](10): Разблокировать платные машины + Сигнал[/bold cyan]")
            console.print("[bold cyan](11): Разблокировать двигатель w16[/bold cyan]")
            console.print("[bold cyan](12): Разблокировать все гудки[/bold cyan]")
            console.print("[bold cyan](13): Разблокировать отключение повреждений[/bold cyan]")
            console.print("[bold cyan](14): Разблокировать неограниченное топливо[/bold cyan]")
            console.print("[bold cyan](15): Разблокировать дом 3[/bold cyan]")
            console.print("[bold cyan](16): Разблокировать дым[/bold cyan]")
            console.print("[bold cyan](17): Изменить победы в гонках[/bold cyan]")
            console.print("[bold cyan](18): Изменить поражения в гонках[/bold cyan]")
            console.print("[bold cyan](19): Разблокировать все машины[/bold cyan]")
            console.print("[bold cyan](20): Разблокировать сигнал для всех машин[/bold cyan]")
            console.print("[bold cyan](21): Клонировать аккаунт[/bold cyan]")
            console.print("[bold cyan](0) : Выйти[/bold cyan]", end="\n\n")
            service = IntPrompt.ask(f"[bold][?] Выберите услугу [red][1-{choices[-1]} или 0][/red][/bold]", choices=choices, show_choices=False)
            if service == 0:  # Выйти
                console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
            elif service == 1:  # Увеличить деньги
                console.print("[bold cyan][!] Введите, сколько денег вы хотите.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold cyan][%] Сохраняем ваши данные[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 50000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 2:  # Увеличить монеты
                console.print("[bold cyan][!] Введите, сколько монет вы хотите.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold cyan][%] Сохраняем ваши данные[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 90000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 3:  # Королевский ранг
                console.print("[bold red][!] Заметка:[/bold red]: если королевский ранг не появляется в игре, закройте и откройте несколько раз.", end=None)
                console.print("[bold red][!] Заметка:[/bold red]: пожалуйста, не получайте королевский ранг на одном аккаунте дважды.", end=None)
                sleep(2)
                console.print("[bold cyan][%] Предоставление королевского ранга[/bold cyan]: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4:  # Изменить ID
                console.print("[bold cyan][!] Введите ваш новый ID. должно быть ровно 12 символов!![/bold cyan]")
                new_id = Prompt.ask("[bold][?] ID[/bold]")
                console.print("[bold cyan][%] Сохраняем ваши данные[/bold cyan]: ", end=None)
                if len(new_id) >= 9 and len(new_id) <= 14 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимый ID.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5:  # Изменить имя
                console.print("[bold cyan][!] Введите ваше новое имя.[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold cyan][%] Сохраняем ваши данные[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6:  # Изменить имя Радуга
                console.print("[bold cyan][!] Введите ваше новое Радужное имя.[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold cyan][%] Сохраняем ваши данные[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 7:  # Удалить аккаунт
                console.print("[bold cyan][!] После удаления вашего аккаунта возврата нет !!.[/bold cyan]")
                answ = Prompt.ask("[bold cyan][?] Хотите удалить этот аккаунт?![/bold cyan]", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold cyan][%] Удаление вашего аккаунта[/bold cyan]: [bold green]УСПЕШНО (✔)[/bold green].")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                else:
                    continue
            elif service == 8:  # Регистрация аккаунта
                console.print("[bold cyan][!] Регистрация нового аккаунта.[/bold cyan]")
                acc2_email = prompt_valid_value("[bold][?] Электронная почта аккаунта[/bold]", "Email", password=False)
                acc2_password = prompt_valid_value("[bold][?] Пароль аккаунта[/bold]", "Password", password=False)
                console.print("[bold cyan][%] Создание нового аккаунта[/bold cyan]: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Эта электронная почта уже существует!.[/bold yellow]")
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 9:  # Удалить друзей
                console.print("[bold cyan][%] Удаление ваших друзей[/bold cyan]: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10:  # Разблокировать все платные машины + Сирену
                console.print("[bold yellow]! Заметка[/bold yellow]: эта функция занимает некоторое время, пожалуйста, не отменяйте.")
                console.print("[bold cyan][%] Разблокировка всех платных машин[/bold cyan]: ", end=None)
                if cpm.unlock_paid_cars():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11:  # Разблокировать двигатель w16
                console.print("[bold cyan][%] Разблокировка двигателя w16[/bold cyan]: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12:  # Разблокировать все гудки
                console.print("[bold cyan][%] Разблокировка всех гудков[/bold cyan]: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 13:  # Отключение повреждений двигателя
                console.print("[bold cyan][%] Разблокировка отключения повреждений[/bold cyan]: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 14:  # Неограниченное топливо
                console.print("[bold cyan][%] Разблокировка неограниченного топлива[/bold cyan]: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 15:  # Разблокировать дом 3
                console.print("[bold cyan][%] Разблокировка дома 3[/bold cyan]: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16:  # Разблокировать дым
                console.print("[bold cyan][%] Разблокировка дыма[/bold cyan]: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17:  # Изменить победы в гонках
                console.print("[bold cyan][!] Введите, сколько гонок вы выиграли.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold cyan][%] Изменение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 999:
                    if cpm.set_player_wins(amount):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18:  # Изменить поражения в гонках
                console.print("[bold cyan][!] Введите, сколько гонок вы проиграли.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold cyan][%] Изменение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 999:
                    if cpm.set_player_loses(amount):
                        console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 21:  # Клонировать аккаунт
                console.print("[bold cyan]Пожалуйста, введите данные аккаунта[/bold cyan]:")
                to_email = prompt_valid_value("[bold][?] Email[/bold]", "Email", password=False)
                to_password = prompt_valid_value("[bold][?] Password[/bold]", "Password", password=False)
                console.print("[bold cyan][%] Клонирование вашего аккаунта[/bold cyan]: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19:  # Разблокировать все машины
                console.print("[bold yellow]! Заметка[/bold yellow]: эта функция занимает некоторое время, пожалуйста, не отменяйте.")
                console.print("[bold cyan][%] Разблокировка всех машин[/bold cyan]: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]УСПЕШНО (✔)[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО (✘)[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 20:  # Разблокировать сигнал для всех машин
                console.print("[bold cyan][%] Разблокировка всех машин с сигналом[/bold cyan]: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, пожалуйста, присоединяйтесь к нашему каналу в телеграм[/bold yellow]: [bold blue]@{base64.b64decode('').decode('utf-8')}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕ УСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            else:
                continue
            break
        break
