#!/bin/sh

set -e

last_tag=`git tag | sort -n | tail -n 1`
git log ${last_tag}.. --no-merges --invert-grep  --author dependabot --format="* %s (%h)"
