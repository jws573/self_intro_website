import streamlit as st
import random
import json
import os
import math
from datetime import datetime

# ============================================================
#  页面配置
# ============================================================
st.set_page_config(
    page_title="孙杰伟 | AI Agent Developer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  调色板 & 常量
# ============================================================
GLACIER       = "#00D4FF"
GLACIER_LIGHT = "#7EE8FA"
GLACIER_DIM   = "#4A9EAF"
DEEP_BG       = "#060B18"
CARD_BG       = "#0D1B2A"
CARD_BG_HOVER = "#111F33"
TERMINAL_BG   = "#0A0F1A"
TEXT_PRIMARY   = "#E0F0FF"
TEXT_SECONDARY = "#8BA4B8"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_GREEN  = "#34D399"
ACCENT_AMBER  = "#FCD34D"
ACCENT_PINK   = "#F472B6"

# ============================================================
#  CSS
# ============================================================
_STAR_COLORS = ['#FFF8DC', '#FFFACD', '#FFFDE7', '#FFF9C4', '#FFF']
STAR_CSS = "\n".join(
    f".s{i}{{position:absolute;border-radius:50%;background:{random.choice(_STAR_COLORS)};"
    f"width:{random.choice([1, 1, 2, 2, 3])}px;"
    f"height:{random.choice([1, 1, 2, 2, 3])}px;"
    f"top:{random.uniform(0, 100):.1f}%;left:{random.uniform(0, 100):.1f}%;"
    f"opacity:{random.uniform(0.15, 0.85):.2f};"
    f"animation:twinkle {random.uniform(2, 6):.1f}s ease-in-out "
    f"{random.uniform(0, 4):.1f}s infinite"
    f"{', drift ' + f'{random.uniform(15, 40):.0f}s ease-in-out ' + f'{random.uniform(0, 10):.1f}s infinite' if random.random() < 0.3 else ''}}}"
    for i in range(180)
)

SHOOTING_STARS_CSS = ""
for i in range(12):
    top = random.uniform(-10, 60)
    left = random.uniform(-15, 50)
    dur = random.uniform(2.5, 6.0)
    delay = random.uniform(0, 8)
    width = random.choice([60, 80, 100, 120, 150])
    SHOOTING_STARS_CSS += f"""
.ss{i} {{
    position: absolute; width: {width}px; height: 1px;
    top: {top:.1f}%; left: {left:.1f}%;
    background: linear-gradient(to right, rgba(255,255,255,0), {GLACIER}, rgba(255,255,255,0));
    animation: shoot {dur:.1f}s linear {delay:.1f}s infinite; opacity: 0;
}}
.ss{i}::after {{
    content: ''; position: absolute; right: 0; top: -1px;
    width: 4px; height: 3px; border-radius: 50%;
    background: {GLACIER_LIGHT}; box-shadow: 0 0 6px 2px rgba(0,212,255,0.4);
}}
"""

MAIN_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ===== 全局 ===== */
html {{
    scroll-behavior: smooth;
}}
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {DEEP_BG}; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, {GLACIER_DIM}, {ACCENT_PURPLE});
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {GLACIER}; }}

.stApp {{
    background: {DEEP_BG} !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.03) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.02) 0%, transparent 60%) !important;
}}
section[data-testid="stSidebar"] {{
    background: rgba(8,14,26,0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(0,212,255,0.12) !important;
}}
section[data-testid="stSidebar"] .stMarkdown {{
    color: {TEXT_SECONDARY} !important;
}}
header[data-testid="stHeader"] {{
    background: rgba(6,11,24,0.7) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid rgba(0,212,255,0.06) !important;
}}
.block-container {{
    padding-top: 0.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 880px !important;
}}
.stMarkdown {{ color: {TEXT_PRIMARY}; }}
a {{ color: {GLACIER} !important; }}

/* ===== Loading Screen ===== */
.loading-screen {{
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: {DEEP_BG}; z-index: 99999;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: loadingFade 2.8s ease forwards;
}}
@keyframes loadingFade {{
    0%,70% {{ opacity: 1; visibility: visible; pointer-events: auto; }}
    100% {{ opacity: 0; visibility: hidden; pointer-events: none; }}
}}
.loading-logo {{
    font-family: 'Inter', sans-serif; font-size: 1.5rem;
    font-weight: 800; margin-bottom: 2rem;
    background: linear-gradient(135deg, {GLACIER_LIGHT}, {ACCENT_PURPLE});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.loading-bar {{
    width: 200px; height: 2px; background: rgba(0,212,255,0.1);
    border-radius: 1px; overflow: hidden;
}}
.loading-bar-inner {{
    width: 0; height: 100%;
    background: linear-gradient(90deg, {GLACIER}, {ACCENT_PURPLE});
    border-radius: 1px;
    animation: loadProgress 2s ease-out forwards;
}}
@keyframes loadProgress {{
    0% {{ width: 0; }}
    30% {{ width: 45%; }}
    60% {{ width: 75%; }}
    90% {{ width: 95%; }}
    100% {{ width: 100%; }}
}}
.loading-text {{
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    color: {TEXT_SECONDARY}; margin-top: 1rem;
}}

/* ===== 滚动显示动画 ===== */
.reveal {{
    opacity: 0; transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}}
.reveal.visible {{
    opacity: 1; transform: translateY(0);
}}
.reveal-left {{
    opacity: 0; transform: translateX(-40px);
    transition: opacity 0.7s ease, transform 0.7s ease;
}}
.reveal-left.visible {{
    opacity: 1; transform: translateX(0);
}}

/* ===== 星空 ===== */
@keyframes twinkle {{
    0%,100% {{ opacity:0.15; transform:scale(0.8); }}
    50% {{ opacity:1; transform:scale(1.3); }}
}}
@keyframes shoot {{
    0% {{ transform: translateX(0) translateY(0) rotate(-35deg); opacity: 0; }}
    5% {{ opacity: 1; }} 70% {{ opacity: 1; }}
    100% {{ transform: translateX(800px) translateY(500px) rotate(-35deg); opacity: 0; }}
}}
.starfield {{
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1; pointer-events: none; overflow: hidden;
}}

/* ===== 极光 / 星云背景 ===== */
.aurora {{
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1; pointer-events: none; overflow: hidden;
    opacity: 0.35;
}}
.aurora-layer {{
    position: absolute; border-radius: 50%; filter: blur(80px);
    mix-blend-mode: screen;
}}
.aurora-layer.a1 {{
    width: 600px; height: 600px; top: -10%; left: -10%;
    background: radial-gradient(circle, rgba(0,212,255,0.15), transparent 70%);
    animation: auroraMove1 20s ease-in-out infinite;
}}
.aurora-layer.a2 {{
    width: 500px; height: 500px; top: 40%; right: -15%;
    background: radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%);
    animation: auroraMove2 25s ease-in-out infinite;
}}
.aurora-layer.a3 {{
    width: 450px; height: 450px; bottom: -5%; left: 30%;
    background: radial-gradient(circle, rgba(52,211,153,0.08), transparent 70%);
    animation: auroraMove3 22s ease-in-out infinite;
}}
@keyframes auroraMove1 {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33% {{ transform: translate(15vw,10vh) scale(1.2); }}
    66% {{ transform: translate(-5vw,20vh) scale(0.9); }}
}}
@keyframes auroraMove2 {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33% {{ transform: translate(-20vw,-8vh) scale(1.15); }}
    66% {{ transform: translate(5vw,15vh) scale(0.85); }}
}}
@keyframes auroraMove3 {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33% {{ transform: translate(10vw,-15vh) scale(1.1); }}
    66% {{ transform: translate(-15vw,-5vh) scale(0.95); }}
}}

