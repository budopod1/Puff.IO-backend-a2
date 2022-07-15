def pad_list(iterable, length, value):
    return [
        value if i >= len(iterable) else iterable[i]
        for i in range(length)
    ]
