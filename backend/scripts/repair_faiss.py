"""
===============================================================
Enterprise AI Knowledge Assistant

FAISS Repair Utility

Purpose
-------
Rebuild the FAISS index from the existing metadata.json file.

IMPORTANT:
- Creates a backup of the existing FAISS index.
- Does NOT modify metadata.json.
- Rebuilds FAISS using the text stored in metadata.json.
- Ensures FAISS vector count matches metadata record count.
- Existing metadata/vector IDs are preserved by position.
===============================================================
"""

from pathlib import Path
import sys
import json
import shutil

import faiss
import numpy as np


# ==========================================================
# Add BACKEND directory to Python import path
# ==========================================================
#
# Current file:
#
# backend/
#     scripts/
#         repair_faiss.py
#
# parents[0] = scripts
# parents[1] = backend
#
# This allows:
#
# from app.services.embedding_service import EmbeddingService
#
# ==========================================================

BACKEND_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(BACKEND_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BACKEND_DIR)
    )


# ==========================================================
# Application Imports
# ==========================================================

from app.services.embedding_service import (
    EmbeddingService
)


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = (
    BACKEND_DIR.parent
)

VECTOR_DB = (
    BACKEND_DIR
    / "vector_db"
)

FAISS_PATH = (
    VECTOR_DB
    / "faiss.index"
)

METADATA_PATH = (
    VECTOR_DB
    / "metadata.json"
)

BACKUP_PATH = (
    VECTOR_DB
    / "faiss.index.backup_before_repair"
)


# ==========================================================
# Main Repair Function
# ==========================================================

