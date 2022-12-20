# https://topaz.github.io/paste/#XQAAAQDwAwAAAAAAAAAzHIoib6q1WFXtvfQ5zSDj1Ztxrl1vCSmi2fap9+hZ1JTXI26/tjkNBYdAV78u4Ik1d7DaV5BkillL0oCodF8dVfq8zZld3FvLYNRXPQtW9MYRd+AYllNwdok2KASOusGdQJMJAk+OW5haJlr75uKyudk6qozi0MGwMQzukb/AaBAE9lJgpIT/MkX3MjyuZhIjokrYqg7S5EuFrXU5weM5KxP4y6MR2C3hr05gajIAuP/mOO29HvZcH7OxFybbE0XHv6zPYoi0S3J0i1YzO3Bqg9bRko/xtSbVNGKVL4gU38OwT7vq/geL+cGe5rjYVwf+8y9V3ZooV0rNgREWFTUllTy6TpYCV2UrgP84Wjqrk/ySTQYy+YzP1CxWuLIQDkUaVmiRGNxvmkex8Vjwl1CYgdnOGgzXo8FIHmUVm52i0GUnmk3qQRw+dtyOHtPSbNDxOTte/lqOeaqV5X424gYSqXJr4DNjIv9vSdfnlShLKfUurMXF4JqhAleZXKkRvP61X8FxMW+qtfJp0u1AGvbD9qtDhAQMjtWnvMWxxnhyqTlWeGgbmpniOIhBypkQY/vtuSzS+yBgi2nLNo5eTJhbtY/Idlkcb0o9KwYmvC1qsWsHDU0GfYqqvl9NHtV3/Dp8rtisSu2P4LuryP0VtN3/+V7pSw==


from time import time

input_file = "../inputs/inputs_day20.txt"

decryption_key = 811589153


def mix(file, n=1):
    l = len(file)
    fileindex = [i for i in range(l)]
    for _ in range(n):
        for i, v in enumerate(file):
            if v == 0:
                continue
            j = fileindex.index(i)
            x = fileindex.pop(j)
            k = (j + v) % (l - 1)
            fileindex.insert(k, x)
    return [file[i] for i in fileindex]


def grove_coordinates(file):
    l = len(file)
    return sum(file[i] for i in
               ((file.index(0) + m) % l for m in [1000, 2000, 3000]))


if __name__ == '__main__':
    start_time = time()
    with open(input_file, 'r') as f:
        file = list(map(int, (n.strip() for n in f.readlines())))

    print("Part #1 :", grove_coordinates(mix(file)))

    file2 = [f * decryption_key for f in file]

    print("Part #2 :", grove_coordinates(mix(file2, 10)))

    print("Execution time: {:.6f}s".format((time() - start_time)))
