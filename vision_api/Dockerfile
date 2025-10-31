FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install "opencv-python>=4.12.0.88,<5.0.0.0" \
                "python-dotenv>=1.1.1,<2.0.0" \
                "fastapi[standard]>=0.118.0,<0.119.0" \
                "ultralytics>=8.3.205,<9.0.0"

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]