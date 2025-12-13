import os
import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import time
import re

# ==========================================
# 1. 환경 설정 및 에이전트 정의
# ==========================================

# ✅ GitHub 업로드 안전 버전:
#   - API 키를 코드에 절대 넣지 않고 환경변수로만 받음
#   - Windows(PowerShell): setx GOOGLE_API_KEY "YOUR_KEY"
#   - 새 터미널에서 실행 후: streamlit run app.py
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    st.set_page_config(page_title="꼬마 작가님의 4컷 만화 일기장", layout="centered")
    st.error("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.\n\n"
             "Windows(PowerShell):  setx GOOGLE_API_KEY \"YOUR_KEY\"\n"
             "macOS/Linux:          export GOOGLE_API_KEY=\"YOUR_KEY\"\n\n"
             "설정 후 새 터미널에서 다시 실행하세요.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# [Painter 에이전트] 이미지를 그리는 역할 (재시도 로직 포함)
def painter_agent(prompt: str):
    max_retries = 3
    last_err = None
    for i in range(max_retries):
        try:
            encoded_prompt = requests.utils.quote(prompt)
            image_url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                f"?width=1024&height=1024&nologo=true&seed={int(time.time()) + i}"
            )
            r = requests.get(image_url, timeout=60)
            r.raise_for_status()
            return Image.open(BytesIO(r.content)).convert("RGB")
        except Exception as e:
            last_err = e
            if i < max_retries - 1:
                time.sleep(3)
            else:
                raise last_err

def to_4_lines(text: str):
    """LLM 응답에서 번호/불릿 제거 후 4줄만 반환"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        s = re.sub(r"^\s*[\-\*\d\.\)\]]+\s*", "", s)
        if s:
            out.append(s)
    return out[:4]

# ==========================================
# 2. UI 디자인 (CSS)
# ==========================================
st.set_page_config(page_title="꼬마 작가님의 4컷 만화 일기장", layout="centered")

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&display=swap" rel="stylesheet">

<style>
:root{
  --paper:#fffaf0;
  --ink:#3b2f2a;
  --muted:#7a6a63;
  --accent:#ff7a59;
  --card:#ffffff;
  --border:#3b2f2a1f;
  --shadow: 0 10px 30px rgba(0,0,0,.08);
}

html, body, [class*="css"] {
  font-family: "Noto Sans KR", sans-serif !important;
}

.stApp { background: var(--paper); color: var(--ink); }

.hero{
  background: linear-gradient(180deg, #fff 0%, #fff6ea 100%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 22px 22px 18px 22px;
  box-shadow: var(--shadow);
  margin-bottom: 14px;
}

.hero-title{
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--ink);
  margin: 0;
}

.card{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  box-shadow: var(--shadow);
  margin-bottom: 14px;
}

.stButton > button{
  width: 100%;
  border-radius: 999px;
  height: 3.2rem;
  font-weight: 800;
  color: white;
  background: linear-gradient(90deg, var(--accent) 0%, #ff946f 100%);
  border: none;
}

.panel{
  background:#fff;
  border: 4px solid #3b2f2a;
  border-radius: 16px;
  padding: 10px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}

.caption{
  margin-top: 10px;
  font-weight: 800;
  text-align: center;
}

.bubble{
  position: relative;
  margin: 10px auto 0 auto;
  padding: 10px 12px;
  background: #fff8f2;
  border: 1px solid var(--border);
  border-radius: 14px;
  font-size: .98rem;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 메인 화면 구성
# ==========================================
st.markdown("""
<div class="hero">
  <div style="display:inline-block; padding:6px 10px; border-radius:999px; font-weight:800; font-size:.85rem; background: #fff3ea; border: 1px solid var(--border);">
    🎨 에이전트 협업형
  </div>
  <h1 class="hero-title">꼬마 작가님의 4컷 만화 일기장</h1>
  <p style="color:var(--muted);">오늘의 소중한 기억을 읽고 따뜻한 만화로 그려드려요.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
diary_text = st.text_area("📝 오늘의 일기", height=170, placeholder="예: 오늘 유치원에서 친구랑 모래성 쌓기를 했다. 정말 재미있었다!")

colA, colB, colC = st.columns(3)
with colA:
    comic_style = st.selectbox("그림 분위기", ["따뜻한 동화책", "심플한 4컷", "웹툰풍"])
with colB:
    tone = st.selectbox("말풍선 톤", ["아이 말투 그대로", "조금 더 또박또박", "짧고 귀엽게"])
with colC:
    seed_mode = st.selectbox("그림 변화", ["매번 새롭게", "비슷하게(고정)"])

