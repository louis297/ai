# /usr/bin/python

# main controller
# Louis
# 02/03/2017

# import
from settings import settings
from frontend import frontend
from util import utils
import itchat

from db import dbc
from algo import algo

# main
def main():
    if settings.debug:
        print('-'*10 + "DEBUG" + '-'*10)
        print(dbc.placeholder)
        print(algo.placeholder)
        print(utils.placeholder)

        itchat.run()
    pass


# call main
if __name__ == "__main__":
    main()
