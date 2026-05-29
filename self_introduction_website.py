import streamlit as st
import random
import json
import os
from datetime import datetime

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
GLACIER       = "#00D4FF"
GLACIER_LIGHT = "#7EE8FA"
GLACIER_DIM   = "#4A9EAF"
DEEP_BG       = "#060B18"
CARD_BG       = "#0D1B2A"
TERMINAL_BG   = "#0A0F1A"
TEXT_PRIMARY   = "#E0F0FF"
TEXT_SECONDARY = "#8BA4B8"
ACCENT_PURPLE = "#8B5CF6"

# ============================================================
#  CSS — 星空 / 流星 / 动画 / 全局样式
# ============================================================
STAR_CSS = "\n".join(
    f".s{i}{{position:absolute;border-radius:50%;background:#fff;"
    f"width:{random.choice([1, 1, 2, 2, 3])}px;"
    f"height:{random.choice([1, 1, 2, 2, 3])}px;"
    f"top:{random.uniform(0, 100):.1f}%;left:{random.uniform(0, 100):.1f}%;"
    f"opacity:{random.uniform(0.15, 0.85):.2f};"
    f"animation:twinkle {random.uniform(2, 6):.1f}s ease-in-out "
    f"{random.uniform(0, 4):.1f}s infinite}}"
    for i in range(200)
)

# 生成 15 颗流星的 CSS
SHOOTING_STARS_CSS = ""
for i in range(15):
    top = random.uniform(-10, 60)
    left = random.uniform(-15, 50)
    dur = random.uniform(2.5, 6.0)
    delay = random.uniform(0, 8)
    width = random.choice([60, 80, 100, 120, 150])
    SHOOTING_STARS_CSS += f"""
.ss{i} {{
    position: absolute;
    width: {width}px; height: 1px;
    top: {top:.1f}%; left: {left:.1f}%;
    background: linear-gradient(to right, rgba(255,255,255,0), {GLACIER}, rgba(255,255,255,0));
    animation: shoot {dur:.1f}s linear {delay:.1f}s infinite;
    opacity: 0;
}}
.ss{i}::after {{
    content: '';
    position: absolute;
    right: 0; top: -1px;
    width: 4px; height: 3px;
    border-radius: 50%;
    background: {GLACIER_LIGHT};
    box-shadow: 0 0 6px 2px rgba(0,212,255,0.4);
}}
"""

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
    0%,100% {{ opacity:0.15; transform:scale(0.8); }}
    50% {{ opacity:1; transform:scale(1.3); }}
}}
@keyframes shoot {{
    0% {{ transform: translateX(0) translateY(0) rotate(-35deg); opacity: 0; }}
    5% {{ opacity: 1; }}
    70% {{ opacity: 1; }}
    100% {{ transform: translateX(800px) translateY(500px) rotate(-35deg); opacity: 0; }}
}}
.starfield {{
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1; pointer-events: none; overflow: hidden;
}}
{STAR_CSS}
{SHOOTING_STARS_CSS}

