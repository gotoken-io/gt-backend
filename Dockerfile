FROM python:3.7
WORKDIR /code/gt-backend

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=manage:app

EXPOSE 5000

CMD ["gunicorn", "manage:app", "-c", "./gunicorn.conf.py"]