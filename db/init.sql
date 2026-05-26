CREATE DATABASE ai_tutor_chatbot;
CREATE DATABASE ai_tutor_chatbot_test;

-- 유저 ENUM
CREATE TYPE user_role AS ENUM ('USER', 'ADMIN');
-- 채팅 ENUM
CREATE TYPE message_role AS ENUM ('user', 'assistant');

-- 유저
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    login_id    VARCHAR(30) UNIQUE NOT NULL, -- 로그인 아이디
    password    VARCHAR(60) NOT NULL,       -- BCrypt 암호화
    email       VARCHAR(40) UNIQUE NOT NULL, -- 이메일
    role        user_role DEFAULT 'USER',  -- 'USER' or 'ADMIN'
    is_active   BOOLEAN DEFAULT TRUE,        -- 계정 활성화 여부
    created_at  TIMESTAMP DEFAULT NOW() -- 생성일
);
COMMENT ON TABLE users IS '유저';
COMMENT ON COLUMN users.id IS '유저 고유 번호';
COMMENT ON COLUMN users.login_id IS '로그인 아이디';
COMMENT ON COLUMN users.password IS 'BCrypt 암호화';
COMMENT ON COLUMN users.email IS '이메일';
COMMENT ON COLUMN users.role IS 'USER or ADMIN';
COMMENT ON COLUMN users.is_active IS '계정 활성화 여부';
COMMENT ON COLUMN users.created_at IS '생성일';

-- 대화방
CREATE TABLE IF NOT EXISTS chat_rooms (
    id          SERIAL PRIMARY KEY,
    member_id   INTEGER NOT NULL, -- 회원 FK
    title       VARCHAR(20) NOT NULL, -- 대화방 제목
    persona     VARCHAR(50) NOT NULL, -- 페르소나 종류
    created_at  TIMESTAMP DEFAULT NOW(), -- 생성일
    CONSTRAINT fk_chat_rooms_member_id_users_id FOREIGN KEY (member_id) REFERENCES users(id)
);
COMMENT ON TABLE chat_rooms IS '대화방';
COMMENT ON COLUMN chat_rooms.id IS '대화방 고유 번호';
COMMENT ON COLUMN chat_rooms.member_id IS '회원 FK';
COMMENT ON COLUMN chat_rooms.title IS '대화방 제목';
COMMENT ON COLUMN chat_rooms.persona IS '페르소나 종류';
COMMENT ON COLUMN chat_rooms.created_at IS '생성일';

-- 메시지
CREATE TABLE IF NOT EXISTS messages (
    id          SERIAL PRIMARY KEY,
    room_id     INTEGER NOT NULL , -- 대화방 FK
    role        message_role NOT NULL , -- 'user' or 'assistant'
    content     TEXT NOT NULL , -- 내용
    created_at  TIMESTAMP DEFAULT NOW(), -- 문자 보낸 일시
    CONSTRAINT fk_messages_id_chat_room_id FOREIGN KEY (room_id) REFERENCES chat_rooms(id)
);
COMMENT ON TABLE messages IS '메시지';
COMMENT ON COLUMN messages.id IS '메시지 고유 번호';
COMMENT ON COLUMN messages.room_id IS '대화방 FK';
COMMENT ON COLUMN messages.role IS 'user or assistant';
COMMENT ON COLUMN messages.content IS '내용';
COMMENT ON COLUMN messages.created_at IS '메시지 전송 일시';

-- 파일 업로드
CREATE TABLE IF NOT EXISTS uploaded_files (
    id          SERIAL PRIMARY KEY,
    room_id     INTEGER NOT NULL , -- 대화방 FK
    file_name   VARCHAR(50) NOT NULL, -- 파일명
    file_path   VARCHAR(255) NOT NULL , -- 파일경로
    created_at  TIMESTAMP DEFAULT NOW(), -- 생성일
    CONSTRAINT fk_uploaded_files_id_chat_rooms_id FOREIGN KEY (room_id) REFERENCES chat_rooms(id)
);
COMMENT ON TABLE uploaded_files IS '파일 업로드';
COMMENT ON COLUMN uploaded_files.id IS '파일 고유 번호';
COMMENT ON COLUMN uploaded_files.room_id IS '대화방 FK';
COMMENT ON COLUMN uploaded_files.file_name IS '파일명';
COMMENT ON COLUMN uploaded_files.file_path IS '파일 경로';
COMMENT ON COLUMN uploaded_files.created_at IS '생성일';