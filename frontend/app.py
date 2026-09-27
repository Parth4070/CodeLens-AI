import os
import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = os.getenv(
    "CODELENS_API_URL",
    "http://127.0.0.1:8000"
)


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="CodeLens AI",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #0b0f14;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Header ---------- */

    .hero {
        padding: 1rem 0 1.5rem 0;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.25rem;
    }

    .hero-title span {
        color: #8b7cff;
    }

    .hero-subtitle {
        color: #8b949e;
        font-size: 1.05rem;
    }

    /* ---------- Cards ---------- */

    .card {
        background: #111720;
        border: 1px solid #222b36;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .source-card {
        background: #111720;
        border: 1px solid #252f3b;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-top: 0.6rem;
    }

    .source-file {
        font-weight: 700;
        color: #e6edf3;
        font-size: 0.95rem;
    }

    .source-symbol {
        color: #9aa5b1;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }

    .source-lines {
        color: #6f7b88;
        font-size: 0.78rem;
        margin-top: 0.3rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #0e131a;
        border-right: 1px solid #202832;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* ---------- Chat ---------- */

    .answer-label {
        color: #8b7cff;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .sources-label {
        color: #8b7cff;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* ---------- Status ---------- */

    .status {
        padding: 0.45rem 0.7rem;
        border-radius: 7px;
        font-size: 0.8rem;
        background: #122016;
        border: 1px solid #24492d;
        color: #7ee787;
        display: inline-block;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session state
# ============================================================

if "repo_id" not in st.session_state:
    st.session_state.repo_id = ""

if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown("## ⌘ CodeLens AI")

    st.caption("Repository Intelligence")

    st.divider()

    st.markdown("### Repository")

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/user/repository",
    )

    if st.button(
        "Clone & Index Repository",
        use_container_width=True,
        type="primary",
    ):

        if not repo_url.strip():
            st.warning("Enter a GitHub repository URL first.")

        else:

            with st.spinner("Cloning and indexing repository..."):

                try:

                    response = requests.post(
                        f"{API_URL}/github/clone",
                        json={
                            "repo_url": repo_url.strip()
                        },
                        timeout=600,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.repo_id = data["repo_id"]
                        st.session_state.repo_name = data["repository"]

                        st.session_state.messages = []

                        st.success(
                            f"Indexed {data['repository']} "
                            f"({data['document_count']} chunks)"
                        )

                    else:

                        try:
                            detail = response.json().get(
                                "detail",
                                response.text
                            )
                        except Exception:
                            detail = response.text

                        st.error(
                            f"Indexing failed: {detail}"
                        )

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to CodeLens API. "
                        "Make sure FastAPI is running."
                    )

                except Exception as e:
                    st.error(str(e))

    st.divider()

    if st.session_state.repo_id:

        st.markdown("### Active Repository")

        st.markdown(
            f"""
            <div class="status">
                ● {st.session_state.repo_name}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            f"Repository ID: `{st.session_state.repo_id}`"
        )

    else:

        st.info(
            "Clone a GitHub repository to start asking questions."
        )

    st.divider()

    st.caption("CodeLens AI")
    st.caption("AI-powered repository understanding")


# ============================================================
# Main header
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            <span>CodeLens</span> AI
        </div>
        <div class="hero-subtitle">
            Understand your codebase with natural language.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Empty state
# ============================================================

if not st.session_state.repo_id:

    st.markdown(
        """
        <div class="card">

        ### 👋 Welcome to CodeLens

        Connect a GitHub repository from the sidebar and ask
        questions about its codebase.

        <br>

        **Try questions like:**

        - Where are users created?
        - How does authentication work?
        - Where is the database initialized?
        - What does `create_user()` do?
        - How does the API handle requests?

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Chat history
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown(
                '<div class="sources-label">SOURCES</div>',
                unsafe_allow_html=True,
            )

            for source in message["sources"]:

                file_path = source.get(
                    "file_path",
                    "Unknown file"
                )

                class_name = source.get("class_name")
                function_name = source.get("function_name")

                symbols = []

                if class_name:
                    symbols.append(class_name)

                if function_name:
                    symbols.append(function_name)

                symbol_text = (
                    " → ".join(symbols)
                    if symbols
                    else source.get("chunk_type", "")
                )

                start_line = source.get("start_line")
                end_line = source.get("end_line")

                if start_line and end_line:
                    line_text = (
                        f"Lines {start_line}–{end_line}"
                    )
                else:
                    line_text = ""

                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-file">
                            📄 {file_path}
                        </div>

                        <div class="source-symbol">
                            {symbol_text}
                        </div>

                        <div class="source-lines">
                            {line_text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# Chat input
# ============================================================

question = st.chat_input(
    "Ask anything about your repository..."
)


if question:

    if not st.session_state.repo_id:

        st.warning(
            "Please clone and index a repository first."
        )

        st.stop()

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Analyzing your codebase..."):

            try:

                response = requests.post(
                    f"{API_URL}/rag/ask",
                    json={
                        "repo_id": st.session_state.repo_id,
                        "question": question,
                        "top_k": 5,
                    },
                    timeout=300,
                )

                if response.status_code != 200:

                    try:
                        detail = response.json().get(
                            "detail",
                            response.text
                        )
                    except Exception:
                        detail = response.text

                    st.error(
                        f"Request failed: {detail}"
                    )

                    st.stop()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer returned."
                )

                sources = data.get(
                    "sources",
                    []
                )

                st.markdown(answer)

                # Sources
                if sources:

                    st.markdown(
                        '<div class="sources-label">SOURCES</div>',
                        unsafe_allow_html=True,
                    )

                    for source in sources:

                        file_path = source.get(
                            "file_path",
                            "Unknown file"
                        )

                        class_name = source.get(
                            "class_name"
                        )

                        function_name = source.get(
                            "function_name"
                        )

                        symbols = []

                        if class_name:
                            symbols.append(class_name)

                        if function_name:
                            symbols.append(function_name)

                        symbol_text = (
                            " → ".join(symbols)
                            if symbols
                            else source.get(
                                "chunk_type",
                                ""
                            )
                        )

                        start_line = source.get(
                            "start_line"
                        )

                        end_line = source.get(
                            "end_line"
                        )

                        if start_line and end_line:
                            line_text = (
                                f"Lines {start_line}–{end_line}"
                            )
                        else:
                            line_text = ""

                        st.markdown(
                            f"""
                            <div class="source-card">
                                <div class="source-file">
                                    📄 {file_path}
                                </div>

                                <div class="source-symbol">
                                    {symbol_text}
                                </div>

                                <div class="source-lines">
                                    {line_text}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to CodeLens API. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "The repository or LLM may be taking too long."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )