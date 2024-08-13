import streamlit as st
import os
import shutil
import json
from llama_index.core import StorageContext, load_index_from_storage
from datetime import datetime
from streamlit_pills import pills
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def ensure_examples_dir():
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    os.makedirs(examples_dir, exist_ok=True)
    return examples_dir

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Ensure the uploaded_files directory exists
def ensure_upload_dir():
    upload_dir = os.path.join(os.path.dirname(__file__), "uploaded_files")
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def save_example():
    examples_dir = ensure_examples_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    example_name = f"example_{timestamp}"
    example_dir = os.path.join(examples_dir, example_name)
    os.makedirs(example_dir, exist_ok=True)

    # Save uploaded files
    for file in st.session_state.uploaded_files:
        shutil.copy(file, example_dir)

    # Save index
    if 'index' in st.session_state:
        st.session_state.index.storage_context.persist(persist_dir=os.path.join(example_dir, "index"))

    # Save chat history
    with open(os.path.join(example_dir, "chat_history.json"), "w") as f:
        json.dump(st.session_state.messages, f)

    return example_name

def load_example(example_name):
    examples_dir = ensure_examples_dir()
    example_dir = os.path.join(examples_dir, example_name)

    # Load uploaded files
    upload_dir = ensure_upload_dir()
    st.session_state.uploaded_files = []
    for file in os.listdir(example_dir):
        if file not in ["index", "chat_history.json"]:
            src = os.path.join(example_dir, file)
            dst = os.path.join(upload_dir, file)
            shutil.copy(src, dst)
            st.session_state.uploaded_files.append(dst)

    # Load index
    index_dir = os.path.join(example_dir, "index")
    if os.path.exists(index_dir):
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        st.session_state.index = load_index_from_storage(storage_context)

    # Load chat history
    with open(os.path.join(example_dir, "chat_history.json"), "r") as f:
        st.session_state.messages = json.load(f)

def get_saved_examples():
    examples_dir = ensure_examples_dir()
    return [d for d in os.listdir(examples_dir) if os.path.isdir(os.path.join(examples_dir, d))]

# Initialize LlamaIndex settings
Settings.llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=300, temperature=0.2)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state.messages.append(message)

@st.cache_resource
def create_index(files):
    docs = SimpleDirectoryReader(input_files=files).load_data()
    return VectorStoreIndex.from_documents(docs)

def main():
    st.set_page_config(
        page_title="Chatbot with File Upload",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.title("Chatbot with File Upload 💬🤖")

    # Sidebar
    with st.sidebar:
        st.header("Options")
        
        # Check if an example was just loaded
        if st.session_state.get('example_loaded', False):
            st.success(f"Example {st.session_state.get('last_loaded_example', '')} loaded successfully!")
            st.session_state['example_loaded'] = False
        else:
            # File uploader
            uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
            if uploaded_files:
                upload_dir = ensure_upload_dir()
                for file in uploaded_files:
                    if file.name not in [os.path.basename(f) for f in st.session_state.uploaded_files]:
                        file_path = os.path.join(upload_dir, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getvalue())
                        st.session_state.uploaded_files.append(file_path)
                st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

        # Index button
        if st.button("Index Files"):
            if st.session_state.uploaded_files:
                with st.spinner("Indexing files..."):
                    try:
                        st.session_state.index = create_index(st.session_state.uploaded_files)
                        st.success("Files indexed successfully!")
                    except Exception as e:
                        st.error(f"An error occurred while indexing files: {str(e)}")
            else:
                st.warning("Please upload files before indexing.")

        # Save Example button
        if st.button("Save Example"):
            if 'index' in st.session_state and st.session_state.uploaded_files:
                example_name = save_example()
                st.success(f"Example saved as {example_name}")
            else:
                st.warning("Please upload and index files before saving an example.")

        # Load Example selectbox
        saved_examples = get_saved_examples()
        if saved_examples:
            selected_example = st.selectbox("Load Example", [""] + saved_examples)
            if selected_example and selected_example != st.session_state.get('last_loaded_example', ''):
                load_example(selected_example)
                st.session_state['last_loaded_example'] = selected_example
                st.session_state['example_loaded'] = True
                st.success(f"Example {selected_example} loaded successfully!")

        # Reset button
        if st.button("Reset Everything"):
            st.session_state.messages = [
                {"role": "assistant", "content": "How can I help you today?"}
            ]
            upload_dir = ensure_upload_dir()
            for file in st.session_state.uploaded_files:
                os.remove(file)
            st.session_state.uploaded_files = []
            if 'index' in st.session_state:
                del st.session_state.index
            if 'selected_pill' in st.session_state:
                del st.session_state.selected_pill
            st.success("Everything has been reset!")
            st.rerun()

    # Main chat interface
    if 'selected_pill' not in st.session_state:
        st.session_state.selected_pill = None

    selected = pills(
        "Choose a question to get started or write your own below.",
        [
            "What files have been uploaded?",
            "How can I use this chatbot?",
            "What kind of questions can I ask?",
            "Can you summarize the uploaded documents?",
        ],
        clearable=True,
        index=None,
    )
    
    if selected:
        st.session_state.selected_pill = selected
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.selected_pill:
        if 'index' in st.session_state and st.session_state.index:
            if 'last_processed_pill' not in st.session_state or st.session_state.last_processed_pill != st.session_state.selected_pill:
                add_to_message_history("user", st.session_state.selected_pill)
                with st.chat_message("user"):
                    st.write(st.session_state.selected_pill)
                with st.chat_message("assistant"):
                    chat_engine = st.session_state.index.as_chat_engine(chat_mode="context", verbose=True)
                    response = chat_engine.chat(st.session_state.selected_pill)
                    st.write(response.response)
                    add_to_message_history("assistant", response.response)
                st.session_state.last_processed_pill = st.session_state.selected_pill
        else:
            st.warning("Please upload and index some files before selecting a question.")
        st.session_state.selected_pill = None

    if prompt := st.chat_input("Your question"):
        add_to_message_history("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            if 'index' in st.session_state and st.session_state.index:
                chat_engine = st.session_state.index.as_chat_engine(chat_mode="context", verbose=True)
                response = chat_engine.chat(prompt)
                st.write(response.response)
                add_to_message_history("assistant", response.response)
            else:
                st.write("Please upload and index some files before asking questions.")
                add_to_message_history("assistant", "Please upload and index some files before asking questions.")

if __name__ == "__main__":
    main()
    if 'selected_pill' in st.session_state:
        st.session_state.selected_pill = None
