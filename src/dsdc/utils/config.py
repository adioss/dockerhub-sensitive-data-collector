import logging
import re


class Config:
    """ Config class """
    instance: dict[str, any] = None

    @staticmethod
    def init(parser=None):
        """ Get singleton instance of Config """
        if Config.instance is not None:
            return Config.instance
        args = parser.parse_args()
        config = {
            'logLevel': args.log_level if "log_level" in args else 'INFO',
            'outputPath': args.output_path if "output_path" in args is not None else "output.txt",
            'tag': args.tag if "tag" in args is not None else None,
            'regexp': re.compile(
                args.regexp if "regexp" in args is not None else "") if "regexp" in args is not None else None
        }
        logging.basicConfig(level=config['logLevel'],
                            format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
        Config.instance = config
        return Config.instance

    @staticmethod
    def output_path():
        """ Getter """
        # pylint: disable=E1136
        return Config.instance['outputPath']

    @staticmethod
    def log_level():
        """ Getter """
        # pylint: disable=E1136
        return Config.instance['logLevel']

    @staticmethod
    def tag():
        """ Getter """
        # pylint: disable=E1136
        return Config.instance['tag']

    @staticmethod
    def regexp():
        """ Getter """
        # pylint: disable=E1136
        return Config.instance['regexp']
