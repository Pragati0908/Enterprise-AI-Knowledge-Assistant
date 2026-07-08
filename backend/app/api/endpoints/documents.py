from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

documents = [
    {
        "id": 1,
        "filename": "AI_Project_Report.pdf"
    },
    {
        "id": 2,
        "filename": "Machine_Learning.docx"
    },
    {
        "id": 3,
        "filename": "Research_Paper.pdf"
    }
]


@router.get("/")
def get_documents():

    return {
        "total_documents": len(documents),
        "documents": documents
    }