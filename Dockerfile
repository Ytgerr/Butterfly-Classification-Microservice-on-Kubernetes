FROM python:3.11

WORKDIR /scr

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 2005
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "2005"]
