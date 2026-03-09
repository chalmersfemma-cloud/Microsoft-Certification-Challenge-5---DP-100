from __future__ import annotations

from src.rag import RAGService


def main() -> None:
    service = RAGService()
    print("PDF chatbot terminal mode")
    print("Type 'exit' to stop. Make sure an index already exists.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        result = service.ask(question)
        print("\nAnswer:\n")
        print(result.answer)
        print("\nSources:")
        for chunk, score in result.sources:
            print(
                f"- {chunk.source_file} | page {chunk.page_number} | score={score:.4f}"
            )


if __name__ == "__main__":
    main()
