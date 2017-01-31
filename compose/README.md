
    git clone --recursive --depth 100 git@github.com:webjunkie/arches.git
    git checkout feature/dockercompose
    
Then in the folder:
    
    docker-compose up -d
    docker-compose run django ./compose/django/install_arches.sh
    docker-compose run django python manage.py createsuperuser
