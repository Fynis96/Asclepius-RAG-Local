from typing import Any, Dict
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    SummaryIndex, 
    SimpleDirectoryReader, 
    ChatPromptTemplate,
    StorageContext,
    load_index_from_storage
    )
from llama_index.core.llama_pack.base import BaseLlamaPack

class StreamlitChatPack(BaseLlamaPack):
    """Streamlit chatbot pack."""

    def __init__(
        self,
        run_from_main: bool = False,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if not run_from_main:
            raise ValueError(
                "Please run this llama-pack directly with "
                "`streamlit run [download_dir]/streamlit_chatbot/base.py`"
            )


    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import streamlit as st
        from streamlit_pills import pills

        st.set_page_config(
            page_title=f"Title",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items=None,
        )

        if "messages" not in st.session_state:  # Initialize the chat messages history
            st.session_state["messages"] = [
            ]

        st.title(
            f"Title"
        )

        def add_to_message_history(role, content):
            message = {"role": role, "content": str(content)}
            st.session_state["messages"].append(
                message
            )  # Add response to message history

        @st.cache_resource
        def load_index_data():
            docs = SimpleDirectoryReader(input_dir=r"C:\dir\Learning\Asclepius\data\output\206424552- OCR").load_data()
            Settings.llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=300, temperature=0.2)
            Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
            return VectorStoreIndex.from_documents(
                docs
            )

        index = load_index_data()

        selected = pills(
            "Choose a question to get started or write your own below.",
            [
                "Tell me about the patient",
                "What type of Appeal is needed for the denied claim?",
                "Fill in this template based on the patients documents: [Patient Name], [DOB], [Insurance Company], [Claim Number]",
            ],
            clearable=True,
            index=None,
        )

        if "chat_engine" not in st.session_state:  # Initialize the query engine
            st.session_state["chat_engine"] = index.as_chat_engine(
                chat_mode="context", verbose=True
            )

        for message in st.session_state["messages"]:  # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # To avoid duplicated display of answered pill questions each rerun
        if selected and selected not in st.session_state.get(
            "displayed_pill_questions", set()
        ):
            st.session_state.setdefault("displayed_pill_questions", set()).add(selected)
            with st.chat_message("user"):
                st.write(selected)
            with st.chat_message("assistant"):
                response = st.session_state["chat_engine"].stream_chat(selected)
                response_str = ""
                response_container = st.empty()
                for token in response.response_gen:
                    response_str += token
                    response_container.write(response_str)
                add_to_message_history("user", selected)
                add_to_message_history("assistant", response)

        if prompt := st.chat_input(
            "Your question"
        ):  # Prompt for user input and save to chat history
            add_to_message_history("user", prompt)

            # Display the new question immediately after it is entered
            with st.chat_message("user"):
                st.write(prompt)

            # If last message is not from assistant, generate a new response
            # if st.session_state["messages"][-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                response = st.session_state["chat_engine"].astream_chat(prompt)
                response_str = ""
                response_container = st.empty()
                for token in response.response_gen:
                    response_str += token
                    response_container.write(response_str)
                # st.write(response.response)
                add_to_message_history("assistant", response.response)

            # Save the state of the generator
            st.session_state["response_gen"] = response.response_gen


if __name__ == "__main__":
    StreamlitChatPack(run_from_main=True).run()
########################
# import asyncio
# from typing import Any, Dict
# import os
# import streamlit as st
# from llama_index.llms.ollama import Ollama
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core import (
#     Settings, 
#     VectorStoreIndex, 
#     SimpleDirectoryReader
# )
# from llama_index.core.llama_pack.base import BaseLlamaPack


# def setup_page() -> None:
#     """Set up the Streamlit page configuration."""
#     st.set_page_config(
#         page_title="Title",
#         layout="centered",
#         initial_sidebar_state="auto",
#         menu_items=None,
#     )
#     st.sidebar.title("Upload Documents")


# def handle_file_uploads(upload_dir: str) -> None:
#     """Handle file uploads and save them to a directory."""
#     uploaded_files = st.sidebar.file_uploader("Upload your documents", accept_multiple_files=True)

#     if uploaded_files:
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)

#         for uploaded_file in uploaded_files:
#             with open(os.path.join(upload_dir, uploaded_file.name), "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#         st.sidebar.success("Files successfully uploaded and saved to the folder.")
#         return True
#     return False


# @st.cache_resource
# def load_index_data(upload_dir: str) -> VectorStoreIndex:
#     """Load and index data from the uploaded files."""
#     docs = load_documents(upload_dir)
#     Settings.llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=300, temperature=0.2)
#     Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
#     return VectorStoreIndex.from_documents(docs)


