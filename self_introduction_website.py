import streamlit as st
import random
import time

# ============================================================
#  页面配置
# ============================================================
st.set_page_config(
    page_title="孙杰伟 | AI Agent Developer",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
#  调色板 & 常量
# ============================================================
GLACIER      = "#00D4FF"
GLACIER_LIGHT= "#7EE8FA"
GLACIER_DIM  = "#4A9EAF"
DEEP_BG      = "#060B18"
CARD_BG      = "#0D1B2A"
TERMINAL_BG  = "#0A0F1A"
TEXT_PRIMARY  = "#E0F0FF"
TEXT_SECONDARY= "#8BA4B8"
ACCENT_PURPLE= "#8B5CF6"

# ============================================================
#  CSS — 星空 / 动画 / 全局样式
# ============================================================
STAR_CSS = "\n".join(
    f".s{i}{{position:absolute;border-radius:50%;background:#fff;"
    f"width:{random.choice([1,1,2,2,3])}px;"
    f"height:{random.choice([1,1,2,2,3])}px;"
    f"top:{random.uniform(0,100):.1f}%;left:{random.uniform(0,100):.1f}%;opacity:{random.uniform(0.15,0.85):.2f};"
    f"animation:twinkle {random.uniform(2,6):.1f}s ease-in-out {random.uniform(0,4):.1f}s infinite}}"
    for i in range(180)
)

MAIN_CSS = f"""
<style>
/* ===== 全局 ===== */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

.stApp {{
    background: {DEEP_BG} !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.03) 0%, transparent 60%) !important;
}}
section[data-testid="stSidebar"] {{ display: none; }}
header[data-testid="stHeader"] {{
    background: transparent !important;
    backdrop-filter: blur(8px);
}}
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 900px !important;
}}
.stMarkdown {{ color: {TEXT_PRIMARY}; }}
a {{ color: {GLACIER} !important; }}

/* ===== 星空 ===== */
@keyframes twinkle {{
    0%,100%{{ opacity:0.15; transform:scale(0.8); }}
    50%{{ opacity:1; transform:scale(1.3); }}
}}
@keyframes shootingStar {{
    0%{{ transform:translateX(0) translateY(0) rotate(-45deg); opacity:1; }}
    70%{{ opacity:1; }}
    100%{{ transform:translateX(600px) translateY(600px) rotate(-45deg); opacity:0; }}
}}
.starfield {{
    position:fixed; top:0; left:0; width:100%; height:100%;
    z-index:-1; pointer-events:none;
}}
.shooting-star {{
    position:absolute; width:100px; height:1px;
    background:linear-gradient(to right, rgba(255,255,255,0), {GLACIER});
    animation: shootingStar 4s ease-in-out infinite;
}}
.shooting-star:nth-child(2) {{
    top:15%; left:-5%; animation-delay:2s; animation-duration:5s;
}}
.shooting-star:nth-child(3) {{
    top:45%; left:-10%; animation-delay:6s; animation-duration:4.5s;
}}
{STAR_CSS}

/* ===== 动画 ===== */
@keyframes gradientShift {{
    0%{{ background-position:0% 50%; }}
    50%{{ background-position:100% 50%; }}
    100%{{ background-position:0% 50%; }}
}}
@keyframes typewriter {{
    from {{ width:0; }}
    to   {{ width:24ch; }}
}}
@keyframes blink {{
    0%,100%{{ border-color:{GLACIER}; }}
    50%{{ border-color:transparent; }}
}}
@keyframes float {{
    0%,100%{{ transform:translateY(0px); }}
    50%{{ transform:translateY(-6px); }}
}}
@keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(24px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes pulseRing {{
    0%{{ box-shadow:0 0 0 0 rgba(0,212,255,0.35); }}
    70%{{ box-shadow:0 0 0 14px rgba(0,212,255,0); }}
    100%{{ box-shadow:0 0 0 0 rgba(0,212,255,0); }}
}}
@keyframes borderGlow {{
    0%,100%{{ border-color:rgba(0,212,255,0.12); }}
    50%{{ border-color:rgba(0,212,255,0.35); }}
}}

/* ===== Hero ===== */
.hero-title {{
    font-family:'Inter',sans-serif;
    font-size:3.2rem; font-weight:700; text-align:center;
    background:linear-gradient(135deg,{GLACIER_LIGHT},{GLACIER},{ACCENT_PURPLE},{GLACIER});
    background-size:300% 300%;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
    animation:gradientShift 5s ease infinite;
    margin:2rem 0 0.3rem; line-height:1.2;
}}
.hero-sub {{
    font-family:'JetBrains Mono',monospace;
    font-size:1rem; color:{TEXT_SECONDARY}; text-align:center;
    overflow:hidden; white-space:nowrap;
    border-right:3px solid {GLACIER};
    width:0; margin:0 auto;
    animation:typewriter 2.8s steps(28,end) 0.6s forwards, blink 0.75s step-end infinite;
}}
.hero-tagline {{
    text-align:center; color:{TEXT_SECONDARY};
    font-size:0.88rem; margin-top:1rem;
    animation:fadeUp 1s ease 3.5s both;
}}

/* ===== ASCII ===== */
.ascii-box {{
    font-family:'JetBrains Mono',monospace;
    color:{GLACIER_DIM}; font-size:0.6rem; line-height:1.15;
    text-align:center; white-space:pre;
    margin:1.5rem auto 0; opacity:0.55;
}}
.ascii-line {{
    height:1px; width:100%; margin:0.6rem 0;
    background:linear-gradient(to right,transparent,{GLACIER_DIM},transparent);
    opacity:0.35;
}}
.section-hdr {{
    font-family:'JetBrains Mono',monospace;
    color:{GLACIER}; font-size:1.25rem; font-weight:700;
    margin:2.5rem 0 1rem;
    display:flex; align-items:center; gap:0.7rem;
    animation:fadeUp 0.6s ease both;
}}
.section-hdr .ico {{
    display:inline-flex; align-items:center; justify-content:center;
    width:2.2rem; height:2.2rem;
    border:1.5px solid {GLACIER}; border-radius:8px;
    font-size:0.95rem;
    animation:pulseRing 2.5s ease infinite;
}}

/* ===== 卡片 ===== */
.glow-card {{
    background:{CARD_BG};
    border:1px solid rgba(0,212,255,0.12);
    border-radius:12px; padding:1.4rem;
    position:relative; overflow:hidden;
    animation:fadeUp 0.7s ease both, borderGlow 4s ease infinite;
    transition:transform 0.3s, box-shadow 0.3s;
}}
.glow-card:hover {{
    transform:translateY(-3px);
    box-shadow:0 8px 30px rgba(0,212,255,0.08);
}}
.glow-card::after {{
    content:''; position:absolute; top:0; left:-100%;
    width:60%; height:100%;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.04),transparent);
    transition:left 0.6s ease;
}}
.glow-card:hover::after {{ left:120%; }}

/* ===== 终端 ===== */
.terminal {{
    background:{TERMINAL_BG};
    border:1px solid rgba(0,212,255,0.18);
    border-radius:10px; overflow:hidden;
    margin:1rem 0;
    animation:fadeUp 0.8s ease both;
}}
.terminal-bar {{
    background:#111827; padding:0.45rem 1rem;
    display:flex; align-items:center; gap:0.45rem;
    border-bottom:1px solid rgba(0,212,255,0.08);
}}
.dot-r{{ color:#FF5F56; }} .dot-y{{ color:#FFBD2E; }} .dot-g{{ color:#27C93F; }}
.terminal-title {{
    font-family:'JetBrains Mono',monospace;
    color:{TEXT_SECONDARY}; font-size:0.7rem; margin-left:0.8rem;
}}
.terminal-body {{
    font-family:'JetBrains Mono',monospace;
    font-size:0.82rem; color:{TEXT_PRIMARY};
    padding:1.1rem 1.2rem; line-height:1.85;
}}
.prompt {{ color:{GLACIER}; font-weight:700; }}
.comment {{ color:#546178; }}
.val {{ color:{GLACIER_LIGHT}; }}
.key {{ color:#C792EA; }}
.str {{ color:#C3E88D; }}

/* ===== 徽章 ===== */
.badge {{
    display:inline-block;
    padding:0.35rem 0.85rem; margin:0.25rem;
    border-radius:20px; font-size:0.8rem;
    font-family:'JetBrains Mono',monospace;
    animation:float 3s ease infinite;
    transition:transform 0.2s;
}}
.badge:hover {{ transform:scale(1.12) !important; }}
.b0{{ background:rgba(0,212,255,0.10); color:{GLACIER_LIGHT}; border:1px solid rgba(0,212,255,0.25); }}
.b1{{ background:rgba(139,92,246,0.10); color:#A78BFA; border:1px solid rgba(139,92,246,0.25); }}
.b2{{ background:rgba(52,211,153,0.10); color:#6EE7B7; border:1px solid rgba(52,211,153,0.25); }}
.b3{{ background:rgba(251,191,36,0.10); color:#FCD34D; border:1px solid rgba(251,191,36,0.25); }}

/* ===== 特性列表 ===== */
.feat {{
    padding:0.7rem 1rem; margin:0.4rem 0;
    border-left:3px solid {GLACIER};
    background:rgba(0,212,255,0.025);
    border-radius:0 8px 8px 0;
    animation:fadeUp 0.5s ease both;
    transition:border-color 0.3s, background 0.3s;
}}
.feat:hover {{
    border-left-color:{GLACIER_LIGHT};
    background:rgba(0,212,255,0.06);
}}
.feat-title {{
    color:{GLACIER_LIGHT}; font-weight:600;
    font-size:0.92rem; margin-bottom:0.15rem;
}}
.feat-desc {{ color:{TEXT_SECONDARY}; font-size:0.82rem; }}

/* ===== 优势 ===== */
.adv {{
    padding:0.9rem 1.1rem; margin:0.45rem 0;
    background:{CARD_BG}; border-radius:10px;
    border-left:3px solid {GLACIER};
    animation:fadeUp 0.6s ease both;
    transition:border-color 0.3s, transform 0.2s;
}}
.adv:hover {{ border-left-color:{GLACIER_LIGHT}; transform:translateX(4px); }}
.adv-t {{ color:{GLACIER_LIGHT}; font-weight:600; font-size:0.95rem; }}
.adv-d {{ color:{TEXT_SECONDARY}; font-size:0.82rem; margin-top:0.2rem; }}

/* ===== 联系按钮 ===== */
.contact-btn {{
    display:inline-block; padding:0.75rem 2rem;
    background:linear-gradient(135deg,{GLACIER},{ACCENT_PURPLE});
    background-size:200% 200%;
    color:#fff !important; text-decoration:none !important;
    border-radius:10px; font-weight:600; font-size:0.95rem;
    margin:0.4rem; transition:all 0.3s;
    animation:gradientShift 4s ease infinite;
}}
.contact-btn:hover {{
    transform:translateY(-3px);
    box-shadow:0 10px 28px rgba(0,212,255,0.25);
}}

/* ===== 隐藏 Streamlit 默认元素 ===== */
#MainMenu, footer, [data-testid="stToolbar"] {{ display:none !important; }}
</style>
"""

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ============================================================
#  星空背景
# ============================================================
_stars = "".join(f'<div class="s{i}"></div>' for i in range(180))
_shooting = '<div class="shooting-star"></div>' * 3
st.markdown(
    f'<div class="starfield">{_stars}{_shooting}</div>',
    unsafe_allow_html=True,
)

# ============================================================
#  ASCII 装饰
# ============================================================
ASCII_BANNER = r"""
 _____ _____ _ _ _       ___        __
|   __|  |  | | | |_ ___|  _|_ _  __|  |
|__   |  |  | | | '_| -_|  _| | || -_|  |__
|_____|_____|___|_,_|___|_| |___||___|_____|
"""

ASCII_SECTION = {
    "about":   "[ // ABOUT ]",
    "strength": "[ // STRENGTHS ]",
    "project": "[ // PROJECT ]",
    "stack":   "[ // TECH_STACK ]",
    "contact": "[ // CONTACT ]",
}

# ============================================================
#  HERO
# ============================================================
st.markdown(f'<pre class="ascii-box">{ASCII_BANNER}</pre>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Sun Jiewei</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">AI Agent Developer & Explorer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-tagline">'
    'Nanchang University &middot; Artificial Intelligence &middot; Class of 2027'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="ascii-line"></div>', unsafe_allow_html=True)

# ============================================================
#  ABOUT
# ============================================================
st.markdown(
    f'<div class="section-hdr"><span class="ico">01</span>{ASCII_SECTION["about"]}</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="terminal"><div class="terminal-bar">'
    '<span class="dot-r">*</span><span class="dot-y">*</span><span class="dot-g">*</span>'
    '<span class="terminal-title">~/about_me.sh</span></div>'
    '<div class="terminal-body">'
    f'<span class="prompt">$</span> <span class="key">cat</span> profile.json<br><br>'
    '{<br>'
    f'&nbsp;&nbsp;<span class="key">"name"</span>: <span class="str">"孙杰伟"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"university"</span>: <span class="str">"南昌大学 (211)"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"major"</span>: <span class="str">"人工智能 · AI 实验班"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"focus"</span>: [<span class="str">"LLM"</span>, <span class="str">"Agent"</span>, <span class="str">"RAG"</span>],<br>'
    f'&nbsp;&nbsp;<span class="key">"seeking"</span>: <span class="str">"Agent 实习 / 工作机会"</span><br>'
    '}<br><br>'
    f'<span class="prompt">$</span> <span class="key">echo</span> <span class="str">"About"</span><br><br>'
    f'<span class="comment">#  热衷于探索 LLM + Agent 的应用边界，注重工程化思维与实际落地</span><br>'
    f'<span class="comment">#  独立开发智能编程助手 Agent，擅长 Prompt Engineering & Advanced RAG</span><br>'
    f'<span class="comment">#  希望将大语言模型的能力转化为解决实际问题的工具</span><br>'
    '<br><span class="prompt">$</span> <span class="blink-cursor">_</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="ascii-line"></div>', unsafe_allow_html=True)

# ============================================================
#  STRENGTHS
# ============================================================
st.markdown(
    f'<div class="section-hdr"><span class="ico">02</span>{ASCII_SECTION["strength"]}</div>',
    unsafe_allow_html=True,
)

advantages = [
    ("Project Delivery", "独立开发 Agent 项目并部署至 Hugging Face Space，掌握从开发到上线的完整流程"),
    ("Self-Driven", "围绕目标岗位主动学习 LangChain / LangGraph / RAG / LlamaIndex / MCP 等技术，快速产出可用原型"),
    ("Teamwork", "担任过团支书，重视沟通与协作，积极配合团队目标，具备良好执行力"),
    ("Academic", "南昌大学 AI 实验班（211），课程与自学结合，持续跟进 LLM + Agent 前沿方向"),
]
for i, (title, desc) in enumerate(advantages):
    st.markdown(
        f'<div class="adv" style="animation-delay:{i*0.12}s">'
        f'<div class="adv-t">{title}</div>'
        f'<div class="adv-d">{desc}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="ascii-line"></div>', unsafe_allow_html=True)

# ============================================================
#  PROJECT
# ============================================================
st.markdown(
    f'<div class="section-hdr"><span class="ico">03</span>{ASCII_SECTION["project"]}</div>',
    unsafe_allow_html=True,
)

# 项目卡片
st.markdown(
    '<div class="glow-card" style="animation-delay:0.1s">'
    '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">'
    '<div style="font-size:1.2rem;font-weight:700;color:#7EE8FA">'
    'Coding Assistant Agent</div>'
    '<div style="font-size:0.75rem;color:#8BA4B8;font-family:\'JetBrains Mono\',monospace">'
    'v1.0 / production</div></div>'
    '<div style="color:#8BA4B8;font-size:0.88rem;margin-top:0.4rem">'
    '基于 LangChain + LangGraph 的智能编程助手，支持代码生成、调试、RAG 知识检索</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.link_button("Open Project on HF Spaces", "https://jieweisun-coding-agent.hf.space")

st.markdown("<br>", unsafe_allow_html=True)

# 技术栈 - 终端风格
st.markdown(
    '<div class="terminal"><div class="terminal-bar">'
    '<span class="dot-r">*</span><span class="dot-y">*</span><span class="dot-g">*</span>'
    '<span class="terminal-title">tech_stack.toml</span></div>'
    '<div class="terminal-body">'
    f'<span class="comment"># Core Stack</span><br>'
    f'<span class="key">agent_framework</span> = <span class="str">"LangChain 1.x + LangGraph"</span><br>'
    f'<span class="key">llm_provider</span>&nbsp;&nbsp; = <span class="str">"阿里百炼 qwen-max"</span><br>'
    f'<span class="key">vector_db</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"Chroma"</span><br>'
    f'<span class="key">embedding</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"阿里百炼 text-embedding-v3"</span><br>'
    f'<span class="key">frontend</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"Gradio 6.x"</span><br>'
    f'<span class="key">deployment</span>&nbsp;&nbsp;&nbsp; = <span class="str">"Hugging Face Spaces"</span><br><br>'
    f'<span class="comment"># Role</span><br>'
    f'<span class="key">role</span> = <span class="str">"独立开发者 (全栈 + Prompt Engineering)"</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# 成果亮点
st.markdown(
    '<div style="font-family:\'JetBrains Mono\',monospace;color:#7EE8FA;'
    'font-size:0.95rem;margin-bottom:0.8rem">## features.md</div>',
    unsafe_allow_html=True,
)
features = [
    ("Secure Code Execution", "子进程 + 临时文件 + 超时机制隔离执行 Python 代码"),
    ("Local RAG Retrieval", "Chroma 向量库 + 阿里百炼 Embedding 检索私有文档"),
    ("Multi-turn Memory", "LangGraph Checkpointer 自动维护会话上下文"),
    ("Auto Retry", "代码执行出错时 Agent 自动分析错误并重试 (max 3)"),
    ("Free-tier Quota", "基于 IP 的终身 10 次免费试用，支持自定义 API Key"),
    ("Web Interface", "Gradio 聊天界面，部署 Hugging Face Spaces 公网访问"),
]
for i, (title, desc) in enumerate(features):
    st.markdown(
        f'<div class="feat" style="animation-delay:{i*0.08}s">'
        f'<div class="feat-title">> {title}</div>'
        f'<div class="feat-desc">&nbsp; {desc}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="ascii-line"></div>', unsafe_allow_html=True)

# ============================================================
#  TECH STACK
# ============================================================
st.markdown(
    f'<div class="section-hdr"><span class="ico">04</span>{ASCII_SECTION["stack"]}</div>',
    unsafe_allow_html=True,
)

techs = [
    "LangChain", "LangGraph", "RAG", "Prompt Engineering",
    "LlamaIndex", "MCP", "Docker", "Streamlit",
    "FastAPI", "PyTorch", "MySQL", "Python",
]
badges_html = "".join(
    f'<span class="badge b{i%4}" style="animation-delay:{i*0.18}s">{t}</span>'
    for i, t in enumerate(techs)
)
st.markdown(
    f'<div class="glow-card" style="text-align:center;padding:1.5rem;animation-delay:0.2s">'
    f'{badges_html}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="ascii-line"></div>', unsafe_allow_html=True)

# ============================================================
#  CONTACT
# ============================================================
st.markdown(
    f'<div class="section-hdr"><span class="ico">05</span>{ASCII_SECTION["contact"]}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="text-align:center;margin:1.5rem 0">'
    '<a class="contact-btn" href="https://github.com/jws573/coding-assistant-agent" target="_blank">'
    '> GitHub Repository</a>'
    '<a class="contact-btn" href="mailto:3028789475@qq.com">'
    '> Email Me</a>'
    '</div>',
    unsafe_allow_html=True,
)

# 页脚
st.markdown(
    '<div class="ascii-line"></div>'
    '<div style="text-align:center;padding:1.5rem 0">'
    '<pre style="font-family:\'JetBrains Mono\',monospace;color:#4A9EAF;'
    'font-size:0.65rem;opacity:0.5;margin:0">'
    '/* Built with Streamlit | Designed by Sun Jiewei */\n'
    '/* EOF */'
    '</pre>'
    '<div style="font-family:\'JetBrains Mono\',monospace;'
    f'color:{TEXT_SECONDARY};font-size:0.8rem;margin-top:0.5rem">'
    'Thank you for visiting. Let\'s build the future of AI Agents together.'
    '</div></div>',
    unsafe_allow_html=True,
)
