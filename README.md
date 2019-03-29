# Ein Telegram Abrechnungsbot

For testing create new virtualenv and install requirements.

~~~bash
mkdir env
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
~~~

## Development

Start `python` and import `test`.
To reload the module:

~~~python
from importlib import reload
reload(test)
~~~

For automated unit-testing:

~~~bash
cd abrechnung
python -m unittest discover
~~~

## Build and run docker image

~~~bash
docker build -t abrechnung .
docker run abrechnung --name abrechnung
~~~

~~~bash
docker-compose build
docker-compose up -d
~~~

## Bot commands

Here are all commands listed.

 - `start`
    + This registers a new global group
    + This has to save the group id
 - `add_account [name]`
    + This command will add a new account with an empty balance
 - `add_event [cost] [payer] [participants]`
    + This command adds a new event and debits the accounts
 - `do_transaction [amount] [source] [destination]`
    + This command can be used if someone pays money to another member
 - `show_account_data`
    + This command will show the current account balances
 - `calculate_balancing`
    + This command will calculate the money transfers needed to balance the accounts
 - `do_balancing`
    + This command will calculate and print the transfer operations
    + Will reset all account balances to 0

## Telegram BotFather info

    start - start - Create or recreate group
    add_account - add_account [name] - Create new account for name
    add_event - add_event [amount] [payer] [remaining participants] - This will add a new event and debit the accounts
    do_transaction - do_transaction [amount] [source] [destination]
    show_account_data - show_account_data - This will print the current account data
    calculate_balancing - calculate_balancing - This will calculate the resulting transactions
