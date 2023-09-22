ZIP_NAME='TODO.zip'
VPS_URI='TODO'
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
