import datetime
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Date, Time, Integer, Integer
from sqlalchemy.orm import relationship, backref
from database import Base


# -------------------one to many- parent to child, many to one- child to parent--------------
class A_Parent(Base):
    __tablename__ = "A_parent_table"  # table names are converted to lower case in the database
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    children = relationship(
        "A_Child")  # children should be list-like, also use backref paremeter to explicitely define one directional relationship, mentioned in C table below


class A_Child(Base):
    __tablename__ = "A_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("A_parent_table.id"))


# ---To establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one---
#  using back_populates relationship parameter
class B_Parent(Base):
    __tablename__ = "B_parent_table"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    children = relationship("B_Child", back_populates="parent")  # children should be list-like


class B_Child(Base):
    __tablename__ = "B_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("B_parent_table.id"))
    parent = relationship("B_Parent", back_populates="children", lazy='immediate') # immediately loads the relation
    # object


# Alternatively, the relationship.backref option may be used on a single relationship() instead of using
# relationship.back_populates on the Parent table.
class C_Parent(Base):
    __tablename__ = "C_parent_table"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    children = relationship("C_Child",
                            backref="parent")  # it will create the backref="parent" relation in the child tabe and use by itself we don't need to border


class C_Child(Base):
    __tablename__ = "C_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("C_parent_table.id"))
    # parent = relationship("C_Parent", back_populates="children") # cant use this statement when using backref in parent


# Using foreign key ON DELETE cascade
class D_Parent(Base):
    __tablename__ = "D_parent_table"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    children = relationship("D_Child", cascade="all, delete",
                            passive_deletes=True, )  # delete all its child on deletion


class D_Child(Base):
    __tablename__ = "D_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("D_parent_table.id",
                                           ondelete="CASCADE"))  # onDelete parameter will allow to delete from navicat despite of foreign keys


# ---one-to-one-----
# “collection” side ie the child is converted into a scalar relationship using the uselist=False
# flag. when we load a Parent object, the Parent.child attribute will refer to a single Child object rather than a
# collection. If we replace the value of Parent.child with a new Child object, the ORM’s unit of work process will
# replace the previous Child row with the new one, setting the previous child.parent_id column to NULL by default
# unless there are specific cascade behaviors set up.
class E_Parent(Base):
    __tablename__ = "E_parent_table"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    children = relationship("E_Child", back_populates="parent", uselist=False)


class E_Child(Base):
    __tablename__ = "E_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("E_parent_table.id"), nullable=False)
    parent = relationship("E_Parent", back_populates="children")


# In the case where the relationship.backref parameter is used to define the “one-to-many” side,
# this can be converted to the “one-to-one” convention using the backref() function which allows the relationship
# generated by the relationship.backref parameter to receive custom parameters, in this case the uselist parameter:
class F_Parent(Base):
    __tablename__ = "F_parent_table"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))


class F_Child(Base):
    __tablename__ = "F_child_table"
    id = Column(Integer, primary_key=True)
    childName = Column(String(50))
    parent_id = Column(Integer, ForeignKey("F_parent_table.id", ondelete="CASCADE"), nullable=False)
    parent = relationship("F_Parent", backref=backref("children",
                                                      uselist=False))  # uselist=False will allow only a object and will prevent passing array, or list


# relationship within same table implimentation
class G_User(Base):
    __tablename__ = "G_user"
    id = Column(Integer, primary_key=True)
    parentName = Column(String(50))
    created_by_id = Column(Integer, ForeignKey("G_user.id"))  # self Foreign key

# Sql triggers refer docs
