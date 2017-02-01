### Clone


    git clone --recursive --depth 100 git@github.com:webjunkie/arches.git
    git checkout feature/dockercompose
    
    
### Set `MODE = 'DEV'` in `settings_local.py`

To install Arches for development, the `MODE` setting must be updated accordingly. To do this you'll need to create a new file called `settings_local.py`. Place it as shown below, next to the existing `settings.py` file.

> Projects/<br>
> &#9492;&#9472;&nbsp;arches/<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&nbsp;arches/<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&nbsp;settings.py _#existing file_<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9492;&#9472;&nbsp;settings_local.py _#add this file_<br>
> &#9492;&#9472;&nbsp;ENV/<br>

Copy the following text and paste it into your new `settings_local.py` file.
    
```Python
# Override MODE in settings.py for development (gets you extra dependencies)
# https://github.com/archesproject/arches/wiki/Installation#installing-arches
MODE = 'DEV'

# create a MapBox account and insert your API key below
# https://www.mapbox.com/
MAPBOX_API_KEY = '<insert key here>'
```
    
### Get MapBox API key and add to `settings_local.py`

Arches uses MapBox, so you will need an API key to enable the mapping capabilities. Acquiring a key is very easy, just create a free account at [MapBox](https://www.mapbox.com). On your [studio home page](https://www.mapbox.com/studio/), you'll see a default Access Token (it begins with `pk.`). Paste this key to `settings_local.py`.

### Fire up Docker and run install scripts

Then in the folder:
    
    docker-compose up -d
    docker-compose run django ./compose/django/install_arches.sh
    docker-compose run django python manage.py createsuperuser
