# ============================================================
# НКА для варианта 2б: алфавит {1,2,3}, последний символ
# не встречался ранее в строке
# ============================================================

ALPHABET_NKA = ['1', '2', '3']

# Состояния:
#   'q0'          — начальное
#   'q_c'         — угадали последний символ c, читаем префикс (c запрещён)
#   'qf_c'        — последний символ прочитан = c (принимающее, без исходящих)

EPSILON = 'ε'

def build_nka_table():
    table = {}

    # ε-переходы из начального состояния
    table[('q0', EPSILON)] = {'q_1', 'q_2', 'q_3'}

    for c in ALPHABET_NKA:
        state_qc = f'q_{c}'
        state_qfc = f'qf_{c}'

        # Из q_c: читаем любой символ кроме c -> остаёмся в q_c
        for x in ALPHABET_NKA:
            if x != c:
                table[(state_qc, x)] = {state_qc}
            else:
                # символ c: переход в принимающее состояние (конец строки)
                table[(state_qc, x)] = {state_qfc}

        # Из qf_c: нет исходящих переходов (строка должна закончиться)
        # явно не добавляем — отсутствие ключа = нет перехода

    return table

NKA_TABLE = build_nka_table()
NKA_START = 'q0'
NKA_ACCEPTING = {'qf_1', 'qf_2', 'qf_3'}


def epsilon_closure(states, table):
    """Вычисляет ε-замыкание множества состояний."""
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        key = (s, EPSILON)
        if key in table:
            for ns in table[key]:
                if ns not in closure:
                    closure.add(ns)
                    stack.append(ns)
    return closure


def simulate_nka(word):
    """Симуляция НКА через множества состояний."""
    current = epsilon_closure({NKA_START}, NKA_TABLE)
    all_states_history = [set(current)]

    for symbol in word:
        if symbol not in ALPHABET_NKA:
            return False, all_states_history
        next_states = set()
        for s in current:
            key = (s, symbol)
            if key in NKA_TABLE:
                next_states |= NKA_TABLE[key]
        current = epsilon_closure(next_states, NKA_TABLE)
        all_states_history.append(set(current))
        if not current:
            break

    accepted = bool(current & NKA_ACCEPTING)
    return accepted, all_states_history


def print_nka_result(word, accepted, history):
    word_str = ''.join(word) if word else 'ε'
    print(f"Слово: {word_str}")
    print(f"Множества состояний по шагам:")
    for i, states in enumerate(history):
        if i == 0:
            print(f"  [ε-замыкание старта] {states}")
        else:
            print(f"  после символа '{word[i-1]}': {states}")
    print(f"Результат: {'ПРИНЯТО' if accepted else 'ОТВЕРГНУТО'}")
    print("-" * 50)


# Тесты
print("=== НКА (вариант 2б) ===\n")
test_words_nka = [
    list("2321"),   # последний 1, не встречался -> ПРИНЯТО
    list("1231"),   # последний 1, встречался -> ОТВЕРГНУТО
    list("1"),      # последний 1, не встречался -> ПРИНЯТО
    list("123"),    # последний 3, не встречался -> ПРИНЯТО
    list("11"),     # последний 1, встречался -> ОТВЕРГНУТО
    list("321"),    # последний 1, не встречался -> ПРИНЯТО
    list("22"),     # последний 2, встречался -> ОТВЕРГНУТО
    list("1232"),   # последний 2, встречался -> ОТВЕРГНУТО
    list("312"),    # последний 2, не встречался -> ПРИНЯТО
    list(""),       # пустая -> ОТВЕРГНУТО
]

for w in test_words_nka:
    acc, hist = simulate_nka(w)
    print_nka_result(w, acc, hist)