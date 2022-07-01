# import models
# main menu - add, search, analysis, exit, view
# 
# add books to db
# edit books
# search books
# data cleaning
# loop that runs program
#

from models import (Base, session, Book, engine)



if __name__ == '__main__':
    Base.metadata.create_all(engine)