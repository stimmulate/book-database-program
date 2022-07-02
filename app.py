# import models
# main menu - add, search, analysis, exit, view
# 
# add books to db
# edit books
# search books
# data cleaning
# loop that runs program
#

from ast import Try
from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nPROGRAMMING BOOKS
            \r1)Add Book
            \r2)View All Books
            \r3)Search For Book
            \r4)Book Analysis
            \r5)Exit'''
        )
        choice = input('What would you like to do?  ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input ('''
                \rPlease choose an option from those listed above.
                \rA number 1-5.
                \rPress enter to try again.            
            ''')

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, date_published=date, price=price)
                session.add(new_book)
        session.commit()

def clean_date(date_str):

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR *******
            \rThe date should include a valid Month Day, Year from the past.
            \rEx: January 01, 2013
            \rPress Enter to try again.
            \r**************************''')
    else:
        return return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
            \n****** Price ERROR *******
            \rThe price should be a number without a currency symbol
            \rEx: 10.99
            \rPress Enter to try again.
            \r**************************''')
    else:
        return int(price_float * 100)

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
            \n****** ID ERROR *******
            \rThe id should be a number
            \rPress Enter to try again.
            \r**************************''')
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
            \n****** ID ERROR *******
            \rOption: {options}
            \rPress Enter to try again.
            \r**************************''')
            return

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # Add Book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.65): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, date_published=date, price=price)
            session.add(new_book)
            session.commit()
            print('The Book Was Added')
            time.sleep(1.5)        
        elif choice == '2':
            # View Books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.date_published} | {book.price}')
            input('\nPress enter to return to the menu!')    
            pass
        elif choice == '3':
            # Search For Book
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author} 
                \rPublished: {the_book.date_published}
                \rPrice: {the_book.price / 100}''')
            input('Press Enter to return to the menu!')
            pass
        elif choice == '4':
            # Book Analysis
            pass
        else:
            print('GOODBYE~!')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book):
    #     print(book)

