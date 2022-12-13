import mysql.connector
from tabulate import tabulate

query = """
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(255),
    location VARCHAR(255)
)
"""
mydb = mysql.connector.connect( host="localhost", user="root", password="")
mycursor = mydb.cursor()  
mycursor.execute("USE librarymanagement")

mycursor.execute("SELECT DATABASE()")
myresult = mycursor.fetchone()

mycursor.execute("SHOW TABLES LIKE 'books'")

if mycursor.fetchone() is None:
    mycursor.execute(query)
    mydb.commit()
else:
    pass

while True:
    book_details = []
    myresult = []

    print("\nWelcome to the Library Management Tool. Please select an option: ")
    print("\n1. Add a book")
    print("2. Search for a book")
    print("3. Delete a book")
    print("4. Edit a book details")
    print("5. Print the list of books in the library")
    print("6. Print the total number of books in the library")
    print("7. Exit\n")

    choice = input("Enter your choice: ")

    if choice == "1":
        for i in range(1):
            
            while True:
                title = input("\nEnter the Title of the book: ")
                if title != "":
                    break
                else:
                    print("\nPlease enter a valid title.")

            mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
            myresult = mycursor.fetchall()
            if myresult != [] :
                print("\nBook already exists in the library")
                continue
            
            else:
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

                book_details.append((title, author, genre, location))
                mycursor.executemany("INSERT INTO books (title, author, genre, location) VALUES (%s, %s, %s, %s)", book_details)
                mydb.commit()
                print("\nBook successfully added to the library.")

    elif choice == "2":
        while True:
            title = input("\nEnter the Title of the book: ")
            if title != "":
                break
            else:
                print("\nPlease enter a valid title.")

        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        print(type(myresult))

        if myresult == []:
            print("\nBook not found in the library.")

        else:
            query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
            mycursor.execute(query)

            for entry in mycursor:
                print("\nBook Name:", entry[1])
                print("Book Author:", entry[2])
                print("Book Genre:", entry[3])
                print("Book Location:", entry[4], "\n")

    elif choice == "3":
        while True:
            title = input("\nEnter the Title of the book: ")
            if title != "":
                break
            else:
                print("\nPlease enter a valid title.")

        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        if myresult == []:
            print("\nBook not found in the library")
            continue
        else:
            confirmation = input("Are you sure you want to delete the book? (y/n)")

            if confirmation == "y":
                mycursor.execute("DELETE FROM books WHERE title = %s", (title,))
                mydb.commit()
                print("\nBook successfully deleted from the library. Total number of books deleted:\n", mycursor.rowcount)

            else:
                print("\nOperation cancelled.\n")

    elif choice == "4":
        while True:
            title = input("\nEnter the Title of the book: ")
            if title != "":
                break
            else:
                print("\nPlease enter a valid title.")

        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        
        if myresult == []:
            print("\nBook not found in the library")
            continue
        else:
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

                    mycursor.execute("UPDATE books SET title = %s WHERE title = %s", (new_title, title))
                    mydb.commit()
                    print("\nBook title successfully updated.")

                elif edit_choice == "2":
                    while True:
                        new_author = input("\nEnter the new Author of the book: ")
                        if new_author != "":
                            break
                        else:
                            print("\nPlease enter a valid author.")

                    mycursor.execute("UPDATE books SET author = %s WHERE title = %s", (new_author, title))
                    mydb.commit()
                    print("\nBook author successfully updated.")

                elif edit_choice == "3":
                    while True:
                        new_genre = input("\nEnter the new Genre of the book: ")
                        if new_genre != "":
                            break
                        else:
                            print("\nPlease enter a valid genre.")

                    mycursor.execute("UPDATE books SET genre = %s WHERE title = %s", (new_genre, title))
                    mydb.commit()
                    print("\nBook genre successfully updated.")

                elif edit_choice == "4":
                    while True:
                        new_location = input("\nEnter the new Location of the book: ")
                        if new_location != "":
                            break
                        else:
                            print("\nPlease enter a valid location.")

                    mycursor.execute("UPDATE books SET location = %s WHERE title = %s", (new_location, title))
                    mydb.commit()
                    print("\nBook location successfully updated.")

                elif edit_choice == "5":
                    print("\nOperation cancelled.\n")
                    break

    elif choice == "5":
        mycursor.execute("SELECT * FROM books")
        myresult = mycursor.fetchall()

        for i in range(len(myresult)):
            myresult[i] = list(myresult[i])
            myresult[i][0] = i + 1
            myresult[i] = tuple(myresult[i])

        print(tabulate(myresult, headers=["Sr","Title", "Author", "Genre", "Location"], tablefmt="grid"))

    elif choice == "6":
        mycursor.execute("SELECT COUNT(*) FROM books")
        myresult = mycursor.fetchone()
        print("\nTotal number of books in the library: ", myresult[0])

    elif choice == "7":
        print("\nThank you for using the Library Management Tool. Goodbye!")
        break



