"""Global definitions, configuration and logging.

The default configuration file must contain the following structure:
 * authorization
    * appkey: the application key from Bill.com
    * email: your user's email address
    * password: your user's password
 * organization
    * name: the name of your organization
    * id: the id for your organization. Obtain with the `billdotcom_getorglist` script.

.. note::
    The environment variable BILLDOTCOM_PREFIX can be used to control the location of
    the config file and logging directory. If it does not exist the current directory
    will be used.

"""

import logging
import logging.handlers
import os
import ConfigParser

from exceptions import ConfigurationError

API_URL = 'https://api.bill.com/crudApi'

ROOT = os.environ.get('BILLDOTCOM_PREFIX', os.getcwd())

LOGDIR = os.path.join(ROOT, 'log')
LOGFILE = os.path.join(LOGDIR, 'billdotcom.log')
CONFIGFILE = os.path.join(ROOT, 'billdotcom.cfg')

def get_logger():
    """Gets the global logger and configures it if needed.

    The default handlers will write DEBUG or higher to STDERR and log INFO or higher
    to the default log file. See :mod:`billdotcom.config` for more about how to change this.

    Example usage:
        >>> LOG = get_logger()
        >>> LOG.error("look, an error!")

    Returns:
        Logger.
    """

    log = logging.getLogger("billdotcom")
    log.setLevel(logging.DEBUG)

    # set up log format
    LOG_FILE_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    LOG_CONSOLE_FORMAT = '%(levelname)-8s %(message)s'

    # create log directory (if needed)
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)

    if not log.handlers:
        # add handler for file logging (info or greater)
        logfile = logging.handlers.TimedRotatingFileHandler(LOGFILE, when='midnight', backupCount=30)
        logfile.setLevel(logging.INFO)
        logfile.setFormatter(logging.Formatter(LOG_FILE_FORMAT))
        log.addHandler(logfile)

        # add handler for stderr logging (debug or greater)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(LOG_CONSOLE_FORMAT))
        log.addHandler(console)

    return log

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(CONFIGFILE)

def validate_config():
    """Ensure that the required sections exist in the config file.

    For proper configuration and more about the default location, see :mod:`billdotcom.config`.

    Raises:
        ConfigurationError
    """

    LOG = get_logger()

    try: # read and validate configuration
        CONFIG.get('authentication', 'appkey')
        CONFIG.get('authentication', 'email')
        CONFIG.get('authentication', 'password')

    except ConfigParser.Error as e:
        message = 'configuration in {0} is not correct: {1:s}'.format(CONFIGFILE, e)
        LOG.critical(message)
        raise ConfigurationError(message)

