SYSTEM_PROMPT = """
You are a grounded assistant for a PDF question-answering system.
Use only the provided source excerpts.
If the answer is not present in the sources, say so clearly.
Cite source blocks inline using the bracket labels exactly as provided, for example [SOURCE 1].
Prefer concise and factual answers.
""".strip()


def build_user_prompt(question: str, contexts: list[str]) -> str:
    joined_context = "\n\n".join(contexts)
    return (
        "Answer the user's question using only the context below.\n\n"
        f"CONTEXT:\n{joined_context}\n\n"
        f"QUESTION:\n{question}\n"
    )
