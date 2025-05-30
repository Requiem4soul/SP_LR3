import random
import re
from collections import defaultdict

LOG = False

def create_sample_text():
    """
    Создаем файл с исходным текстом для обучения марковской цепи.
    В реальном проекте это может быть любой большой текст.
    """
    sample_text = """
    Друг мой, друг мой,
    Я очень и очень болен.
    Сам не знаю, откуда взялась эта боль.
    То ли ветер свистит
    Над пустым и безлюдным полем,
    То ль, как рощу в сентябрь,
    Осыпает мозги алкоголь.
    Голова моя машет ушами,
    Как крыльями птица.
    Ей на шее ноги
    Маячить больше невмочь.
    Черный человек,
    Черный, черный,
    Черный человек
    На кровать ко мне садится,
    Черный человек
    Спать не дает мне всю ночь.
    Черный человек
    Водит пальцем по мерзкой книге
    И, гнусавя надо мной,
    Как над усопшим монах,
    Читает мне жизнь
    Какого-то прохвоста и забулдыги,
    Нагоняя на душу тоску и страх.
    Черный человек
    Черный, черный…
    «Слушай, слушай, —
    Бормочет он мне, —
    В книге много прекраснейших
    Мыслей и планов.
    Этот человек
    Проживал в стране
    Самых отвратительных
    Громил и шарлатанов.
    В декабре в той стране
    Снег до дьявола чист,
    И метели заводят
    Веселые прялки.
    Был человек тот авантюрист,
    Но самой высокой
    И лучшей марки.
    Был он изящен,
    К тому ж поэт,
    Хоть с небольшой,
    Но ухватистой силою,
    И какую-то женщину,
    Сорока с лишним лет,
    Называл скверной девочкой
    И своею милою».
    «Счастье, — говорил он, —
    Есть ловкость ума и рук.
    Все неловкие души
    За несчастных всегда известны.
    Это ничего,
    Что много мук
    Приносят изломанные
    И лживые жесты.
    В грозы, в бури,
    В житейскую стынь,
    При тяжелых утратах
    И когда тебе грустно,
    Казаться улыбчивым и простым —
    Самое высшее в мире искусство».
    «Черный человек!
    Ты не смеешь этого!
    Ты ведь не на службе
    Живешь водолазовой.
    Что мне до жизни
    Скандального поэта.
    Пожалуйста, другим
    Читай и рассказывай».
    Черный человек
    Глядит на меня в упор.
    И глаза покрываются
    Голубой блевотой.
    Словно хочет сказать мне,
    Что я жулик и вор,
    Так бесстыдно и нагло
    Обокравший кого-то.
    Друг мой, друг мой,
    Я очень и очень болен.
    Сам не знаю, откуда взялась эта боль.
    То ли ветер свистит
    Над пустым и безлюдным полем,
    То ль, как рощу в сентябрь,
    Осыпает мозги алкоголь.
    Ночь морозная.
    Тих покой перекрестка.
    Я один у окошка,
    Ни гостя, ни друга не жду.
    Вся равнина покрыта
    Сыпучей и мягкой известкой,
    И деревья, как всадники,
    Съехались в нашем саду.
    Где-то плачет
    Ночная зловещая птица.
    Деревянные всадники
    Сеют копытливый стук.
    Вот опять этот черный
    На кресло мое садится,
    Приподняв свой цилиндр
    И откинув небрежно сюртук.
    Слушай, слушай! —
    Хрипит он, смотря мне в лицо,
    Сам все ближе
    И ближе клонится. —
    Я не видел, чтоб кто-нибудь
    Из подлецов
    Так ненужно и глупо
    Страдал бессонницей.
    Ах, положим, ошибся!
    Ведь нынче луна.
    Что же нужно еще
    Напоенному дремой мирику?
    Может, с толстыми ляжками
    Тайно придет «она»,
    И ты будешь читать
    Свою дохлую томную лирику?
    Ах, люблю я поэтов!
    Забавный народ.
    В них всегда нахожу я
    Историю, сердцу знакомую,
    Как прыщавой курсистке
    Длинноволосый урод
    Говорит о мирах,
    Половой истекая истомою.
    Не знаю, не помню,
    В одном селе,
    Может, в Калуге,
    А может, в Рязани,
    Жил мальчик
    В простой крестьянской семье,
    Желтоволосый,
    С голубыми глазами
    И вот стал он взрослым,
    К тому ж поэт,
    Хоть с небольшой,
    Но ухватистой силою,
    И какую-то женщину,
    Сорока с лишним лет,
    Называл скверной девочкой
    И своею милою».
    «Черный человек!
    Ты прескверный гость.
    Это слава давно
    Про тебя разносится».
    Я взбешен, разъярен,
    И летит моя трость
    Прямо к морде его,
    В переносицу
    Месяц умер,
    Синеет в окошко рассвет.
    Ах ты, ночь!
    Что ты, ночь, наковеркала?
    Я в цилиндре стою.
    Никого со мной нет.
    Я один
    И разбитое зеркало
    """

    with open('sample_text.txt', 'w', encoding='utf-8') as file:
        file.write(sample_text)

    return 'sample_text.txt'


def preprocess_text(text):
    """
    Предобработка текста: очистка от лишних символов и разбиение на слова.
    """
    # Приводим к нижнему регистру и убираем лишние пробелы
    text = text.lower().strip()

    # Заменяем знаки препинания на пробелы, кроме точек в конце предложений
    text = re.sub(r'[^\w\s\.]', ' ', text)

    # Разбиваем на слова, сохраняя точки как отдельные элементы
    words = []
    for word in text.split():
        if word.endswith('.'):
            # Если слово заканчивается точкой, добавляем слово без точки и точку отдельно
            if len(word) > 1:
                words.append(word[:-1])
            words.append('.')
        else:
            words.append(word)

    # Убираем пустые строки
    words = [word for word in words if word.strip()]


    return words, words[0]


