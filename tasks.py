# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import logging
from celery import Task

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.conf import settings
from django.db import transaction

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from config.celery import app


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ LOGGED TASK HANDLER                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘


class LoggedTaskHandler(Task):
    """ A log-endabled TaskHandler """

    # Initialize logger
    logger = logging.getLogger("django.request")

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ON FAILURE                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """ Handles and logs failed Celery tasks """

        # Log exception
        self.logger.exception("Celery Task Failure", exc_info=exc)

        # Call parent on failure
        super().on_failure(exc, task_id, args, kwargs, einfo)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ ON-COMMIT TASK HANDLER                                                             │
# └────────────────────────────────────────────────────────────────────────────────────┘


class OnCommitTaskHandler(Task):
    """ An on-commit enabled TaskHandler """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ APPLY ASYNC                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def apply_async(self, *args, **kwargs):
        """
        Only executes tasks after transaction has been committed.
        Unlike the default Celery task, this task does not return an async result.
        See https://docs.djangoproject.com/en/2.1/topics/db/transactions/#performing-
        actions-after-commit
        See http://docs.celeryproject.org/en/latest/userguide/tasks.html#database-
        transactions
        """

        # Wrap method in an on commit handler
        transaction.on_commit(
            lambda: super(OnCommitTaskHandler, self).apply_async(*args, **kwargs)
        )


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ LOGGED ON-COMMIT TASK HANDLER                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘


class LoggedOnCommitTaskHandler(LoggedTaskHandler, OnCommitTaskHandler):
    """ An on-commit enabled TaskHandler """


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BACKGROUND TASK                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


def background_task(func, *args, **kwargs):
    """ A custom decorator for Celery background tasks """

    # Handle case of Celery on-commit
    if settings.ENABLE_CELERY_ON_COMMIT:
        task_handler = (
            LoggedOnCommitTaskHandler
            if settings.ENABLE_CELERY_LOGGING
            else OnCommitTaskHandler
        )

    # Otherwise handle case of enabled Celery logging
    elif settings.ENABLE_CELERY_LOGGING:
        task_handler = LoggedTaskHandler

    # Otherwise use vanilla Celery task
    else:
        task_handler = Task

    # Return async task
    return app.task(func, *args, base=task_handler, **kwargs)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PERIODIC TASK                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘


def periodic_task(func, *args, **kwargs):
    """ A custom decorator for periodic tasks """

    # Handle case of enabled Celery logging
    if settings.ENABLE_CELERY_LOGGING:
        task_handler = LoggedTaskHandler

    # Otherwise handle disabled logging
    else:
        task_handler = Task

    # Return the async task
    return app.task(func, *args, base=task_handler, **kwargs)
