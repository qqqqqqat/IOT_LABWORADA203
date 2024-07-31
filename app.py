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

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all() 
    # .all เอาข้อมูลจากฐานข้อมูลทั้งหมด

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()
    # เอาอันแรกอันเดียว

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(
        title=book['title'], 
        author=book['author'], 
        year=book['year'],
        describe=book['describe'],
        summary=book['summary'],
        category=book['category'],
        is_published=book['is_published'],
        imgurl=book['imgurl'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: str, book: dict, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Book).filter(models.Book.id == book_id).first()
    if (bk is None):
        response.status_code = 400
        return {
            "message" : "Book's ID not found."
        }
    keys = ["id", "title", "year", "is_published", "summary","describe","category","imgurl"]
    for key in keys:
        if key in book:
            setattr(bk, key, book[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Book's info edited successfully"
    }

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: str, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Book).filter(models.Book.id == book_id).first()
    if (bk is not None):
        db.delete(bk)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Book's ID not found."
    }


@router_v1.get('/infostudents')
async def get_infostudents(db: Session = Depends(get_db)):
    return db.query(models.Info).all()

@router_v1.get('/infostudents/{info_id}')
async def get_book(info_id: int, db: Session = Depends(get_db)):
    return db.query(models.Info).filter(models.Info.id == info_id).first()
    # เอาอันแรกอันเดียว

@router_v1.post('/infostudents')
async def create_Info(Informations: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newInfostu = models.Info( firstname=Informations['firstname'], surname=Informations['surname'], id=Informations['id'], dateofbirth=Informations['dateofbirth'], gender=Informations['gender'])
    db.add(newInfostu)
    db.commit()
    db.refresh(newInfostu)
    response.status_code = 201
    return newInfostu

@router_v1.put('/infostudents/{info_id}')
def update_book(info_id: int, Informations: dict, response: Response,db: Session = Depends(get_db)):
    for i, b in enumerate(books):
        if b['id'] == book_id:
            books[i] = book
            return book
    response.status_code = 404
    return {
        'message': 'Book not found'
    }

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

@router_v1.get('/menu')
async def get_menu(db: Session = Depends(get_db)):
    return db.query(models.Menu).all() 
    # .all เอาข้อมูลจากฐานข้อมูลทั้งหมด

@router_v1.get('/menu/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    # เอาอันแรกอันเดียว

@router_v1.post('/menu')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newmenu = models.Menu(
        menuname=menu['menuname'], 
        price=menu['price'],
        imgurl=menu['imgurl'],
        is_published=menu['is_published'])

    db.add(newmenu)
    db.commit()
    db.refresh(newmenu)
    response.status_code = 201
    return newmenu

@router_v1.patch('/menu/{menu_id}')
async def update_menu(menu_id: str, menu: dict, response: Response, db: Session = Depends(get_db)):
    mn = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if (mn is None):
        response.status_code = 400
        return {
            "message" : "Menu's ID not found."
        }
    keys = ["id", "menuname", "price", "is_published","imgurl"]
    for key in keys:
        if key in menu:
            setattr(mn, key, menu[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Menu's info edited successfully"
    }

@router_v1.delete('/menu/{menu_id}')
async def delete_menu(menu_id: str, response: Response, db: Session = Depends(get_db)):
    mn = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if (mn is not None):
        db.delete(mn)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Menu's ID not found."
    }


# การสั่ง

@router_v1.get('/order')
async def get_order(db: Session = Depends(get_db)):
    return db.query(models.Order).all() 
    # .all เอาข้อมูลจากฐานข้อมูลทั้งหมด

@router_v1.get('/order/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()
    # เอาอันแรกอันเดียว

@router_v1.post('/order')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    neworder = models.Order(
        amount=order['amount'], 
        total=order['total'],
        detail=order['detail'], 
        getmenuname=order['getmenuname'])

    db.add(neworder)
    db.commit()
    db.refresh(neworder)
    response.status_code = 201
    return neworder

@router_v1.patch('/order/{order_id}')
async def update_order(order_id: str, order: dict, response: Response, db: Session = Depends(get_db)):
    od = db.query(models.Order).filter(models.Order.id == order_id).first()
    if (od is None):
        response.status_code = 400
        return {
            "message" : "Order's ID not found."
        }
    keys = ["id", "amount", "total","detail","getmenuname"]
    for key in keys:
        if key in order:
            setattr(od, key, order[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Order's info edited successfully"
    }

@router_v1.delete('/order/{order_id}')
async def delete_order(order_id: str, response: Response, db: Session = Depends(get_db)):
    od = db.query(models.Order).filter(models.Order.id == order_id).first()
    if (od is not None):
        db.delete(od)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Order's ID not found."
    }











app.include_router(router_v1)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,port=3000)