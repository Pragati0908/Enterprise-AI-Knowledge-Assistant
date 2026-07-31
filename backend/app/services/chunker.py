import re


class TextChunker:

    @staticmethod
    def chunk_text(

        text,

        source,

        chunk_size=500,

        overlap=100,

        min_chunk_size=200

    ):

        if not isinstance(text, str):

            raise TypeError(

                "Text must be a string."

            )

        if overlap >= chunk_size:

            raise ValueError(

                "Overlap must be smaller than chunk size."

            )

        # Normalize whitespace
        text = re.sub(

            r"\s+",

            " ",

            text

        ).strip()

        # Split into sentences
        sentences = re.split(

            r'(?<=[.!?])\s+',

            text

        )

        chunks = []

        current_chunk = ""

        chunk_id = 1

        start_index = 0

        current_position = 0

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:

                continue

            candidate = (

                current_chunk + " " + sentence

            ).strip()

            # Chunk full
            if (

                len(candidate)

                > chunk_size

                and current_chunk

            ):

                chunk_text = current_chunk.strip()

                end_index = start_index + len(chunk_text)

                chunks.append(

                    {

                        "chunk_id": chunk_id,

                        "text": chunk_text,

                        "source": source,

                        "start_index": start_index,

                        "end_index": end_index,

                        "chunk_length": len(chunk_text)

                    }

                )

                chunk_id += 1

                # -----------------------------
                # Create overlap WITHOUT
                # splitting a word
                # -----------------------------

                overlap_start = max(

                    0,

                    len(chunk_text) - overlap

                )

                # Move to next space if overlap
                # starts inside a word
                while (

                    overlap_start < len(chunk_text)

                    and overlap_start > 0

                    and chunk_text[overlap_start - 1] != " "

                ):

                    overlap_start += 1

                overlap_text = chunk_text[overlap_start:].strip()

                start_index = (

                    end_index

                    - len(overlap_text)

                )

                current_chunk = (

                    overlap_text

                    + " "

                    + sentence

                ).strip()

            else:

                current_chunk = candidate

        # Add last chunk
        if current_chunk:

            chunk_text = current_chunk.strip()

            if (

                len(chunk_text)

                >= min_chunk_size

                or not chunks

            ):

                end_index = start_index + len(chunk_text)

                chunks.append(

                    {

                        "chunk_id": chunk_id,

                        "text": chunk_text,

                        "source": source,

                        "start_index": start_index,

                        "end_index": end_index,

                        "chunk_length": len(chunk_text)

                    }

                )

        return chunks