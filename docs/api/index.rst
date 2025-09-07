.. JDINBot documentation master file

JDINBot Documentation
=====================

Welcome to the JDINBot documentation. This project is a high-performance Telegram bot built with Aiogram 3.x, FastAPI, and async PostgreSQL, designed for scalability and maintainability. This documentation covers the Telegram bot commands, REST API endpoints, development setup, and architecture.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   development
   deployment
   architecture
   api/index

Bot Commands
============

The following Telegram bot commands are available in the current release (M1 milestone). Additional commands (e.g., ``/transfer``, ``/promote``, ``/ban``) are planned for the M2 milestone.

.. _start_command:

``/start``
---------

Sends a welcome message to the user, introducing JDINBot and suggesting next steps.

**Usage**: ``/start``

**Response**:

.. code-block:: text

    Welcome to JDINBot! 🎉
    Try /balance to check your balance or /help for more commands.

**Example**:

.. code-block:: text

    User: /start
    Bot: Welcome to JDINBot! 🎉
         Try /balance to check your balance or /help for more commands.

.. _balance_command:

``/balance``
-----------

Displays the user's current balance.

**Usage**: ``/balance``

**Response**:

.. code-block:: text

    Your current balance is 0.

**Example**:

.. code-block:: text

    User: /balance
    Bot: Your current balance is 0.

API Documentation
=================

.. toctree::
   :maxdepth: 2
   :caption: API Endpoints:

   api/health

The REST API endpoints are under development and will be fully implemented in the M2 milestone. The ``/health`` endpoint is currently available for basic API status checks.