# Simple Autocompleter with tornado, redis and angularjs

# Requirements

* redis-server
* python3 && virtualenv

# Usage

    $ virtualenv -p python3 env
    $ ./env/bin/pip install -r requirements.txt
    $ ./autocomplete.py

Open browser on http://localhost:5000/ and type away.

# WARNING

The setup step deletes all redis keys in the "ac:" namespace.
