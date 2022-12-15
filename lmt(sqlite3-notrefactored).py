
import datetime
import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('bookshelf.db')
c = conn.cursor()
date_time = datetime.datetime.now()

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
    
    c.execute("INSERT INTO books VALUES (:serial, :title, :author, :genre, :location, :added_on, :last_updated_on)",
              {   'serial': counter,
                  'title': title,
                  'author': author,
                  'genre': genre,
                  'location': location,
                  'added_on': date_time,
                  'last_updated_on': None
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
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
    if books[0][0] == 0:
        print("\nThere are no books in the library.")
    else:    
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
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
    if books[0][0] == 0:
        print("\nThere are no books in the library.")
    else:   
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
                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET title = ?, last_updated_on = ? WHERE serial = ?''',(new_title, update_details ,serial))
                        conn.commit()
                        print("\nTitle updated successfully\n")
                        c.execute("SELECT * FROM books WHERE title = :title", {'title': new_title})
                        conn.commit()
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
                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET author = ?, last_updated_on = ? WHERE serial = ?''',(new_author, update_details ,serial))
                        conn.commit()
                        print("\nAuthor updated successfully\n")
                        c.execute("SELECT * FROM books WHERE author = :author", {'author': new_author})
                        conn.commit()
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
                        date_time_str = str(date_time)
                        update_details = "The genre of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET genre = ?, last_updated_on = ? WHERE serial = ?''',(new_genre, update_details ,serial))
                        conn.commit()
                        print("\nGenre updated successfully\n")
                        c.execute("SELECT * FROM books WHERE genre = :genre", {'genre': new_genre})
                        conn.commit()
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
                        date_time_str = str(date_time)
                        update_details = "The location of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET location = ?, last_updated_on = ? WHERE serial = ?''',(new_location, date_time ,serial))
                        conn.commit()
                        print("\nLocation updated successfully\n")
                        c.execute("SELECT * FROM books WHERE location = :location", {'location': new_location})
                        conn.commit()
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

                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET title = ?, last_updated_on = ? WHERE serial = ?''',(new_title, update_details ,serial))
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

                        date_time_str = str(date_time)
                        update_details = "The author of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET author = ?, last_updated_on = ? WHERE serial = ?''',(new_author, update_details ,serial))
                        conn.commit()
                        print("\nAuthor updated successfully\n")
                        
                        c.execute("SELECT * FROM books WHERE author = :author", {'author': new_author})
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

                        date_time_str = str(date_time)
                        update_details = "The genre of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET genre = ?, last_updated_on = ? WHERE serial = ?''',(new_genre, update_details ,serial))
                        conn.commit()
                        print("\nGenre updated successfully\n")

                        c.execute("SELECT * FROM books WHERE genre = :genre", {'genre': new_genre})
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

                        date_time_str = str(date_time)
                        update_details = "The location of the book was last updated on" + " " + date_time_str
                        c.execute('''UPDATE books SET location = ?, last_updated_on = ? WHERE serial = ?''',(new_location, update_details ,serial))
                        conn.commit()
                        print("\nLocation updated successfully\n")

                        c.execute("SELECT * FROM books WHERE location = :location", {'location': new_location})
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
            print("\nAre you sure you want to delete the table?(yes)/(no):")
            delete_table_choice = input()
            while True:
                if delete_table_choice == "yes":
                    delete_table()
                    while True:
                        create_new_table = input("Do you want to create a new table with same columns as of previous table:(yes)/(no):\n")
                        if create_new_table == "yes":
                            create_table()
                            print("\nNew table with same columns as of previous table was created successfully\n")
                            break
                        elif create_new_table == "no":
                            break
                        else:
                            print("\nPlease enter a valid choice.")
                            break
                    break
                elif delete_table_choice == "no":
                    break
                else:
                    print("\nPlease enter a valid choice.")
                    delete_table_choice = input()

        elif choice == "":
            print("\nPlease enter a valid choice.")
        else:
            print("\nPlease enter a valid choice.")

main()

conn.close()

