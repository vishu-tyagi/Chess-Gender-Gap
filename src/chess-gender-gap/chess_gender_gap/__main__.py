import sys
import logging

from chess_gender_gap.data_access import fetch

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


def main():
    try:
        if sys.argv[1] == "fetch":
            fetch()
        else:
            raise ValueError("Invalid endpoint")
    except IndexError:
        raise IndexError("Call to API requires an endpoint")
    except AttributeError:
        raise AttributeError("Required schema name")
    return


if __name__ == "__main__":
    main()