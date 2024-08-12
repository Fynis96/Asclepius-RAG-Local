import asyncio
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

# Create a new event loop
loop = asyncio.new_event_loop()

# Set the event loop as the current event loop
asyncio.set_event_loop(loop)


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
                "What is Snowflake?",
                "What company did Snowflake announce they would acquire in October 2023?",
                "What company did Snowflake acquire in March 2022?",
                "When did Snowflake IPO?",
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
                response = st.session_state["chat_engine"].stream_chat(prompt)
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