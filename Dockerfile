FROM python:3

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3","-u", "src/main.py"]