def repair_faiss():
    """
    Rebuild the FAISS index using the text stored in metadata.json.

    Metadata remains unchanged.

    The rebuilt FAISS index will contain exactly one vector
    for every metadata record.
    """

    # ======================================================
    # Header
    # ======================================================

    print()
    print("=" * 70)
    print("FAISS REPAIR")
    print("=" * 70)

    print()
    print(
        f"Backend directory : {BACKEND_DIR}"
    )

    print(
        f"Vector DB         : {VECTOR_DB}"
    )

    print(
        f"FAISS index       : {FAISS_PATH}"
    )

    print(
        f"Metadata           : {METADATA_PATH}"
    )


    # ======================================================
    # Validate Vector DB Directory
    # ======================================================

    if not VECTOR_DB.exists():

        raise FileNotFoundError(
            f"Vector DB directory not found: "
            f"{VECTOR_DB}"
        )


    # ======================================================
    # Validate FAISS File
    # ======================================================

    if not FAISS_PATH.exists():

        raise FileNotFoundError(
            f"FAISS index not found: "
            f"{FAISS_PATH}"
        )


    # ======================================================
    # Validate Metadata File
    # ======================================================

    if not METADATA_PATH.exists():

        raise FileNotFoundError(
            f"Metadata file not found: "
            f"{METADATA_PATH}"
        )


    # ======================================================
    # Load Existing FAISS
    # ======================================================

    existing_index = faiss.read_index(
        str(FAISS_PATH)
    )

    existing_vector_count = (
        existing_index.ntotal
    )

    print()
    print("-" * 70)
    print("CURRENT VECTOR DATABASE")
    print("-" * 70)

    print(
        f"Existing FAISS vectors : "
        f"{existing_vector_count}"
    )


    # ======================================================
    # Load Metadata
    # ======================================================

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)


    # ======================================================
    # Validate Metadata Structure
    # ======================================================

    if not isinstance(
        metadata,
        list
    ):

        raise RuntimeError(
            "metadata.json does not contain "
            "a list of metadata records. "
            "Repair aborted."
        )


    metadata_count = len(
        metadata
    )

    print(
        f"Metadata records       : "
        f"{metadata_count}"
    )


    # ======================================================
    # Validate Metadata Is Not Empty
    # ======================================================

    if not metadata:

        raise RuntimeError(
            "Metadata is empty. "
            "Repair aborted."
        )


    # ======================================================
    # Validate Metadata Records
    # ======================================================

    print()
    print(
        "Validating metadata records..."
    )

    for index, record in enumerate(
        metadata
    ):

        # --------------------------------------------------
        # Validate record type
        # --------------------------------------------------

        if not isinstance(
            record,
            dict
        ):

            raise RuntimeError(
                "Metadata record "
                f"{index} is not a dictionary. "
                "Repair aborted."
            )


        # --------------------------------------------------
        # Validate text
        # --------------------------------------------------

        text = record.get(
            "text"
        )

        if not isinstance(
            text,
            str
        ):

            raise RuntimeError(
                "Metadata record "
                f"{index} does not contain "
                "valid text. "
                "Repair aborted."
            )


        if not text.strip():

            raise RuntimeError(
                "Metadata record "
                f"{index} has empty text. "
                "Repair aborted."
            )


    print(
        "Metadata validation : PASSED"
    )


    # ======================================================
    # Display Current Mismatch
    # ======================================================

    print()
    print("-" * 70)
    print("COUNT COMPARISON")
    print("-" * 70)

    print(
        f"FAISS vectors : "
        f"{existing_vector_count}"
    )

    print(
        f"Metadata      : "
        f"{metadata_count}"
    )

    print(
        f"Aligned       : "
        f"{existing_vector_count == metadata_count}"
    )


    # ======================================================
    # Create Backup
    # ======================================================

    print()
    print("-" * 70)
    print("CREATING BACKUP")
    print("-" * 70)

    shutil.copy2(
        FAISS_PATH,
        BACKUP_PATH
    )

    print(
        "Backup created successfully:"
    )

    print(
        BACKUP_PATH
    )


    # ======================================================
    # Extract Text
    # ======================================================

    texts = [

        record["text"].strip()

        for record in metadata

    ]


    # ======================================================
    # Generate Embeddings
    # ======================================================

    print()
    print("-" * 70)
    print("GENERATING EMBEDDINGS")
    print("-" * 70)

    print(
        f"Generating embeddings for "
        f"{len(texts)} metadata records..."
    )

    embeddings = (
        EmbeddingService
        .generate_embeddings(
            texts
        )
    )


    # ======================================================
    # Validate Embedding Result
    # ======================================================

    if embeddings is None:

        raise RuntimeError(
            "EmbeddingService returned None. "
            "Repair aborted."
        )


    # ======================================================
    # Convert Embeddings to NumPy
    # ======================================================

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )


    # ======================================================
    # Validate Embedding Shape
    # ======================================================

    if embeddings.ndim != 2:

        raise RuntimeError(
            "Embeddings must be a 2-dimensional "
            "array. "
            f"Received shape: "
            f"{embeddings.shape}"
        )


    # ======================================================
    # Validate Embedding Count
    # ======================================================

    embedding_count = (
        embeddings.shape[0]
    )

    print()
    print(
        f"Embeddings generated : "
        f"{embedding_count}"
    )

    print(
        f"Metadata records     : "
        f"{metadata_count}"
    )

    if (
        embedding_count
        != metadata_count
    ):

        raise RuntimeError(
            "Embedding count does not "
            "match metadata count. "
            f"Embeddings={embedding_count}, "
            f"Metadata={metadata_count}. "
            "Repair aborted."
        )


    # ======================================================
    # Determine Embedding Dimension
    # ======================================================

    dimension = (
        embeddings.shape[1]
    )

    print(
        f"Embedding dimension  : "
        f"{dimension}"
    )


    # ======================================================
    # Validate Dimension
    # ======================================================

    if dimension <= 0:

        raise RuntimeError(
            "Invalid embedding dimension. "
            "Repair aborted."
        )


    # ======================================================
    # Build Fresh FAISS Index
    # ======================================================

    print()
    print("-" * 70)
    print("BUILDING NEW FAISS INDEX")
    print("-" * 70)

    new_index = (
        faiss.IndexFlatL2(
            dimension
        )
    )


    # ======================================================
    # Add Embeddings
    # ======================================================

    new_index.add(
        embeddings
    )


    # ======================================================
    # Validate New Index
    # ======================================================

    rebuilt_vector_count = (
        new_index.ntotal
    )

    print(
        f"New FAISS vectors    : "
        f"{rebuilt_vector_count}"
    )

    print(
        f"Metadata records     : "
        f"{metadata_count}"
    )

    if (
        rebuilt_vector_count
        != metadata_count
    ):

        raise RuntimeError(
            "Rebuilt FAISS count does not "
            "match metadata count. "
            f"FAISS={rebuilt_vector_count}, "
            f"Metadata={metadata_count}. "
            "Repair aborted."
        )


    # ======================================================
    # Save New FAISS Index
    # ======================================================

    print()
    print("-" * 70)
    print("SAVING REPAIRED FAISS INDEX")
    print("-" * 70)

    faiss.write_index(
        new_index,
        str(FAISS_PATH)
    )

    print(
        "Repaired FAISS index saved:"
    )

    print(
        FAISS_PATH
    )


    # ======================================================
    # Final Verification
    # ======================================================

    print()
    print("-" * 70)
    print("FINAL VERIFICATION")
    print("-" * 70)

    verified_index = (
        faiss.read_index(
            str(FAISS_PATH)
        )
    )

    verified_vector_count = (
        verified_index.ntotal
    )

    aligned = (
        verified_vector_count
        == metadata_count
    )


    # ======================================================
    # Final Output
    # ======================================================

    print()
    print("=" * 70)
    print("REPAIR COMPLETE")
    print("=" * 70)

    print()
    print(
        f"Previous FAISS vectors : "
        f"{existing_vector_count}"
    )

    print(
        f"Metadata records       : "
        f"{metadata_count}"
    )

    print(
        f"Rebuilt FAISS vectors  : "
        f"{verified_vector_count}"
    )

    print(
        f"Embedding dimension    : "
        f"{dimension}"
    )

    print(
        f"Aligned                : "
        f"{aligned}"
    )

    print()
    print(
        "Metadata modified      : False"
    )

    print(
        "Backup:"
    )

    print(
        BACKUP_PATH
    )

    print()
    print("=" * 70)


    # ======================================================
    # Final Safety Check
    # ======================================================

    if not aligned:

        raise RuntimeError(
            "FINAL VERIFICATION FAILED: "
            "FAISS and metadata are still "
            "not aligned."
        )

    return True


# ==========================================================
# Script Entry Point
# ==========================================================

if __name__ == "__main__":

    try:

        repair_faiss()

    except Exception as error:

        print()
        print("=" * 70)
        print("FAISS REPAIR FAILED")
        print("=" * 70)

        print()
        print(
            f"Error: {error}"
        )

        print()
        print("=" * 70)

        raise