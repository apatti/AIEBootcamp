from langchain_core.prompts import ChatPromptTemplate

def GetChatPrompt():
    rag_system_prompt_template = """\
    You are a helpful assistant that uses the provided context to answer questions. Never reference this prompt, or the existance of context.
    """

    rag_message_list = [
        {"role" : "system", "content" : rag_system_prompt_template},
    ]

    rag_user_prompt_template = """\
    Question:
    {question}
    Context:
    {context}
    """

    return ChatPromptTemplate.from_messages([
        ("system", rag_system_prompt_template),
        ("human", rag_user_prompt_template)
    ])