/* ===== 光环扫描线 ===== */
.scanline {{
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1; pointer-events: none; overflow: hidden;
}}
.scanline::after {{
    content: ''; position: absolute; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.06), transparent);
    animation: scanDown 8s linear infinite;
}}
@keyframes scanDown {{
    0% {{ top: -2px; }}
    100% {{ top: 100%; }}
}}

/* ===== 光标跟随光晕 ===== */
.cursor-glow {{
    position: fixed; width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.04) 0%, transparent 70%);
    pointer-events: none; z-index: -1;
    transform: translate(-50%, -50%);
    transition: left 0.8s ease-out, top 0.8s ease-out;
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
    from {{ width: 0; }} to {{ width: 30ch; }}
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
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }} to {{ opacity: 1; }}
}}
@keyframes pulseRing {{
    0% {{ box-shadow: 0 0 0 0 rgba(0,212,255,0.35); }}
    70% {{ box-shadow: 0 0 0 14px rgba(0,212,255,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(0,212,255,0); }}
}}
@keyframes borderGlow {{
    0%,100% {{ border-color: rgba(0,212,255,0.12); }}
    50% {{ border-color: rgba(0,212,255,0.30); }}
}}
@keyframes cursorBlink {{
    0%,100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
@keyframes slideIn {{
    from {{ opacity: 0; transform: translateX(-16px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes countUp {{
    from {{ opacity: 0; transform: scale(0.5); }}
    to {{ opacity: 1; transform: scale(1); }}
}}
@keyframes progressFill {{
    from {{ width: 0; }}
}}
@keyframes glowPulse {{
    0%,100% {{ box-shadow: 0 0 5px rgba(0,212,255,0.15); }}
    50% {{ box-shadow: 0 0 20px rgba(0,212,255,0.25); }}
}}
@keyframes drift {{
    0% {{ transform: translate(0, 0); }}
    25% {{ transform: translate(15px, -10px); }}
    50% {{ transform: translate(-8px, 12px); }}
    75% {{ transform: translate(12px, 8px); }}
    100% {{ transform: translate(0, 0); }}
}}
@keyframes constellationMove {{
    0% {{ transform: translate(0, 0) rotate(0deg); }}
    25% {{ transform: translate(20px, -15px) rotate(2deg); }}
    50% {{ transform: translate(-10px, 18px) rotate(-1deg); }}
    75% {{ transform: translate(15px, 10px) rotate(1.5deg); }}
    100% {{ transform: translate(0, 0) rotate(0deg); }}
}}
@keyframes constellationTwinkle {{
    0%,100% {{ opacity:0.7; filter:blur(0px); }}
    50% {{ opacity:1; filter:blur(0.5px); box-shadow:0 0 8px 3px rgba(0,212,255,0.6); }}
}}
@keyframes qdotPulse {{
    0%,100% {{ r:2; opacity:0.6; }}
    50% {{ r:3.5; opacity:1; }}
}}
@keyframes iconFloat {{
    0%,100% {{ transform:translateY(0); }}
    50% {{ transform:translateY(-8px); }}
}}
@keyframes lineGlow {{
    0%,100% {{ stroke-dashoffset:0; opacity:0.4; }}
    50% {{ stroke-dashoffset:10; opacity:0.8; }}
}}

/* ===== 星座连线 ===== */
.constellation {{
    position:fixed; top:0; left:0; width:100%; height:100%;
    z-index:-1; pointer-events:none; overflow:hidden;
    animation: constellationMove 25s ease-in-out infinite;
}}
.constellation-star {{
    position:absolute; width:4px; height:4px; border-radius:50%;
    background:#fff; animation: constellationTwinkle 3s ease-in-out infinite;
}}
.constellation-star.bright {{
    width:5px; height:5px;
    box-shadow: 0 0 6px 2px rgba(0,212,255,0.5);
}}
.constellation-line {{
    position:absolute; height:1px;
    background:linear-gradient(90deg, rgba(0,212,255,0.3), rgba(139,92,246,0.3));
    transform-origin: 0 0;
    animation: lineGlow 4s ease-in-out infinite;
}}

/* ===== 量子点光图标 ===== */
.qdot-icon {{
    position:fixed; z-index:-1; pointer-events:none;
    animation: iconFloat 6s ease-in-out infinite;
    opacity:0.5;
}}
.qdot-icon svg {{ overflow:visible; }}
.qdot-icon circle {{
    fill:{GLACIER};
    animation: qdotPulse 2s ease-in-out infinite;
}}
.qdot-icon.purple circle {{ fill:{ACCENT_PURPLE}; }}
.qdot-icon.green circle {{ fill:{ACCENT_GREEN}; }}

/* ===== 留言板删除按钮 ===== */
.guestbook-del {{
    float:right; background:none; border:none; color:#546178;
    font-size:0.72rem; cursor:pointer; padding:0.1rem 0.4rem;
    border-radius:4px; font-family:'JetBrains Mono',monospace;
    transition: all 0.2s;
}}
.guestbook-del:hover {{ color:#FF5370; background:rgba(255,83,112,0.1); }}

/* ===== 侧边栏内容 ===== */
.sidebar-profile {{
    text-align: center; padding: 1rem 0;
}}
.sidebar-avatar {{
    width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 0.8rem;
    background: linear-gradient(135deg, {GLACIER}, {ACCENT_PURPLE});
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 700; color: #fff;
    border: 2px solid rgba(0,212,255,0.3);
    animation: glowPulse 3s ease infinite;
    position: relative;
    transform-style: preserve-3d;
}}
.sidebar-avatar::before {{
    content: ''; position: absolute;
    width: 96px; height: 96px; border-radius: 50%;
    border: 1.5px solid transparent;
    border-top-color: {GLACIER}; border-right-color: {ACCENT_PURPLE};
    animation: avatarRing 4s linear infinite;
}}
.sidebar-avatar::after {{
    content: ''; position: absolute;
    width: 106px; height: 106px; border-radius: 50%;
    border: 1px solid transparent;
    border-bottom-color: rgba(0,212,255,0.2); border-left-color: rgba(139,92,246,0.2);
    animation: avatarRing 6s linear infinite reverse;
}}
@keyframes avatarRing {{
    from {{ transform: rotateZ(0deg); }}
    to {{ transform: rotateZ(360deg); }}
}}
.sidebar-name {{
    font-family: 'Inter', sans-serif; font-size: 1.1rem;
    font-weight: 700; color: {TEXT_PRIMARY}; margin-bottom: 0.2rem;
}}
.sidebar-role {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: {GLACIER_DIM};
}}
.sidebar-divider {{
    height: 1px; margin: 1rem 0;
    background: linear-gradient(to right, transparent, rgba(0,212,255,0.15), transparent);
}}
.sidebar-nav {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}}
.sidebar-nav a {{
    display: block; padding: 0.45rem 0.8rem;
    color: {TEXT_SECONDARY} !important; text-decoration: none !important;
    border-radius: 6px; transition: all 0.2s;
    border-left: 2px solid transparent;
}}
.sidebar-nav a:hover {{
    color: {GLACIER} !important;
    background: rgba(0,212,255,0.05);
    border-left-color: {GLACIER};
}}
.sidebar-section-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; color: #4A9EAF;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin: 1.2rem 0 0.5rem 0.8rem;
}}
.sidebar-social {{
    display: flex; gap: 0.6rem; justify-content: center;
    margin-top: 0.8rem;
}}
.sidebar-social a {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 8px;
    background: rgba(0,212,255,0.06); border: 1px solid rgba(0,212,255,0.12);
    color: {TEXT_SECONDARY} !important; text-decoration: none !important;
    font-size: 0.75rem; transition: all 0.2s;
}}
.sidebar-social a:hover {{
    background: rgba(0,212,255,0.12); color: {GLACIER} !important;
    transform: translateY(-2px);
}}
.sidebar-availability {{
    margin-top: 1rem; padding: 0.5rem 0.8rem;
    background: rgba(52,211,153,0.06);
    border: 1px solid rgba(52,211,153,0.15);
    border-radius: 8px; text-align: center;
}}
.sidebar-availability .dot {{
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; background: {ACCENT_GREEN};
    margin-right: 0.4rem; animation: pulseRing 2s ease infinite;
}}
.sidebar-availability span {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: {ACCENT_GREEN};
}}

/* ===== Hero ===== */
.hero-title {{
    font-family: 'Inter', sans-serif;
    font-size: 3rem; font-weight: 800; text-align: left;
    background: linear-gradient(135deg, {GLACIER_LIGHT}, {GLACIER}, {ACCENT_PURPLE}, {GLACIER});
    background-size: 300% 300%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 5s ease infinite;
    margin: 2rem 0 0.3rem; line-height: 1.15;
    letter-spacing: -0.02em;
}}
.hero-sub {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem; color: {TEXT_SECONDARY};
    text-align: left; overflow: hidden; white-space: nowrap;
    border-right: 3px solid {GLACIER};
    width: 0;
    animation: typewriter 3s steps(38, end) 0.5s forwards, blink 0.75s step-end infinite;
}}
.hero-tagline {{
    text-align: left; color: {TEXT_SECONDARY};
    font-size: 0.88rem; margin-top: 0.8rem;
    animation: fadeUp 1s ease 3.5s both;
    font-family: 'Inter', sans-serif; line-height: 1.6;
}}
.hero-status {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.35rem 0.9rem; border-radius: 20px;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    color: {ACCENT_GREEN}; font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    animation: fadeUp 1s ease 4s both;
    margin-top: 1rem;
}}
.status-dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: {ACCENT_GREEN}; animation: pulseRing 2s ease infinite;
}}

