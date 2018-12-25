# DankFaceBot repo

[![Build Status](https://travis-ci.org/Dixneuf19/dank-face-bot.svg?branch=service)](https://travis-ci.org/Dixneuf19/dank-face-bot)

The Dank Face bot is reborn... Again.

Now as multiples micro-services, connected trough GRPC, hosted on Google Kubernetes Engine, built with Travis CI.

This repo only contains the bot part, which will call some other micro-services to function.    

## Create Travis secret

```bash
travis encrypt-file client-secret.json
```

Then add at the a before

```bash
openssl aes-256-cbc -K $encrypted_8301fcd250ef_key -iv $encrypted_8301fcd250ef_iv -in client-secret.json.enc -out client-secret.json -d
```