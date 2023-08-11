"""
ユーティリティ関数・クラス群
"""
def snake_to_camel(key: str):
    """
    スネークケースの文字列を(lower)キャメルケースに変換

    >>> snake_to_camel("test")
    'test'
    >>> snake_to_camel("test_example_value")
    'testExampleValue'
    >>> snake_to_camel("test1")
    'test1'
    >>> snake_to_camel("test_1")
    'test1'
    """
    words = key.split("_")
    converted_words = words[:1] + [word.capitalize() for word in words[1:]]
    return "".join(converted_words)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
