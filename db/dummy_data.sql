BEGIN;

-- 유저 더미 데이터
INSERT INTO users (login_id, password, email, role, is_active)
VALUES
    ('dummy_seed_user01', 'password123', 'dummy01@test.com', 'USER', TRUE),
    ('dummy_seed_user02', 'password123', 'dummy02@test.com', 'USER', TRUE),
    ('dummy_seed_admin01', 'password123', 'dummyadmin@test.com', 'ADMIN', TRUE);

-- 채팅방 더미 데이터
INSERT INTO chat_rooms (member_id, title, persona)
VALUES
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-01', 'python_tutor'),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-02', 'algo_tutor'),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-03', 'db_tutor'),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-04', 'web_tutor'),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-05', 'api_tutor'),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_admin01'), 'dummy-room-06', 'admin_tutor');

-- 메시지 더미 데이터
INSERT INTO messages (room_id, role, content)
VALUES
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '파이썬 변수는 어떻게 선언하나요?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '파이썬은 변수 타입 선언 없이 바로 값을 대입하면 됩니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '리스트와 튜플 차이를 알려줘.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '리스트는 수정 가능하고 튜플은 수정할 수 없습니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '함수 정의 예시도 보여줘.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'def greet(name): return f''Hello {name}'' 같은 형태로 작성할 수 있습니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '반복문 예제도 궁금해.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'for item in items: print(item) 형태를 가장 많이 사용합니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'user', '이분 탐색은 언제 쓰나요?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'assistant', '정렬된 데이터에서 빠르게 값을 찾을 때 사용합니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'user', '정규화는 왜 필요한가요?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'assistant', '중복을 줄이고 데이터 일관성을 높이기 위해 사용합니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-04'), 'user', 'HTML과 CSS 역할 차이가 뭐야?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-04'), 'assistant', 'HTML은 구조, CSS는 스타일을 담당합니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-05'), 'user', 'REST API는 어떤 규칙을 따르나요?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-05'), 'assistant', '리소스 중심 URL, HTTP 메서드 활용, 무상태성 같은 원칙을 따릅니다.'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-06'), 'user', '관리자 화면에서 어떤 로그를 봐야 할까?'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-06'), 'assistant', '인증 실패, 서버 오류, 주요 요청 로그를 우선 보는 것이 좋습니다.');

-- 업로드 파일 더미 데이터
INSERT INTO uploaded_files (room_id, file_name, file_path)
VALUES
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_01.pdf', 'uploads/dummy/room01/python_intro_01.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_02.pdf', 'uploads/dummy/room01/python_intro_02.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_03.pdf', 'uploads/dummy/room01/python_intro_03.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_04.pdf', 'uploads/dummy/room01/python_intro_04.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_05.pdf', 'uploads/dummy/room01/python_intro_05.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_06.pdf', 'uploads/dummy/room01/python_intro_06.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_07.pdf', 'uploads/dummy/room01/python_intro_07.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'algorithm_basic.pdf', 'uploads/dummy/room02/algorithm_basic.pdf'),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'database_normalization.pdf', 'uploads/dummy/room03/database_normalization.pdf');

COMMIT;
