#!/bin/bash

set -e
TAG_IMAGE="$(git log -n 1 --pretty='format:%cd-%h' --date=format:'%Y%m%d%H%M')"


build_containers(){
  docker build -f docker/server.dockerfile -t server-container:$TAG_IMAGE .
  docker build -f docker/client.dockerfile -t client-container:$TAG_IMAGE .
}

run_server_container(){
  docker rm -f server-container
  docker run -it --name server-container --net containers --restart always server-container
}

run_client_container(){
  docker run -it --name client-container --net containers --restart always client-container
}


#########################
# The command line help #
#########################
display_help() {
    echo
    echo "Como usar:" >&2
    echo "Criar as imagens = ./docker.sh build_container"
    echo "Rodar o container Server = ./docker.sh run_server_container"
    echo "rodar o container cliente = ./docker.sh run_client_container"
    echo
    exit 1
}


case $1 in 
 -h) display_help ;; 
  h) display_help ;;
  help) display_help ;;
  "") display_help ;;
  build_containers) build_containers ;;
  run_server_container) run_server_container ;;
  aci_deploy) aci_deploy ;;
  run_client_container) run_client_container;;
esac
