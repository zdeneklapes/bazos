#!/bin/bash
#set -x # log

RM="rm -rfd"
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'


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

function usage() {
  # Print usage on stdout
  function_names=$(grep '^[[:space:]]*function ' start.sh | sed -E 's/^[[:space:]]*function[[:space:]]+([^[:space:]()]+).*/\1/')
  echo "Available functions:"
  # shellcheck disable=SC2068
  for func_name in ${function_names[@]}; do
    printf "    $func_name\n"
    awk "/function ${func_name}()/ { flag = 1 }; flag && /^\ +#/ { print \"        \" \$0 }; flag && !/^\ +#/ && !/function ${func_name}()/  { exit }" start.sh
  done
}

function error_exit() {
  # Print error message on stdout and exit
  printf "${RED}ERROR: $1${NC}\n"
  usage
  exit 1
}

function main() {
  # Main function: Call other functions based on input arguments
  [[ "$#" -eq 0 ]] && usage && exit 0
  while [ "$#" -gt 0 ]; do
    case "$1" in
    *) "$1" || error_exit "Failed to call function $1" ;;
    esac
    shift
  done
}

main "$@"
