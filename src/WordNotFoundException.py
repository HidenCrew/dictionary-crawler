class WordNotFoundException(Exception):
    def __init__(self, word: str, source: str):
        self.word = word
        self.source = source

    def __str__(self):
        return f"Failed to find \"{self.word}\" from \"{self.source}\""
