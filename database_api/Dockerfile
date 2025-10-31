FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

RUN pip install \
    "python-dotenv>=1.0.1,<2.0.0" \
    "sqlalchemy>=2.0.43,<3.0.0" \
    "fastapi[standard]>=0.118.0,<0.119.0" \
    "betterproto[compiler]>=1.2.5,<2.0.0" \
    "mysqlclient>=2.2.7,<3.0.0" \
    "bcrypt>=5.0.0,<6.0.0"

COPY . .

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]

