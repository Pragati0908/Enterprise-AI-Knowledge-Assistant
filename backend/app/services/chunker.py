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

            # Create chunk when limit is reached

            if (

                len(current_chunk)

                + len(sentence)

                + 1

                > chunk_size

            ):

                chunk_data = {

                    "chunk_id": chunk_id,

                    "text": current_chunk.strip(),

                    "source": source,

                    "start_index": start_index,

                    "end_index": current_position,

                    "chunk_length": len(

                        current_chunk.strip()

                    )

                }

                chunks.append(

                    chunk_data

                )

                chunk_id += 1

                overlap_text = current_chunk[-overlap:]

                space_index = overlap_text.find(" ")

                if space_index != -1:

                   overlap_text = overlap_text[
                       space_index + 1:
                   ]

                start_index = (

                   current_position

                   - len(overlap_text)

    )

                current_chunk = (

                    overlap_text

                    + " "

                    + sentence

     )

            else:

                current_chunk += (

                    " "

                    + sentence

                )

            current_position += (

                len(sentence)

                + 1

            )

        # Add the last chunk

        if (

            len(current_chunk.strip())

            >= min_chunk_size

        ):

            chunk_data = {

                "chunk_id": chunk_id,

                "text": current_chunk.strip(),

                "source": source,

                "start_index": start_index,

                "end_index": current_position,

                "chunk_length": len(

                    current_chunk.strip()

                )

            }

            chunks.append(

                chunk_data

            )

        return chunks