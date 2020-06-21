eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
sudo docker stop wa_clone
sudo docker rm wa_clone
sudo docker rmi andresangfajar/be_wa_clone:latest
sudo docker run -d --name wa_clone -p 5050:5050 andresangfajar/be_wa_clone:latest