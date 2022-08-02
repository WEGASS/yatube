# def cache_args(func):
#
#     _cache = {}
#     def saved_value(num):
#         if num in _cache.keys():
#             return _cache[num]
#         value = func(num)
#         _cache[num] = value
#         return value
#     return saved_value
#
#
#
# @cache_args
# def long_heavy(num):
#     print(f"Долго и сложно {num}")
#     return num**num
#
# print(long_heavy(1))
# print(long_heavy(1))
# print(long_heavy(2))
# print(long_heavy(2))

# Создайте в декораторе переменную-кеш, сохраните в ней результат
# выполнения декорируемой функции. Создайте в декораторе
# переменную, хранящую счётчик запросов. Пока значение счётчика ниже предельного
# — отдавайте результат, сохранённый в кеше. Когда число запросов к функции превысит
# предел и пора будет снова высчитывать результат выполнения функции — сбросьте счётчик,
# выполните декорируемую функцию и заново сохраните результат её выполнения в
# переменную-кеш. В предыдущем уроке мы рассказывали, как создавать переменные в
# декораторах, этот пример пригодится и здесь.

def cache3(func):
    cached = {'count': 0, 'value': None}
    def new_func():
        if cached['count'] < 2 and cached['value'] is not None:
            cached['count'] += 1
            return cached['value']
        else:
            cached['value'] = func()
            cached['count'] = 0
            return cached['value']
    return new_func

@cache3
def heavy():
    print('Сложные вычисления')
    return 1

print(heavy())
print(heavy())
print(heavy())
print(heavy())