sudo docker stop willy && sudo docker rm willy
yes | sudo docker system prune -a
sudo docker build -t rollcall . && sudo docker container run --publish 80:80 --detach --name willy rollcall
