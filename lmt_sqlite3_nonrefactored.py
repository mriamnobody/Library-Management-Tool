import datetime
import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('bookshelf.db')
c = conn.cursor()
date_time = datetime.datetime.now()

def input_field(field):
    while (inp := input(f"\nEnter the {field} of the book: ")) == "":
        print(f"\nPlease enter a valid {field}.")
    return inp

def print_book_details(books):
    for book in books:
        print("\nSerial:",book[0])
        print("Title:",book[1])
        print("Author:",book[2])
        print("Genre:",book[3])
        print("Location:",book[4])

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS books (
            serial INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            location TEXT,
            added_on DATE,
            last_updated_on TEXT
    )""")
    conn.commit()
create_table()

trigger_sql = '''
CREATE TRIGGER IF NOT EXISTS update_serials AFTER DELETE ON books
BEGIN
    UPDATE books SET serial = serial - 1 WHERE serial > old.serial;
END;
'''

c.execute(trigger_sql)
conn.commit()

def add_book():
    c.execute("SELECT serial FROM books ORDER BY serial DESC LIMIT 1")
    counter = c.fetchone()

    counter = 0 if counter is None else counter[0]
    counter = counter + 1
    title = input_field("Title")
    c.execute("SELECT * FROM books WHERE title = ?", (title,))
    books = c.fetchall()

    if books != [] :
        print("\nBook already exists in the library\n")
        return

    author = input_field("Author")
    genre = input_field("Genre")
    location = input_field("Location")

    c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
              (   counter,
                  title,
                  author,
                  genre,
                  location,
                  date_time,
                  None
              ))
    conn.commit()

    c.execute("SELECT * FROM books WHERE title = ?", (title,))
    books = c.fetchall()
    print("\nBook added successfully")
    print_book_details(books)

def view_books():
    try:
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        print(tabulate(books, headers=['Sr','Title', 'Author', 'Genre', 'Location','Date Added', 'What and When was last Updated'], tablefmt='grid'))
    except:
        print("\nNo table exists yet")
        
def delete_book():
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()

    if books[0][0] == 0:
        print("\nThere are no books in the library.")
    else:   
        title = input_field("title")
        pattern = "%"+title+"%"
        c.execute("SELECT * FROM books WHERE title LIKE = ?", (pattern,))
        conn.commit()
        books = c.fetchall()

        if len(books) > 1:
            print_book_details(books)
            if books != []:
                while True:
                    serial = input("\nEnter the serial number of the book which you want to delete:\n")
                    if serial != "":
                        break
                    else:
                        print("\nPlease enter a valid serial number.")

                while books == []:
                    print("\nBook with that serial number doesn't exist. Please enter a valid serial number.")
                    serial = input("\nEnter the serial number of the book which you want to delete:\n")
                    c.execute("SELECT * FROM books WHERE serial = ?", (serial,))
                    conn.commit()
                    books = c.fetchall()
                title = books[0][1]

                while True:
                    print(f"\nBook with Serial number {serial} and Title {title} will be deleted:\n")
                    confirmation = input(f"\nDo you want to delete this book? (yes/no):\n")
                    if confirmation == "yes":
                        c.execute("DELETE FROM books WHERE serial = ?", (serial,))
                        conn.commit()
                        print("\nBook Deleted successfully\n")
                        break
                    elif confirmation == "no":
                        print("\nOperation cancelled.\n")
                        break
                    else:
                        print("\nInvalid input.\n")
        else:
            if books != []:
                print_book_details(books)
                while True:
                    confirmation = input("\nDo you want to delete this book? (yes/no):\n")
                    if confirmation == "yes":
                        c.execute("DELETE FROM books WHERE title LIKE ?", (pattern,))
                        conn.commit()
                        print("\nBook successfully deleted from the library.\n")
                        break
                    elif confirmation == "no":
                        print("\nOperation cancelled.\n")
                        break
                    else:
                        print("\nInvalid input.\n")
            else:
                print("\nBook not found\n")
        
def search_book():
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()

    if books[0][0] == 0:
        print("\nThere are no books in the library.")
    else:
        title = input_field("title")
        pattern = f"%{title}%"
        c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
        books = c.fetchall()
        if books != []:
            print("\nBook found in the library")
            print_book_details(books)
        else:
            print("\nBook not found in the library")

def update_book():
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
    if books[0][0] == 0:
        print("\nThere are no books in the library.")
    else:   
        while (title := input("\nEnter the Title of the book: ")) == "":
            print("\nPlease enter a valid title.")

        pattern = "%"+title+"%"
        c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
        conn.commit()
        books = c.fetchall()

        if len(books) > 1:
            print("\nWe have found the following books in the library:")
            print_book_details(books)

            while True:
                serial = input("\nEnter the serial number of the book which you want to edit:\n")
                if serial != "":
                    break
                else:
                    print("\nPlease enter a valid serial number.")

            while books == []:
                print("\nBook with that serial number doesn't exist. Please enter a valid serial number.")
                serial = input("\nEnter the serial number of the book which you want to edit:\n")
                c.execute("SELECT * FROM books WHERE serial = ?", (serial,))
                conn.commit()
                books = c.fetchall()

            print(f"\nBook with Serial number {serial} and Title {title} will be edited:\n")
            c.execute("SELECT * FROM books WHERE serial = ?", (serial,))
            conn.commit()
            books = c.fetchone()

            if books != []:
                while True:
                    print("\nWhat would you like to edit?")
                    print("1. Title")
                    print("2. Author")
                    print("3. Genre")
                    print("4. Location")
                    print("5. Cancel\n")
                    edit_choice = input("Enter your choice: ")

                    if edit_choice == "1":
                        new_title = input_field("new Title")
                        date_time_str = str(date_time)
                        update_details = "The title of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET title = ?, last_updated_on = ? WHERE serial = ?''',(new_title, update_details ,serial))
                        conn.commit()
                        print("\nTitle updated successfully\n")
                        c.execute("SELECT * FROM books WHERE title = ? ", (new_title,))
                        conn.commit()
                        books = c.fetchall()
                        print_book_details(books)
                        break

                    elif edit_choice == "2":
                        new_author = input_field("new Author")
                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET author = ?, last_updated_on = ? WHERE serial = ?''',(new_author, update_details ,serial))
                        conn.commit()
                        print("\nAuthor updated successfully\n")
                        c.execute("SELECT * FROM books WHERE author = ?", (new_author,))
                        conn.commit()
                        books = c.fetchall()
                        print_book_details(books)
                        break

                    elif edit_choice == "3":
                        new_genre = input_field("new Genre")
                        date_time_str = str(date_time)
                        update_details = "The genre of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET genre = ?, last_updated_on = ? WHERE serial = ?''',(new_genre, update_details ,serial))
                        conn.commit()
                        print("\nGenre updated successfully\n")
                        c.execute("SELECT * FROM books WHERE genre = ? ", (new_genre,))
                        conn.commit()
                        books = c.fetchall()
                        print_book_details(books)
                        break

                    elif edit_choice == "4":
                        new_location = input_field("new Location")
                        date_time_str = str(date_time)
                        update_details = "The location of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET location = ?, last_updated_on = ? WHERE serial = ?''',(new_location, date_time ,serial))
                        conn.commit()
                        print("\nLocation updated successfully\n")
                        c.execute("SELECT * FROM books WHERE location = ? ", (new_location,))
                        conn.commit()
                        books = c.fetchall()
                        print_book_details(books)
                        break

                    elif edit_choice == "5":
                        break
                    else:
                        print("\nPlease enter a valid choice.\n")
            else:
                print("\nBook not found in the library")
        
        else:
            if books != []:
                print("\nWe have found the following book in the library:")
                print_book_details(books)

                while True:
                    print("\nWhat would you like to edit?")
                    print("1. Title")
                    print("2. Author")
                    print("3. Genre")
                    print("4. Location")
                    print("5. Cancel\n")
                    edit_choice = input("Enter your choice: ")

                    if edit_choice == "1":
                        new_title = input_field("new Title")
                        date_time_str = str(date_time)
                        update_details = "The Title of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET title = ?, last_updated_on = ? WHERE title = ?''',(new_title, update_details, title))
                        conn.commit()
                        print("\nTitle updated successfully\n")
                        c.execute("SELECT * FROM books WHERE title = ? ", (new_title,))
                        conn.commit()
                        books = c.fetchall()
                        break

                    elif edit_choice == "2":
                        new_author = input_field("new Author")
                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET author = ?, last_updated_on = ? WHERE title = ?''',(new_author, update_details ,title))
                        conn.commit()
                        print("\nAuthor updated successfully\n")
                        c.execute("SELECT * FROM books WHERE author = ? ", (new_author,))
                        conn.commit()
                        books = c.fetchall()
                        break

                    elif edit_choice == "3":
                        new_genre = input_field("new Genre")
                        date_time_str = str(date_time)
                        update_details = "The genre of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET genre = ?, last_updated_on = ? WHERE title = ?''',(new_genre, update_details ,title))
                        conn.commit()
                        print("\nGenre updated successfully\n")
                        c.execute("SELECT * FROM books WHERE genre = ? ", (new_genre,))
                        conn.commit()
                        books = c.fetchall()
                        break

                    elif edit_choice == "4":
                        new_location = input_field("new Location")
                        date_time_str = str(date_time)
                        update_details = "The location of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET location = ?, last_updated_on = ? WHERE title = ?''',(new_location, update_details ,title))
                        conn.commit()
                        print("\nLocation updated successfully\n")
                        c.execute("SELECT * FROM books WHERE location = ? ", (new_location,))
                        conn.commit()
                        books = c.fetchall()
                        break

                    elif edit_choice == "5":
                        break
                    else:
                        print("\nPlease enter a valid choice.\n")
            else:
                print("\nBook not found in the library")

def total_books():
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
    print(f"There are total {books[0][0]} books in the library")

def delete_table():
    print("\nAre you sure you want to delete all books from the library?")
    print("1. Yes")
    print("2. No\n")
    choice = input("Enter your choice: ")
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
 
    if choice == "1" and books[0][0] != 0:
        c.execute("DROP TABLE books")
        conn.commit()
        print("\nAll books deleted successfully\n")
        conn.commit()
    elif choice == "1" and books[0][0] == 0:
        print("\nThere are no books in the library to delete\n")
    elif choice == "2":
        print("\nBooks not deleted\n")
    else:
        print("\nPlease enter a valid choice\n")

def main():
    counter = 1
    while True:
        print("\n" + " " * 10 + "Library Management Tool" + " " * 10 + "\n")
        print("1. Add a new Book")
        print("2. View all Books")
        print("3. Search for a Book")
        print("4. Delete a Book")
        print("5. Update a Book")
        print("6. Total Books")
        print("7. Delete all Books")
        print("8. Exit\n")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            update_book()
        elif choice == "6":
            total_books()
        elif choice == "7":
            delete_table()
            create_table()
        elif choice == "8":
            print("\nExiting...")
            print("Thank you for using Library Management Tool\n")
            exit()
            conn.close()
        elif choice == "":
            print("\nPlease enter a valid choice.")
        else:
            print("\nPlease enter a valid choice.")
main()
