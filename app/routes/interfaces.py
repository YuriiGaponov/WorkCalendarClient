from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def index_page():
    return 'Заглушка'
