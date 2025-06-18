FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 종속성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . .

# 5. 실행 명령어
CMD ["python", "main.py"]
