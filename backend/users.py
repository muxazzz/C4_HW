# импортируем модули стандартной библиотеки uuid и datetime

import uuid
import datetime
import server

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///user.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

"""
class Athlet(Base):
	__tablename__ = 'athelete'
	id = sa.Column(sa.INTEGER, primary_key=True)
	age = sa.Column(sa.INTEGER)
	gender = sa.Column(sa.TEXT)
	gold_medals = sa.Column(sa.INTEGER)

engine = sa.create_engine(DB_PATH)
sessions = sessionmaker(engine)
session = sessions()

atheletes = session.query(Athlet).filter(Athlet.gender=="Female").count()
atheletes_age = session.query(Athlet).filter(Athlet.age > 30).count()
atheletes_gold = session.query(Athlet).filter(Athlet.age > 25, Athlet.gender == "Male", Athlet.gold_medals >= 2).count()
print(atheletes, atheletes_age, atheletes_gold)
"""


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    uid = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    description = sa.Column(sa.TEXT)
    # фамилия пользователя
    is_completed = sa.Column(sa.Boolean)


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # запрашиваем у пользователя данные
    uid = uid
    description = description
    is_completed = is_completed
    # генерируем идентификатор пользователя и сохраняем его строковое представление
   
    # создаем нового пользователя
    user = User(
        uid=uid,
        description=description,
        is_completed=is_completed,
    )

    return user


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
        # запрашиваем данные пользоватлея
    user = request_data()
        # добавляем нового пользователя в сессию
    session.add(user)
        # обновляем время последнего визита для этого пользователя
        # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")
   

if __name__ == "__main__":
    main()