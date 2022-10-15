import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils import logger

my_logger = logger.get_logger()


def main():
    my_logger.info("Cleaning up...")


if __name__ == "__main__":
    main()
