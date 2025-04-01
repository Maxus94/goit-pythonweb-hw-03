# goit-pythonweb-hw-03

Створення образу

docker build --no-cache . -t maxus94/site-docker

Запуск контейнера зі зберіганням даних поза контейнером

docker run -it -p 8000:3000 -v "C:/Projects/goit-pythonweb-hw-03/storage:/app/storage" maxus94/site-docker
