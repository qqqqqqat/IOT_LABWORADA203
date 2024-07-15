from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

# @router_v1.get('/books')
# async def get_books(db: Session = Depends(get_db)):
#     return db.query(models.Book).all() 
#     # .all เอาข้อมูลจากฐานข้อมูลทั้งหมด

# @router_v1.get('/books/{book_id}')
# async def get_book(book_id: int, db: Session = Depends(get_db)):
#     return db.query(models.Book).filter(models.Book.id == book_id).first()
#     # เอาอันแรกอันเดียว

# @router_v1.post('/books')
# async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
#     # TODO: Add validation
#     newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
#     db.add(newbook)
#     db.commit()
#     db.refresh(newbook)
#     response.status_code = 201
#     return newbook

@router_v1.get('/infostudents')
async def get_infostudents(db: Session = Depends(get_db)):
    return db.query(models.Info).all()

# @router_v1.get('/infostudents/{info_id}')
# async def get_book(info_id: int, db: Session = Depends(get_db)):
#     return db.query(models.Info).filter(models.Info.id == info_id).first()
#     # เอาอันแรกอันเดียว

@router_v1.post('/infostudents')
async def create_Info(Informations: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newInfostu = models.Info( firstname=Informations['firstname'], surname=Informations['surname'], id=Informations['id'], dateofbirth=Informations['dateofbirth'], gender=Informations['gender'])
    db.add(newInfostu)
    db.commit()
    db.refresh(newInfostu)
    response.status_code = 201
    return newInfostu

# @router_v1.put('/infostudents/{info_id}')
# def update_book(info_id: int, Informations: dict, response: Response,db: Session = Depends(get_db)):
#     for i, b in enumerate(books):
#         if b['id'] == book_id:
#             books[i] = book
#             return book
#     response.status_code = 404
#     return {
#         'message': 'Book not found'
#     }

@router_v1.put('/infostudents/{info_id}')
async def update_Info(info_id: str, Informations: dict, response: Response, db: Session = Depends(get_db)):
    # Check if student exists
    modifystu = db.query(models.Info).filter(models.Info.id == info_id).first()
    if modifystu is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update student information
    modifystu.firstname = Informations.get('firstname', modifystu.firstname)
    modifystu.surname = Informations.get('surname', modifystu.surname)
    modifystu.dateofbirth = Informations.get('dateofbirth', modifystu.dateofbirth)
    modifystu.gender = Informations.get('gender', modifystu.gender)

    db.commit()
    db.refresh(modifystu)
    response.status_code = 200
    return modifystu

# @router_v1.patch('/books/{book_id}')
# async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
#     pass

# @router_v1.delete('/books/{book_id}')
# async def delete_book(book_id: int, db: Session = Depends(get_db)):
#     pass


@router_v1.delete('/infostudents/{info_id}')
async def delete_Info(info_id: str, response: Response, db: Session = Depends(get_db)):
    # Check if student exists
    delete_Info = db.query(models.Info).filter(models.Info.id == info_id).first()
    if delete_Info is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete student
    db.delete(delete_Info)
    db.commit()

    response.status_code = 200
    return {"detail": "Student deleted successfully"}


app.include_router(router_v1)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
