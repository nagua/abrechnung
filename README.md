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

## Build and run docker image

~~~bash
docker build -t abrechnung .
docker run abrechnung --name abrechnung
~~~