/* ===== 向下滚动指示 ===== */
.scroll-indicator {{
    text-align: center; margin-top: 2.5rem;
    animation: fadeUp 1s ease 4.5s both;
}}
.scroll-arrow {{
    display: inline-block; width: 24px; height: 24px;
    border-right: 2px solid rgba(0,212,255,0.4);
    border-bottom: 2px solid rgba(0,212,255,0.4);
    transform: rotate(45deg);
    animation: bounceArrow 2s ease-in-out infinite;
}}
@keyframes bounceArrow {{
    0%,100% {{ transform: rotate(45deg) translateY(0); opacity: 0.4; }}
    50% {{ transform: rotate(45deg) translateY(8px); opacity: 1; }}
}}
.scroll-text {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; color: rgba(0,212,255,0.3);
    margin-top: 0.6rem; letter-spacing: 0.15em;
}}

/* ===== 分割线 ===== */
.divider {{
    height: 1px; width: 100%; margin: 1.5rem 0;
    background: linear-gradient(to right, transparent, rgba(0,212,255,0.15), transparent);
}}

/* ===== 区块标题 ===== */
.section-hdr {{
    font-family: 'JetBrains Mono', monospace;
    color: {GLACIER}; font-size: 1.05rem; font-weight: 700;
    margin: 2rem 0 1rem;
    display: flex; align-items: center; gap: 0.8rem;
    animation: fadeUp 0.6s ease both;
}}
.section-hdr .num {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 1.8rem; height: 1.8rem;
    border: 1.5px solid {GLACIER}; border-radius: 8px;
    font-size: 0.8rem; animation: pulseRing 2.5s ease infinite;
}}
.section-hdr .line {{
    flex: 1; height: 1px;
    background: linear-gradient(to right, rgba(0,212,255,0.25), transparent);
}}

/* ===== 统计卡片 ===== */
.stats-row {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem;
    margin: 1rem 0;
}}
.stat-card {{
    background: rgba(13,27,42,0.6); border: 1px solid rgba(0,212,255,0.10);
    border-radius: 10px; padding: 1rem; text-align: center;
    animation: fadeUp 0.6s ease both;
    transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
    position: relative; overflow: hidden;
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
}}
.stat-card:hover {{
    transform: translateY(-4px); border-color: rgba(0,212,255,0.3);
    box-shadow: 0 0 20px rgba(0,212,255,0.08), inset 0 0 20px rgba(0,212,255,0.03);
}}
.stat-card::after {{
    content: ''; position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(0,212,255,0.05), transparent 30%);
    animation: cardRotate 6s linear infinite;
    opacity: 0; transition: opacity 0.3s;
}}
.stat-card:hover::after {{ opacity: 1; }}
@keyframes cardRotate {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}
.stat-num {{
    font-family: 'Inter', sans-serif; font-size: 1.8rem;
    font-weight: 800; color: {GLACIER_LIGHT};
    animation: countUp 0.8s ease both;
}}
.stat-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: {TEXT_SECONDARY};
    margin-top: 0.3rem;
}}

/* ===== 卡片 ===== */
.glow-card {{
    background: rgba(13,27,42,0.55);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0,212,255,0.10);
    border-radius: 12px; padding: 1.3rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.7s ease both, borderGlow 4s ease infinite;
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}}
.glow-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,212,255,0.08), 0 0 40px rgba(0,212,255,0.04);
    border-color: rgba(0,212,255,0.2);
}}
.glow-card::before {{
    content: ''; position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(0,212,255,0.02), transparent 50%);
    opacity: 0; transition: opacity 0.3s;
}}
.glow-card:hover::before {{ opacity: 1; }}
.glow-card::after {{
    content: ''; position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.04), transparent);
    transition: left 0.7s ease;
}}
.glow-card:hover::after {{ left: 120%; }}

