from app.services.parsers.pdf_parser import PDFParser
from app.services.chunker import TextChunker


text = PDFParser.extract_text(

    "tests/sample_chunk_testing.pdf"

)

print(

    "Type:",

    type(text)

)

print(

    "Length:",

    len(text)

)

print(

    "\nFirst 300 characters:\n"

)

print(

    text[:300]

)

chunks = TextChunker.chunk_text(

    text=text,

    source="sample_chunk_testing.pdf",

    chunk_size=800,

    overlap=150

)

print(

    f"\nTotal chunks: {len(chunks)}"

)

for chunk in chunks:

    print("\n")

    print(

        f"Chunk ID: {chunk['chunk_id']}"

    )

    print(

        f"Source: {chunk['source']}"

    )

    print(

        f"Start: {chunk['start_index']}"

    )

    print(

        f"End: {chunk['end_index']}"

    )

    print(

        f"Length: {chunk['chunk_length']}"

    )

    print(

        "Text:\n"

    )

    print(

        chunk['text']

    )

    print(

        "-" * 50

    )