import json
from pathlib import Path


class MetadataStore:
    """
    ==========================================================
    Metadata Store

    Responsibilities
    ----------------
    • Store metadata for every embedding
    • Save metadata to JSON
    • Load metadata from JSON
    • Retrieve metadata by vector ID

    Each metadata record contains:

        chunk_id
        document
        page
        text
        etc.
    ==========================================================
    """

    def __init__(self):

        self.metadata = []

        # =====================================================
        # Project Root
        # =====================================================

        self.project_root = Path(__file__).resolve().parents[3]

        self.vector_db = (
            self.project_root /
            "backend" /
            "vector_db"
        )

        self.vector_db.mkdir(
            parents=True,
            exist_ok=True
        )

        self.default_metadata_path = (
            self.vector_db /
            "metadata.json"
        )

    # =====================================================
    # Add Single Metadata
    # =====================================================

    def add(
        self,
        metadata
    ):

        self.metadata.append(metadata)

    # =====================================================
    # Add Multiple Metadata
    # =====================================================

    def add_many(
        self,
        metadata_list
    ):

        self.metadata.extend(metadata_list)

    # =====================================================
    # Get Metadata using Vector ID
    # =====================================================

    def get(
        self,
        vector_id
    ):

        if (
            0 <= vector_id <
            len(self.metadata)
        ):

            return self.metadata[vector_id]

        return None

    # =====================================================
    # Get All Metadata
    # =====================================================

    def get_all(
        self
    ):

        return self.metadata

    # =====================================================
    # Total Metadata Records
    # =====================================================

    def total(
        self
    ):

        return len(self.metadata)

    # =====================================================
    # Check if Metadata Exists
    # =====================================================

    def exists(
        self
    ) -> bool:

        return self.default_metadata_path.exists()

    # =====================================================
    # Clear Metadata
    # =====================================================

    def clear(
        self
    ):

        self.metadata = []

    # =====================================================
    # Save Metadata
    # =====================================================

    def save(
        self,
        file_path=None
    ):

        if file_path is None:

            file_path = self.default_metadata_path

        else:

            file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
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

        print("\nMetadata saved successfully.")
        print(f"Location : {file_path.resolve()}")
        print(f"Records  : {self.total()}\n")

    # =====================================================
    # Load Metadata
    # =====================================================

    def load(
        self,
        file_path=None
    ):

        if file_path is None:

            file_path = self.default_metadata_path

        else:

            file_path = Path(file_path)

        if not file_path.exists():

            self.metadata = []

            print("\nMetadata file not found.")
            print(f"Expected : {file_path.resolve()}\n")

            return

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        print("\nMetadata loaded successfully.")
        print(f"Location : {file_path.resolve()}")
        print(f"Records  : {self.total()}\n")