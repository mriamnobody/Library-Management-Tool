# Library-Management-Tool
Library Management Tool

Using this tool you can manage your Library (Personal Physical Library) smoothly. I have a mini library at my home. It has a variety of Genres. When I first arranged the books in the Library it was easy to remember the location of the books which I mostly read but later it became a nightmare. I tried arranging the books by their genre but the issue was I had alot of different genres plus the books I have are of various sizes. This made it look awful. Thats why I have created this tool.

As of now, this tool has following features:

1. Add book details

    When a user selects this option the tool will ask four things. Title, Author, Genre and the location where you have kept the book in the library.

2. View all books

3. Search for a book

4. Delete a book

5. Print the total number of books in library

6. Delete all books at once

Prerequesites:

1. Python 3.7 or above
2. Mysql

There are three python files. 
  1. lmt_mysql.py - This needs Mysql to work
  2. lmt_sqlite3_refactored.py - This file doesn't require any external database, instead it works with builtin Sqlite3 database. Code of this file is refactored. 
  3. lmt_sqlite3_notrefactored.py - This file doesn't require any external database, instead it works with builtin Sqlite3 database. The code of this file not refactored but has imporved logic over the refactored sqlite3.py file. (Refactoring will not affect the logic of the program)
A lot of work is needed at the time of writing this readme. As of now the tool works through CLI. I will try to build a GUI app for this tool soon.

![](https://komarev.com/ghpvc/?username=mriamnobody&label=Total+Visitors)
