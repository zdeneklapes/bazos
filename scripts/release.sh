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
