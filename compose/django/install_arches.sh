#!/usr/bin/env bash

bower install --allow-root -q
#python manage.py packages -o setup # this sets up elasticsearch as well, some configs need to be carried over
python manage.py packages -o setup_db
python manage.py packages -o import_json
python manage.py packages -o add_tilserver_layer -m arches/tileserver/hillshade.xml -n hillshade
python manage.py packages -o add_tilserver_layer -m arches/tileserver/world.xml -n world
