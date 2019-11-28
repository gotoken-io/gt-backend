FROM python:3.7
WORKDIR /code/gt-backend

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "manage:app", "-c", "./gunicorn.conf.py"]