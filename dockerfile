FROM python:3.12
WORKDIR /usr/local/pzHabitTracker

COPY manage.py ./
COPY db.sqlite3 ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY habits ./habits
COPY PZHabitTracker ./PZHabitTracker

RUN useradd app
USER app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]