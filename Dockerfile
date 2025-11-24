# Python 3.10 slim bazasi
FROM python:3.10-slim

# Yaxshi pratika uchun Python muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Zarur paketlarni o'rnatish (agar kompilyatsiya kerak bo'lsa)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements faylini nusxalab o'rnatamiz
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Dastur fayllarini nusxalab olamiz
COPY . /app

# Non-root foydalanuvchi yarating va huquqlarni bering
RUN useradd -m botuser \
    && chown -R botuser:botuser /app

USER botuser

# Dastur ishga tushishi
CMD ["python", "main.py"]
