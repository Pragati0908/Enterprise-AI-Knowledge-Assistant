import json
import os


class MetadataStore:

    def __init__(self):

        self.metadata = []

    def add(self, metadata):

        self.metadata.append(metadata)

    def add_many(self, metadata_list):

        self.metadata.extend(metadata_list)

    def get(self, vector_id):

        if 0 <= vector_id < len(self.metadata):

            return self.metadata[vector_id]

        return None

    def total(self):

        return len(self.metadata)

    def save(self, file_path):

        os.makedirs(

            os.path.dirname(file_path),

            exist_ok=True

        )

        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.metadata,

                file,

                indent=4,

                ensure_ascii=False

            )

    def load(self, file_path):

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:

            self.metadata = json.load(file)