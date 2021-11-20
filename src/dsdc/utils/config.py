import logging
import re


class Config:
    """ Config class """
    instance = {'initialized': False}

    @staticmethod
    def init(parser=None):
        """ Get singleton instance of Config """
        if Config.instance['initialized']:
            return Config.instance
        args = parser.parse_args()
        config = {
            'logLevel': args.log_level if "log_level" in args and args.log_level is not None else 'INFO',
            'outputPath': args.output_path if "output_path" in args and args.output_path is not None else None,
            'tag': args.tag if "tag" in args is not None and args.tag is not None else None,
            'regexp': args.regexp if "regexp" in args is not None and args.regexp is not None else None,
            'initialized': True
        }
        logging.basicConfig(level=config['logLevel'],
                            format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
        Config.instance = config
        return Config.instance

    @staticmethod
    def output_path():
        """ Getter """
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
        if Config.instance['regexp'] is None:
            return None
        return re.compile(Config.instance['regexp'])
