"""
Create the SQLAlchemy parts
"""
# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
"connecting" to a SQLite database (opening a file with SQLite database)
The file will be located at the same directory in the file `sql_app.db`.
That's why the last part is `./sql_app.db`.
If using a **PostgreSQL** database instead, would have to uncomment the second line
...and adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other)
"""
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

"""
creating a SQLAlchemy "engine"
will be later used in other places
The argument `connect_args={"check_same_thread":False}`
...is needed only for SQLite. It's not needed for other databases.
"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

"""
Each instance of the `SessionLocal` class will be a database session. The class itself is not a database session yet.
But once we create an instance of the `SessionLocal` class, this instance will be the actual database session.
"""
# creating the `SessionLocal` class, using the function `sessionmaker`:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# using the function `declarative_base()` that returns a class.
# later we will inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()