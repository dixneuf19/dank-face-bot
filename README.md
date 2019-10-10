# DankFaceBot repo

[![Build Status](https://travis-ci.org/dixneuf19/dank-face-bot.svg?branch=master)](https://travis-ci.org/dixneuf19/dank-face-bot)

The Dank Face bot is reborn... Again.

Dank Face bot is a small architecture project, which takes pictures and return the cropped faces it found on the pictures.

First as a simple and dirty python project, it's now separated into three micro-services :
- dank-face-bot: the Telegram bot part, which receives and process the different messages from Telegram. It then dispatch the commands to two other micro-services.
- fuzzy-octo-disco (Find Faces) : the part which actually does some ML and image manipulation. Scrapped from an old school project, it use two python libraries to find faces and then crop the image around the faces.
- insult-jmk : Well... Just a small Go project to demonstrate my micro-services architecture. Generate small french insults.

Theses services are connected trough GRPC.
They *were* hosted on Google Kubernetes Engine, built with Travis CI.
But today, for cost issues, I just use on a local machine with *docker-compose*.

This repo only contains the bot part, which will call some other micro-services to function.

## Launch

Clone the repo `git clone git@github.com/dixneuf19/dank-face-bot.git`.

Create a virtualenv with `virtualenvwrapper`: `mkvirtualenv dank-face-bot` (make sur you have python3 for your virtualenv).

Install dependencies with `pip install -r requirements.txt`

You need at least a *bot telegram token* to launch it. You also need to specify the host of the micro-services which will be used, if they're not hosted on the same machine.

```bash
TOKEN=******bot-telegram-token*** INSULT_JMK_HOST=<IP_ADDRESS> python main.py
```

You can also use `.env`.

## Deploy on k8s

It uses the Travis script, update `.travis.yml` with the correct cluster configuration.

If this is the first deploy, it's a bit more complex. Configure your `gcloud` CLI access correctly, then get the *cluster credentials* with

```bash
gcloud gcloud container clusters get-credentials $CLUSTER_NAME
```

Then you probably need two manual action before letting *Travis* do the job.

First, add the **Telegram Token secret** to the GKE cluster. See [this topic](###Create-a-secret-on-k8s).

Then, you need to create the nfs volume for the [face recognition](https://github.com/dixneuf19/fuzzy-octo-disco) part, otherwise it will fail (TODO: make this optional for the bot):

```bash
k apply -f nfs-server.yml
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

## Local deployment with docker-compose

Instead of a complicated and quite expensive Kubernetes cluster, you can also run it locally on a VM or you desktop.

You need to clone the selected services along the main *dank-face-bot* repositery :

```bash
your-project-path/
            ./dank-face-bot/
            ./fuzzy-octo-disco/
            ./insult-jmk/
```

The path to build this services are relative from `dank-face-bot/` folder in the `docker-compose.yml` file, you can comment out a service if it's not used.

Specify the TOKEN in a `.env` file : `echo "TOKEN=******bot-telegram-token***" >> .env` and just run `docker-compose up` in the *dank-face-bot* folder.