# def load_documents(upload_dir: str):
#     """Load documents from the specified directory."""
#     return SimpleDirectoryReader(input_dir=upload_dir).load_data()


# def initialize_chat_history() -> None:
#     """Initialize the chat history in Streamlit's session state."""
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = []


# def initialize_chat_engine(index: VectorStoreIndex) -> None:
#     """Initialize the chat engine based on the indexed data."""
#     if "chat_engine" not in st.session_state:
#         st.session_state["chat_engine"] = None
#     if index:
#         st.session_state["chat_engine"] = index.as_chat_engine(
#             chat_mode="context", verbose=True
#         )


# def display_chat_interface() -> None:
#     """Display the chat interface and handle user interactions."""
#     st.title("Title")
#     selected_question = get_user_selected_question()
#     display_chat_history()
#     if selected_question:
#         handle_user_question(selected_question)
#     handle_user_input()


# def get_user_selected_question() -> str:
#     """Allow the user to select a predefined question."""
#     return st.sidebar.selectbox(
#         "Choose a question to get started or write your own below.",
#         [
#             "Tell me about the patient",
#             "What type of Appeal is needed for the denied claim?",
#             "Fill in this template based on the patients documents: [Patient Name], [DOB], [Insurance Company], [Claim Number]",
#         ],
#         index=0
#     )


# def display_chat_history() -> None:
#     """Display the chat history."""
#     for message in st.session_state["messages"]:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])


# def handle_user_question(question: str) -> None:
#     """Handle a user-selected question."""
#     if question not in st.session_state.get("displayed_pill_questions", set()):
#         st.session_state.setdefault("displayed_pill_questions", set()).add(question)
#         add_to_message_history("user", question)
#         generate_response(question)


# def handle_user_input() -> None:
#     """Handle user input from the chat interface."""
#     prompt = st.chat_input("Your question")
#     if prompt:
#         add_to_message_history("user", prompt)
#         generate_response(prompt)


# def generate_response(prompt: str) -> None:
#     """Generate and display a response from the chat engine."""
#     if st.session_state["chat_engine"] is not None:
#         with st.chat_message("assistant"):
#             response = st.session_state["chat_engine"].stream_chat(prompt)
#             response_str = ""
#             response_container = st.empty()
#             for token in response.response_gen:
#                 response_str += token
#                 response_container.write(response_str)
#             add_to_message_history("assistant", response.response)


# def add_to_message_history(role: str, content: str) -> None:
#     """Add a message to the chat history."""
#     message = {"role": role, "content": content}
#     st.session_state["messages"].append(message)


# def main():
#     upload_dir = r"C:\dir\Learning\Asclepius\data\output\206424552- OCR"  # Change to your desired path
#     setup_page()
#     files_uploaded = handle_file_uploads(upload_dir)
#     if files_uploaded:
#         index = load_index_data(upload_dir)
#         initialize_chat_history()
#         initialize_chat_engine(index)
#         display_chat_interface()


# if __name__ == "__main__":
#     main()


# import streamlit as st
# from index_utils import get_chat_engine
# from ui_components import render_sidebar, render_chat_interface

# def main():
#     st.set_page_config(page_title="LlamaIndex Demo", layout="wide")
#     st.title("LlamaIndex Streamlit Demo")

#     render_sidebar()

#     if "index_requested" in st.session_state and st.session_state.index_requested:
#         with st.spinner("Indexing documents..."):
#             chat_engine = get_chat_engine()
#         st.success("Documents indexed successfully!")
#         st.session_state.index_requested = False
#     else:
#         chat_engine = get_chat_engine()

#     selected, user_input = render_chat_interface()

#     if selected and selected not in st.session_state.get("displayed_suggestions", set()):
#         st.session_state.setdefault("displayed_suggestions", set()).add(selected)
#         handle_user_input(selected, chat_engine)

#     if user_input:
#         handle_user_input(user_input, chat_engine)

#     if st.button("Clear Chat History"):
#         st.session_state.messages = []
#         st.session_state.displayed_suggestions = set()
#         st.rerun()

# def handle_user_input(input_text, chat_engine):
#     st.session_state.messages.append({"role": "user", "content": input_text})
    
#     if chat_engine:
#         with st.chat_message("assistant"):
#             response = chat_engine.stream_chat(input_text)
#             response_str = ""
#             response_container = st.empty()
#             for token in response.response_gen:
#                 response_str += token
#                 response_container.write(response_str)
#             st.session_state.messages.append({"role": "assistant", "content": response_str})
#     else:
#         st.error("Please index some documents first!")

# if __name__ == "__main__":
#     main()