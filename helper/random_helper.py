import random

def random_n_int(n: int) -> int:
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)

def random_float_num(min_val: int, max_val: int, num_decimals: int):
    raw_float = random.uniform(min_val, max_val)
    rounded_float = round(raw_float, num_decimals)
    return rounded_float

def random_n_chars(num_char: int, s: set) -> str:
    result = ''
    for i in range(num_char):
        result += random.choice(list(s))
    return result

def random_bool() -> bool:
    return random.choice([True, False])