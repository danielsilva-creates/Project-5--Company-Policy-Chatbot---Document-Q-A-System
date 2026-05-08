import streamlit as st
from document_qa import DocumentQA

# Configure the page
st.set_page_config(
    page_title="Company Policy Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Company Policy Q&A Chatbot")
st.write("Ask questions about company policies with AI-powered semantic search.")

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []


# TODO 8: Initialize DocumentQA in session_state
# Check if 'qa_system' exists in st.session_state
# If not, create DocumentQA('data/policies') and store it
# Use st.spinner("Loading policy documents and building search index...")
# Handle any errors with st.error() and st.stop()
# After initialization, assign: qa_system = st.session_state.qa_system

if "qa_system" not in st.session_state:
    with st.spinner("Loading policy documents and building search index..."):
        try:
            st.session_state.qa_system = DocumentQA('data/policies')
            qa_system = st.session_state.qa_system
        except Exception as e:
            st.error(f"Error initializing QA system: {e}")
            st.stop()
else:
    qa_system = st.session_state.qa_system




# Display sidebar with system information
with st.sidebar:
    st.header("📖 System Info")

    # TODO 12: Sidebar with system info and controls
    # 1. Call qa_system.get_stats() to get document and chunk counts
    # 2. Display metrics using st.metric() (Documents, Chunks)
    # 3. List loaded document filenames from stats['documents']
    # 4. Add a "Clear Chat History" button that resets st.session_state.messages and calls st.rerun()
    try:
        stats = qa_system.get_stats()
        st.metric("Documents Loaded", stats['num_documents'])
        st.metric("Chunks Indexed", stats['num_chunks'])
        st.subheader("Loaded Documents")
        for doc in stats['documents']:
            st.write(f"- {doc}")
    except Exception as e:
        st.error(f"Error fetching system stats: {e}")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()







# TODO 9: Display chat history
# Loop through st.session_state.messages
# Use st.chat_message(msg['role']) to display each message
# For assistant messages with 'sources', show sources in an expander
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        if msg['role'] == 'assistant' and 'sources' in msg:
            with st.expander("Sources"):
                for source, node in zip(msg['sources'], msg['nodes']):
                    st.write(f"- {source} (Relevance: {node.score:.2f})")


# TODO 10: Process user input
# Use st.chat_input("Ask a question about company policies...")
# When user sends a message:
# 1. Add it to st.session_state.messages with role='user'
# 2. Display it with st.chat_message("user")
user_input = st.chat_input("Ask a question about company policies...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)


# TODO 11: Generate and display answer with sources
# Inside an st.chat_message("assistant") block:
# 1. Show a spinner while searching
# 2. Call qa_system.answer_question(user_input)
# 3. Display the answer with st.markdown()
# 4. Add to messages history with role='assistant', content, and sources
# 5. Show sources in an st.expander with relevance scores
# 6. Handle errors gracefully
if user_input:
    with st.chat_message("assistant"):
        with st.spinner("Searching for answers..."):
            try:
                answer_dict = qa_system.answer_question(user_input)
                answer = answer_dict.get("answer", "Sorry, I couldn't find an answer.")
                sources = answer_dict.get("sources", [])
                nodes = answer_dict.get("nodes", [])
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "nodes": nodes
                })
                if sources:
                    with st.expander("Sources"):
                        for i in range(len(sources)):
                            source = sources[i]
                            node = nodes[i]
                            st.write(f"- {source} (Relevance: {node.score:.2f})")
            except Exception as e:
                st.error(f"Error generating answer: {e}")
