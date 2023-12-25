#!/bin/bash
#set -x # log

RM="rm -rfd"
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
DEBUG=1
ZIP_NAME='TODO.zip'
VPS_URI='TODO'

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
    docker build -t zdeneklapes/bazos-api:latest -f Dockerfile . && \
    docker run -it --rm \
        -v=./tmp/fish/:/root/.local/share/fish/ \
        -v=./bazos/:/app/bazos/ \
        -v=./scripts/:/app/scripts/ \
        -v=$HOME/Documents/photos-archive/bazos:/app/images/bazos/ \
        zdeneklapes/bazos-api:latest
}

function create_venv() {
    # Create venv
    python3 -m venv venv
    deactivate
    source venv/bin/activate.fish
    pip3 install -r requirements.txt
    deactivate
}

function release_patch() {
    # Get tagName, which is in format 0.0.0 (regex: v[0-9]+\.[0-9]+\.[0-9]+)
    tag_name=$(gh release view --jq ".tagName" --json tagName)
    patch_version=$(echo "${tag_name}" | sed -E 's/[0-9]+\.[0-9]+\.([0-9]+)/\1/')
    minor_version=$(echo "${tag_name}" | sed -E 's/[0-9]+\.([0-9]+)\.[0-9]+/\1/')
    major_version=$(echo "${tag_name}" | sed -E 's/([0-9]+)\.[0-9]+\.[0-9]+/\1/')

    # Increment patch version
    new_patch_version=$((patch_version + 1))

    # Create new tag
    tag_name="${major_version}.${minor_version}.${patch_version}"
    new_tag_name="${major_version}.${minor_version}.${new_patch_version}"
    echo "Releasing... ${tag_name} -> ${new_tag_name}"

    # Create release
    gh release create "${new_tag_name}" -t "Release ${patch_version}" -n "Released new patch version ${patch_version}"
}

function release_minor() {
    # Get tagName, which is in format 0.0.0 (regex: v[0-9]+\.[0-9]+\.[0-9]+)
    tag_name=$(gh release view --jq ".tagName" --json tagName)
    patch_version=$(echo "$tag_name" | sed -E 's/[0-9]+\.[0-9]+\.([0-9]+)/\1/')
    minor_version=$(echo "$tag_name" | sed -E 's/[0-9]+\.([0-9]+)\.[0-9]+/\1/')
    major_version=$(echo "$tag_name" | sed -E 's/([0-9]+)\.[0-9]+\.[0-9]+/\1/')

    # Increment minor version
    new_minor_version=$((minor_version + 1))

    # Create new tag
    tag_name="${major_version}.${minor_version}.${patch_version}"
    new_tag_name="${major_version}.${new_minor_version}.0"
    echo "Releasing... ${tag_name} -> ${new_tag_name}"

    # Create release
    gh release create "${new_tag_name}" -t "Release ${new_tag_name}" -n "Released new minor version ${new_tag_name}"
}

function release_major() {
    # Get tagName, which is in format 0.0.0 (regex: v[0-9]+\.[0-9]+\.[0-9]+)
    tag_name=$(gh release view --jq ".tagName" --json tagName)
    patch_version=$(echo "$tag_name" | sed -E 's/[0-9]+\.[0-9]+\.([0-9]+)/\1/')
    minor_version=$(echo "$tag_name" | sed -E 's/[0-9]+\.([0-9]+)\.[0-9]+/\1/')
    major_version=$(echo "$tag_name" | sed -E 's/([0-9]+)\.[0-9]+\.[0-9]+/\1/')

    # Increment major version
    new_major_version=$((major_version + 1))

    # Create new tag
    tag_name="${major_version}.${minor_version}.${patch_version}"
    new_tag_name="${new_major_version}.0.0"
    echo "Releasing... ${tag_name} -> ${new_tag_name}"

    # Create release
    gh release create "${new_tag_name}" -t "Release ${new_tag_name}" -n "Released new major version ${new_tag_name}"
}

function clean() {
    # Clean project folder in order to see what will be done, set env variable $DEBUG=1
    ${RM} *.zip
    # Folders
    for folder in \
            "venv" \
            "*__pycache__" \
            "*.ruff_cache" \
            "*.pytest_cache" \
            "*.cache" \
            "*htmlcov*" \
            "skip-covered"\
            ; do
        if [ "$DEBUG" -eq 1 ]; then find . -type d -iname "${folder}"; else find . -type d -iname "${folder}" | xargs ${RM} -rf; fi
    done
    # Files
    for file in \
            "*.DS_Store" \
            "tags" \
            "db.sqlite3" \
            "*.png" \
            "*.zip" \
            "*.log" \
            "coverage.xml" \
            "*.coverage" \
            "coverage.lcov" \
            ; do
        if [ "$DEBUG" -eq 1 ]; then find . -type f -iname "${file}"; else find . -type f -iname "${file}" | xargs ${RM}; fi
    done
}

function tags() {
    # Create tags and cscope
    ctags -R .
    cscope -Rb
}

function pack() {
    # Clean and Zip project
    clean
    zip -r "${ZIP_NAME}" \
        .editorconfig \
        Dockerfile \
        requirements.txt \
        .gitignore \
        README.md \
        pyproject.toml \
        bazos \
        scripts \
        main.sh
}

function send() {
    # Send zipped project to VPS and then remove the zip file
    scp "${ZIP_NAME}" "${VPS_URI}"
    rm ${ZIP_NAME}
}

function help() {
    # Print usage on stdout
    echo "Available functions:"
    for file in ./scripts/*.sh; do
        function_names=$(cat ${file} | grep -E "(\ *)function\ +.*\(\)\ *\{" | sed -E "s/\ *function\ +//" | sed -E "s/\ *\(\)\ *\{\ *//")
        for func_name in ${function_names[@]}; do
            printf "    $func_name\n"
            awk "/function ${func_name}()/ { flag = 1 }; flag && /^\ +#/ { print \"        \" \$0 }; flag && !/^\ +#/ && !/function ${func_name}()/  { print "\n"; exit }" ${file}
        done
    done

}

function usage() {
    # Print usage on stdout
    help
}

function die() {
    # Print error message on stdout and exit
    printf "${RED}ERROR: $1${NC}\n"
    help
    exit 1
}

function main() {
    # Main function: Call other functions based on input arguments
    [[ "$#" -eq 0 ]] && die "No arguments provided"
    while [ "$#" -gt 0 ]; do
        case "$1" in
        *) "$1" || die "Unknown function: $1()" ;;
        esac
        shift
    done
}

main "$@"
