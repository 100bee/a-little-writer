# 꼬마 작가님의 4컷 만화 일기장

> 멀티 에이전트(Planner · Designer · Painter) 협업으로 일기 텍스트를 4컷 만화로 자동 생성하는 Streamlit 앱

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=flat-square&logo=google&logoColor=white)

---

## Overview

일기 텍스트를 입력하면 3개의 AI 에이전트가 협업하여 자동으로 4컷 만화를 생성합니다.

```
[일기 텍스트 입력]
       ↓
 Planner Agent   — Gemini가 일기를 4개 장면으로 분할
       ↓
 Designer Agent  — 장면별 이미지 프롬프트 + 말풍선 대사 생성
       ↓
 Painter Agent   — Pollinations API로 4컷 이미지 생성
       ↓
  [2×2 만화 출력]
```

---

## 🛠️ Tech Stack

| 역할 | 기술 |
|------|------|
| UI | Python, Streamlit |
| LLM (장면 기획 · 대사 생성) | Google Gemini 2.5 Flash API |
| 이미지 생성 | Pollinations AI |
| 폰트 | Noto Sans KR (Google Fonts) |

---

## Features

- **멀티 에이전트 구조** — Planner / Designer / Painter 역할 분리
- **그림 스타일 선택** — 따뜻한 동화책 / 심플한 4컷 / 웹툰풍
- **말풍선 톤 선택** — 아이 말투 그대로 / 또박또박 / 짧고 귀엽게
- **캐릭터 일관성** — 매 컷 동일한 주인공 유지 (프롬프트 고정)
- **재시도 로직** — 이미지 생성 실패 시 최대 3회 재시도

---

## Getting Started

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. API 키 환경변수 설정

```bash
# macOS / Linux
export GOOGLE_API_KEY="your_gemini_api_key"

# Windows (PowerShell)
setx GOOGLE_API_KEY "your_gemini_api_key"
```

> ⚠️ API 키를 코드에 직접 넣지 마세요. 환경변수로만 관리합니다.

### 3. 실행

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
a-little-writer/
├── app.py              # 메인 앱 (멀티 에이전트 로직 + UI)
├── requirements.txt    # 의존성 목록
├── 일기장예시.txt       # 입력 예시 텍스트
└── .gitignore
```

---

## 💡 배운 점 / 회고

- **멀티 에이전트 설계** — 하나의 LLM에 모든 역할을 맡기는 대신 Planner / Designer / Painter로 역할을 분리하면 각 단계의 품질과 제어성이 높아진다는 것을 경험했습니다.
- **프롬프트 엔지니어링** — 캐릭터 일관성 유지를 위해 프롬프트에 고정 속성(옷 색상, 헤어스타일)을 명시하는 방식을 적용했습니다.
- **외부 API 연동** — Gemini API와 Pollinations API를 함께 활용하며 타임아웃 처리 및 재시도 로직의 중요성을 깨달았습니다.
