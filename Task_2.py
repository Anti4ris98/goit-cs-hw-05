import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    # Сортування результатів
    sorted_values = sorted(reduced_values, key=lambda x: x[1], reverse=True)

    return dict(sorted_values)

def visualize_top_words(result, top_n=10):
    # Отримання ключів та значень з результату
    keys = list(result.keys())[:top_n]
    values = list(result.values())[:top_n]

    # Візуалізація
    plt.figure(figsize=(10, 5))
    plt.bar(keys, values)
    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), color='blue', fontweight='bold')
    plt.xlabel('Слова')
    plt.ylabel('Кількість')
    plt.title('Топ слів')
    plt.show()

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        result = map_reduce(text)

        # Візуалізація результату
        visualize_top_words(result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")