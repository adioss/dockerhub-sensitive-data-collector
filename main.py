import argparse
import logging


def main():
    """ main """
    parser = argparse.ArgumentParser(description='HERE ADD THE DESCRIPTION')
    parser.add_argument('--configuration-file', type=int, required=True, help='Configuration file')
    parser.add_argument("--log-level", default=logging.INFO, type=lambda x: getattr(logging, x),
                        help="Configure the logging level.")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)


if __name__ == '__main__':
    main()
