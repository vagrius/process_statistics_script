import csv
import datetime
import subprocess
import time
import psutil
import os

# Обработка ввода пути к файлу
filepath = ''
file_exist = False
while not file_exist:
    print('Enter executable file path to run:')
    filepath = r'{0}'.format(input())
    if os.path.isfile(filepath) and filepath[-4:] == '.exe':
        file_exist = True
    else:
        print('Path is incorrect or file does not exist or not executable!', end='\n\n')

# Обработка ввода интервала
print('Enter check interval in seconds:')
try:
    interval = int(input())
except ValueError:
    interval = 5
    print('Value is not correct, so the default (5 sec) has been set', end='\n\n')

print('The process has been started successfully. Press Ctrl+F2 to stop.', end='\n\n')

# Старт процесса
proc_pid = subprocess.Popen(filepath).pid
proc = psutil.Process(proc_pid)
run = True

# Вывод заголовков колонок
labels = ['Date and time', 'CPU load %', 'Working set', 'Private bytes', 'Handle numbers']
for label in labels:
    print(label.ljust(25), end='')
print()

# Выводим информацию, а также записываем в csv-файл
with open(f'.\\{proc.name()}_{proc_pid}.csv', 'w', newline='') as log_file:
    writer = csv.writer(log_file, delimiter=';')
    try:
        while run:
            data_row = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                proc.cpu_percent(),
                proc.memory_info().rss,
                proc.memory_info().vms,
                proc.num_handles(),
            ]
            for value in data_row:
                print(str(value).ljust(25), end='')
            print()
            writer.writerow(data_row)
            time.sleep(interval)
    except psutil.NoSuchProcess:
        run = False
        print('The process was interrupted. Program finished.')
    except KeyboardInterrupt:
        proc.kill()
        print('Program stopped.')
