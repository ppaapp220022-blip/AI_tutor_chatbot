# Docker + Jenkins Deployment Guide

## 1. Server prerequisites

Install Docker and the Compose plugin on the Naver Cloud server.

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

If Jenkins runs as the `jenkins` user on the same host, allow Docker access.

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

## 2. Prepare the application directory

```bash
sudo mkdir -p /opt/ai_tutor_chatbot
sudo chown -R $USER:$USER /opt/ai_tutor_chatbot
cd /opt/ai_tutor_chatbot
git clone <YOUR_REPOSITORY_URL> .
cp .env.example .env
```

Edit `.env` and fill in real secrets before the first deploy.

## 3. Important environment values

`.env` is used both by Docker Compose and the app containers.

Required values:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `NAVER_EMAIL`
- `NAVER_PASSWORD`
- `JWT_SECRET_KEY`
- `OPENAI_API_KEY`

Recommended production values:

```env
POSTGRES_DB=ai_tutor_chatbot
POSTGRES_USER=ai_tutor
POSTGRES_PASSWORD=change-me
NGINX_PORT=80
NAVER_EMAIL=your_email@naver.com
NAVER_PASSWORD=your_password
JWT_SECRET_KEY=replace-with-a-long-random-string
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7
OPENAI_API_KEY=sk-...
CORS_ALLOW_ORIGINS=http://223.130.159.82
BACKEND_API_BASE_URL=http://backend:8000
```

## 4. First manual deploy

```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f backend
```

Check these URLs:

- `http://SERVER_IP/`
- `http://SERVER_IP/docs`
- `http://SERVER_IP/health`

## 5. Jenkins job setup

Use a Pipeline job and point it at this repository so it reads the `Jenkinsfile`.

The Jenkins agent must be able to run:

```bash
docker compose build
docker compose up -d
```

Recommended Jenkins credentials:

- Git repository credentials if the repo is private
- Optional secret file or secret text strategy for `.env`

If you prefer not to store `.env` inside the repo checkout, create it once on the server at the workspace root before the pipeline runs.

## 6. Naver Cloud network rules

Open only the ports below in ACG:

- `22` for SSH
- `80` for HTTP
- `443` for HTTPS after TLS is added

Do not expose `5432`, `6379`, `8000`, or `8501` publicly in production.
