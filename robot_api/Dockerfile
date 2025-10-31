FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install "pyniryo==1.1.1" --no-deps && \
    pip install \
    "opencv-contrib-python>=4.10.0.84,<5.0.0.0" \
    "python-dotenv>=1.0.1,<2.0.0" \
    "fastapi[standard]>=0.118.0,<0.119.0"

COPY . .

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

