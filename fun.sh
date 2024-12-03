#!/bin/bash

if ! command -v hangman &> /dev/null
then
    sudo apt update && sudo apt install -y bsdgames
fi

hangman

