# /usr/bin/python

# main controller
# Louis
# 02/03/2017

# import
from settings import settings
from frontend import frontend
from util import utils
import itchat
import argparse  # Command line parsing

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


@staticmethod
def parse_args(args):
    """
    Parse the arguments from the given command line
    Args:
        args (list<str>): List of arguments to parse. If None, the default sys.argv will be parsed
    """
    parser = argparse.ArgumentParser()

    # Misc options
    misc_args = parser.add_argument_group('Misc options')
    misc_args.add_argument('--debug', '-d', default=False, help='debug mode, will output debug info')

# call main
if __name__ == "__main__":
    main()
