# class User:
#         def __init__(self, name, passwordh):
#             self.name = name
#             self.password = passwordh
#
#         def add_user(user):
#             return
class Book:
    def __init__(self, title="Titleplaceholder", author="Author", year=0000, isbn="1234567890123", review_count=0, average_score=0):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn #Primary_Key
        self.review_count = review_count
        self.average_score = average_score
        work_ratings_count = 0 #to be imported form goodreads
        average_rating = 0 #to be imported from goodreads

    # def new_review(score):
    #     self.review_count += 1
    #     self.average_score = (self.average_score*self.review.count + score)/(self.review_count+1)


class Review:
    def __init__(self, book_isbn, review, rating):
        self.book_isbn = book_isbn
        self.review = review
        self.rating = rating

    def store_review():
        #add reviews table row and add book elements
        rate = db.execute("SELECT review_count, average_score FROM books WHERE isbn=:isbn", {"isbn":self.book_isbn})
        new_score = (rate[1]*rate[0]+self.rating)/(rate[0]+1)
        db.execute("UPDATE books SET review_count+=1, average_score=:new_score WHERE isbn=:isbn", {"new_score":new_score, "isbn":self.book_isbn})

        db.execute("INSERT INTO reviews (isbn, rating, review) VALUES (:isbn, :rating, :review)", {"isbn":self.book_isbn, "rating":self.rating, "review":self.review})
        return
