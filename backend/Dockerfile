FROM python:3.10.10
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
LABEL author='Yuriy Semenov' version=1.0.0