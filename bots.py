# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from queue import Queue
from threading import Thread

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TELEGRAM IMPORTS                                                                   │
# └────────────────────────────────────────────────────────────────────────────────────┘

from telegram import Bot, Update
from telegram.ext import Dispatcher


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BASE BOT                                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class BaseBot:
    """ A base bot """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ENTER METHOD                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __enter__(self):
        """ Enter Method """
        return self

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EXIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __exit__(self, *args, **kwargs):
        """ Exit Method """

        # Close the adapter
        self.close()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ PROCESS WEBHOOK                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def process_webhook(self, data):
        """ Processes data passed in via webhook """

        raise NotImplementedError


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TELEGRAM BOT                                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘


class TelegramBot(BaseBot):
    """ A class for Telegram bots """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(self, api_key, *args, should_thread=False, **kwargs):
        """ Custom Init Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PARENT INIT METHOD                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Call parent init method
        super().__init__(*args, **kwargs)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ BOT INSTANCE                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize bot instance
        bot = Bot(token=api_key)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ UPDATE QUEUE                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if should thread is True
        if should_thread is True:

            # Initialize update queue
            update_queue = Queue() if should_thread else None

            # Initialize dispatcher
            dispatcher = Dispatcher(bot, update_queue)

        # Otherwise handle case of no threading
        else:

            # Initialize update queue to None
            update_queue = None

            # Initialize dispatcher
            dispatcher = Dispatcher(bot, None, workers=0)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HANDLERS                                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ START THREAD                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        if should_thread is True:

            # Start the thread
            thread = Thread(target=dispatcher.start, name="dispatcher")
            thread.start()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SET INSTANCE ATTRIBUTES                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set bot, dispatcher, and update queue
        self.bot = bot
        self.dispatcher = dispatcher
        self.update_queue = update_queue

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ PROCESS WEBHOOK                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def process_webhook(self, data):
        """ Processes data passed in via webhook """

        # Decode data into Update object
        update = Update.de_json(data, self.bot)

        # Pass update into queue or dispatcher
        self.update_queue.put(
            update
        ) if self.update_queue else self.dispatcher.process_update(update)
