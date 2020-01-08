===
iry
===

``iry`` is a CLI (command line interface) and a tool for tracking
incoming money transfers.


Installation
============

``iry`` works with Python 3.6+ and is installed using ``flit`` package
manager. To install ``iry``, it is recommended  that you set up a
`virtual environment`_. Install ``flit``, from the terminal, by typing::

$ pip3 install flit

.. _virtual environment: https://docs.python.org/3/tutorial/venv.html

Make sure your working directory is inside the repository and type::

$ flit install

After a successful installation typing ``iry`` in the terminal returns:

::

  Usage: iry [OPTIONS] COMMAND [ARGS]...

  Options:
    -V, --version       Show the version and exit.
    -p, --pklfile TEXT  select pickle file
    -c, --cfgfile TEXT  select configuration file
    --help              Show this message and exit.

  Commands:
    add
    show


Data
====

By default, there are 5 fields that ``iry`` tracks:

#. Date - date when the transaction was made
#. Name - name of the person who made the transaction
#. Amount - amount of money that was transfered
#. Origin - form in which the transaction was made (e.g., bank transfer,
   cash, etc.)
#. Currency - currency of the "Amount"

Additional fields can be added in ``src/iry/config.py``.

Data is stored in a pickle file and every time an action is issued the
pickle file is used. By default, the data is stored in a file called
``valut.pkl`` located inside the current working directory. However, if
``./valut.pkl`` doesn't exist ``iry`` looks at the user data directory
which depends on the OS (e.g., for Ubuntu 18 this is
``/home/user/.local/share/iry``). Paths to pickle files can also be
`specified manually`_.


Usage
=====

Whenever feeling confused type ``iry --help`` for helpful documentation.
Two main subcommands are ``add`` and ``show``. The first subcommand
stores data and the second previews it.

To create and save a record use ``iry add --no-defaults``. This prompts
you about the data that you want to save. To save several records in the
same time use ``-q`` option. Instead of filling in the "Date" filed use
``iry add --no-defaults --now`` and ``iry`` will automatically fill it
with the current date and time. Defaults values for other fields can be
set in ``src\iry\config.py``. This is useful, for example, if you want
to set value of "Currency" to a default currency so that you don't have
to enter it every time manually. Use ``--default`` option to fill data
with default values (this option is also the default behaviour of the
CLI).

To preview the data use ``iry show`` which shows all the data. To select
fields for previewing use ``iry show -f Name -f Date -f Amount`` to show
any combination of data fields (in this case fields "Name", "Date" and
"Amount" in that particular order).

.. _specified manually:

To manually specify a pickle file path use ``iry -p file_locatoin`` with
a following subcommand.

FAQs
====

Why does ``iry`` keep data in a pickle (.pkl) file?

In Python, pickle file (.pkl) preforms quite fast for operations such as
reading and writing. Additionally, .pkl is a binary file and for
security reasons it is better to keep sensitive data in binary format
than in ASCII. Main drawback of pickle file is that it is not
cross-platform compatible. This will, howerver, be solved once ``iry``
is able to export to .csv, .json or .yaml is implemented.

License
=======

The code is shared under the terms of Apache License 2.0.
