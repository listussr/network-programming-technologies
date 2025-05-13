FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libreadline-dev \
    libssl-dev \
    libbz2-dev \
    libsqlite3-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    liblzma-dev \
    libffi-dev \
    libsqlite3-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410200.tar.gz && \
    tar xzf sqlite-autoconf-3410200.tar.gz && \
    cd sqlite-autoconf-3410200 && \
    ./configure --prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3410200*

RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
