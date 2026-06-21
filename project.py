# project.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

engine = create_engine('sqlite:///library.db', echo=True)
print(f"Engine создан: {engine}")


Base = declarative_base() # ← базовый класс

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    
    books = relationship('Book', back_populates='author')
    
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_year={self.birth_year})>"


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))
    
    author = relationship('Author', back_populates='books')
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', year={self.year}, author_id={self.author_id})>"

#Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии для работы с БД
Session = sessionmaker(bind=engine)
session = Session()

# Добавление 3 авторов и 5 книг
print("Добавление авторов и книг")

# Создаём авторов
lev= Author(name='Лев Толстой', birth_year=1828)
dost = Author(name='Фёдор Достоевский', birth_year=1821)
gog = Author(name='Ybrjkfq Ujujkm', birth_year=1809)
bis = Author(name = 'pro', birth_year=4242)

# Добавляем авторов в сессию
session.add_all([lev, dost, gog, bis])
session.commit()
print("Добавлены авторы")

# Создаём книги
wap = Book(title='Война и мир', year=1869, author=lev)
kav = Book(title='Кавказский пленник', year=1872, author=lev)
prest = Book(title='Преступление и наказание', year=1866, author=dost)
idiot = Book(title='Идиот', year=1869, author=dost)
dead = Book(title='Мертвые души', year=1852, author=gog)
kniga1950 = Book(title='я1950+', year=1952, author=bis)
kniga19502 = Book(title='я1951+', year=1953, author=bis)

session.add_all([wap, kav, prest, idiot, dead, kniga1950, kniga19502])
session.commit()
print("Добавлены книги")

# Вывод имён всех авторов
print("-------------------------------------")
print("Имена всех авторов")
authors = session.query(Author).all()
for author in authors:
    print(f"Автор: {author.name}")
print()

# Изменение имени одного автора
print("-------------------------------------")
print("Изменение имени автора")
novia = session.query(Author).filter(Author.name == 'Ybrjkfq Ujujkm').first()
if novia:
    old_name = novia.name
    novia.name = 'Николай Гоголь'
    session.commit()
    print(f"Имя изменено: '{old_name}' -> '{novia.name}'")

# Удаление одной книги
print("-------------------------------------")
print("Удаление книги")
ploxkniga = session.query(Book).filter(Book.title == 'Кавказский пленник').first()
if ploxkniga:
    title = ploxkniga.title
    session.delete(ploxkniga)
    session.commit()
    print(f"Книга удалена: '{title}'")

# Все книги, отсортированные по году (от новых к старым)
print("-------------------------------------")
print("Все книги, отсортированные по году (от новых к старым)")
all_books = session.query(Book).order_by(Book.year.desc()).all()
for book in all_books:
    print(f"{book.title} ({book.year}) - {book.author.name}")
print()

# Книги, изданные после 1950 года
print("-------------------------------------")
print("Книги, изданные после 1950 года")
posle1950 = session.query(Book).filter(Book.year > 1950).all()
if posle1950:
    for book in posle1950:
        print(f"{book.title} ({book.year}) - {book.author.name}")
else:
    print("Книг, изданных после 1950 года, не найдено")
print()

#  Автор по конкретному имени
print("-------------------------------------")
print("Поиск автора по имени")
print("Введи автора (по умолчанию pro)")
author_name = input().strip()
if author_name == "":
    author_name = "pro"
nashel = session.query(Author).filter(Author.name == author_name).first()
if nashel:
    print(f"Найден автор: {nashel.name} (год рождения: {nashel.birth_year})")
    print("Его книги:")
    for book in nashel.books:
        print(f"  - {book.title} ({book.year})")
else:
    print(f"Автор с именем '{author_name}' не найден")
print()

# Количество книг через func.count()
print("-------------------------------------")
print("Количество книг")
skol = session.query(func.count(Book.id)).scalar()
print(f"Всего книг в библиотеке: {skol}")
print()

#  Первые 3 книги в алфавитном порядке
print("-------------------------------------")
print("Первые 3 книги в алфавитном порядке")
pervie3 = session.query(Book).order_by(Book.title).limit(3).all()
for book in pervie3:
    print(f"{book.title} ({book.year}) - {book.author.name}")



#Очистка с предыдущего раза
Base.metadata.drop_all(engine)
# Закрытие сессии
session.close()