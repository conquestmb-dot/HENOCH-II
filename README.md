# II Księga Henocha — audiobook (73 rozdziały)

Generator dla Windows 11: pobiera trzy istniejące nagrania HeyGen, tworzy kolejne przez Edge TTS z dostarczonych **pełnych polskich tekstów** i scala 73 pliki FFmpeg.

**Stan:** nagrania 1–3 są dostępne pod adresami HeyGen. Teksty 4–73 nie są jeszcze umieszczone w repozytorium; skrypt **nie tworzy ich ze streszczeń**. Brak tekstu oznacza pominięcie nagrania.

## Szybki start (Windows 11)
1. Zainstaluj Python 3.10+ i FFmpeg (obie komendy: `py --version`, `ffmpeg -version` muszą działać).
2. Pobierz repozytorium jako ZIP (Code → Download ZIP), rozpakuj.
3. Uruchom `START_WINDOWS.bat`, aby zainstalować `edge-tts` i pobrać rozdziały 1–3.
4. Umieść kompletne, zweryfikowane polskie teksty rozdziałów 4–73 w folderze `teksty`, np. `Henoch_II_004.txt` (UTF-8).
5. Uruchom `py generator.py generate --start 4 --end 73`, potem `py generator.py check`.
6. Gdy jest **73/73 MP3**, uruchom `py generator.py join`.

Wynik: `II_Ksiega_Henocha_1-73_CALOSC.mp3`. Brak jednego rozdziału wstrzymuje montaż.

**Głos:** rozdziały 1–3 z HeyGen (Steadfast Stefan), kolejne domyślnie `pl-PL-MarekNeural`. To różne głosy. Jeśli ma być jednolity, trzeba przygotować cały tekst, usunąć wcześniejsze MP3 z folderu lokalnego i nagrać wszystkie 73 tym samym lektorem.

**Uwagi:** Edge TTS korzysta z nieoficjalnego klienta internetowej usługi; dostępność może się zmieniać. Nie wgrywaj kluczy API ani cudzych chronionych przekładów bez uprawnień. Repozytorium jest obecnie PUBLICZNE, a pliki MP3 są wykluczone z repozytorium przez .gitignore.
