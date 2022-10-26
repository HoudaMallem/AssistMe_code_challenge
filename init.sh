docker-compose build 
#docker-compose build --no-cache
docker-compose up -d
docker exec assistme-dev-web python manage.py makemigrations
docker exec assistme-dev-web python manage.py migrate