FROM python:3.10-slim

WORKDIR /app

RUN pip install \
    "fastapi[standard]>=0.118.0,<0.119.0" \
    "requests>=2.32.5,<3.0.0" \
    "betterproto[compiler]>=1.2.5,<2.0.0" \
    "python-dotenv>=1.0.1,<2.0.0" \
    "pyserial>=3.5,<4.0" \
    "transitions>=0.9.3,<0.10.0"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

