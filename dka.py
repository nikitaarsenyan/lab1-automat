# ============================================================
# ДКА для варианта 2а: алфавит {a, b}, ровно 2 'a' и >2 'b'
# ============================================================

# Состояния: (count_a, count_b), где 3 означает "3 или больше"
# Начальное состояние: (0, 0)
# Принимающие: (2, 3) — ровно 2 'a' и 3+ 'b'

ALPHABET_DKA = ['a', 'b']

def build_dka_table():
    table = {}
    for ca in range(4):   # 0,1,2,3(=>=3)
        for cb in range(4):
            state = (ca, cb)
            # переход по 'a'
            new_ca = min(ca + 1, 3)
            table[(state, 'a')] = (new_ca, cb)
            # переход по 'b'
            new_cb = min(cb + 1, 3)
            table[(state, 'b')] = (ca, new_cb)
    return table

DKA_TABLE = build_dka_table()
DKA_START = (0, 0)
DKA_ACCEPTING = {(2, 3)}


def simulate_dka(word):
    """Симуляция ДКА. word — список символов."""
    state = DKA_START
    path = [state]
    for symbol in word:
        if symbol not in ALPHABET_DKA:
            return False, path
        state = DKA_TABLE[(state, symbol)]
        path.append(state)
    accepted = state in DKA_ACCEPTING
    return accepted, path


def print_dka_result(word, accepted, path):
    word_str = ''.join(word) if word else 'ε'
    print(f"Слово: {word_str}")
    print(f"Путь состояний: {path}")
    print(f"Результат: {'ПРИНЯТО' if accepted else 'ОТВЕРГНУТО'}")
    print("-" * 50)


# Тесты
print("=== ДКА (вариант 2а) ===\n")
test_words_dka = [
    list("aabbb"),    # 2 a, 3 b -> ПРИНЯТО
    list("ababbb"),   # 2 a, 4 b -> ПРИНЯТО
    list("bbbaab"),   # 2 a, 4 b -> ПРИНЯТО
    list("aab"),      # 2 a, 1 b -> ОТВЕРГНУТО
    list("aaabbb"),   # 3 a, 3 b -> ОТВЕРГНУТО
    list("ab"),       # 1 a, 1 b -> ОТВЕРГНУТО
    list("aabbbb"),   # 2 a, 4 b -> ПРИНЯТО
    list("bbaabb"),   # 2 a, 4 b -> ПРИНЯТО
    list("aaa"),      # 3 a, 0 b -> ОТВЕРГНУТО
    list("bbbb"),     # 0 a, 4 b -> ОТВЕРГНУТО
    list(""),         # пустая -> ОТВЕРГНУТО
]

for w in test_words_dka:
    acc, path = simulate_dka(w)
    print_dka_result(w, acc, path)