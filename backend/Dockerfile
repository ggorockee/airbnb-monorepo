# backend/Dockerfile

# --- 1. 기반 이미지 설정 (Base Image) ---
# Python 3.12의 슬림 버전을 기반으로 시작
# 'bookworm'은 안정적인 데비안 배포판 버전
FROM python:3.12-slim-bookworm

# --- 2. 환경 변수 설정 (Environment Variables) ---
# 파이썬이 .pyc 파일을 생성하지 않도록 하여 이미지 용량을 줄이고,
# print() 문의 출력이 버퍼링 없이 바로 터미널에 표시되도록 함.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- 3. 작업 디렉토리 설정 (Work Directory) ---
# 컨테이너 내부에서 명령이 실행될 기본 디렉토리를 설정.
WORKDIR /app

# --- 4. 파이썬 의존성 설치 (Install Dependencies) ---
# requirements.txt 파일만 먼저 복사하여 의존성을 설치
# 이렇게 하면 소스 코드가 변경될 때마다 의존성을 새로 설치하는 것을 방지
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 5. 소스 코드 복사 (Copy Source Code) ---
# 현재 디렉토리(backend/)의 모든 파일을 컨테이너의 /app 디렉토리로 복사
# .dockerignore 파일에 명시된 파일들은 복사에서 제외.
COPY . .

# --- 7. 포트 노출 (Expose Port) ---
# Gunicorn 서버가 실행될 포트를 8000번으로 지정하고 외부에 노출.
# 이 포트는 Kubernetes의 Service와 연결.
EXPOSE 8000

# --- 8. 컨테이너 실행 명령어 (Command to Run) ---
# 컨테이너가 시작될 때 Gunicorn을 실행.
# --bind 0.0.0.0:8000 : 컨테이너의 모든 네트워크 인터페이스 8000번 포트에서 요청을 받음.
# --workers 2 : 2개의 워커 프로세스로 요청을 병렬 처리합니다. (서버 CPU 코어 수에 따라 2~4배로 조절)
# config.wsgi: Django 프로젝트의 WSGI 애플리케이션 경로. 
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "config.wsgi:application"]

