import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)


# --------------------------
# Session State
# --------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------
# Header
# --------------------------

st.title("🤖 AI Research Assistant")
st.caption("Chat with your PDFs using RAG + Ollama")


# --------------------------
# Sidebar
# --------------------------

with st.sidebar:

    st.header("📂 Document Upload")


    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )


    if uploaded_file:

        st.success(
            f"Selected: {uploaded_file.name}"
        )


        if st.button("📤 Upload & Process"):

            try:

                with st.spinner(
                    "Creating embeddings..."
                ):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }


                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=120
                    )


                    if response.status_code == 200:

                        st.success(
                            "✅ PDF processed successfully"
                        )


                    else:

                        st.error(
                            response.text
                        )


            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )



    st.divider()


    st.subheader("⚙ Server Status")


    try:

        health = requests.get(
            f"{API_URL}/health",
            timeout=5
        )


        if health.status_code == 200:

            st.success(
                "🟢 Backend Connected"
            )

        else:

            st.error(
                "🔴 Backend Error"
            )


    except:

        st.error(
            "🔴 Backend Offline"
        )



    st.divider()


    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()



# --------------------------
# Main Layout
# --------------------------

left, right = st.columns(
    [3,1]
)



# --------------------------
# Chat Section
# --------------------------

with left:

    st.subheader(
        "💬 Chat"
    )


    question = st.chat_input(
        "Ask something about your PDF..."
    )


    if question:


        with st.spinner(
            "🤖 Thinking..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "question": question
                    },
                    timeout=120
                )


                if response.status_code == 200:


                    result = response.json()


                    # Fix missing question key

                    if "question" not in result:

                        result["question"] = question


                    if "answer" not in result:

                        result["answer"] = (
                            "No answer returned from backend."
                        )


                    st.session_state.chat_history.append(
                        result
                    )


                    st.rerun()



                else:

                    st.error(
                        response.text
                    )


            except Exception as e:

                st.error(
                    f"Chat Error: {e}"
                )



# --------------------------
# Statistics
# --------------------------

with right:


    st.subheader(
        "📊 Statistics"
    )


    try:


        docs_response = requests.get(
            f"{API_URL}/documents",
            timeout=5
        )


        if docs_response.status_code == 200:


            docs = docs_response.json()


            total_docs = len(
                docs.get(
                    "documents",
                    []
                )
            )


        else:

            total_docs = 0



    except:

        total_docs = 0



    st.metric(
        "📄 Uploaded PDFs",
        total_docs
    )


    st.metric(
        "💬 Questions Asked",
        len(
            st.session_state.chat_history
        )
    )



# --------------------------
# Conversation History
# --------------------------

st.divider()


st.subheader(
    "💬 Conversation"
)



if not st.session_state.chat_history:

    st.info(
        "👋 Upload a PDF and start chatting."
    )



for item in reversed(
    st.session_state.chat_history
):


    if not isinstance(
        item,
        dict
    ):
        continue



    question = item.get(
        "question",
        "Unknown question"
    )


    answer = item.get(
        "answer",
        "No answer"
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )


        sources = item.get(
            "sources",
            []
        )


        if sources:


            with st.expander(
                "📚 Sources"
            ):


                for source in sources:


                    st.write(
                        f"📄 {source.get('source','Unknown')} | Page {source.get('page','N/A')}"
                    )



        st.caption(
            f"⚡ Response Time: {item.get('response_time',0)} sec"
        )