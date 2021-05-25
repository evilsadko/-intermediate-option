### Серверная часть   

![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/v0.2/github/save.png)
    sudo docker images -a
    sudo docker ps -a -f status=exited
    sudo docker rm $(sudo docker ps -a -f status=exited -q)
    sudo docker rmi $(sudo docker images -a -q)
