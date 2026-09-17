"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.

Tell me what question it could answer on its own. If it can't answer anything on its own, say so and tell me what's missing.


"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Use reply boundaries rather than raw character windows.

    The advice-thread corpus is organized by reply blocks, and each reply often
    contains a complete opinion or recommendation. Splitting on these boundaries
    preserves the useful unit of meaning better than slicing every 800
    characters with a fixed overlap.

    We also keep the thread title with each reply so retrieval can match the
    actual topic words from the document question instead of only the reply text.
    """
    chunks: list[Chunk] = []

    reply_pattern = re.compile(r"(?ms)^--- reply .*? ---\s*\n(.*?)(?=^--- reply |\Z)")

    for doc in documents:
        title = next(
            (line.strip() for line in doc.text.splitlines() if line.strip().startswith("THREAD:")),
            "",
        )
        context = f"{title}\n" if title else ""
        matches = list(reply_pattern.finditer(doc.text.strip()))

        if matches:
            for index, match in enumerate(matches):
                text = match.group(0).strip()
                if text:
                    chunks.append(
                        Chunk(
                            text=f"{context}{text}",
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
            continue

        # Fallback for any corpus that does not mark replies explicitly.
        if doc.text.strip():
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", doc.text.strip()) if p.strip()]
            buffer = ""
            index = 0
            for paragraph in paragraphs:
                candidate = f"{buffer} {paragraph}" if buffer else paragraph
                if len(candidate) <= config.CHUNK_SIZE:
                    buffer = candidate
                    continue
                if buffer:
                    chunks.append(
                        Chunk(
                            text=f"{context}{buffer.strip()}",
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                    buffer = paragraph
                else:
                    chunks.append(
                        Chunk(
                            text=f"{context}{paragraph[: config.CHUNK_SIZE].strip()}",
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
            if buffer:
                chunks.append(
                    Chunk(
                        text=f"{context}{buffer.strip()}",
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
