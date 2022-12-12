import mysql.connector
from colorama import init
from termcolor import colored

init()

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
    print(colored("\nWelcome to the Library Management Tool. Please select an option: "))
    print(colored("\n1. Add a book"))
    print(colored("2. Search for a book"))
    print(colored("3. Delete a book"))
    print(colored("4. Exit\n"))
    choice = input("Enter your choice: ")

    if choice == "1":
        book_details = []

        for i in range(1):
            title = input("Enter the Title of the book: ")
            mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
            myresult = mycursor.fetchall()
            if myresult != []:
                print("\nBook already exists in the library")
                continue
            else:
                author = input("Enter the Author of the book: ")
                genre = input("Enter the Genre of the book: ")
                location = input("Enter the Location of the book: ")
                book_details.append((title, author, genre, location))
                mycursor.executemany("INSERT INTO books (title, author, genre, location) VALUES (%s, %s, %s, %s)", book_details)
                mydb.commit()
                print(colored("\nBook successfully added to the library."))
        
    elif choice == "2":
        title = input("Enter the Title of the book: ")
        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))  
        myresult = mycursor.fetchall()

        if myresult == []:
            print(colored("\nBook not found in the library."))
            continue
        else:
            print(colored("\nBook found in the library.\n"))
            for x in myresult:
                print("Book Name:", x[1])
                print("Book Author:", x[2])
                print("Book Genre:", x[3])
                print("Book Location:", x[4], "\n")

    elif choice == "3":
        title = input("Enter the Title of the book: ")

        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        if myresult == []:
            print(colored("\nBook not found in the library"))
            continue
        else:
            confirmation = input("Are you sure you want to delete the book? (y/n)")

            if confirmation == "y":
                mycursor.execute("DELETE FROM books WHERE title = %s", (title,))
                mydb.commit()
                print(colored("\nBook successfully deleted from the library.\n"))
            else:
                print(colored("\nOperation cancelled.\n"))

    elif choice == "4":
        print ("\nThank you for using the Library Management Tool.\n")
        break

    else:
        print("\nInvalid choice")
