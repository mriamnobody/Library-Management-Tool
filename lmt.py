import mysql.connector

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
    print("\nWelcome to the Library Management Tool. Please select an option: ")
    print("\n1. Add a book")
    print("2. Search for a book")
    print("3. Delete a book")
    print("4. Exit\n")
    choice = input("Enter your choice: ")

    if choice == "1":
        book_details = []

        for i in range(1):
            title = input("Enter the Title of the book: ")
            author = input("Enter the Author of the book: ")
            genre = input("Enter the Genre of the book: ")
            location = input("Enter the Location of the book: ")
        
        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        if myresult != []:
            print("\nBook already exists in the library")
            continue
        else:
            book_details.append((title, author, genre, location))
            mycursor.executemany("INSERT INTO books (title, author, genre, location) VALUES (%s, %s, %s, %s)", book_details)
            mydb.commit()
            print("\nBook successfully added to the library.")

    elif choice == "2":
        title = input("Enter the Title of the book: ")
        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))  
        myresult = mycursor.fetchall()

        if myresult == []:
            print("\nBook not found in the library")
            continue
        else:
            for x in myresult:
                print(x)

    elif choice == "3":
        title = input("Enter the Title of the book: ")
        mycursor.execute("SELECT * FROM books WHERE title = %s", (title,))
        myresult = mycursor.fetchall()
        if myresult == []:
            print("\nBook not found in the library")
            continue
        else:
            mycursor.execute("DELETE FROM books WHERE title = %s", (title,))
            mydb.commit()
            print(mycursor.rowcount, "\nBook {title} successfully deleted from the library.\n")

    elif choice == "4":
        print ("\nThank you for using the Library Management Tool.\n")
        break

    else:
        print("\nInvalid choice")