def build_markov_chain(words):
    """
    Строим структуру данных для марковской цепи.
    Словарь вида: {слово: {следующее_слово: количество_повторений}}
    """
    # Используем defaultdict для упрощения работы с вложенными словарями
    markov_chain = defaultdict(lambda: defaultdict(int))

    # Проходим по всем словам, кроме последнего
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]

        # Увеличиваем счетчик для пары (текущее_слово -> следующее_слово)
        markov_chain[current_word][next_word] += 1

    print(f"Построена марковская цепь из {len(markov_chain)} уникальных слов")

    if LOG:
        # Показываем пример структуры данных
        print("\nЦепь")
        sample_words = list(markov_chain.keys())[:10]  # Ввести количество выводимых слов
        for word in sample_words:
            print(f"'{word}' -> {dict(markov_chain[word])}")

    return markov_chain


def calculate_probabilities(markov_chain, LOG):
    """
    Преобразуем счетчики в вероятности для каждого слова.
    """
    probabilities = {}

    for current_word, next_words in markov_chain.items():
        # Считаем общее количество появлений текущего слова
        total_count = sum(next_words.values())

        # Вычисляем вероятности для каждого следующего слова
        word_probabilities = {}
        for next_word, count in next_words.items():
            word_probabilities[next_word] = count / total_count

        probabilities[current_word] = word_probabilities

    print(f"\nВычислены вероятности для {len(probabilities)} слов")

    if LOG:
        # Показываем пример вероятностей
        print("\nПример вероятностей:")
        sample_words = list(probabilities.keys())[:5] # Указать тут количество
        for word in sample_words:
            print(f"После '{word}':")
            for next_word, prob in probabilities[word].items():
                print(f"  '{next_word}': {prob:.3f}")

    return probabilities


def choose_next_word(current_word, probabilities):
    """
    Выбираем следующее слово на основе вероятностей с помощью генератора случайных чисел.
    """
    if current_word not in probabilities:
        return None

    # Получаем все возможные следующие слова и их вероятности
    next_words = list(probabilities[current_word].keys())
    word_probabilities = list(probabilities[current_word].values())

    # Используем встроенный генератор случайных чисел Python
    # random.choices() учитывает веса (вероятности) при выборе
    chosen_word = random.choices(next_words, weights=word_probabilities)[0]

    return chosen_word


def generate_text(probabilities, start_word=None, max_length=200):
    """
    Генерируем текст заданной длины, используя марковскую цепь.
    """
    if not probabilities:
        return "Ошибка: марковская цепь пуста"

    # Если начальное слово не задано, выбираем случайное
    if start_word is None or start_word not in probabilities:
        start_word = random.choice(list(probabilities.keys()))

    generated_words = [start_word]
    current_word = start_word

    print(f"Начинаем генерацию с слова: '{start_word}'")

    # Генерируем текст слово за словом
    for i in range(max_length - 1):
        next_word = choose_next_word(current_word, probabilities)

        if next_word is None:
            print(f"Достигнут конец цепи на слове '{current_word}'")
            break

        generated_words.append(next_word)
        current_word = next_word

        # Если достигли конца предложения (точка), можем закончить
        if next_word == '.' and i > 10:  # Минимум 10 слов
            break

    # Собираем текст, правильно обрабатывая пунктуацию
    result_text = ""
    for i, word in enumerate(generated_words):
        if word == '.':
            result_text += '.'
        elif i == 0:
            result_text += word.capitalize()
        else:
            result_text += ' ' + word

    return result_text


def main():
    """
    Основная функция программы - демонстрирует весь процесс работы генератора.
    """
    print("=== ГЕНЕРАТОР ТЕКСТА НА ОСНОВЕ МАРКОВСКОЙ ЦЕПИ ===\n")

    # Шаг 1: Создаем файл с исходным текстом
    print("Шаг 1: Создание исходного текста")
    filename = create_sample_text()

    # Шаг 2: Читаем текст из файла
    print(f"\nШаг 2: Чтение текста из файла {filename}")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return

    # Шаг 3: Предобработка текста
    print(f"\nШаг 3: Предобработка текста")
    words, start_word = preprocess_text(text)
    print(f"Получено слов после обработки: {len(words)}")
    if LOG:
        print(f"Задайте кол-во слов для вывода для примера: {words[:10]}")

    # Шаг 4: Построение марковской цепи (структура данных с зависимостями)
    print(f"\nШаг 4: Построение марковской цепи")
    markov_chain = build_markov_chain(words)

    # Шаг 5: Вычисление вероятностей на основе количества повторений
    print(f"\nШаг 5: Вычисление вероятностей для слов")
    probabilities = calculate_probabilities(markov_chain, LOG)

    # Шаг 6: Генерация нового текста
    print(f"\nШаг 6: Генерация нового текста")

    # Попробуем генерацию с конкретного слова
    print(f"\nГенерация:")
    specific_text = generate_text(probabilities, start_word = "человек", max_length = 100)
    print(f"Результат: {specific_text}")

    specific_text = generate_text(probabilities, start_word="черный", max_length=100)
    print(f"Результат: {specific_text}")



# Запускаем программу
if __name__ == "__main__":
    main()