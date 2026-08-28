"""Experimental asyncio-based file reader for very large logs.

Idea: read in chunks with a thread executor and hand complete lines to the
synchronous parsers. Benchmarks so far show no win over plain iteration; the
parsing regex dominates, not I/O.
"""

import asyncio
from pathlib import Path
from typing import AsyncIterator, Callable


async def aparse_file(path: Path, parse_line: Callable, chunk_size: int = 1 << 20) -> AsyncIterator:
    loop = asyncio.get_running_loop()
    with open(path, "rb") as handle:
        buffer = b""
        while True:
            chunk = await loop.run_in_executor(None, handle.read, chunk_size)
            if not chunk:
                break
            buffer += chunk
            *lines, buffer = buffer.split(b"\n")
            for raw in lines:
                if raw.strip():
                    yield parse_line(raw.decode("utf-8", "replace"))
        if buffer.strip():
            yield parse_line(buffer.decode("utf-8", "replace"))
