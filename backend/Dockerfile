FROM python:3.13
WORKDIR /app
COPY ../requirements.txt .
COPY ../data .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]