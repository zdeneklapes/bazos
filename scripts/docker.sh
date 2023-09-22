function prune_docker() {
    # Stop and remove all containers
    docker stop $(docker ps -aq)
    docker system prune --all --force --volumes

    # Remove all volumes: not just dangling ones
    for i in $(docker volume ls --format json | jq -r ".Name"); do
        docker volume rm -f ${i}
    done
}

function docker_show_ipaddress() {
    # Show ip address of running containers
    for docker_container in $(docker ps -aq); do
        CMD1="$(docker ps -a | grep "${docker_container}" | grep --invert-match "Exited\|Created" | awk '{print $2}'): "
        if [ ${CMD1} != ": " ]; then
            printf "${CMD1}"
            printf "$(docker inspect ${docker_container} | grep "IPAddress" | tail -n 1)\n"
        fi
    done
}

function dev_docker_up() {
    docker build -t zdeneklapes/bazos-api:latest -f Dockerfile .
    docker run -it --rm -v=./tmp/fish/:/root/.local/share/fish/ zdeneklapes/bazos-api:latest
}