/* ===== 动画 ===== */
@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
@keyframes typewriter {{
    from {{ width: 0; }}
    to {{ width: 32ch; }}
}}
@keyframes blink {{
    0%,100% {{ border-color: {GLACIER}; }}
    50% {{ border-color: transparent; }}
}}
@keyframes float {{
    0%,100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-6px); }}
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseRing {{
    0% {{ box-shadow: 0 0 0 0 rgba(0,212,255,0.35); }}
    70% {{ box-shadow: 0 0 0 14px rgba(0,212,255,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(0,212,255,0); }}
}}
@keyframes borderGlow {{
    0%,100% {{ border-color: rgba(0,212,255,0.12); }}
    50% {{ border-color: rgba(0,212,255,0.35); }}
}}
@keyframes cursorBlink {{
    0%,100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
@keyframes slideIn {{
    from {{ opacity: 0; transform: translateX(-20px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

/* ===== Hero ===== */
.hero-title {{
    font-family: 'Inter', sans-serif;
    font-size: 3.4rem; font-weight: 700; text-align: center;
    background: linear-gradient(135deg, {GLACIER_LIGHT}, {GLACIER}, {ACCENT_PURPLE}, {GLACIER});
    background-size: 300% 300%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 5s ease infinite;
    margin: 2.5rem 0 0.3rem; line-height: 1.2;
    letter-spacing: -0.02em;
}}
.hero-sub {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem; color: {TEXT_SECONDARY}; text-align: center;
    overflow: hidden; white-space: nowrap;
    border-right: 3px solid {GLACIER};
    width: 0; margin: 0 auto;
    animation: typewriter 3s steps(32, end) 0.5s forwards, blink 0.75s step-end infinite;
}}
.hero-tagline {{
    text-align: center; color: {TEXT_SECONDARY};
    font-size: 0.9rem; margin-top: 1rem;
    animation: fadeUp 1s ease 3.5s both;
    font-family: 'Inter', sans-serif;
}}
.hero-status {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.4rem 1rem; border-radius: 20px;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    color: #6EE7B7; font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
    animation: fadeUp 1s ease 4s both;
    margin-top: 1.2rem;
}}
.status-dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: #34D399;
    animation: pulseRing 2s ease infinite;
}}

/* ===== 分割线 ===== */
.divider {{
    height: 1px; width: 100%; margin: 2rem 0;
    background: linear-gradient(to right, transparent, rgba(0,212,255,0.2), transparent);
}}

/* ===== 区块标题 ===== */
.section-hdr {{
    font-family: 'JetBrains Mono', monospace;
    color: {GLACIER}; font-size: 1.15rem; font-weight: 700;
    margin: 2.5rem 0 1.2rem;
    display: flex; align-items: center; gap: 0.8rem;
    animation: fadeUp 0.6s ease both;
}}
.section-hdr .num {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 2rem; height: 2rem;
    border: 1.5px solid {GLACIER}; border-radius: 8px;
    font-size: 0.85rem;
    animation: pulseRing 2.5s ease infinite;
}}
.section-hdr .line {{
    flex: 1; height: 1px;
    background: linear-gradient(to right, rgba(0,212,255,0.3), transparent);
}}

/* ===== 卡片 ===== */
.glow-card {{
    background: {CARD_BG};
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 12px; padding: 1.4rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.7s ease both, borderGlow 4s ease infinite;
    transition: transform 0.3s, box-shadow 0.3s;
}}
.glow-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,212,255,0.08);
}}
.glow-card::after {{
    content: ''; position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.04), transparent);
    transition: left 0.6s ease;
}}
.glow-card:hover::after {{ left: 120%; }}

