import threading
import time
from flask import Response, request, stream_with_context
from collections import deque
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from Mainfold.utils.PromptTemp import system_prompt
from Mainfold.utils.StreamCallback import GeminiSSECallbackHandler
from Mainfold.utils.other_func import retrieval, stream_LLM
from Mainfold.utils.Embedd import creating_model

model = creating_model()


def _run_streaming_rag(user_msg, user_id, book_id, queue):
    """
    Runs the RAG chain in a background thread.
    Tokens are pushed into `queue` by the callback handler.
    """
    handler = GeminiSSECallbackHandler(queue)

    llm = stream_LLM(handler)

    doc_retrieval = retrieval(
        model=model,
        user_id=user_id,
        book_id=book_id
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_input}")
    ])

    rag_chain = (
        {
            "context": doc_retrieval | (lambda docs: "\n\n".join(d.page_content for d in docs)),
            "user_input": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    # This triggers Gemini streaming
    rag_chain.invoke(user_msg)

    # Signal stream completion
    queue.append("[DONE]")


def chat_stream():
    data = request.json

    user_msg = data.get("message")
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not user_msg:
        return Response(
            "data: No message received\n\n",
            mimetype="text/event-stream"
        )

    def generate():
        # Initial feedback to user
        yield "data: 🔍 Searching book...\n\n"

        queue = deque()

        thread = threading.Thread(
            target=_run_streaming_rag,
            args=(user_msg, user_id, book_id, queue),
            daemon=True
        )
        thread.start()

        while thread.is_alive() or queue:
            while queue:
                token = queue.popleft()
                yield f"data: {token}\n\n"
            time.sleep(0.05)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )
