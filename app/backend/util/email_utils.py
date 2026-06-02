import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

NAVER_EMAIL: str = os.getenv("NAVER_EMAIL") or ''
NAVER_PASSWORD: str = os.getenv("NAVER_PASSWORD") or ''


def send_email(to_email: str, code: str) -> None:
    """
    OTP 인증번호 메일 발송
    :param to_email: 보낼 이메일
    :param code: OTP 코드
    """
    if not NAVER_EMAIL or not NAVER_PASSWORD:
        raise ValueError("NAVER_EMAIL 또는 NAVER_PASSWORD 환경변수가 설정되지 않았습니다")

    try:
        msg = MIMEMultipart()
        msg["From"] = NAVER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = '[AI Tutor] 이메일 인증코드'

        body = f"""
            안녕하세요.

            인증코드: {code}

            인증코드는 5분간 유효합니다.
            """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.naver.com', port=465) as smtp:
            smtp.login(NAVER_EMAIL, NAVER_PASSWORD)
            smtp.send_message(msg)

        logger.info(f'인증번호 코드 발송 완료 : {to_email}')

    except Exception as e:
        logger.error(f'메일 발송 실패 {e}')
        raise ValueError('이메일 발송에 실패 했습니다.')
