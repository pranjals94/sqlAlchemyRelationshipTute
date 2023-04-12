import database
import model
# from models import testModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from database import engine
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

# if using virtual environment activate it and then type the following.
# pip uninstall <packagename> # uninstall a package
# pip list #lists oll the modules
# pip freeze > requirements.txt  #cli to generate requirements.txt
# pip install -r requirements.txt # install oll the package at one go

print("----------main.py file serving-------------------------")
model.Base.metadata.create_all(bind=engine)  # create database

# app = FastAPI(docs_url="/documentation", redoc_url=None)  # Disable swagger (auto API UI)

app = FastAPI()

# --------------allow cors--------------------------
origins = [
    "http://localhost:3000",
    "localhost:3000",
]
# A "middleware" is a function that works with every request before it is processed by any specific path operation.
# And also with every response before returning it. refer docs for more info
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- APIs'----
@app.get("/A")
async def read_item(db: Session = Depends(database.get_db)):
    # one to many

    db_child = model.A_Child(childName="Chintu A")
    db_child_1 = model.A_Child(childName="Rickey A")
    db_parent = model.A_Parent(parentName="Bob A", children=[db_child, db_child_1])  # children should be list-like
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return {"item_id": db_parent.children}


@app.get("/B")
async def read_item(db: Session = Depends(database.get_db)):
    # To establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one

    # db_child = model.B_Child(childName="Chintu B")
    # db_child_1 = model.B_Child(childName="Rickey B")
    # db_parent = model.B_Parent(parentName="Bob B", children=[db_child, db_child_1])  # children should be list-like
    # db.add(db_parent)
    # db.commit()

    # db_parent = model.B_Parent(parentName="Tom B")
    # db_child = model.B_Child(childName="Layla B", parent=db_parent)
    # db.add(db_child)
    # db.commit()

    # parent = db.get(model.B_Parent, 1) #  we can either use db.get(model.B_Parent or model.B_Child) using both
    # together gives error.
    child = db.get(model.B_Child, 1)
    # print(child.parent)  # if we don't use this statement here , only parent_id is sent in the return statement ( in case lazy='select' default value in ORM Relationship setting)

    return {"child": child}


@app.get("/D")
async def read_item(db: Session = Depends(database.get_db)):
    db_child = model.D_Child(childName="Chintu D")
    db_child_1 = model.D_Child(childName="Rickey D")
    db_parent = model.D_Parent(parentName="Bob D", children=[db_child, db_child_1])  # children should be list-like
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return {"item_id": db_parent.children}


@app.get("/E")
async def read_item(db: Session = Depends(database.get_db)):
    db_child = model.E_Child(childName="Chintu E")
    db_parent = model.E_Parent(parentName="Bob E", children=db_child)  # children cannot be list like refer model E
    db.add(db_parent)
    db.commit()

    # try to update the child
    # foreign key id cannot be null error
    # db_child_1 = model.E_Child(childName="Rickey E")
    # db_parent = db.get(model.E_Parent, 1)
    # db_parent.children = db_child_1
    # db.add(db_parent)
    # db.commit()
    db.refresh(db_parent)
    return {"item_id": db_parent.children}


@app.get("/F")
async def read_item(db: Session = Depends(database.get_db)):
    db_parent = model.F_Parent(parentName="Bob F")
    db_child = model.F_Child(childName="Chintu F", parent=db_parent)  # cannot pass list in parent
    db.add(db_child)
    db.commit()

    return {"item_id": db_parent.children}
