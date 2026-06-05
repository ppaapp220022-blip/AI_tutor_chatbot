BEGIN;

-- 유저 더미 데이터
INSERT INTO users (login_id, password, email, role, is_active, created_at)
VALUES
    ('dummy_seed_user01', 'password123', 'dummy01@test.com', 'USER', TRUE, CURRENT_TIMESTAMP),
    ('dummy_seed_user02', 'password123', 'dummy02@test.com', 'USER', TRUE, CURRENT_TIMESTAMP),
    ('dummy_seed_admin01', 'password123', 'dummyadmin@test.com', 'ADMIN', TRUE, CURRENT_TIMESTAMP);

-- 채팅방 더미 데이터
INSERT INTO chat_rooms (member_id, title, persona, created_at)
VALUES
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-01', 'python_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-02', 'algo_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-03', 'db_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-07', 'network_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-08', 'os_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user01'), 'dummy-room-09', 'java_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-04', 'web_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-05', 'api_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-10', 'security_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-11', 'cloud_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_user02'), 'dummy-room-12', 'data_tutor', CURRENT_TIMESTAMP),
    ((SELECT id FROM users WHERE login_id = 'dummy_seed_admin01'), 'dummy-room-06', 'admin_tutor', CURRENT_TIMESTAMP);

-- 메시지 더미 데이터
INSERT INTO messages (room_id, role, content, created_at)
VALUES
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '파이썬 변수는 어떻게 선언하나요?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '파이썬은 변수 타입 선언 없이 바로 값을 대입하면 됩니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '리스트와 튜플 차이를 알려줘.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '리스트는 수정 가능하고 튜플은 수정할 수 없습니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '함수 정의 예시도 보여줘.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'def greet(name): return f''Hello {name}'' 같은 형태로 작성할 수 있습니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '반복문 예제도 궁금해.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'for item in items: print(item) 형태를 가장 많이 사용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '딕셔너리는 언제 사용하면 좋아?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '키와 값으로 빠르게 데이터를 조회해야 할 때 유용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '클래스와 객체 차이도 설명해줘.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', '클래스는 설계도이고 객체는 그 설계도로 만든 실제 인스턴스입니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '예외 처리는 어떤 식으로 작성해?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'try-except 문으로 예외 발생 가능 구간을 감싸고 상황별로 처리합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'user', '파일 읽기 예제도 하나 보여줄래?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'assistant', 'with open("sample.txt", "r", encoding="utf-8") as f: data = f.read() 형태로 많이 작성합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'user', '이분 탐색은 언제 쓰나요?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'assistant', '정렬된 데이터에서 빠르게 값을 찾을 때 사용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'user', '정규화는 왜 필요한가요?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'assistant', '중복을 줄이고 데이터 일관성을 높이기 위해 사용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-04'), 'user', 'HTML과 CSS 역할 차이가 뭐야?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-04'), 'assistant', 'HTML은 구조, CSS는 스타일을 담당합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-05'), 'user', 'REST API는 어떤 규칙을 따르나요?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-05'), 'assistant', '리소스 중심 URL, HTTP 메서드 활용, 무상태성 같은 원칙을 따릅니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-07'), 'user', 'TCP와 UDP 차이점을 알려줘.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-07'), 'assistant', 'TCP는 연결 지향적이고 신뢰성을 보장하며, UDP는 빠르지만 손실 가능성이 있습니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-08'), 'user', '프로세스와 스레드 차이는 뭐야?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-08'), 'assistant', '프로세스는 독립된 실행 단위이고 스레드는 같은 프로세스 안의 작업 흐름입니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-09'), 'user', '자바에서 인터페이스는 왜 써?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-09'), 'assistant', '구현 클래스 간 공통 계약을 정의하고 다형성을 높이기 위해 사용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-10'), 'user', 'JWT는 왜 서명을 하나요?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-10'), 'assistant', '토큰이 위변조되지 않았는지 검증하기 위해 서명을 사용합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-11'), 'user', '오토스케일링은 어떤 상황에 필요해?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-11'), 'assistant', '트래픽이 변동될 때 서버 수를 자동으로 늘리거나 줄이기 위해 필요합니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-12'), 'user', '데이터 파이프라인은 보통 어떻게 구성돼?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-12'), 'assistant', '수집, 저장, 변환, 적재, 분석 단계로 나누어 구성하는 경우가 많습니다.', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-06'), 'user', '관리자 화면에서 어떤 로그를 봐야 할까?', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-06'), 'assistant', '인증 실패, 서버 오류, 주요 요청 로그를 우선 보는 것이 좋습니다.', CURRENT_TIMESTAMP);

-- 업로드 파일 더미 데이터
INSERT INTO uploaded_files (room_id, file_name, file_path, created_at)
VALUES
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_01.pdf', 'uploads/dummy/room01/python_intro_01.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_02.pdf', 'uploads/dummy/room01/python_intro_02.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_03.pdf', 'uploads/dummy/room01/python_intro_03.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_04.pdf', 'uploads/dummy/room01/python_intro_04.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_05.pdf', 'uploads/dummy/room01/python_intro_05.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_06.pdf', 'uploads/dummy/room01/python_intro_06.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-01'), 'python_intro_07.pdf', 'uploads/dummy/room01/python_intro_07.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-02'), 'algorithm_basic.pdf', 'uploads/dummy/room02/algorithm_basic.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-03'), 'database_normalization.pdf', 'uploads/dummy/room03/database_normalization.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-07'), 'network_handshake.pdf', 'uploads/dummy/room07/network_handshake.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-08'), 'process_thread_notes.pdf', 'uploads/dummy/room08/process_thread_notes.pdf', CURRENT_TIMESTAMP),
    ((SELECT id FROM chat_rooms WHERE title = 'dummy-room-09'), 'java_interface_guide.pdf', 'uploads/dummy/room09/java_interface_guide.pdf', CURRENT_TIMESTAMP);

COMMIT;
