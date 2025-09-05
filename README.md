# 🎮 Multi-Game Discord Helper Bot

여러 게임의 API를 활용하여 게임 정보를 조회해주는 디스코드 도우미 봇입니다.

## ✨ 주요 기능

### 🎯 Apex Legends
- **전적 조회**: `!전적 [플레이어명]` - 플레이어의 상세 전적 정보 조회
- **맵 로테이션**: `!맵테스트` - 현재 맵 로테이션 상태 확인
- **자동 맵 알림**: 특정 맵(E-District, Broken Moon) 감지 시 자동 알림
- **한글 지원**: 레전드 이름과 맵 이름을 한글로 표시

### 🍁 MapleStory (예정)
- 메이플스토리 캐릭터 정보 조회 기능 (개발 중)

### 😀 이모티콘 확대
- **자동 확대**: 메시지에 이모티콘이 포함되면 자동으로 확대해서 표시
- **수동 확대**: `!이모지확대 [이모티콘]` - 특정 이모티콘을 확대해서 보기
- **서버 이모티콘**: `!서버이모지` - 서버의 모든 커스텀 이모티콘 목록 보기
- **커스텀/유니코드 지원**: 디스코드 커스텀 이모티콘과 유니코드 이모티콘 모두 지원

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/사용자명/apex_bot.git
cd apex_bot
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 입력하세요:
```env
DISCORD_TOKEN=your_discord_bot_token_here
APEX_API_KEY=your_apex_api_key_here
```

### 4. 봇 실행
```bash
python main.py
```

## 📋 필요한 API 키

### Discord Bot Token
1. [Discord Developer Portal](https://discord.com/developers/applications)에서 새 애플리케이션 생성
2. Bot 섹션에서 토큰 복사
3. OAuth2 > URL Generator에서 필요한 권한 선택:
   - Send Messages
   - Embed Links
   - Read Message History

### Apex Legends API Key
1. [Apex Legends API](https://apexlegendsapi.com/)에서 API 키 발급
2. 무료 플랜으로도 기본 기능 사용 가능

## 🛠️ 프로젝트 구조

```
apex_bot/
├── main.py                 # 봇 메인 파일
├── cogs/                   # 기능별 모듈 (Cogs)
│   ├── __init__.py
│   ├── apex_cog.py        # Apex Legends 관련 기능
│   └── maplestory_cog.py  # 메이플스토리 관련 기능 (개발 중)
├── .env                   # 환경 변수 (Git에 업로드되지 않음)
├── .gitignore            # Git 무시 파일 목록
└── README.md             # 프로젝트 설명서
```

## 🎮 사용법

### Apex Legends 명령어

#### 전적 조회
```
!전적 [플레이어명]
```
- 플레이어의 랭크, 킬, K/D, 주력 레전드 등 상세 정보 표시
- 상위 3개 레전드의 킬 수와 상위 퍼센트 표시

#### 맵 로테이션 확인
```
!맵테스트
```
- 현재 일반게임/랭크 맵 정보
- 남은 시간 표시
- 알림 대상 맵 여부 확인

#### 이모티콘 확대 명령어

#### 특정 이모티콘 확대
```
!이모지확대 [이모티콘]
```
- 커스텀 이모티콘: `<:이모지이름:ID>` 또는 `<a:애니메이션이모지:ID>`
- 유니코드 이모티콘: 😀, 🎮, 🚀 등

#### 서버 이모티콘 목록
```
!서버이모지
```
- 서버의 모든 커스텀 이모티콘을 목록으로 표시

### 자동 기능
- **맵 알림**: 1시간 30분마다 맵 로테이션 체크
- **특정 맵 감지**: E-District, Broken Moon 맵 감지 시 자동 알림
- **이모티콘 자동 확대**: 메시지에 이모티콘이 포함되면 자동으로 확대해서 표시

## 🔧 개발 정보

### 기술 스택
- **Python 3.8+**
- **discord.py** - Discord 봇 프레임워크
- **requests** - HTTP API 요청
- **python-dotenv** - 환경 변수 관리

### Cogs 구조
이 봇은 Discord.py의 Cogs 시스템을 사용하여 모듈화되어 있습니다:
- 각 게임별로 별도의 Cog 파일
- 기능별로 코드가 분리되어 유지보수 용이
- 새로운 게임 기능 추가 시 새 Cog 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**주의**: 이 봇은 개인/교육 목적으로 제작되었습니다. 상업적 사용 시 해당 게임의 API 이용약관을 확인해주세요.
