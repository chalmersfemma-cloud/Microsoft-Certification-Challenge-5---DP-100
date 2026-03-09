from __future__ import annotations

from typing import Iterable

from src.config import settings
from src.schemas import DocumentChunk
from src.prompts import SYSTEM_PROMPT, build_user_prompt


class AnswerGenerator:
    def __init__(self) -> None:
        self._client = None

    @property
    def mode(self) -> str:
        return "azure" if settings.is_azure_configured else "fallback"

    def _get_client(self):
        if self._client is None:
            from openai import AzureOpenAI

            self._client = AzureOpenAI(
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_endpoint=settings.azure_openai_endpoint,
            )
        return self._client

    @staticmethod
    def _format_context(chunks: Iterable[DocumentChunk]) -> list[str]:
        contexts: list[str] = []
        for index, chunk in enumerate(chunks, start=1):
            contexts.append(
                f"[SOURCE {index}] file={chunk.source_file} page={chunk.page_number}\n{chunk.text}"
            )
        return contexts

    def generate(self, question: str, chunks: list[DocumentChunk]) -> str:
        contexts = self._format_context(chunks)

        if settings.is_azure_configured:
            client = self._get_client()
            response = client.chat.completions.create(
                model=settings.azure_chat_deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": build_user_prompt(question, contexts),
                    },
                ],
                temperature=0.1,
            )
            return response.choices[0].message.content or "No answer was generated."

        fallback_lines = [
            "Azure OpenAI is not configured, so the app is returning a grounded fallback answer.",
            "The most relevant evidence found was:",
        ]
        for index, chunk in enumerate(chunks, start=1):
            preview = chunk.text[:320].strip()
            fallback_lines.append(
                f"- [SOURCE {index}] {chunk.source_file}, page {chunk.page_number}: {preview}"
            )
        fallback_lines.append(
            "Configure Azure OpenAI in .env to generate a natural-language final answer from these sources."
        )
        return "\n".join(fallback_lines)
