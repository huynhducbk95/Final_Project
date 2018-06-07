from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
import os.path

Base = declarative_base()
CURRENT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    birthday = Column(String(50))
    class_name = Column(String(50))

    def __repr__(self):
        return "sinh vien %s, ngay sinh %s, thuoc lop %s" % (
            self.name, self.birthday, self.class_name
        )


engine = create_engine(
    'sqlite:///' + CURRENT_FOLDER_PATH + '/database.sqlite', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.metadata.create_all(engine)


class DatabaseDriver():
    def __init__(self):
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))

    def list(self):
        student_list = self.session.query(Student).all()
        return student_list

    def add_student(self, name, birthday, class_name):
        student = Student(name=name, birthday=birthday, class_name=class_name)
        self.session.add(student)
        self.session.commit()
