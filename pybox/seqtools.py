def next_number(step):
    index = 0
    while True:
        yield int(step * index)
        index += 1


def _to_halves(numbers, limit, step):
    for x in next_number(step):
        if x > limit:
            break
        try:
            numbers.remove(x)
        except ValueError:
            continue
        yield x

    yield from _to_halves(numbers, limit, step / 2.0)


def non_sequentially(iterable):
    """

    Example::
        >>> iterable = list(range(10))
        >>> iterable
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> [i for i in non_sequentially(iterable)]
        [0, 9, 4, 2, 6, 1, 3, 5, 7, 8]
        >>> import random
        >>> random.shuffle(iterable)
        >>> iterable = {chr(i+100): i for i in iterable}
        >>> iterable
        {'l': 8, 'j': 6, 'e': 1, 'f': 2, 'd': 0, 'm': 9, 'i': 5, 'g': 3, 'k': 7, 'h': 4}
        >>> for k, v in non_sequentially(iterable.items()):
        ...    print(k, v)
        l 8
        h 4
        d 0
        e 1
        i 5
        j 6
        f 2
        m 9
        g 3
        k 7

    :param iterable:
    :return:
    """
    mapped = {i: v for i, v in enumerate(iterable)}
    limit = max(mapped)
    for x in _to_halves(list(range(limit+1)), limit, limit):
        yield mapped[x]


def resize(iterable, resolution):
    """
    Get a list of different size with values remmaped from an iterable.

    :param iterable: Sequence of (int|float) values
    :param resolution: Length of the new list
    :return: List with the remapped values (resized)
    """
    if resolution < 2:
        msg = 'Can not resize to a resolution lower than 2.'
        raise ValueError(msg)
    current_len = len(iterable)
    if current_len == resolution:
        return iterable[:]
    max_index = resolution - 1
    step = (current_len - 1) / max_index
    mapped = [iterable[0]]
    for x in range(1, max_index):
        findex = x * step
        index = int(findex)
        current = iterable[index]
        try:
            scalar = findex % index
        except ZeroDivisionError:
            scalar = findex
        mapped.append(current + (iterable[index + 1] - current) * scalar)
    mapped.append(iterable[-1])
    return mapped