/* ===== 终端 ===== */
.terminal {{
    background: {TERMINAL_BG};
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 10px; overflow: hidden;
    margin: 1rem 0;
    animation: fadeUp 0.8s ease both;
}}
.terminal-bar {{
    background: #111827; padding: 0.45rem 1rem;
    display: flex; align-items: center; gap: 0.45rem;
    border-bottom: 1px solid rgba(0,212,255,0.08);
}}
.dot-r {{ color: #FF5F56; }} .dot-y {{ color: #FFBD2E; }} .dot-g {{ color: #27C93F; }}
.terminal-title {{
    font-family: 'JetBrains Mono', monospace;
    color: {TEXT_SECONDARY}; font-size: 0.7rem; margin-left: 0.8rem;
}}
.terminal-body {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; color: {TEXT_PRIMARY};
    padding: 1.1rem 1.2rem; line-height: 1.85;
}}
.prompt {{ color: {GLACIER}; font-weight: 700; }}
.comment {{ color: #546178; }}
.key {{ color: #C792EA; }}
.str {{ color: #C3E88D; }}
.num {{ color: #F78C6C; }}
.bool {{ color: #FF5370; }}

/* ===== 徽章 ===== */
.badge {{
    display: inline-block;
    padding: 0.35rem 0.85rem; margin: 0.25rem;
    border-radius: 20px; font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    animation: float 3s ease infinite;
    transition: transform 0.2s;
    cursor: default;
}}
.badge:hover {{ transform: scale(1.12) !important; }}
.b0 {{ background: rgba(0,212,255,0.10); color: {GLACIER_LIGHT}; border: 1px solid rgba(0,212,255,0.25); }}
.b1 {{ background: rgba(139,92,246,0.10); color: #A78BFA; border: 1px solid rgba(139,92,246,0.25); }}
.b2 {{ background: rgba(52,211,153,0.10); color: #6EE7B7; border: 1px solid rgba(52,211,153,0.25); }}
.b3 {{ background: rgba(251,191,36,0.10); color: #FCD34D; border: 1px solid rgba(251,191,36,0.25); }}

/* ===== 特性列表 ===== */
.feat {{
    padding: 0.7rem 1rem; margin: 0.4rem 0;
    border-left: 3px solid {GLACIER};
    background: rgba(0,212,255,0.025);
    border-radius: 0 8px 8px 0;
    animation: fadeUp 0.5s ease both;
    transition: border-color 0.3s, background 0.3s;
}}
.feat:hover {{
    border-left-color: {GLACIER_LIGHT};
    background: rgba(0,212,255,0.06);
}}
.feat-title {{
    color: {GLACIER_LIGHT}; font-weight: 600;
    font-size: 0.92rem; margin-bottom: 0.15rem;
}}
.feat-desc {{ color: {TEXT_SECONDARY}; font-size: 0.82rem; }}

/* ===== 优势 ===== */
.adv {{
    padding: 0.9rem 1.1rem; margin: 0.45rem 0;
    background: {CARD_BG}; border-radius: 10px;
    border-left: 3px solid {GLACIER};
    animation: fadeUp 0.6s ease both;
    transition: border-color 0.3s, transform 0.2s;
}}
.adv:hover {{ border-left-color: {GLACIER_LIGHT}; transform: translateX(4px); }}
.adv-t {{ color: {GLACIER_LIGHT}; font-weight: 600; font-size: 0.95rem; }}
.adv-d {{ color: {TEXT_SECONDARY}; font-size: 0.82rem; margin-top: 0.2rem; }}

/* ===== 联系按钮 ===== */
.contact-btn {{
    display: inline-block; padding: 0.75rem 2rem;
    background: linear-gradient(135deg, {GLACIER}, {ACCENT_PURPLE});
    background-size: 200% 200%;
    color: #fff !important; text-decoration: none !important;
    border-radius: 10px; font-weight: 600; font-size: 0.95rem;
    margin: 0.4rem; transition: all 0.3s;
    animation: gradientShift 4s ease infinite;
}}
.contact-btn:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,212,255,0.25);
}}

/* ===== 交互终端 ===== */
.interactive-terminal {{
    background: {TERMINAL_BG};
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px; overflow: hidden;
    margin: 1rem 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}}
.interactive-terminal .terminal-body {{
    min-height: 180px; max-height: 300px;
    overflow-y: auto;
}}
.chat-msg {{
    margin: 0.3rem 0; line-height: 1.6;
    animation: slideIn 0.3s ease both;
}}
.chat-user {{ color: {GLACIER}; }}
.chat-bot {{ color: {TEXT_PRIMARY}; }}
.chat-system {{ color: #546178; font-style: italic; }}
.chat-highlight {{ color: #C3E88D; }}
.chat-cursor {{
    display: inline-block; width: 8px; height: 16px;
    background: {GLACIER}; margin-left: 2px;
    animation: cursorBlink 1s step-end infinite;
    vertical-align: text-bottom;
}}

/* ===== 留言板 ===== */
.guestbook-entry {{
    padding: 0.8rem 1rem; margin: 0.5rem 0;
    background: rgba(0,212,255,0.03);
    border: 1px solid rgba(0,212,255,0.08);
    border-radius: 8px;
    animation: fadeUp 0.4s ease both;
}}
.guestbook-name {{ color: {GLACIER_LIGHT}; font-weight: 600; font-size: 0.88rem; }}
.guestbook-time {{ color: #546178; font-size: 0.72rem; margin-left: 0.5rem; }}
.guestbook-msg {{ color: {TEXT_SECONDARY}; font-size: 0.82rem; margin-top: 0.3rem; }}

/* ===== 隐藏默认元素 ===== */
#MainMenu, footer, [data-testid="stToolbar"] {{ display: none !important; }}
</style>
"""

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ============================================================
#  星空背景 + 流星
# ============================================================
_stars = "".join(f'<div class="s{i}"></div>' for i in range(200))
_shooting = "".join(f'<div class="ss{i}"></div>' for i in range(15))
st.markdown(
    f'<div class="starfield">{_stars}{_shooting}</div>',
    unsafe_allow_html=True,
)

# ============================================================
#  HERO
# ============================================================
st.markdown('<div class="hero-title">Sun Jiewei</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">AI Agent Developer &amp; Explorer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-tagline">'
    'Nanchang University (211) &middot; Artificial Intelligence &middot; 2025 级'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align:center">'
    '<div class="hero-status">'
    '<span class="status-dot"></span>'
    'Open to Agent Internship Opportunities'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  ABOUT
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">01</span> ABOUT'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="terminal"><div class="terminal-bar">'
    '<span class="dot-r">*</span><span class="dot-y">*</span><span class="dot-g">*</span>'
    '<span class="terminal-title">~/about_me.json</span></div>'
    '<div class="terminal-body">'
    '{<br>'
    f'&nbsp;&nbsp;<span class="key">"name"</span>: <span class="str">"孙杰伟"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"university"</span>: <span class="str">"南昌大学 (211)"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"major"</span>: <span class="str">"人工智能 · AI 实验班"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"enrolled"</span>: <span class="num">2025</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"focus"</span>: [<span class="str">"LLM"</span>, <span class="str">"Agent"</span>, <span class="str">"RAG"</span>],<br>'
    f'&nbsp;&nbsp;<span class="key">"seeking"</span>: <span class="str">"Agent 实习 / 工作机会"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"available"</span>: <span class="bool">true</span><br>'
    '}<br><br>'
    f'<span class="comment">// 热衷于探索 LLM + Agent 的应用边界</span><br>'
    f'<span class="comment">// 独立开发智能编程助手，擅长 Prompt Engineering &amp; Advanced RAG</span><br>'
    f'<span class="comment">// 希望将大语言模型的能力转化为解决实际问题的工具</span><br>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  STRENGTHS
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">02</span> STRENGTHS'
    '<span class="line"></span></div>',
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
        f'<div class="adv" style="animation-delay:{i * 0.12}s">'
        f'<div class="adv-t">{title}</div>'
        f'<div class="adv-d">{desc}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  PROJECT
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">03</span> PROJECT'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="glow-card" style="animation-delay:0.1s">'
    '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">'
    '<div style="font-size:1.2rem;font-weight:700;color:#7EE8FA">'
    'Coding Assistant Agent</div>'
    '<div style="font-size:0.75rem;color:#8BA4B8;font-family:\'JetBrains Mono\',monospace;'
    'padding:0.2rem 0.6rem;border:1px solid rgba(52,211,153,0.3);border-radius:12px;color:#6EE7B7">'
    'production</div></div>'
    '<div style="color:#8BA4B8;font-size:0.88rem;margin-top:0.5rem">'
    '基于 LangChain + LangGraph 的智能编程助手，支持代码生成、调试、RAG 知识检索</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.link_button("Open Project on HF Spaces", "https://jieweisun-coding-agent.hf.space")

st.markdown("<br>", unsafe_allow_html=True)

# 技术栈终端
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
    'font-size:0.9rem;margin-bottom:0.8rem;opacity:0.7">features.md</div>',
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
        f'<div class="feat" style="animation-delay:{i * 0.08}s">'
        f'<div class="feat-title">> {title}</div>'
        f'<div class="feat-desc">&nbsp; {desc}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  TECH STACK
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">04</span> TECH STACK'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

techs = [
    "LangChain", "LangGraph", "RAG", "Prompt Engineering",
    "LlamaIndex", "MCP", "Docker", "Streamlit",
    "FastAPI", "PyTorch", "MySQL", "Python",
]
badges_html = "".join(
    f'<span class="badge b{i % 4}" style="animation-delay:{i * 0.18}s">{t}</span>'
    for i, t in enumerate(techs)
)
st.markdown(
    f'<div class="glow-card" style="text-align:center;padding:1.5rem;animation-delay:0.2s">'
    f'{badges_html}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  INTERACTIVE TERMINAL — 访问者交互
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">05</span> INTERACTIVE TERMINAL'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

# 初始化聊天记录
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("system", "Welcome to jws-terminal v1.0. Type 'help' to get started."),
    ]

COMMANDS = {
    "help": (
        "Available commands:\n"
        "  help      — Show this help message\n"
        "  about     — Who am I?\n"
        "  skills    — My tech stack & skills\n"
        "  project   — View my featured project\n"
        "  contact   — Get my contact info\n"
        "  hire      — Why you should hire me\n"
        "  joke      — Tell a programmer joke\n"
        "  clear     — Clear terminal\n"
        "  date      — Show current time\n"
    ),
    "about": (
        "Sun Jiewei (孙杰伟)\n"
        "  University: Nanchang University (211)\n"
        "  Major: Artificial Intelligence, AI Experimental Class\n"
        "  Enrolled: 2025\n"
        "  Focus: LLM + Agent application development\n"
        "  Goal: Turning LLM capabilities into practical tools"
    ),
    "skills": (
        "Tech Stack:\n"
        "  [Agent]    LangChain, LangGraph, RAG, MCP\n"
        "  [LLM]      Prompt Engineering, Fine-tuning\n"
        "  [Data]     Chroma, LlamaIndex, MySQL\n"
        "  [Deploy]   Docker, Hugging Face, Streamlit\n"
        "  [Backend]  FastAPI, PyTorch, Python"
    ),
    "project": (
        "Coding Assistant Agent\n"
        "  A LangChain + LangGraph powered coding assistant.\n"
        "  Features: code execution, RAG retrieval, auto-retry, multi-turn memory.\n"
        "  Deployed on Hugging Face Spaces.\n"
        "  -> https://jieweisun-coding-agent.hf.space"
    ),
    "contact": (
        "Contact me:\n"
        "  Email:  3028789475@qq.com\n"
        "  GitHub: https://github.com/jws573\n"
        "  Status: Open to Agent internship opportunities"
    ),
    "hire": (
        "Why hire me?\n"
        "  1. I build and ship real projects (deployed on HF Spaces)\n"
        "  2. I learn fast — self-taught LangChain, RAG, MCP in months\n"
        "  3. I value teamwork — experience as class league secretary\n"
        "  4. I'm passionate about Agent technology and its applications"
    ),
    "joke": (
        random.choice([
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "A SQL query walks into a bar, sees two tables and asks: 'Can I JOIN you?'",
            "Why do Java developers wear glasses? Because they don't C#.",
            "There are only 10 types of people: those who understand binary and those who don't.",
            "!false — it's funny because it's true.",
            "A programmer's wife tells him: 'Go to the store and buy a loaf of bread. If they have eggs, buy a dozen.' He comes home with 12 loaves.",
        ])
    ),
    "date": datetime.now().strftime("  Server time: %Y-%m-%d %H:%M:%S CST"),
}

def process_command(cmd):
    cmd = cmd.strip().lower()
    if not cmd:
        return None
    if cmd == "clear":
        st.session_state.chat_history = [
            ("system", "Terminal cleared."),
        ]
        return True
    if cmd in COMMANDS:
        return COMMANDS[cmd]
    return f"Command not found: '{cmd}'. Type 'help' for available commands."

# 渲染终端
chat_html = ""
for role, msg in st.session_state.chat_history:
    if role == "system":
        chat_html += f'<div class="chat-msg chat-system">{msg}</div>'
    elif role == "user":
        chat_html += f'<div class="chat-msg chat-user"><span class="prompt">visitor@jws:~$</span> {msg}</div>'
    elif role == "bot":
        formatted = msg.replace("\n", "<br>")
        chat_html += f'<div class="chat-msg chat-bot">{formatted}</div>'

chat_html += '<div class="chat-msg chat-user"><span class="prompt">visitor@jws:~$</span> <span class="chat-cursor"></span></div>'

st.markdown(
    f'<div class="interactive-terminal">'
    f'<div class="terminal-bar">'
    f'<span class="dot-r">*</span><span class="dot-y">*</span><span class="dot-g">*</span>'
    f'<span class="terminal-title">jws-terminal — interactive</span></div>'
    f'<div class="terminal-body">{chat_html}</div></div>',
    unsafe_allow_html=True,
)

# 输入框
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_cmd = st.text_input(
        "Terminal Input",
        placeholder="Type a command... (try 'help')",
        label_visibility="collapsed",
        key="terminal_input",
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run_cmd = st.button("Run", use_container_width=True)

if run_cmd and user_cmd:
    st.session_state.chat_history.append(("user", user_cmd))
    result = process_command(user_cmd)
    if result is True:
        pass  # clear command
    elif result:
        st.session_state.chat_history.append(("bot", result))
    st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  GUESTBOOK — 留言板
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">06</span> GUESTBOOK'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="color:#8BA4B8;font-size:0.88rem;margin-bottom:1rem;'
    'font-family:\'JetBrains Mono\',monospace">'
    'Leave a message for me. Recruiters are welcome to leave contact info.</div>',
    unsafe_allow_html=True,
)

# 留言板数据文件
GUESTBOOK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".guestbook.json")

def load_guestbook():
    if os.path.exists(GUESTBOOK_FILE):
        try:
            with open(GUESTBOOK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {"name": "System", "msg": "Welcome to the guestbook! Be the first to sign in.", "time": "2025-01-01"},
    ]

def save_guestbook(entries):
    with open(GUESTBOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

if "guestbook" not in st.session_state:
    st.session_state.guestbook = load_guestbook()

# 留言表单
with st.form("guestbook_form", clear_on_submit=True):
    gb_cols = st.columns([2, 4])
    with gb_cols[0]:
        gb_name = st.text_input("Name / 姓名", placeholder="Your name")
    with gb_cols[1]:
        gb_msg = st.text_input("Message / 留言", placeholder="Leave your message or contact info...")
    gb_submit = st.form_submit_button("Sign Guestbook / 提交留言")

if gb_submit and gb_name.strip() and gb_msg.strip():
    entry = {
        "name": gb_name.strip(),
        "msg": gb_msg.strip(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.guestbook.insert(0, entry)
    save_guestbook(st.session_state.guestbook)
    st.rerun()

# 显示留言
st.markdown("<br>", unsafe_allow_html=True)
for i, entry in enumerate(st.session_state.guestbook[:20]):
    st.markdown(
        f'<div class="guestbook-entry" style="animation-delay:{i * 0.05}s">'
        f'<span class="guestbook-name">{entry["name"]}</span>'
        f'<span class="guestbook-time">{entry["time"]}</span>'
        f'<div class="guestbook-msg">{entry["msg"]}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  CONTACT
# ============================================================
st.markdown(
    '<div class="section-hdr">'
    '<span class="num">07</span> CONTACT'
    '<span class="line"></span></div>',
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
    '<div class="divider"></div>'
    '<div style="text-align:center;padding:1.5rem 0">'
    '<div style="font-family:\'JetBrains Mono\',monospace;'
    f'color:{TEXT_SECONDARY};font-size:0.8rem">'
    'Thank you for visiting. Let\'s build the future of AI Agents together.'
    '</div>'
    '<div style="font-family:\'JetBrains Mono\',monospace;color:#4A9EAF;'
    'font-size:0.65rem;opacity:0.4;margin-top:0.8rem">'
    '/* Built with Streamlit | Sun Jiewei &copy; 2025 */'
    '</div></div>',
    unsafe_allow_html=True,
)
