#!/bin/bash

bash --version

# Set tool locations
MARKDOWNLINT="markdownlint"

echo "Working with these files"
DOCS=$(find ./docs -type f -name "*.md")
README=$(find . -type f -name "README.md")
FILES=( "${DOCS[@]}" "${README[@]}" )

for file in $FILES; do
    echo "$file"
done
echo

#echo "Linting markdown files with alex"
#npx alex
# "$ALEx"

# set -euo pipefail
echo "Linting markdown files with markdownlint"
for file in $FILES; do
    echo "$MARKDOWNLINT" "$file" --ignore node_modules --ignore .git --ignore .idea
    npx "$MARKDOWNLINT" "$file" --ignore node_modules --ignore .git --ignore .idea
done

echo "Checking links in markdown files with linkcheckMarkdown"

for file in $FILES; do
    linkcheckMarkdown "$file"
done


echo "Checking with proselint"
for file in $FILES; do
    proselint "$file"
done

echo "Checking links in markdown files with write-good"
for file in $FILES; do
    npx write-good "$file"
done

