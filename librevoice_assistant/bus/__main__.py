from mycroft.messagebus.load_config import load_message_bus_config
from mycroft.messagebus.service.event_handler import MessageBusEventHandler
from ovos_utils import create_daemon, wait_for_exit_signal
from ovos_utils.log import LOG, init_service_logger
from ovos_utils.process_utils import reset_sigint_handler, PIDLock
from tornado import web, ioloop

from librevoice_assistant.config import init_config_dir


def on_ready():
    LOG.info('Message bus service started!')


def on_error(e='Unknown'):
    LOG.info('Message bus failed to start ({})'.format(repr(e)))


def on_stopping():
    LOG.info('Message bus is shutting down...')


def main(ready_hook=on_ready, error_hook=on_error, stopping_hook=on_stopping):
    PIDLock("BUS")
    init_config_dir()
    init_service_logger("bus")
    LOG.info('Starting message bus service...')
    reset_sigint_handler()
    config = load_message_bus_config()
    routes = [(config.route, MessageBusEventHandler)]
    application = web.Application(routes)
    application.listen(config.port, config.host)
    create_daemon(ioloop.IOLoop.instance().start)
    ready_hook()
    wait_for_exit_signal()
    stopping_hook()


if __name__ == "__main__":
    main()
