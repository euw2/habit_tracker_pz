FROM python:3.12
WORKDIR /usr/local/pzHabitTracker

COPY manage.py ./
COPY env ./env
COPY requirements.txt ./
COPY habits ./habits
COPY PZHabitTracker ./PZHabitTracker

RUN pip install -r requirements.txt

RUN useradd app
USER app

EXPOSE 8000

CMD env/dev_env_entry_point.sh