import sqlite3
from tabulate import tabulate

conn = sqlite3.connect("bookshelf.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS books (
            serial INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            location TEXT
    )"""
)
conn.commit()


def ensure_input(input_prompt, invalid_prompt):
    while True:
        inp = input(input_prompt)
        if inp != "":
            return inp
        else:
            print(invalid_prompt)


def print_book_details(book):
    print("\nSerial:", book[0])
    print("Title:", book[1])
    print("Author:", book[2])
    print("Genre:", book[3])
    print("Location:", book[4])


def get_books_by_title(title):
    c.execute("SELECT * FROM books WHERE title = ?", (title,))
    books = c.fetchall()
    return books


def get_books_by_pattern(pattern):
    c.execute("SELECT * FROM books WHERE title LIKE ?", (pattern,))
    books = c.fetchall()
    return books


def get_book_by_serial(serial):
    c.execute("SELECT * FROM books WHERE serial = ?", (serial,))
    book = c.fetchall()
    return book


def update_book_by_serial(serial, column, value):
    c.execute(f"UPDATE books SET {column} = ? WHERE serial = ?", (value, serial))
    conn.commit()


def add_book():
    c.execute("SELECT serial FROM books ORDER BY serial DESC LIMIT 1")
    counter = c.fetchone()
    if counter == None:
        counter = 0
    else:
        counter = counter[0]
    counter = counter + 1

    title = ensure_input(
        "\nEnter the Title of the book: ", "\nPlease enter a valid title."
    )
    c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
    books = c.fetchall()
    if books != []:
        print("\nBook already exists in the library\n")
        return

    author = ensure_input(
        "\nEnter the Author of the book: ", "\nPlease enter a valid author."
    )
    genre = ensure_input(
        "\nEnter the Genre of the book: ", "\nPlease enter a valid genre."
    )
    location = ensure_input(
        "\nEnter the Location of the book: ", "\nPlease enter a valid location."
    )

    c.execute(
        "INSERT INTO books VALUES (:serial, :title, :author, :genre, :location)",
        {
            "serial": counter,
            "title": title,
            "author": author,
            "genre": genre,
            "location": location,
        },
    )
    conn.commit()

    c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
    books = c.fetchall()
    print("\nBook added successfully")
    for book in books:
        print_book_details(book)


def view_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    print(
        tabulate(
            books,
            headers=["Sr", "Title", "Author", "Genre", "Location"],
            tablefmt="grid",
        )
    )


def delete_book():
    title = ensure_input(
        "\nEnter the Title of the book: ", "\nPlease enter a valid title."
    )

    books = get_books_by_title(title)

    if books != []:
        c.execute("DELETE FROM books WHERE title = ?", title)
        print("\nBook deleted successfully\n")
        for book in books:
            print_book_details(book)
    else:
        print("\nBook not found\n")
    conn.commit()


def search_book():
    while True:
        title = input("\nEnter the Title of the book: ")
        if title != "":
            break
        else:
            print("\nPlease enter a valid title.")
    pattern = f"%{title}%"
    books = get_books_by_pattern(pattern)
    if books != []:
        print("\nBook found in the library")
        for book in books:
            print_book_details(book)
    else:
        print("\nBook not found in the library")


def update_book():

    title = ensure_input(
        "\nEnter the Title of the book: ", "\nPlease enter a valid title."
    )

    pattern = f"%{title}%"
    books = get_books_by_pattern(pattern)

    print(
        f"\nWe have found the following book{'s' if len(books) > 1 else ''} in the library:"
    )

    for book in books:
        print_book_details(book)
    # check how many books are there with the same title

    serial = None

    if len(books) > 1:
        serial = ensure_input(
            "\nEnter the serial number of the book which you want to edit:\n",
            "\nPlease enter a valid serial number.",
        )

        print(f"\nBook with Serial number {serial} and Title {title} will be edited:\n")
    elif len(books) == 1:
        serial = books[0][0]
    else:
        print("\nBook not found\n")
        return
    if serial:
        choices = [
            {
                "prompt": "title",
                "action": lambda value: update_book_by_serial(serial, "title", value),
            },
            {
                "prompt": "author",
                "action": lambda value: update_book_by_serial(serial, "author", value),
            },
            {
                "prompt": "genre",
                "action": lambda value: update_book_by_serial(serial, "genre", value),
            },
            {
                "prompt": "location",
                "action": lambda value: update_book_by_serial(serial, "location", value),
            },
            {
                "prompt": "cancel",
                "action": None,
            },
        ]
        while True:
            print("\nWhat would you like to edit?")
            for i, choice in enumerate(choices):
                print(f"{i + 1}. {choice['prompt'].capitalize()}")
            edit_choice = input("Enter your choice: ")
            if edit_choice.isnumeric() and int(edit_choice) >= 1 and int(edit_choice) <= len(choices):
                selected_choice = choices[int(edit_choice) - 1]
                if selected_choice["prompt"] == "cancel":
                    break
                value = ensure_input(f"\nEnter the new {selected_choice['prompt']} of the book: ", f"\nPlease enter a valid {selected_choice['prompt']}.")
                selected_choice["action"](value)
                print(f"{selected_choice['prompt']} updated successfully\n")
                break
            else:
                print("\nPlease enter a valid input.")


def total_books():
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchall()
    # count total entries in the table books under column title and print it out as an integer value
    print(f"There are total {books[0][0]} books in the library")


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

        elif choice == "":
            print("\nPlease enter a valid choice.")
        else:
            print("\nPlease enter a valid choice.")


main()

conn.close()
