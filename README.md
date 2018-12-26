# DankFaceBot repo

[![Build Status](https://travis-ci.org/dixneuf19/dank-face-bot.svg?branch=service)](https://travis-ci.org/dixneuf19/dank-face-bot)

The Dank Face bot is reborn... Again.

Now as multiples micro-services, connected trough GRPC, hosted on Google Kubernetes Engine, built with Travis CI.

This repo only contains the bot part, which will call some other micro-services to function.

## Launch

Clone the repo `git clone git@github.com/dixneuf19/dank-face-bot.git`.

Create a virtualenv with `virtualenvwrapper`: `mkvirtualenv dank-face-bot` (make sur you have python3 for your virtualenv).

Install dependencies with `pip install -r requirements.txt`

```bash
TOKEN=******bot-telegram-token*** INSULT_JMK_HOST=<IP_ADDRESS> python main.py
```

## Add dependencies

Just `pip install <dep>` (activate the correct *virtualenv* with `workon dank-face-bot`).
Then update `requirement.txt` with `pip freeze > requirement.txt`.

## Create Travis secret

```bash
travis encrypt-file client-secret.json
```

Then add at the a before

```bash
openssl aes-256-cbc -K $encrypted_8301fcd250ef_key -iv $encrypted_8301fcd250ef_iv -in client-secret.json.enc -out client-secret.json -d
```

## Fix path import issue for GRPC

There is an issue with the way `protoc` generate the pb files and `__init__.py`, which create a module.

@see <https://github.com/protocolbuffers/protobuf/issues/1491>

Anyway, a fix for now : 
In `service_grpc/insult_jmk/insult_jmk_pb2_grpc.py` change 

```python
import insult_jmk_pb2 as insult__jmk__pb2
```

to

```python
from . import insult_jmk_pb2 as insult__jmk__pb2
```

This isn't a great solution however...