# 꼬마 작가님의 4컷 만화 일기장
멀티 에이전트(Planner/Designer/Painter) 협업 기반으로 일기 텍스트를 4컷 만화로 생성하는 Streamlit 앱입니다.

## Features
- Scene Planner (Gemini): 일기를 4개 장면으로 분할
- Prompt Designer (Gemini): 장면별 이미지 프롬프트 + 말풍선 대사 생성
- Painter (Pollinations): 4컷 이미지 생성
- Streamlit UI: 진행 상태 표시 및 2x2 만화 출력

## Tech Stack
- Python, Streamlit
- Google Gemini 2.5 Flash API
- Pollinations (image generation)
- CSS (Noto Sans KR)

## Run (Local)
### 1) Install
```bash
pip install -r requirements.txt