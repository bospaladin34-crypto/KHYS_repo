#!/bin/bash
echo "--- [VESPER-01: GLOBAL REPO IGNITION START] ---"
git fetch --all
for branch in $(git branch -r | grep -v '\->'); do
    echo "[SHIFTING]: Entering Branch $branch"
    git checkout ${branch#origin/}
    find . -type f \( -name "*.py" -o -name "*.sh" \) -exec chmod +x {} +
    git add .
    git commit -m "[IGNITION]: Global Executable Lock. 15Hz Sync Active."
done
git checkout sovereign-main
git push --all origin --force
echo "STATUS: TOTALITY ACHIEVED."
