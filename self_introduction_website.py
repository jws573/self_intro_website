import streamlit as st

# ---------- 页面配置 ----------
st.set_page_config(
    page_title="孙杰伟 · AI Agent 探索学习者",   # 浏览器标签页标题
    page_icon="👨‍💻",
    layout="centered",
)

# ---------- 个人信息 ----------
name = "孙杰伟"          
email = "3028789475@qq.com"  
github_username = "jws573/coding-assistant-agent"     

# ---------- 页面内容 ----------
# 头部大标题
st.title(f"👋 你好，我是 {name}")
st.caption("南昌大学 人工智能专业 · 技术追求者")

# 分隔线
st.divider()

# 自我介绍
st.subheader("📖 关于我")
st.write("""
- 热衷于探索 **LLM + Agent** 的应用边界，注重工程化思维与实际落地。
- 利用vibe coding独立开发了一款能辅助代码生成与调试的智能编程助手，擅长 Prompt Engineering、advanced RAG 设计思路与方案等。
- 目前正在寻找 **Agent 实习 / 工作机会**，希望将大语言模型的能力转化为解决实际问题的工具。
""")

st.divider()

st.subheader("💪 我的优势")

advantages = """
- 🚀 **项目落地能力**：独立开发的 Agent 项目已部署公网（Hugging Face Space），掌握从开发到上线的完整流程。
- 🧠 **技术自驱力**：围绕目标岗位主动学习 LangChain、LangGraph、RAG 、llamaindex、mcp等技术，能快速上手并产出可用原型。
- 🤝 **团队协作与执行力**：重视沟通、积极配合团队目标，。
- 📚 **学术背景**：南昌大学 AI 实验班（211），课程与自学结合，持续跟进 LLM + Agent 前沿方向。
"""
st.markdown(advantages)

st.divider()

st.subheader("🚀 核心项目：智能编程助手 Agent")

# 第一行：项目名称 + 链接按钮并排
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.markdown("### coding-assistant-agent")
with col_btn:
    st.link_button("🔗 打开项目 Space", "https://jieweisun-coding-agent.hf.space")

# 技术栈表格（修正后）
st.markdown("#### 📚 技术栈")
tech_table = """
| 类别 | 技术 |
|------|------|
| Agent框架 | LangChain 1.x + langgraph |
| 大模型 | 阿里百炼 qwen-max |
| 向量数据库 | Chroma |
| Embedding | 阿里百炼 text-embedding-v3 |
| 前端界面 | Gradio 6.x |
| 部署平台 | Hugging Face Spaces |
"""
st.markdown(tech_table)

# 我的角色
st.info("**👤 我的角色**：独立开发者（全栈 + 提示词优化）")

# 成果亮点（使用带图标的列表）
st.markdown("#### ✨ 成果亮点")
highlights = """
- 🔒 **安全代码执行**：通过子进程+临时文件+超时机制隔离执行 Python 代码
- 📚 **本地知识库检索（RAG）**：基于 Chroma 向量库 + 阿里百炼 Embedding 检索私有文档
- 💬 **多轮对话记忆**：基于 LangGraph Checkpointer 自动维护会话上下文
- 🔁 **工具自动重试**：代码执行出错时，Agent 自动分析并重试（最多3次）
- 🎫 **免费额度管理**：基于 IP 的终身10次免费试用，超出后可填入自己的 API Key
- 🌐 **Web 界面**：Gradio 构建的聊天界面，支持公网访问（Hugging Face Spaces）
"""
st.markdown(highlights)



st.divider()

# 技术栈
st.subheader("🛠️ 技术栈（在不断学习中）")
cols = st.columns(4)
techs = [ "LangChain", "RAG", "Prompt Engineering","docker", "llamaindex", "Streamlit", "llm_base_knowledge","pytorch","mysql","langgraph","FastAPI","MCP"]
for i, tech in enumerate(techs):
    cols[i % 4].markdown(f"- {tech}")

st.divider()

# 联系方式
st.subheader("📫 联系我")
col_github, col_mail = st.columns(2)
with col_github:
    st.markdown(f"[GitHub](https://github.com/{github_username})")
with col_mail:
    st.markdown(f"[{email}](mailto:{email})")
 # 没有可以删掉

st.caption("✨ 感谢访问 — 期待与志同道合的团队一起探索 Agent ！")