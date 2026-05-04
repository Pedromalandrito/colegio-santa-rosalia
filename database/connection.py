from sqlmodel import Session, create_engine
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/colegio_santa_rosalia"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session