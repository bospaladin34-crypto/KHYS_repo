#!/bin/bash
LatticeDir="/c/Users/Nbell/KHYS_repo"
LogPath="$LatticeDir/Lattice_Log.txt"
Command=$1

if [ "$Command" == "audit" ]; then
    git status >> "$LogPath"
    tail -n 10 "$LogPath"
elif [ "$Command" == "dampen" ]; then
    git -C "$LatticeDir" fetch origin
    git -C "$LatticeDir" reset --hard origin/main
    echo "[STATUS: STATE-SPACE_RE-ALIGNED_TO_J1748]"
fi
