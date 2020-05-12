import os
import werkzeug
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

  # import file
  f = open("books.csv")
  reader = csv.reader(f)
  next(reader)
  for row in reader:
      db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn":row[0], "title":row[1], "author":row[2], "year":row[3]})
  db.commit() #dlaczego w przykładach jest session przed commit

if __name__ == "__main__":
    # with app.app_context():
    main()
