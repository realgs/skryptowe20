import argparse

from app.app import run


def parse_args():
    parser = argparse.ArgumentParser(
        description="Server that provides an API for accessing PLN to USD daily "
        "exchange rates and daily bike store sales in both PLN and USD currencies.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=3000,
        help="Choose the port on which the server will run.",
    )

    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update all rates and sales in the database before starting the server "
        "by using the NBP API.",
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Run Flask in debug mode."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args)