/* ===== 终端 ===== */
.terminal {{
    background: rgba(10,15,26,0.7);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px; overflow: hidden;
    margin: 0.8rem 0; animation: fadeUp 0.8s ease both;
}}
.terminal-bar {{
    background: #111827; padding: 0.4rem 1rem;
    display: flex; align-items: center; gap: 0.45rem;
    border-bottom: 1px solid rgba(0,212,255,0.06);
}}
.dot-r {{ color: #FF5F56; }} .dot-y {{ color: #FFBD2E; }} .dot-g {{ color: #27C93F; }}
.terminal-title {{
    font-family: 'JetBrains Mono', monospace;
    color: {TEXT_SECONDARY}; font-size: 0.68rem; margin-left: 0.8rem;
}}
.terminal-body {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem; color: {TEXT_PRIMARY};
    padding: 1rem 1.2rem; line-height: 1.8;
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
    padding: 0.3rem 0.8rem; margin: 0.2rem;
    border-radius: 20px; font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    animation: float 3s ease infinite;
    transition: transform 0.2s; cursor: default;
}}
.badge:hover {{ transform: scale(1.12) !important; }}
.b0 {{ background: rgba(0,212,255,0.10); color: {GLACIER_LIGHT}; border: 1px solid rgba(0,212,255,0.25); }}
.b1 {{ background: rgba(139,92,246,0.10); color: #A78BFA; border: 1px solid rgba(139,92,246,0.25); }}
.b2 {{ background: rgba(52,211,153,0.10); color: #6EE7B7; border: 1px solid rgba(52,211,153,0.25); }}
.b3 {{ background: rgba(251,191,36,0.10); color: #FCD34D; border: 1px solid rgba(251,191,36,0.25); }}
.b4 {{ background: rgba(244,114,182,0.10); color: #F9A8D4; border: 1px solid rgba(244,114,182,0.25); }}

/* ===== 技能进度条 ===== */
.skill-bar-wrap {{
    margin: 0.5rem 0; animation: fadeUp 0.5s ease both;
}}
.skill-bar-label {{
    display: flex; justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: {TEXT_SECONDARY};
    margin-bottom: 0.3rem;
}}
.skill-bar-track {{
    height: 6px; background: rgba(0,212,255,0.08);
    border-radius: 3px; overflow: hidden;
}}
.skill-bar-fill {{
    height: 100%; border-radius: 3px;
    animation: progressFill 1.5s ease both;
    background: linear-gradient(90deg, {GLACIER}, {ACCENT_PURPLE});
}}

/* ===== 特性列表 ===== */
.feat {{
    padding: 0.6rem 0.9rem; margin: 0.3rem 0;
    border-left: 3px solid {GLACIER};
    background: rgba(0,212,255,0.02);
    border-radius: 0 8px 8px 0;
    animation: fadeUp 0.5s ease both;
    transition: border-color 0.3s, background 0.3s;
}}
.feat:hover {{
    border-left-color: {GLACIER_LIGHT};
    background: rgba(0,212,255,0.05);
}}
.feat-title {{
    color: {GLACIER_LIGHT}; font-weight: 600;
    font-size: 0.88rem; margin-bottom: 0.1rem;
}}
.feat-desc {{ color: {TEXT_SECONDARY}; font-size: 0.78rem; }}

/* ===== 优势 ===== */
.adv {{
    padding: 0.8rem 1rem; margin: 0.35rem 0;
    background: {CARD_BG}; border-radius: 10px;
    border-left: 3px solid {GLACIER};
    animation: fadeUp 0.6s ease both;
    transition: border-color 0.3s, transform 0.2s;
}}
.adv:hover {{ border-left-color: {GLACIER_LIGHT}; transform: translateX(4px); }}
.adv-t {{ color: {GLACIER_LIGHT}; font-weight: 600; font-size: 0.9rem; }}
.adv-d {{ color: {TEXT_SECONDARY}; font-size: 0.78rem; margin-top: 0.15rem; }}

/* ===== 时间线 ===== */
.timeline {{
    position: relative; padding-left: 2rem; margin: 1rem 0;
}}
.timeline::before {{
    content: ''; position: absolute; left: 7px; top: 0; bottom: 0;
    width: 2px; background: linear-gradient(to bottom, {GLACIER}, rgba(0,212,255,0.1));
}}
.timeline-item {{
    position: relative; margin-bottom: 1.2rem;
    animation: fadeUp 0.6s ease both;
}}
.timeline-dot {{
    position: absolute; left: -2rem; top: 0.3rem;
    width: 12px; height: 12px; border-radius: 50%;
    background: {DEEP_BG}; border: 2px solid {GLACIER};
    z-index: 1;
}}
.timeline-dot.active {{
    background: {GLACIER};
    box-shadow: 0 0 8px rgba(0,212,255,0.4);
}}
.timeline-title {{
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size: 0.92rem; color: {TEXT_PRIMARY};
}}
.timeline-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: {GLACIER_DIM};
    margin-top: 0.1rem;
}}
.timeline-desc {{
    font-size: 0.8rem; color: {TEXT_SECONDARY};
    margin-top: 0.3rem; line-height: 1.5;
}}

/* ===== 项目卡片 ===== */
.project-card {{
    background: rgba(13,27,42,0.55);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(0,212,255,0.10);
    border-radius: 12px; overflow: hidden;
    animation: fadeUp 0.7s ease both;
    transition: transform 0.3s, box-shadow 0.4s, border-color 0.3s;
    position: relative;
}}
.project-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,212,255,0.1), 0 0 60px rgba(139,92,246,0.05);
    border-color: rgba(0,212,255,0.3);
}}
.project-card::before {{
    content: ''; position: absolute; top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, {GLACIER}, {ACCENT_PURPLE}, {GLACIER});
    background-size: 200% 100%;
    animation: gradientShift 3s ease infinite;
    opacity: 0; transition: opacity 0.3s;
}}
.project-card:hover::before {{ opacity: 1; }}
.project-card-body {{
    padding: 1.2rem;
}}
.project-card-tag {{
    display: inline-block; font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; padding: 0.15rem 0.5rem;
    border-radius: 10px; margin-right: 0.3rem;
}}
.tag-production {{
    background: rgba(52,211,153,0.1); color: {ACCENT_GREEN};
    border: 1px solid rgba(52,211,153,0.25);
}}
.tag-wip {{
    background: rgba(251,191,36,0.1); color: {ACCENT_AMBER};
    border: 1px solid rgba(251,191,36,0.25);
}}
.tag-concept {{
    background: rgba(139,92,246,0.1); color: #A78BFA;
    border: 1px solid rgba(139,92,246,0.25);
}}

/* ===== 联系按钮 ===== */
.contact-btn {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.7rem 1.8rem;
    background: linear-gradient(135deg, {GLACIER}, {ACCENT_PURPLE});
    background-size: 200% 200%;
    color: #fff !important; text-decoration: none !important;
    border-radius: 10px; font-weight: 600; font-size: 0.88rem;
    margin: 0.3rem; transition: all 0.3s;
    animation: gradientShift 4s ease infinite;
    font-family: 'Inter', sans-serif;
}}
.contact-btn:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,212,255,0.25);
}}
.contact-btn-outline {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.65rem 1.7rem;
    background: transparent; border: 1.5px solid rgba(0,212,255,0.3);
    color: {GLACIER} !important; text-decoration: none !important;
    border-radius: 10px; font-weight: 600; font-size: 0.88rem;
    margin: 0.3rem; transition: all 0.3s;
    font-family: 'Inter', sans-serif;
}}
.contact-btn-outline:hover {{
    background: rgba(0,212,255,0.08);
    border-color: {GLACIER}; transform: translateY(-2px);
}}

/* ===== 交互终端 ===== */
.interactive-terminal {{
    background: rgba(10,15,26,0.65);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 12px; overflow: hidden;
    margin: 0.8rem 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}}
.interactive-terminal .terminal-body {{
    min-height: 160px; max-height: 280px; overflow-y: auto;
}}
.chat-msg {{
    margin: 0.25rem 0; line-height: 1.6;
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
    padding: 0.7rem 0.9rem; margin: 0.4rem 0;
    background: rgba(0,212,255,0.02);
    border: 1px solid rgba(0,212,255,0.06);
    border-radius: 8px;
    animation: fadeUp 0.4s ease both;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
    position: relative; overflow: hidden;
}}
.guestbook-entry:hover {{
    border-color: rgba(0,212,255,0.2);
    box-shadow: 0 0 15px rgba(0,212,255,0.04);
    transform: translateX(4px);
}}
.guestbook-name {{ color: {GLACIER_LIGHT}; font-weight: 600; font-size: 0.85rem; }}
.guestbook-time {{ color: #546178; font-size: 0.7rem; margin-left: 0.5rem; }}
.guestbook-msg {{ color: {TEXT_SECONDARY}; font-size: 0.8rem; margin-top: 0.2rem; }}

/* ===== 编辑面板 ===== */
.edit-panel {{
    background: rgba(13,27,42,0.5);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 12px; padding: 1.2rem; margin: 0.8rem 0;
}}
.edit-panel-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem; color: {GLACIER_LIGHT};
    margin-bottom: 0.8rem; font-weight: 600;
}}

