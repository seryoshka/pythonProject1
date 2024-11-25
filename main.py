import os
import re
import csv
import charset_normalizer

# регулряка для парсинга лога
LOG_PARSING = r"(\d{8}T\d{6})\.\d{3} \d+ (\w+) (\w+)"

# определяем кодировуку
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:  # открываем файл в бинарном виде
        result = charset_normalizer.detect(file.read())
        return result['encoding']  # возвращаем найденную кодировку

# принимаем путь к дирректории с логами
def pars_logs(directory):
    # создаем пустой словарь (дата-час, категория, компонент - ключ, количество сообщений - знаение)
    aggregated_data = {}

    #  проходим по всем файлам в директории
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path): # проверяем, что это файл
            encoding = detect_encoding(file_path)# проверяем кодировку
            with open(file_path, 'r', encoding=encoding, errors='replace') as file: # открываем файл в режиме чтения
                for line in file: #читаем построчно
                    match = re.match(LOG_PARSING, line) # созраняем если есть совпадения
                    if match:
                        day_hour = match.group(1)[:10]  # извлекаем дату и час
                        category = match.group(2)       # категория (INFO, WARN и т.д.)
                        component = match.group(3)      # компонент (IMDB, SLC и т.д.)

                        # сохраняем данные в словарь
                        key = (day_hour, category, component)
                        if key not in aggregated_data: # проверяем есть ли такая запись в словаре, если нет, добавляем со значением 0
                            aggregated_data[key] = 0
                        aggregated_data[key] += 1 # если есть, увеличиваем на 1
    # возвращаем словарь
    return aggregated_data

# созраняем в файл
def save_to_csv(data, output_file):

    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day & Hour", "Category", "Component", "Number of Messages"]) # записыввем строку в файл, 1я строка - заголовки столбцов

        for (day_hour, category, component), count in sorted(data.items()):
            writer.writerow([day_hour, category, component, count])

# выволдим в консоль
def display_table(data):
    print(f"{'Day & Hour':<15} {'Category':<10} {'Component':<15} {'Number of Messages':<5}") # выводим заголовки
    print("-" * 50) # выводим горизонталнцю линию

    for (day_hour, category, component), count in sorted(data.items()):
        print(f"{day_hour:<15} {category:<10} {component:<15} {count:<10}") # выводим строки с заданной шириной

def main():
    # получаем директорию и имя выходного файла
    directory = input("Введите путь к директории с логами: ")
    output_file = input("Введите имя CSV файла для сохранения: ")

    # парсим логи и сохраняем результат
    data = pars_logs(directory)
    save_to_csv(data, output_file)

    # показываем таблицу в консоли
    print("\nДанные сохранены в CSV файл.\n")
    display_table(data)

if __name__ == "__main__":
    main()
