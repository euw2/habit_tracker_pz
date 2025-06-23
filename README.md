**Habit Tracker**(ENG)

Habit Tracker is a mobile application designed for users who want to build and maintain positive habits in their daily lives.

**Running App**

If you wish to run this app:

1. Make sure you have docker and docker-compose installed on you machine
2. Open project's root directory in the terminal
3. Setup local development environment
```
    python env/generate_stub_env.py
```
4. Build docker image
```
    docker-compose.exe --env-file=env/db_env.env build
```
5. Run 
```
    docker-compose.exe --env-file=env/db_env.env up
```
6. Visit http://localhost:3000/habits/

Project Goals:
- Help in building good habits
- Increase motivation and self-discipline
- Personalization and ease of use
- Progress Analysis

Project Assumptions:
- Simple and user-friendly interface, easy to use for users of all ages
- Notification System: Reminds about planned or unfinished habits.
- Tracking breaks and failures
- Visualization of progress in various forms

Team Members:
- Igor Jastrzębski
- Dominik Filipiuk
- Paweł Wziętek
- Szymon Grodek


**Habit Tracker**(PL)

Habit Tracker to aplikacja mobilna zaprojektowana z myślą o użytkownikach pragnących zbudować i utrzymywać pozytywne nawyki w swoim codziennym życiu.

Jeśli chcesz uruchomić tę aplikację:

1. Upewnij się, że masz zainstalowane docker i docker-compose na swoim komputerze
2. Otwórz katalog główny projektu w terminalu
3. Zainicjalizuj środowisko developerskie.
```
    python env/generate_stub_env.py
```
4. Zbuduj obraz dockera
```
docker-compose.exe --env-file=env/db_env.env build
```
5. Uruchom 
```
docker-compose.exe --env-file=env/db_env.env up
```
6. Odwiedź http://localhost:3000/habits/

Cele Projektu:
- Pomoc w budowaniu dobrych nawyków
- Zwiększenie motywacji i samodyscypliny
- Personalizacja i łatwość użytkowania
- Analiza Postępów

Załóżenie projektu:
- Prosty i przyjazny interfejs, łatwy w obsłudze dla użytkowników w każdym wieku
- System Powiadomień: Przypomina o planowanych lub nieukończonych nawykach.
- Śledzenie przerw i niepowodzeń
- Wizualizacja postępów w różnych formach

Członkowie zespołu:
- Igor Jastrzębski
- Dominik Filipiuk
- Paweł Wziętek
- Szymon Grodek