make_btn = st.button("✨ 에이전트 협업하여 만화 만들기")
st.markdown("</div>", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("Project Info")
    st.write("이 앱은 **Multi-Agent** 구조로 작동합니다.")
    st.write("1) **Planner**: 장면 기획")
    st.write("2) **Designer**: 프롬프트 설계")
    st.write("3) **Painter**: 이미지 생성")
    st.markdown("---")
    st.caption("GitHub 업로드 안전 버전 (v2025.12.13)")

# ==========================================
# 4. 실행 로직 (멀티 에이전트 워크플로우)
# ==========================================
if make_btn:
    if not diary_text.strip():
        st.warning("일기 내용을 입력해주세요!")
        st.stop()

    try:
        # 스타일 가이드
        style_line = {
            "따뜻한 동화책": "Warm hand-drawn watercolor illustration, children's picture book texture, soft pastel colors",
            "심플한 4컷": "Clean 2D cute cartoon, simple lines, bright warm colors, minimal background",
            "웹툰풍": "Korean webtoon style, clean outlines, lively expressions, soft warm palette",
        }[comic_style]

        tone_line = {
            "아이 말투 그대로": "Keep dialogues in child's natural Korean tone.",
            "조금 더 또박또박": "Make dialogues clear and polite but still child-like.",
            "짧고 귀엽게": "Use short, cute dialogues.",
        }[tone]

        fixed_seed = 777 if seed_mode.startswith("비슷하게") else int(time.time())

        # --- Step 1: 장면 기획 (Planner Agent) ---
        with st.status("🛠️ 1단계: 장면 기획 에이전트가 스토리를 나누는 중...", expanded=True):
            planner_prompt = (
                "당신은 아동 4컷 만화 작가입니다. 아래 일기를 읽고 시간 흐름에 따라 장면 4개를 기획하세요.\n\n"
                f"[일기]\n{diary_text}\n\n"
                "[형식]\n- 반드시 4줄\n- 번호 형식(1) ..., 2) ...)\n"
                "- 각 줄은 한 문장으로 짧게"
            )
            scenes_res = model.generate_content(planner_prompt).text
            st.info(scenes_res)

        # --- Step 2: 프롬프트 및 대사 설계 (Designer Agent) ---
        with st.status("🎨 2단계: 디자이너 에이전트가 그림과 대사를 설계 중...", expanded=True):
            designer_prompt = (
                "You are an image prompt engineer.\n"
                "Based on the scenes below, write EXACTLY 4 English prompts (one per line).\n\n"
                f"[Scenes]\n{scenes_res}\n\n"
                "[Fixed main character]\n- A 7-year-old Korean child\n- Yellow t-shirt\n- Same hairstyle and outfit in all panels (consistency)\n\n"
                f"[Style]\n- {style_line}\n\n"
                "[Output rules]\n- Output ONLY 4 lines.\n- No numbering, no bullets, no extra text."
            )
            prompts_res = model.generate_content(designer_prompt).text
            prompts = to_4_lines(prompts_res)

            speech_prompt = (
                "당신은 만화 대사 작가입니다.\n"
                f"아래 장면(4개)에 맞는 짧은 한국어 말풍선 대사를 {tone} 톤으로 4줄 써주세요.\n\n"
                f"[장면]\n{scenes_res}\n\n"
                "[형식]\n- 반드시 4줄\n- 번호/불릿 없이 대사만(한 줄당 한 대사)\n- 15~40자 내"
            )
            speech_res = model.generate_content(speech_prompt).text
            speech_lines = to_4_lines(speech_res)

            # 방어: 4개 미만일 경우 사용자에게 알림
            if len(prompts) < 4:
                st.warning("이미지 프롬프트가 4개 미만으로 생성되었습니다. 일기를 조금 더 자세히 써보거나 다시 시도해 주세요.")
            if len(speech_lines) < 4:
                st.warning("말풍선 대사가 4개 미만으로 생성되었습니다. 다시 시도해 주세요.")

            st.success("프롬프트와 대사가 준비되었습니다!")

        # --- Step 3: 이미지 생성 및 출력 (Painter Agent) ---
        st.markdown("---")
        st.subheader("🖼️ 에이전트들이 협동해서 그린 4컷 만화")

        col1, col2 = st.columns(2)
        for i in range(4):
            target = col1 if i % 2 == 0 else col2
            with target:
                with st.status(f"{i+1}번 장면 그리는 중...", expanded=False) as status:
                    try:
                        prompt_i = prompts[i] if i < len(prompts) else "cute children book illustration, warm scene"
                        # 고정 시드 옵션을 이미지 URL에도 반영해 재현성 약간 확보
                        prompt_i = f"{prompt_i}, same main character, yellow t-shirt, panel {i+1}"
                        encoded = requests.utils.quote(prompt_i)
                        image_url = (
                            f"https://image.pollinations.ai/prompt/{encoded}"
                            f"?width=1024&height=1024&nologo=true&seed={fixed_seed+i}"
                        )

                        # painter_agent를 쓰되, URL을 직접 만들고 싶으면 아래 둘 중 하나만 사용:
                        # 1) painter_agent(prompt_i)
                        # img = painter_agent(prompt_i)

                        # 2) 현재 URL 방식(고정 seed 보장)
                        r = requests.get(image_url, timeout=60)
                        r.raise_for_status()
                        img = Image.open(BytesIO(r.content)).convert("RGB")

                        st.markdown('<div class="panel">', unsafe_allow_html=True)
                        st.image(img, use_container_width=True)
                        st.markdown(f'<div class="caption">장면 {i+1}</div>', unsafe_allow_html=True)

                        bubble_text = speech_lines[i] if i < len(speech_lines) else ""
                        if bubble_text:
                            st.markdown(f'<div class="bubble">{bubble_text}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        status.update(label=f"{i+1}번 장면 완성!", state="complete")
                    except Exception:
                        st.error(f"{i+1}번 장면 생성 실패 (서버 과부하/네트워크 오류)")
                        status.update(label="그리기 실패", state="error")

        st.balloons()
        st.success("완성! 꼬마 작가님의 4컷 만화 일기장이 만들어졌습니다.")

    except Exception as e:
        if "429" in str(e):
            st.error("현재 서버 할당량이 초과되었습니다. 1~2분만 기다렸다가 다시 시도해 주세요!")
        else:
            st.error(f"오류가 발생했습니다: {e}")
