import sqlite3
from fpdf import FPDF
from tabulate import tabulate
from typing import Union, Set, Tuple, List


conn = sqlite3.connect('bookshelf.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS books (
            serial INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            location TEXT
    )""")
conn.commit()

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
    if counter == None:
        counter = 0
    else:
        counter = counter[0]
    counter = counter + 1

    while True:
        title = input("\nEnter the Title of the book: ")
        if title != "":
            break
        else:
            print("\nPlease enter a valid title.")
    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
    books = c.fetchall()
    if books != [] :
        print("\nBook already exists in the library\n")
        return

    while True:
        author = input("\nEnter the Author of the book: ")
        if author != "":
            break
        else:
            print("\nPlease enter a valid author.")

    while True:
        genre = input("\nEnter the Genre of the book: ")
        if genre != "":
            break
        else:
            print("\nPlease enter a valid genre.")
    
    while True:
        location = input("\nEnter the Location of the book: ")
        if location != "":
            break
        else:
            print("\nPlease enter a valid location.")
    
    c.execute("INSERT INTO books VALUES (:serial, :title, :author, :genre, :location)",
              {   'serial': counter,
                  'title': title,
                  'author': author,
                  'genre': genre,
                  'location': location
              })   
    conn.commit()

    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
    books = c.fetchall()
    print("\nBook added successfully")
    for book in books:
        print("\nSerial:",book[0])
        print("Title:",book[1])
        print("Author:",book[2])
        print("Genre:",book[3])
        print("Location:",book[4])

def view_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    print(tabulate(books, headers=['Sr','Title', 'Author', 'Genre', 'Location'], tablefmt='grid'))
    
def delete_book():
    while True:
        title = input("\nEnter the Title of the book: ")
        if title != "":
            break
        else:
            print("\nPlease enter a valid title.")

    pattern = "%"+title+"%"
    c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
    conn.commit()
    books = c.fetchall()
    if len(books) > 1:
        for book in books:
            print("\nSerial:",book[0])
            print("Title:",book[1])
            print("Author:",book[2])
            print("Genre:",book[3])
            print("Location:",book[4])
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
                c.execute("SELECT * FROM books WHERE serial = :serial", {'serial': serial})
                conn.commit()
                books = c.fetchall()
            title = books[0][1]

            while True:
                print(f"\nBook with Serial number {serial} and Title {title} will be deleted:\n")
                confirmation = input(f"\nDo you want to delete this book? (yes/no):\n")
                if confirmation == "yes":
                    c.execute("DELETE FROM books WHERE serial = :serial", {'serial': serial})
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
            for book in books:
                print("\nSerial:",book[0])
                print("Title:",book[1])
                print("Author:",book[2])
                print("Genre:",book[3])
                print("Location:",book[4])

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
    while True:
        title = input("\nEnter the Title of the book: ")
        if title != "":
            break
        else:
            print("\nPlease enter a valid title.")
    pattern = "%"+title+"%"
    c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
    books = c.fetchall()
    if books != []:
        print("\nBook found in the library")
        for book in books:
            print("\nTitle:",book[0])
            print("Author:",book[1])
            print("Genre:",book[2])
            print("Location:",book[3])
    else:
        print("\nBook not found in the library")

def update_book():

    while True:
        title = input("\nEnter the Title of the book: ")
        if title != "":
            break
        else:
            print("\nPlease enter a valid title.")

    pattern = "%"+title+"%"
    c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
    conn.commit()
    books = c.fetchall()
    if len(books) > 1:
        print("\nWe have found the following books in the library:")

    else:
        print("\nWe have found the following book in the library:")

    for book in books:
        print("\nSerial:",book[0])
        print("Title:",book[1])
        print("Author:",book[2])
        print("Genre:",book[3])
        print("Location:",book[4])

    if len(books) > 1:
        while True:
            serial = input("\nEnter the serial number of the book which you want to edit:\n")
            if serial != "":
                break
            else:
                print("\nPlease enter a valid serial number.")

        while books == []:
            print("\nBook with that serial number doesn't exist. Please enter a valid serial number.")
            serial = input("\nEnter the serial number of the book which you want to edit:\n")
            c.execute("SELECT * FROM books WHERE serial = :serial", {'serial': serial})
            conn.commit()
            books = c.fetchall()

        print(f"\nBook with Serial number {serial} and Title {title} will be edited:\n")
        c.execute("SELECT * FROM books WHERE serial = :serial", {'serial': serial})
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
                    while True:
                        new_title = input("\nEnter the new Title of the book: ")
                        if new_title != "":
                            break
                        else:
                            print("\nPlease enter a valid title.")

                    c.execute('''UPDATE books SET title = ? WHERE serial = ?''',(new_title, serial))
                    conn.commit()
                    print("\nTitle updated successfully\n")
                    c.execute("SELECT * FROM books WHERE title = :title", {'title': new_title})
                    books = c.fetchall()
                    for book in books:
                        print("\nTitle:",book[0])
                        print("Author:",book[1])
                        print("Genre:",book[2])
                        print("Location:",book[3])
                    break

                elif edit_choice == "2":
                    while True:
                        new_author = input("\nEnter the new Author of the book: ")
                        if new_author != "":
                            break
                        else:
                            print("\nPlease enter a valid author.")

                    c.execute('''UPDATE books SET author = ? WHERE serial = ?''',(new_author, serial))
                    conn.commit()
                    print("\nAuthor updated successfully\n")
                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    books = c.fetchall()
                    for book in books:
                        print("\nTitle:",book[0])
                        print("Author:",book[1])
                        print("Genre:",book[2])
                        print("Location:",book[3])
                    break

                elif edit_choice == "3":
                    while True:
                        new_genre = input("\nEnter the new Genre of the book: ")
                        if new_genre != "":
                            break
                        else:
                            print("\nPlease enter a valid genre.")

                    c.execute('''UPDATE books SET genre = ? WHERE serial = ?''',(new_genre, serial))
                    conn.commit()
                    print("\nGenre updated successfully\n")
                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    books = c.fetchall()
                    for book in books:
                        print("\nTitle:",book[0])
                        print("Author:",book[1])
                        print("Genre:",book[2])
                        print("Location:",book[3])
                    break

                elif edit_choice == "4":
                    while True:
                        new_location = input("\nEnter the new Location of the book: ")
                        if new_location != "":
                            break
                        else:
                            print("\nPlease enter a valid location.")

                    c.execute('''UPDATE books SET location = ? WHERE serial = ?''',(new_location, serial))
                    conn.commit()
                    print("\nLocation updated successfully\n")
                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    books = c.fetchall()
                    for book in books:
                        print("\nTitle:",book[0])
                        print("Author:",book[1])
                        print("Genre:",book[2])
                        print("Location:",book[3])
                    
                    break
                elif edit_choice == "5":
                    break
                else:
                    print("\nPlease enter a valid choice.\n")
        else:
            print("\nBook not found in the library")
       
    else:

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
                    while True:
                        new_title = input("\nEnter the new Title of the book: ")
                        if new_title != "":
                            break
                        else:
                            print("\nPlease enter a valid title.")

                    c.execute('''UPDATE books SET title = ? WHERE title LIKE ?''',(new_title, pattern))
                    conn.commit()
                    print("\nTitle updated successfully\n")

                    c.execute("SELECT * FROM books WHERE title = :title", {'title': new_title})
                    conn.commit()
                    books = c.fetchall()
                    for book in books:
                        print("\nSerial:",book[0])
                        print("Title:",book[1])
                        print("Author:",book[2])
                        print("Genre:",book[3])
                        print("Location:",book[4])
                    break

                elif edit_choice == "2":
                    while True:
                        new_author = input("\nEnter the new Author of the book: ")
                        if new_author != "":
                            break
                        else:
                            print("\nPlease enter a valid author.")

                    c.execute('''UPDATE books SET author = ? WHERE author LIKE ?''',(new_author, pattern))
                    conn.commit()
                    print("\nAuthor updated successfully\n")
                    
                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    conn.commit()
                    books = c.fetchall()
                    for book in books:
                        print("\nSerial:",book[0])
                        print("Title:",book[1])
                        print("Author:",book[2])
                        print("Genre:",book[3])
                        print("Location:",book[4])
                    break

                elif edit_choice == "3":
                    while True:
                        new_genre = input("\nEnter the new Genre of the book: ")
                        if new_genre != "":
                            break
                        else:
                            print("\nPlease enter a valid genre.")

                    c.execute('''UPDATE books SET genre = ? WHERE genre LIKE ?''',(new_genre, pattern))
                    conn.commit()
                    print("\nGenre updated successfully\n")

                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    conn.commit()
                    books = c.fetchall()
                    for book in books:
                        print("\nSerial:",book[0])
                        print("Title:",book[1])
                        print("Author:",book[2])
                        print("Genre:",book[3])
                        print("Location:",book[4])
                    break

                elif edit_choice == "4":
                    while True:
                        new_location = input("\nEnter the new Location of the book: ")
                        if new_location != "":
                            break
                        else:
                            print("\nPlease enter a valid location.")

                    c.execute('''UPDATE books SET location = ? WHERE location LIKE ?''',(new_location, pattern))
                    conn.commit()
                    print("\nLocation updated successfully\n")

                    c.execute("SELECT * FROM books WHERE title = :title", {'title': title})
                    conn.commit()
                    books = c.fetchall()
                    for book in books:
                        print("\nSerial:",book[0])
                        print("Title:",book[1])
                        print("Author:",book[2])
                        print("Genre:",book[3])
                        print("Location:",book[4])
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
    c.execute("DROP TABLE books")
    conn.commit()
    print("\nTable deleted successfully\n")
    c.execute("""CREATE TABLE IF NOT EXISTS books (
            serial INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            location TEXT
    )""")
    conn.commit()

def main():
    while True:
        print("\n" + " " * 10 + "Library Management Tool" + " " * 10 + "\n")
        print("1. Add a new Book")
        print("2. View all Books")
        print("3. Search for a Book")
        print("4. Delete a Book")
        print("5. Update a Book")
        print("6. Total Books")
        print("7. Exit\n")

        choice = input("Enter your choice: ")
        counter = 1
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
            print("\nExiting...")
            print("Thank you for using Library Management Tool\n")
            break
        elif choice == "8":
            delete_table()
        elif choice == "":
            print("\nPlease enter a valid choice.")
        else:
            print("\nPlease enter a valid choice.")

main()

conn.close()



