import logging
import sys
from os.path import exists

from envyaml import EnvYAML


class Config:
    __instance = None
    __config = None

    @staticmethod
    def get_instance(parser=None):
        """ Get singleton instance of Config """
        if Config.__instance is not None:
            return Config.__instance
        Config.__instance = Config()
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
        Config.__instance.config = config
        return Config.__instance

    @staticmethod
    def output_path():
        return Config.__instance.config['outputPath']

    @staticmethod
    def log_level():
        return Config.__instance.config['logLevel']
