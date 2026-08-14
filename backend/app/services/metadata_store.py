"""
==========================================================
Enterprise AI Knowledge Assistant

Metadata Store

Responsibilities
----------------
• Store metadata for every embedding
• Persist metadata to JSON
• Load existing metadata automatically
• Append metadata for multiple documents
• Retrieve metadata by vector ID
• Maintain FAISS vector-ID alignment

Metadata is stored in the same order as vectors
are added to FAISS.

Example:

    FAISS Vector ID 0
            ↓
    metadata[0]

    FAISS Vector ID 1
            ↓
    metadata[1]

    ...

    FAISS Vector ID 12
            ↓
    metadata[12]

For multiple documents:

    Document A
        ↓
    vectors 0-11
        ↓
    metadata records 0-11

    Document B
        ↓
    vectors 12-26
        ↓
    metadata records 12-26

Therefore:

    FAISS index.ntotal
            ==
    len(metadata)

==========================================================
"""

import json
from pathlib import Path


class MetadataStore:
    """
    Persistent metadata store.

    Metadata records are maintained in exactly
    the same order as FAISS vector IDs.
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):
        """
        Initialize the metadata store.

        If metadata.json already exists, it is loaded
        automatically.

        If it does not exist, an empty metadata list
        is created.
        """

        self.metadata = []

        # ==================================================
        # Project Root
        # ==================================================

        self.project_root = (
            Path(__file__).resolve().parents[3]
        )

        self.vector_db = (
            self.project_root
            / "backend"
            / "vector_db"
        )

        self.vector_db.mkdir(
            parents=True,
            exist_ok=True
        )

        self.default_metadata_path = (
            self.vector_db
            / "metadata.json"
        )

        # ==================================================
        # Load Existing Metadata
        # ==================================================

        if self.default_metadata_path.exists():

            self._load_existing_metadata()

        else:

            print(
                "\nNo existing metadata file found."
            )

            print(
                "Starting with empty metadata store.\n"
            )

    # ======================================================
    # Internal Metadata Loader
    # ======================================================

    def _load_existing_metadata(self):
        """
        Internal method used by __init__() to load
        existing metadata.

        This method does not raise FileNotFoundError
        because the constructor has already checked
        that the file exists.
        """

        try:

            with open(
                self.default_metadata_path,
                "r",
                encoding="utf-8"
            ) as file:

                loaded_metadata = json.load(
                    file
                )

            # ----------------------------------------------
            # Validate JSON structure
            # ----------------------------------------------

            if not isinstance(
                loaded_metadata,
                list
            ):

                raise ValueError(
                    "metadata.json must contain "
                    "a JSON list."
                )

            self.metadata = loaded_metadata

            print(
                "\nExisting metadata loaded."
            )

            print(
                f"Location : "
                f"{self.default_metadata_path.resolve()}"
            )

            print(
                f"Records  : "
                f"{self.total()}\n"
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "metadata.json is not valid JSON."
            ) from error

        except Exception as error:

            raise RuntimeError(
                "Failed to load metadata: "
                f"{error}"
            ) from error

    # ======================================================
    # Add Single Metadata
    # ======================================================

    def add(
        self,
        metadata
    ):
        """
        Append one metadata record.

        The new record receives the next available
        position, which corresponds to the next FAISS
        vector ID.
        """

        if not isinstance(
            metadata,
            dict
        ):

            raise TypeError(
                "Metadata must be a dictionary."
            )

        vector_id = len(
            self.metadata
        )

        # --------------------------------------------------
        # Preserve / assign vector ID
        # --------------------------------------------------

        metadata = dict(
            metadata
        )

        metadata.setdefault(
            "vector_id",
            vector_id
        )

        self.metadata.append(
            metadata
        )

        return vector_id

    # ======================================================
    # Add Multiple Metadata
    # ======================================================

    def add_many(
        self,
        metadata_list
    ):
        """
        Append multiple metadata records.

        Existing records are preserved.

        New records are appended after the existing
        records.

        Example:

            Existing records = 12

            New records = 15

            Result = 27 records
        """

        if metadata_list is None:

            return

        if not isinstance(
            metadata_list,
            list
        ):

            raise TypeError(
                "metadata_list must be a list."
            )

        start_vector_id = len(
            self.metadata
        )

        for offset, metadata in enumerate(
            metadata_list
        ):

            if not isinstance(
                metadata,
                dict
            ):

                raise TypeError(
                    "Every metadata record "
                    "must be a dictionary."
                )

            metadata = dict(
                metadata
            )

            # ----------------------------------------------
            # Assign sequential vector ID
            # ----------------------------------------------

            metadata.setdefault(
                "vector_id",
                start_vector_id + offset
            )

            self.metadata.append(
                metadata
            )

        print(
            "\nMetadata records added."
        )

        print(
            f"Records before : "
            f"{start_vector_id}"
        )

        print(
            f"Records added  : "
            f"{len(metadata_list)}"
        )

        print(
            f"Records after  : "
            f"{self.total()}\n"
        )

    # ======================================================
    # Get Metadata Using Vector ID
    # ======================================================

    def get(
        self,
        vector_id
    ):
        """
        Retrieve metadata corresponding to a FAISS
        vector ID.
        """

        if (
            0 <= vector_id
            < len(self.metadata)
        ):

            return self.metadata[
                vector_id
            ]

        return None

    # ======================================================
    # Get All Metadata
    # ======================================================

    def get_all(
        self
    ):
        """
        Return all metadata records.
        """

        return self.metadata

    # ======================================================
    # Total Metadata Records
    # ======================================================

    def total(
        self
    ):
        """
        Return the number of metadata records.
        """

        return len(
            self.metadata
        )

    # ======================================================
    # Check if Metadata Exists
    # ======================================================

    def exists(
        self
    ) -> bool:
        """
        Check whether metadata.json exists.
        """

        return (
            self.default_metadata_path.exists()
        )

    # ======================================================
    # Clear Metadata
    # ======================================================

    def clear(
        self
    ):
        """
        Clear metadata from memory.

        IMPORTANT:
        This does not automatically delete the
        metadata.json file.
        """

        self.metadata = []

        print(
            "Metadata store cleared in memory."
        )

    # ======================================================
    # Save Metadata
    # ======================================================

    def save(
        self,
        file_path=None
    ):
        """
        Save all metadata records to JSON.

        Existing records are preserved because the
        metadata list itself is cumulative.
        """

        if file_path is None:

            file_path = (
                self.default_metadata_path
            )

        else:

            file_path = Path(
                file_path
            )

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

        print(
            "\nMetadata saved successfully."
        )

        print(
            f"Location : "
            f"{file_path.resolve()}"
        )

        print(
            f"Records  : "
            f"{self.total()}\n"
        )

    # ======================================================
    # Load Metadata
    # ======================================================

    def load(
        self,
        file_path=None
    ):
        """
        Explicitly load metadata from disk.

        Unlike the constructor, this method can be
        used to load a different metadata file.
        """

        if file_path is None:

            file_path = (
                self.default_metadata_path
            )

        else:

            file_path = Path(
                file_path
            )

        if not file_path.exists():

            self.metadata = []

            print(
                "\nMetadata file not found."
            )

            print(
                f"Expected : "
                f"{file_path.resolve()}\n"
            )

            return

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                loaded_metadata = json.load(
                    file
                )

            if not isinstance(
                loaded_metadata,
                list
            ):

                raise ValueError(
                    "Metadata file must contain "
                    "a JSON list."
                )

            self.metadata = (
                loaded_metadata
            )

            print(
                "\nMetadata loaded successfully."
            )

            print(
                f"Location : "
                f"{file_path.resolve()}"
            )

            print(
                f"Records  : "
                f"{self.total()}\n"
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Metadata file contains invalid JSON."
            ) from error

        except Exception as error:

            raise RuntimeError(
                "Failed to load metadata: "
                f"{error}"
            ) from error