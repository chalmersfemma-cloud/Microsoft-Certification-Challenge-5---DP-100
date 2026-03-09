from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    app_title: str = os.getenv("APP_TITLE", "PDF Content Chatbot - DIO DP-100")
    data_dir: Path = Path(os.getenv("DATA_DIR", "data"))
    index_dir: Path = Path(os.getenv("INDEX_DIR", "data/index"))
    pdf_dir: Path = Path(os.getenv("PDF_DIR", "data/uploads"))
    local_embedding_model: str = os.getenv(
        "EMBEDDING_MODEL_LOCAL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("CHAT_TOP_K", "4"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "180"))
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_api_version: str = os.getenv(
        "AZURE_OPENAI_API_VERSION", "2024-10-21"
    )
    azure_chat_deployment: str = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "")
    azure_embedding_deployment: str = os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", ""
    )

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

    @property
    def is_azure_configured(self) -> bool:
        return all(
            [
                self.azure_openai_endpoint,
                self.azure_openai_api_key,
                self.azure_chat_deployment,
                self.azure_embedding_deployment,
            ]
        )


settings = Settings()
settings.ensure_directories()