/* ===== 缩窄输入框 ===== */
.stTextInput input {{
    background: {TERMINAL_BG} !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 8px !important; color: {TEXT_PRIMARY} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}}
.stTextInput input:focus {{
    border-color: {GLACIER} !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.1) !important;
}}
.stTextArea textarea {{
    background: {TERMINAL_BG} !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 8px !important; color: {TEXT_PRIMARY} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}}

/* ===== 页脚 ===== */
.footer {{
    text-align: center; padding: 2rem 0 1rem;
    font-family: 'JetBrains Mono', monospace;
}}

/* ===== 隐藏默认元素 ===== */
#MainMenu, footer, [data-testid="stToolbar"] {{ display: none !important; }}

/* ===== 响应式 ===== */
@media (max-width: 768px) {{
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
    .hero-title {{ font-size: 2.2rem; }}
    .aurora-layer {{ filter: blur(50px); }}
    .aurora-layer.a1 {{ width: 300px; height: 300px; }}
    .aurora-layer.a2 {{ width: 250px; height: 250px; }}
    .aurora-layer.a3 {{ width: 200px; height: 200px; }}
    .qdot-icon {{ display: none; }}
    .cursor-glow {{ display: none; }}
    .constellation {{ opacity: 0.5; }}
}}
</style>
"""

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ============================================================
#  Loading Screen
# ============================================================
st.markdown(
    '<div class="loading-screen">'
    '<div class="loading-logo">S J W</div>'
    '<div class="loading-bar"><div class="loading-bar-inner"></div></div>'
    '<div class="loading-text">initializing portfolio...</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================
#  星空背景 + 流星 + 星座 + 量子点光图标
# ============================================================
_stars = "".join(f'<div class="s{i}"></div>' for i in range(180))
_shooting = "".join(f'<div class="ss{i}"></div>' for i in range(12))

# 7颗相连的星座星星 - 同频移动闪动
# 使用相对坐标，整个星座会一起移动
_constellation_stars = [
    (12, 15), (18, 10), (25, 13), (22, 22),
    (30, 18), (35, 12), (28, 8),
]
_constellation_html = ""
for i, (left_pct, top_pct) in enumerate(_constellation_stars):
    bright = " bright" if i in [1, 3, 5] else ""
    delay = i * 0.4
    _constellation_html += (
        f'<div class="constellation-star{bright}" '
        f'style="left:{left_pct}%;top:{top_pct}%;animation-delay:{delay}s"></div>'
    )
# 星座连线（连接相邻星星）
_lines = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(2,4),(3,6)]
for a, b in _lines:
    ax, ay = _constellation_stars[a]
    bx, by = _constellation_stars[b]
    dx = bx - ax
    dy = by - ay
    length = math.sqrt(dx**2 + dy**2)
    angle = math.degrees(math.atan2(dy, dx))
    _constellation_html += (
        f'<div class="constellation-line" '
        f'style="left:{ax}%;top:{ay}%;width:{length}%;'
        f'transform:rotate({angle}deg);animation-delay:{a*0.3}s"></div>'
    )

# 量子点光图标 - 追逐光、成为光、散发光
def _qdot_svg(icon_type, x, y, color_class="", anim_delay=0):
    """生成由量子点（小圆点）构成的SVG图标"""
    if icon_type == "chase":  # 追逐光 - 奔跑箭头
        dots = [
            (8,18),(12,14),(16,10),(20,6),(24,2),
            (14,18),(18,14),(22,10),
            (26,6),(30,2),(34, -2),
            (10,10),(14,6),(18,2),
        ]
    elif icon_type == "become":  # 成为光 - 人形→星形
        dots = [
            (15,2),(15,8),(15,14),(10,10),(20,10),
            (10,20),(20,20),(15,5),(12,3),(18,3),
            (15,0),(13,1),(17,1),
            (8,12),(22,12),
        ]
    else:  # emit - 散发光 - 圆形辐射
        dots = [
            (15,15),(15,5),(15,25),(5,15),(25,15),
            (8,8),(22,8),(8,22),(22,22),
            (15,10),(15,20),(10,15),(20,15),
            (3,15),(27,15),(15,3),(15,27),
        ]
    circles = ""
    for j, (cx, cy) in enumerate(dots):
        delay = j * 0.15 + anim_delay
        circles += f'<circle cx="{cx}" cy="{cy}" r="2.5" style="animation-delay:{delay}s"/>'
    return (
        f'<div class="qdot-icon {color_class}" style="left:{x}%;top:{y}%">'
        f'<svg width="35" height="30" viewBox="0 0 30 30">{circles}</svg></div>'
    )

_qdot_icons = _qdot_svg("chase", 8, 30, "", 0)
_qdot_icons += _qdot_svg("become", 88, 45, "purple", 0.8)
_qdot_icons += _qdot_svg("emit", 75, 75, "green", 1.5)

st.markdown(
    f'<div class="starfield">{_stars}{_shooting}</div>'
    f'<div class="constellation">{_constellation_html}</div>'
    f'{_qdot_icons}'
    f'<div class="aurora">'
    f'<div class="aurora-layer a1"></div>'
    f'<div class="aurora-layer a2"></div>'
    f'<div class="aurora-layer a3"></div>'
    f'</div>'
    f'<div class="scanline"></div>'
    f'<div class="cursor-glow" id="cursorGlow"></div>'
    f'<script>'
    f'const g=document.getElementById("cursorGlow");'
    f'document.addEventListener("mousemove",e=>{{g.style.left=e.clientX+"px";g.style.top=e.clientY+"px";}});'
    f'</script>',
    unsafe_allow_html=True,
)

# ============================================================
#  侧边栏 — 导航 + 个人信息 + 社交链接
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-profile">'
        '<div class="sidebar-avatar">S</div>'
        '<div class="sidebar-name">孙杰伟 (Sun Jiewei)</div>'
        '<div class="sidebar-role">AI Agent Developer</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-section-label">Navigation</div>'
        '<div class="sidebar-nav">'
        '<a href="#about">01 — About</a>'
        '<a href="#experience">02 — Experience</a>'
        '<a href="#projects">03 — Projects</a>'
        '<a href="#skills">04 — Skills</a>'
        '<a href="#education">05 — Education</a>'
        '<a href="#terminal">06 — Terminal</a>'
        '<a href="#guestbook">07 — Guestbook</a>'
        '<a href="#contact">08 — Contact</a>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-section-label">Connect</div>'
        '<div class="sidebar-social">'
        '<a href="https://github.com/jws573" target="_blank" title="GitHub">GH</a>'
        '<a href="mailto:3028789475@qq.com" title="Email">@</a>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-availability">'
        '<span class="dot"></span><span>Open to Opportunities</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # 侧边栏编辑入口
    st.markdown(
        '<div class="sidebar-section-label">Customize</div>',
        unsafe_allow_html=True,
    )
    if st.button("Edit Profile Info", use_container_width=True, key="sidebar_edit"):
        st.session_state.show_editor = not st.session_state.get("show_editor", False)

# ============================================================
#  HERO
# ============================================================
st.markdown(
    '<div class="hero-title">Sun Jiewei</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">AI Agent Developer &amp; Explorer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-tagline">'
    '南昌大学 (211) · 人工智能 · AI 实验班 · 2025 级<br>'
    '专注 LLM + Agent 应用开发，将大模型能力转化为解决实际问题的工具'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-status">'
    '<span class="status-dot"></span>'
    'Open to Agent Internship Opportunities'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="scroll-indicator">'
    '<div class="scroll-arrow"></div>'
    '<div class="scroll-text">SCROLL</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================
#  数据统计卡片
# ============================================================
st.markdown(
    '<div class="stats-row">'
    '<div class="stat-card reveal" style="animation-delay:0.1s">'
    '<div class="stat-num">1</div>'
    '<div class="stat-label">Production Project</div></div>'
    '<div class="stat-card reveal" style="animation-delay:0.2s">'
    '<div class="stat-num">5+</div>'
    '<div class="stat-label">Core Technologies</div></div>'
    '<div class="stat-card reveal" style="animation-delay:0.3s">'
    '<div class="stat-num">211</div>'
    '<div class="stat-label">University Tier</div></div>'
    '<div class="stat-card reveal" style="animation-delay:0.4s">'
    '<div class="stat-num">∞</div>'
    '<div class="stat-label">Curiosity</div></div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  信息编辑面板 (可折叠)
# ============================================================
if st.session_state.get("show_editor", False):
    st.markdown('<a id="edit"></a>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-hdr reveal">'
        '<span class="num">E</span> EDIT PROFILE'
        '<span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    with st.form("profile_editor"):
        st.markdown(
            '<div class="edit-panel">'
            '<div class="edit-panel-title">// Customize your profile information</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            ed_name_cn = st.text_input("中文姓名", value=st.session_state.get("p_name_cn", "孙杰伟"))
            ed_university = st.text_input("University", value=st.session_state.get("p_university", "南昌大学 (211)"))
            ed_major = st.text_input("Major", value=st.session_state.get("p_major", "人工智能 · AI 实验班"))
            ed_year = st.text_input("Year", value=st.session_state.get("p_year", "2025 级"))
        with c2:
            ed_name_en = st.text_input("English Name", value=st.session_state.get("p_name_en", "Sun Jiewei"))
            ed_email = st.text_input("Email", value=st.session_state.get("p_email", "3028789475@qq.com"))
            ed_github = st.text_input("GitHub URL", value=st.session_state.get("p_github", "https://github.com/jws573"))
            ed_status = st.text_input("Status", value=st.session_state.get("p_status", "Open to Agent Internship Opportunities"))

        ed_bio = st.text_area(
            "Bio / 自我介绍",
            value=st.session_state.get(
                "p_bio",
                "热衷于探索 LLM + Agent 的应用边界。独立开发智能编程助手，擅长 Prompt Engineering & Advanced RAG。希望将大语言模型的能力转化为解决实际问题的工具。"
            ),
            height=80,
        )

        st.markdown('</div>', unsafe_allow_html=True)

        col_save, col_cancel = st.columns([1, 1])
        with col_save:
            save = st.form_submit_button("Save Changes", use_container_width=True)
        with col_cancel:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

    if save:
        st.session_state.p_name_cn = ed_name_cn
        st.session_state.p_name_en = ed_name_en
        st.session_state.p_university = ed_university
        st.session_state.p_major = ed_major
        st.session_state.p_year = ed_year
        st.session_state.p_email = ed_email
        st.session_state.p_github = ed_github
        st.session_state.p_status = ed_status
        st.session_state.p_bio = ed_bio
        st.session_state.show_editor = False
        st.rerun()
    if cancel:
        st.session_state.show_editor = False
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 获取编辑后的值（或默认值）
_p = lambda key, default: st.session_state.get(key, default)

# ============================================================
#  ABOUT
# ============================================================
st.markdown('<a id="about"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">01</span> ABOUT'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

bio_text = _p("p_bio", "热衷于探索 LLM + Agent 的应用边界。独立开发智能编程助手，擅长 Prompt Engineering & Advanced RAG。希望将大语言模型的能力转化为解决实际问题的工具。")

st.markdown(
    '<div class="terminal"><div class="terminal-bar">'
    '<span class="dot-r">●</span><span class="dot-y">●</span><span class="dot-g">●</span>'
    '<span class="terminal-title">~/about_me.json</span></div>'
    '<div class="terminal-body">'
    '{<br>'
    f'&nbsp;&nbsp;<span class="key">"name"</span>: <span class="str">"{_p("p_name_cn", "孙杰伟")}"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"name_en"</span>: <span class="str">"{_p("p_name_en", "Sun Jiewei")}"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"university"</span>: <span class="str">"{_p("p_university", "南昌大学 (211)")}"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"major"</span>: <span class="str">"{_p("p_major", "人工智能 · AI 实验班")}"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"enrolled"</span>: <span class="str">"{_p("p_year", "2025 级")}"</span>,<br>'
    f'&nbsp;&nbsp;<span class="key">"focus"</span>: [<span class="str">"LLM"</span>, <span class="str">"Agent"</span>, <span class="str">"RAG"</span>],<br>'
    f'&nbsp;&nbsp;<span class="key">"available"</span>: <span class="bool">true</span><br>'
    '}<br><br>'
    f'<span class="comment">// {bio_text}</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  EXPERIENCE — 时间线
# ============================================================
st.markdown('<a id="experience"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">02</span> EXPERIENCE &amp; HIGHLIGHTS'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

experiences = [
    {
        "title": "Coding Assistant Agent — 独立开发",
        "meta": "2025 · LangChain + LangGraph · Hugging Face Spaces",
        "desc": "从零构建智能编程助手，实现代码执行、RAG 知识检索、多轮记忆、自动重试等核心功能，部署上线供公网访问。",
        "active": True,
    },
    {
        "title": "Advanced RAG 系统研究",
        "meta": "2025 · LlamaIndex + Chroma + 百炼 Embedding",
        "desc": "深入研究 RAG 架构优化，包括分块策略、混合检索、Re-ranking 等技术方案。",
        "active": False,
    },
    {
        "title": "MCP (Model Context Protocol) 探索",
        "meta": "2025 · Agent Tool Use",
        "desc": "学习 MCP 协议，探索 Agent 与外部工具的安全高效集成方式。",
        "active": False,
    },
    {
        "title": "班级团支书 — 团队协作经历",
        "meta": "University · Leadership",
        "desc": "负责班级团组织工作，锻炼了沟通协调与团队管理能力。",
        "active": False,
    },
]

for i, exp in enumerate(experiences):
    dot_class = "timeline-dot active" if exp["active"] else "timeline-dot"
    st.markdown(
        f'<div class="timeline">'
        f'<div class="timeline-item" style="animation-delay:{i * 0.12}s">'
        f'<div class="{dot_class}"></div>'
        f'<div class="timeline-title">{exp["title"]}</div>'
        f'<div class="timeline-meta">{exp["meta"]}</div>'
        f'<div class="timeline-desc">{exp["desc"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  PROJECTS
# ============================================================
st.markdown('<a id="projects"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">03</span> PROJECTS'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

# 项目1 — 主项目
st.markdown(
    '<div class="project-card reveal" style="animation-delay:0.1s">'
    '<div class="project-card-body">'
    '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.4rem">'
    '<div style="font-size:1.1rem;font-weight:700;color:#7EE8FA">Coding Assistant Agent</div>'
    '<div><span class="project-card-tag tag-production">Production</span></div>'
    '</div>'
    '<div style="color:#8BA4B8;font-size:0.82rem;margin-top:0.5rem;line-height:1.5">'
    '基于 LangChain + LangGraph 的智能编程助手。支持安全代码执行、'
    'RAG 知识检索、多轮对话记忆、自动错误重试。已部署至 Hugging Face Spaces 公网访问。'
    '</div>'
    '<div style="margin-top:0.8rem;display:flex;flex-wrap:wrap;gap:0.3rem">'
    '<span class="badge b0" style="animation:none;font-size:0.7rem">LangChain</span>'
    '<span class="badge b1" style="animation:none;font-size:0.7rem">LangGraph</span>'
    '<span class="badge b2" style="animation:none;font-size:0.7rem">RAG</span>'
    '<span class="badge b3" style="animation:none;font-size:0.7rem">Chroma</span>'
    '<span class="badge b4" style="animation:none;font-size:0.7rem">Gradio</span>'
    '</div>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.link_button("View Live Demo →", "https://jieweisun-coding-agent.hf.space", use_container_width=False)

st.markdown("<br>", unsafe_allow_html=True)

# 功能亮点
features = [
    ("Secure Code Execution", "子进程 + 临时文件 + 超时机制，安全隔离执行 Python 代码"),
    ("Local RAG Retrieval", "Chroma 向量库 + 阿里百炼 Embedding，精准检索私有文档"),
    ("Multi-turn Memory", "LangGraph Checkpointer 自动维护会话上下文"),
    ("Auto Retry on Error", "代码执行出错时 Agent 自动分析错误并重试 (max 3)"),
    ("Free-tier Quota", "基于 IP 的终身 10 次免费试用，支持自定义 API Key"),
    ("Web Interface", "Gradio 聊天界面，部署在 Hugging Face Spaces 公网可访问"),
]
for i, (title, desc) in enumerate(features):
    st.markdown(
        f'<div class="feat" style="animation-delay:{i * 0.06}s">'
        f'<div class="feat-title">▸ {title}</div>'
        f'<div class="feat-desc">{desc}</div></div>',
        unsafe_allow_html=True,
    )

# 技术栈终端
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div class="terminal"><div class="terminal-bar">'
    '<span class="dot-r">●</span><span class="dot-y">●</span><span class="dot-g">●</span>'
    '<span class="terminal-title">tech_stack.toml</span></div>'
    '<div class="terminal-body">'
    f'<span class="comment"># Core Stack</span><br>'
    f'<span class="key">agent_framework</span> = <span class="str">"LangChain 1.x + LangGraph"</span><br>'
    f'<span class="key">llm_provider</span>&nbsp;&nbsp; = <span class="str">"阿里百炼 qwen-max"</span><br>'
    f'<span class="key">vector_db</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"Chroma"</span><br>'
    f'<span class="key">embedding</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"阿里百炼 text-embedding-v3"</span><br>'
    f'<span class="key">frontend</span>&nbsp;&nbsp;&nbsp;&nbsp; = <span class="str">"Gradio 6.x"</span><br>'
    f'<span class="key">deployment</span>&nbsp;&nbsp;&nbsp; = <span class="str">"Hugging Face Spaces"</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  SKILLS — 进度条 + 徽章
# ============================================================
st.markdown('<a id="skills"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">04</span> SKILLS'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

skill_groups = {
    "Agent & LLM": [
        ("LangChain / LangGraph", 90),
        ("RAG Architecture", 85),
        ("Prompt Engineering", 88),
        ("MCP Protocol", 65),
    ],
    "Data & Backend": [
        ("Chroma / LlamaIndex", 80),
        ("Python", 90),
        ("FastAPI", 70),
        ("MySQL", 65),
    ],
    "ML & Tools": [
        ("PyTorch", 60),
        ("Docker", 65),
        ("Streamlit / Gradio", 85),
        ("Git / GitHub", 80),
    ],
}

for group_name, skills in skill_groups.items():
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;'
        f'color:{GLACIER_DIM};margin:1rem 0 0.3rem">{group_name}</div>',
        unsafe_allow_html=True,
    )
    for i, (name, level) in enumerate(skills):
        color = GLACIER if level >= 80 else (ACCENT_PURPLE if level >= 70 else ACCENT_AMBER)
        st.markdown(
            f'<div class="skill-bar-wrap" style="animation-delay:{i * 0.1}s">'
            f'<div class="skill-bar-label"><span>{name}</span><span>{level}%</span></div>'
            f'<div class="skill-bar-track">'
            f'<div class="skill-bar-fill" style="width:{level}%;background:linear-gradient(90deg,{GLACIER},{color})"></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

# 徽章云
st.markdown("<br>", unsafe_allow_html=True)
techs = [
    "LangChain", "LangGraph", "RAG", "Prompt Engineering",
    "LlamaIndex", "MCP", "Docker", "Streamlit",
    "FastAPI", "PyTorch", "MySQL", "Python",
    "Gradio", "Chroma", "Hugging Face",
]
badges_html = "".join(
    f'<span class="badge b{i % 5}" style="animation-delay:{i * 0.12}s">{t}</span>'
    for i, t in enumerate(techs)
)
st.markdown(
    f'<div class="glow-card" style="text-align:center;padding:1.2rem;animation-delay:0.2s">'
    f'{badges_html}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  EDUCATION
# ============================================================
st.markdown('<a id="education"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">05</span> EDUCATION'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="glow-card" style="animation-delay:0.1s">'
    '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem">'
    '<div>'
    '<div style="font-size:1.05rem;font-weight:700;color:#E0F0FF">南昌大学 (Nanchang University)</div>'
    '<div style="font-size:0.85rem;color:#7EE8FA;margin-top:0.15rem">人工智能 · AI 实验班</div>'
    '<div style="font-size:0.78rem;color:#8BA4B8;margin-top:0.15rem">2025 级 · 211 工程重点建设高校</div>'
    '</div>'
    '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;'
    'color:#4A9EAF;padding:0.2rem 0.6rem;border:1px solid rgba(0,212,255,0.15);border-radius:8px">'
    'Nanchang, China</div>'
    '</div>'
    '<div style="margin-top:0.8rem;color:#8BA4B8;font-size:0.8rem;line-height:1.6">'
    '核心课程：机器学习、深度学习、自然语言处理、计算机视觉、数据结构与算法。'
    '课余专注 LLM + Agent 方向自学，结合项目实践持续提升工程能力。'
    '</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  INTERACTIVE TERMINAL
# ============================================================
st.markdown('<a id="terminal"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">06</span> INTERACTIVE TERMINAL'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("system", "Welcome to jws-terminal v2.0. Type 'help' to explore."),
    ]

COMMANDS = {
    "help": (
        "Available commands:\n"
        "  help      — Show this help message\n"
        "  about     — Who am I?\n"
        "  skills    — My tech stack\n"
        "  project   — Featured project\n"
        "  contact   — Contact info\n"
        "  hire      — Why hire me?\n"
        "  ed        — Education\n"
        "  inspire   — A motivational quote\n"
        "  date      — Current time\n"
        "  clear     — Clear terminal\n"
    ),
    "about": lambda: (
        f"{_p('p_name_en', 'Sun Jiewei')} ({_p('p_name_cn', '孙杰伟')})\n"
        f"  University: {_p('p_university', '南昌大学 (211)')}\n"
        f"  Major: {_p('p_major', '人工智能 · AI 实验班')}\n"
        f"  Focus: LLM + Agent application development\n"
        f"  Goal: Turning LLM capabilities into practical tools"
    ),
    "skills": (
        "Tech Stack:\n"
        "  [Agent]    LangChain, LangGraph, RAG, MCP\n"
        "  [LLM]      Prompt Engineering, Fine-tuning\n"
        "  [Data]     Chroma, LlamaIndex, MySQL\n"
        "  [Deploy]   Docker, Hugging Face, Streamlit, Gradio\n"
        "  [Backend]  FastAPI, PyTorch, Python"
    ),
    "project": (
        "Coding Assistant Agent\n"
        "  A LangChain + LangGraph powered coding assistant.\n"
        "  Features: code exec, RAG, auto-retry, multi-turn memory.\n"
        "  -> https://jieweisun-coding-agent.hf.space"
    ),
    "contact": lambda: (
        f"Contact:\n"
        f"  Email:  {_p('p_email', '3028789475@qq.com')}\n"
        f"  GitHub: {_p('p_github', 'https://github.com/jws573')}\n"
        f"  Status: {_p('p_status', 'Open to Agent internship opportunities')}"
    ),
    "hire": (
        "Why hire me?\n"
        "  1. I build and ship real projects (deployed on HF Spaces)\n"
        "  2. I learn fast — self-taught LangChain, RAG, MCP in months\n"
        "  3. I value teamwork — experience as class league secretary\n"
        "  4. I'm passionate about Agent technology and its applications"
    ),
    "ed": (
        "Education:\n"
        "  Nanchang University (南昌大学) — 211\n"
        "  Major: Artificial Intelligence, AI Experimental Class\n"
        "  Enrolled: 2025\n"
        "  Core: ML, DL, NLP, CV, Data Structures"
    ),
    "inspire": (
        "技术日新月异，但勤奋永恒。\n"
        "好奇为灯，毅力为杖，\n"
        "在知识与实践海洋里探索未知，\n"
        "你的人生刚刚开始！！！"
    ),
    "date": lambda: datetime.now().strftime("  Server time: %Y-%m-%d %H:%M:%S CST"),
}

def process_command(cmd):
    cmd = cmd.strip().lower()
    if not cmd:
        return None
    if cmd == "clear":
        st.session_state.chat_history = [("system", "Terminal cleared.")]
        return True
    if cmd in COMMANDS:
        val = COMMANDS[cmd]
        return val() if callable(val) else val
    return f"Command not found: '{cmd}'. Type 'help' for available commands."

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
    f'<span class="dot-r">●</span><span class="dot-y">●</span><span class="dot-g">●</span>'
    f'<span class="terminal-title">jws-terminal v2.0 — interactive</span></div>'
    f'<div class="terminal-body">{chat_html}</div></div>',
    unsafe_allow_html=True,
)

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
        pass
    elif result:
        st.session_state.chat_history.append(("bot", result))
    st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  GUESTBOOK
# ============================================================
st.markdown('<a id="guestbook"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">07</span> GUESTBOOK'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="color:#8BA4B8;font-size:0.82rem;margin-bottom:0.8rem;'
    'font-family:\'JetBrains Mono\',monospace">'
    'Leave a message. Recruiters welcome to drop contact info.</div>',
    unsafe_allow_html=True,
)

GUESTBOOK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".guestbook.json")

def load_guestbook():
    if os.path.exists(GUESTBOOK_FILE):
        try:
            with open(GUESTBOOK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [{"name": "System", "msg": "Welcome! Be the first to sign.", "time": "2025-01-01"}]

def save_guestbook(entries):
    with open(GUESTBOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

if "guestbook" not in st.session_state:
    st.session_state.guestbook = load_guestbook()

with st.form("guestbook_form", clear_on_submit=True):
    gb_cols = st.columns([2, 4])
    with gb_cols[0]:
        gb_name = st.text_input("Name", placeholder="Your name")
    with gb_cols[1]:
        gb_msg = st.text_input("Message", placeholder="Leave a message or contact info...")
    gb_submit = st.form_submit_button("Sign Guestbook")

if gb_submit and gb_name.strip() and gb_msg.strip():
    entry = {
        "name": gb_name.strip(),
        "msg": gb_msg.strip(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.guestbook.insert(0, entry)
    save_guestbook(st.session_state.guestbook)
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
for i, entry in enumerate(st.session_state.guestbook[:15]):
    col_entry, col_del = st.columns([8, 1])
    with col_entry:
        st.markdown(
            f'<div class="guestbook-entry" style="animation-delay:{i * 0.04}s">'
            f'<span class="guestbook-name">{entry["name"]}</span>'
            f'<span class="guestbook-time">{entry["time"]}</span>'
            f'<div class="guestbook-msg">{entry["msg"]}</div></div>',
            unsafe_allow_html=True,
        )
    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("del", key=f"gb_del_{i}", help="Delete this message"):
            st.session_state.guestbook.pop(i)
            save_guestbook(st.session_state.guestbook)
            st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  CONTACT
# ============================================================
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-hdr reveal">'
    '<span class="num">08</span> CONTACT'
    '<span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="color:#8BA4B8;font-size:0.85rem;margin-bottom:1rem;line-height:1.6">'
    'I\'m actively seeking Agent-related internship and work opportunities.<br>'
    'Feel free to reach out — whether it\'s about collaboration, recruitment, or just tech chat.'
    '</div>',
    unsafe_allow_html=True,
)

github_url = _p("p_github", "https://github.com/jws573")
email_addr = _p("p_email", "3028789475@qq.com")

st.markdown(
    f'<div style="margin:1rem 0">'
    f'<a class="contact-btn" href="{github_url}" target="_blank">GitHub Profile</a>'
    f'<a class="contact-btn-outline" href="mailto:{email_addr}">Send Email</a>'
    f'<a class="contact-btn-outline" href="https://jieweisun-coding-agent.hf.space" target="_blank">Live Demo</a>'
    f'</div>',
    unsafe_allow_html=True,
)

# 联系表单
st.markdown("<br>", unsafe_allow_html=True)
with st.form("contact_form", clear_on_submit=True):
    st.markdown(
        '<div class="edit-panel">'
        '<div class="edit-panel-title">// Or send me a quick message</div>',
        unsafe_allow_html=True,
    )
    cf_cols = st.columns(2)
    with cf_cols[0]:
        cf_name = st.text_input("Your Name", placeholder="Name")
    with cf_cols[1]:
        cf_email = st.text_input("Your Email", placeholder="email@example.com")
    cf_msg = st.text_area("Message", placeholder="What would you like to discuss?", height=80)
    st.markdown('</div>', unsafe_allow_html=True)
    cf_submit = st.form_submit_button("Send Message", use_container_width=True)

if cf_submit and cf_name.strip() and cf_msg.strip():
    # 保存到留言板
    entry = {
        "name": f"{cf_name.strip()} (contact)",
        "msg": f"[{cf_email.strip() or 'no email'}] {cf_msg.strip()}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.guestbook.insert(0, entry)
    save_guestbook(st.session_state.guestbook)
    st.success("Message sent! I'll get back to you soon.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
#  页脚
# ============================================================
st.markdown(
    '<div class="footer">'
    '<div style="color:#8BA4B8;font-size:0.8rem">'
    'Thank you for visiting. Let\'s build the future of AI Agents together.'
    '</div>'
    '<div style="color:#3D5A6E;font-size:0.65rem;margin-top:0.6rem">'
    '/* Built with Streamlit | Sun Jiewei &copy; 2025 */'
    '</div></div>'
    '<script>'
    'const observer=new IntersectionObserver((entries)=>{'
    'entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("visible");'
    'observer.unobserve(e.target);}});'
    '},{threshold:0.1,rootMargin:"0px 0px -40px 0px"});'
    'document.querySelectorAll(".reveal,.reveal-left").forEach(el=>observer.observe(el));'
    '</script>',
    unsafe_allow_html=True,
)
