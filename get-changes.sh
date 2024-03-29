#!/bin/sh

set -e

last_tag="$1"
if [ -z "$last_tag" ]; then
    last_tag=`git tag | sort -n | tail -n 1`
fi
git log ${last_tag}.. --no-merges --perl-regexp --author='^((?!(dependabot|renovate|github-actions)).*)$' --format="* %s (%h)"
