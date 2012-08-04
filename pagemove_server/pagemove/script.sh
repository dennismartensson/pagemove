#!/bin/sh
HOME=/home/urlshare
. $HOME/.virtualenvs/serverUrlshare/bin/activate
cd $HOME/serverurlshare
gunicorn_django -w 3 -b "127.0.0.1:1234" -p $HOME/gunicorn_pid
