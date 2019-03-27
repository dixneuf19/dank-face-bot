# DankFaceBot repo

[![Build Status](https://travis-ci.org/dixneuf19/dank-face-bot.svg?branch=master)](https://travis-ci.org/dixneuf19/dank-face-bot)

The Dank Face bot is reborn... Again.

Now as multiples micro-services, connected trough GRPC, hosted on Google Kubernetes Engine, built with Travis CI.

This repo only contains the bot part, which will call some other micro-services to function.

## Launch

Clone the repo `git clone git@github.com/dixneuf19/dank-face-bot.git`.

Create a virtualenv with `virtualenvwrapper`: `mkvirtualenv dank-face-bot` (make sur you have python3 for your virtualenv).

Install dependencies with `pip install -r requirements.txt`

You need at least a *bot telegram token* to launch it. You also need to specify the host of the micro-services which will be used, if they're not hosted on the same machine.

```bash
TOKEN=******bot-telegram-token*** INSULT_JMK_HOST=<IP_ADDRESS> python main.py
```

## Deploy on k8s

It uses the Travis script, update `.travis.yml` with the correct cluster configuration.

If this is the first deploy, it's a bit more complex. Configure your `gcloud` CLI access correctly, then get the *cluster credentials* with

```bash
gcloud gcloud container clusters get-credentials $CLUSTER_NAME
```

For a local one time deploy, you can use the `deploy.sh` script, with the correct environment variables, after having locally built the image.

```bash
PROJECT_NAME= ...
```

## Micro services

Here are listed the micro-services DFB relies on. Without he only responds to `/help` and `/start`.

### Insulter (or insult-JMK)

[Insulter](https://www.github.com/dixneuf19/insult-jmk)
A french insult generator, written in GO, exposed with GRPC.

### Find Faces (or fuzzy-octo-disco)

[Find Faces (or fuzzy-octo-disco)](https://www.github.com/dixneuf19/fuzzy-octo-disco)
A wrapper around the excellent `face-recognition` python module. Find and extract faces from an image. Share a volume with *dank-face-bot* to avoid a heavy load on network traffic with GRPC.

## Some development tips and remarks

### Add dependencies

Just `pip install <dep>` (activate the correct *virtualenv* with `workon dank-face-bot`).
Then update `requirement.txt` with `pip freeze > requirement.txt`.

### Create Travis secret

```bash
travis encrypt-file client-secret.json
```

Then add at the a before

```bash
openssl aes-256-cbc -K $encrypted_8301fcd250ef_key -iv $encrypted_8301fcd250ef_iv -in client-secret.json.enc -out client-secret.json -d
```

### Fix path import issue for GRPC

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

### Create a secret on k8s

```bash
k create secret generic telegram-token --from-literal token=****token****
```