from app.services.retriever import Retriever
from app.services.search_service import SearchService


def main():

    retriever = Retriever()

    search_service = SearchService(
        retriever=retriever
    )

    result = search_service.search(
        query="What is OCR?",
        top_k=10
    )

    print("\n" + "=" * 70)
    print("MULTI-DOCUMENT SEARCH TEST")
    print("=" * 70)

    print(
        f"\nSuccess : {result['success']}"
    )

    print(
        f"Query : {result['query']}"
    )

    print(
        f"Total Results : {result['total_results']}"
    )

    if result["success"]:

        print(
            f"Documents Found : "
            f"{result.get('documents_found', 0)}"
        )

        print("\nDocuments:")

        for document in result.get(
            "documents",
            []
        ):

            print(
                f"  - {document}"
            )

        print("\nRetrieved Chunks:")

        for item in result["results"]:

            print("\n-----------------------------")

            print(
                f"Document : "
                f"{item['document']}"
            )

            print(
                f"Page : "
                f"{item['page']}"
            )

            print(
                f"Chunk ID : "
                f"{item['chunk_id']}"
            )

            print(
                f"Distance : "
                f"{item['distance']:.4f}"
            )

            print(
                f"Text : "
                f"{item['text'][:200]}"
            )

    else:

        print(
            f"\nError : {result.get('error')}"
        )


if __name__ == "__main__":

    main()