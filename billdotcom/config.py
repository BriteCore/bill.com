"""Global definitions, configuration and logging.

Defines:
    LOG (Logger): a logger that will record INFO or higher messages in a file and everything else to console.

    CONFIG (ConfigParser): the global config file for your Bill.com information.
"""

import logging
import logging.handlers
import os
import ConfigParser

LOGDIR = 'log'
LOGFILE = os.path.join(LOGDIR, 'billdotcom.log')
CONFIGFILE = os.path.abspath('billdotcom.cfg')


LOG = logging.getLogger("billdotcom")
LOG.setLevel(logging.DEBUG)

# set up log format
LOG_FILE_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_CONSOLE_FORMAT = '%(levelname)-8s %(message)s'

# create log directory (if needed)
if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

# add handler for file logging (info or greater)
logfile = logging.handlers.TimedRotatingFileHandler(LOGFILE, when='midnight', backupCount=30)
logfile.setLevel(logging.INFO)
logfile.setFormatter(logging.Formatter(LOG_FILE_FORMAT))
LOG.addHandler(logfile)

# add handler for stderr logging (debug or greater)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter(LOG_CONSOLE_FORMAT))
LOG.addHandler(console)

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(CONFIGFILE)

class ConfigurationError(Exception):
    """An exception raised when the configuration is incorrect."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

def validate_config():
    """Ensure that the required sections exist in the config file.

    Raises:
        ConfigurationError
    """
    try: # read and validate configuration
        CONFIG.get('authentication', 'appkey')
        CONFIG.get('authentication', 'email')
        CONFIG.get('authentication', 'password')

    except ConfigParser.Error as e:
        message = 'configuration in {0} is not correct: {1:s}'.format(CONFIGFILE, e)
        LOG.critical(message)
        raise ConfigurationError(message)

