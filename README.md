# Wywołanie

Żeby wywołać program potrzebny jest plik `word_frequencies.json`, który zawiera ~330000 słów w języku angielskim wraz z częstością ich wykorzystania, znormalizowaną do wartości 1-10000 dla wydajności (dane nie mają wartości naukowej). Ten plik jest generowany przez `normalize_words.py` (wymagane są biblioteki z pliku `requirements.txt`).

Demo znajduje się w pliku `autocomplete.py`. Do uruchomienia potrzebna jest biblioteka `json`, która zazwyczaj jest instalowana razem z Pythonem.

W pliku `trie.py` znajduje się podstawowa wersja struktury danych.

