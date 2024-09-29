def querydata(query_text):
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from dotenv import load_dotenv
    from pathlib import Path
    import os
    import openai
    import numpy as np

    np.float_ = np.float64

    CHROMA_PATH = "chroma"

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """
    load_dotenv(Path(".env"))

    # Set OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        raise ValueError("OpenAI API key not found. Make sure it's set in APIKEY.env.")

    openai.api_key = openai_api_key

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()

    # Use invoke instead of predict
    response = model.invoke(prompt)

    # Assuming response is an object with a 'content' attribute
    if hasattr(response, 'content'):
        return response.content  # Return only the response content
    else:
        return str(response)  # Fallback in case it's not structured as expected
