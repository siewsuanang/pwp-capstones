class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        current_email = self.email
        self.email = address
        print("{name}'s email has been updated from {current_email} to {new_email}.".format(name=self.name, current_email=current_email, new_email=self.email))

    def __repr__(self):
        return "User {name}, email: {email}, books read: {book}".format(name=self.name, email=self.email, book=self.books)

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False
        
    def read_book(self, book, rating=None):
        self.books[book] = rating
        
    def get_average_rating(self):
        total_rating = 0
        count = 0
        for user_rating in self.books.values():
            if not user_rating == None:
                total_rating += user_rating
                count += 1
        try:
            average_rating = total_rating / count
        except ZeroDivisionError:
            average_rating = 0
        return average_rating
        
    def valid_email(self, email):
        valid_character_1 = '@'
        valid_characters_2 = ['.com', '.edu', '.org']    
        valid_flag = False
        for i in range(len(valid_characters_2)):
            if valid_characters_2[i] in email:
               valid_flag = True
               break
        if valid_character_1 in email and valid_flag:
            return True
        else:
            print('Invalid Email')
            return False
           
    
class Book:
    isbn_dict = {}
    
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        Book.isbn_dict[isbn] = self.title
        
    def get_title(self):
        return self.title
        
    def get_isbn(self):
        return self.isbn
        
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("{}'s ISBN has been updated.".format(self.title))
    
    def isbn_exists(self, isbn):
        if isbn in Book.isbn_dict:
            print('ISBN already exists')
            return True
        else:
            return False
            
    def add_rating(self, rating):
        if not rating == None:
            if rating >= 0 and rating <= 4:
                if not rating in self.ratings:
                    self.ratings.append(rating)
            else:
                print('Invalid Rating')
        else:
            print('Invalid Rating')
        
    def __eq__(self, other_book):
        return (self.title, self.isbn) == (other_book.title, other.isbn)
    
    def get_average_rating(self):
        try:
            average_rating = sum(self.ratings) / len(self.ratings)
        except ZeroDivisionError:
            average_rating = 0
        return average_rating
        
    def __hash__(self):
        return hash((self.title, self.isbn))
       
    def __repr__(self):
        return "Book: {}".format(self.title)
        

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
        
    def get_author(self):
        return self.author
        
    def __repr__(self):
        return "Fiction Book: {title} by {author}".format(title=self.title, author=self.author)
        

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
        
    def get_subject(self):
        return self.subject
        
    def get_level(self):
        return self.level
            
    def __repr__(self):
        return "Non-Fiction Book: {title}, a {level} manual in {subject}".format(title=self.title, level=self.level, subject=self.subject)
        
        
class TomeRater(Book):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        if not self.isbn_exists(isbn):
            return Book(title, isbn)
    
    def create_novel(self, title, author, isbn):
        if not self.isbn_exists(isbn):
            return Fiction(title, author, isbn)
        
    def create_non_fiction(self, title, subject, level, isbn):
        if not self.isbn_exists(isbn):
            return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if not email in self.users:
            print('No user with email {}!'.format(email))
        else:    
            this_user = self.users[email]
            this_user.read_book(book, rating)
            book.add_rating(rating)
            if not book in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1
        
    def add_user(self, name, email, user_books=None):
        if User.valid_email(self, email):
            if email in self.users:
                print('This user already exists')
            else:
                self.users[email] = User(name, email)
                if not user_books == None:
                    for user_book in user_books:
                        self.add_book_to_user(user_book, email)
       
    def print_catalog(self):
        print('\nCatalog:')
        count = 0
        for key, value in self.books.items():
            count += 1
            string = '{}) {}'.format(count, key, value)
            print(string)
        
    def print_users(self):
        print('\nUser List:')
        count = 0
        for user, value in self.users.items():
            count += 1
            this_user = value
            string = '{}) {}'.format(count, this_user.name)
            print(string)
        
    def most_read_book(self):
        most_read_book_list = sorted(self.books.items(), key=lambda x: x[1], reverse=True)
        user_count = 0
        book_most_read = []
        for i in range(len(most_read_book_list)):
            if most_read_book_list[i][1] >= user_count:
                user_count = most_read_book_list[i][1]
                book_most_read.append(most_read_book_list[i][0])
            else:
                break
        count = 0
        if len(book_most_read) > 1:
            for book in book_most_read:
                count += 1
                string = '{}) {}'.format(count, book)
                print(string)
            print('Read {} times'.format(user_count))
            return ''
        else:
            string = '{}, read {} times'.format(book_most_read[0], user_count)
            return string
            
    def highest_rated_book(self):
        average_rating = 0
        rated_book_list = []
        for key, value in self.books.items():
            average_rating = key.get_average_rating()
            rated_book_list.append((average_rating, key.title))
        sorted_rated_book_list = sorted(rated_book_list, reverse=True)
        highest_average_rating = 0
        book_title = []
        for i in range(len(sorted_rated_book_list)):
            if sorted_rated_book_list[i][0] >= highest_average_rating:
                highest_average_rating = sorted_rated_book_list[i][0]
                book_title.append(sorted_rated_book_list[i][1])
            else:
                break
        if len(book_title) > 1:
            count = 0
            for book in book_title:
                count += 1
                string = '{}) {}'.format(count, book)
                print(string)
            print('With average rating of {}'.format(highest_average_rating))
            return ''
        else:
            string = '{} with averate rating of {}'.format(book_title[0], highest_average_rating)
            return string
        
    def most_positive_user(self):
        average_rating = 0
        user_name_list = []
        for email, user in self.users.items():
            this_user = self.users[email]
            average_rating = this_user.get_average_rating()
            user_name_list.append((average_rating, this_user.name))
        sorted_user_name_list = sorted(user_name_list, reverse=True)
        highest_average_rating = 0
        user_names = []
        for i in range(len(sorted_user_name_list)):
            if sorted_user_name_list[i][0] >= highest_average_rating:
                highest_average_rating = sorted_user_name_list[i][0]
                user_names.append(sorted_user_name_list[i][1])
            else:
                break
        if len(user_names) > 1:
            count = 0
            for user_name in user_names:
                count += 1
                string = '{}) {}'.format(count, user_name)
                print(string)
            print('With average rating of {}'.format(highest_average_rating))
            return ''
        else:
            string = '{} with averate rating of {}'.format(user_names[0], highest_average_rating)
            return string
         