#!/usr/bin/env bash

bower install
#python manage.py packages -o setup
python manage.py packages -o setup_db
#python manage.py packages -o import_json
#python manage.py packages -o add_tilserver_layer -m arches/tileserver/hillshade.xml -n hillshade
#python manage.py packages -o add_tilserver_layer -m arches/tileserver/world.xml -n world
