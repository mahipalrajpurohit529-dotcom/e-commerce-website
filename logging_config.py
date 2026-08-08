"""
Centralized logging configuration for LuxeThreads.

Logs go to both the console (for local dev) and a rotating file under logs/app.log
(for anything that needs to persist — useful once we're debugging webhook
failures, payment callbacks, and retry logic later in the sprint).
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'app.log')

    log_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    app.logger.info('Logging configured — writing to %s', log_path)
    return app.logger