import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
import sys
from colorama import Fore, Style, init

init()

def print_colored(text, color):
    print(color + text + Style.RESET_ALL)

def animate_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

ascii_art = """
    ____             __  _____                                 
   / __ \____  _____/ /_/ ___/_________ _____  ____  ___  _____
  / /_/ / __ \/ ___/ __/\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /  / /_ ___/ / /__/ /_/ / / / / / / /  __/ /    
/_/    \____/_/   \__//____/\___/\__,_/_/ /_/_/ /_/\___/_/     
                                                               
by PM-Kirill"""

animate_text(ascii_art)

# Определение целевого IP
target = input(Fore.YELLOW + "Введите IP адрес целевого хоста: " + Style.RESET_ALL)
# Определение диапазона портов для сканирования
start_port = int(input(Fore.YELLOW + "Введите начальный порт: " + Style.RESET_ALL))
end_port = int(input(Fore.YELLOW + "Введите конечный порт: " + Style.RESET_ALL))
# Получение IP адреса
target_ip = socket.gethostbyname(target)

# Выводим информацию о сканировании
print_colored(f"Начало сканирования {target_ip}", Fore.GREEN)
print_colored(f"Диапазон портов: {start_port} - {end_port}", Fore.GREEN)
print_colored(f"Время начала: {datetime.now()}", Fore.GREEN)
print_colored("-" * 50, Fore.GREEN)

# Функция для сканирования порта
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target_ip, port))
    sock.close()
    return port, result == 0

# Сканирование портов с многопоточностью
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(scan_port, port) for port in range(start_port, end_port + 1)]
    for future in futures:
        port, is_open = future.result()
        if is_open:
            print_colored(f"Порт {port} открыт", Fore.CYAN)
        else:
            print_colored(f"Порт {port} закрыт", Fore.RED)

print_colored(f"Сканирование завершено: {datetime.now()}", Fore.GREEN)
print_colored("-" * 50, Fore.GREEN)
