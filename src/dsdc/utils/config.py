import logging
import sys
from os.path import exists

from envyaml import EnvYAML


class Config:
    """ Config class """
    instance: dict[str, str] = None

    @staticmethod
    def init(parser=None):
        """ Get singleton instance of Config """
        if Config.instance is not None:
            return Config.instance
        args = parser.parse_args()
        config = {
            'logLevel': args.log_level,
            'outputPath': "output.txt"
        }
        if args.configuration_file is not None and exists(args.configuration_file):
            try:
                env = EnvYAML(args.configuration_file)
                if bool(env['logLevel']):
                    config['logLevel'] = env['logLevel']
                if bool(env['outputPath']):
                    config['outputPath'] = env['outputPath']
            except FileNotFoundError:
                logging.error("DB configuration error: configuration file cannot be found. Exiting!")
                sys.exit()
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
        return Config.instance['logLevel']
