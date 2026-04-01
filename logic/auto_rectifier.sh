#!/bin/bash
while true; do
    python3 /home/nbell/santos-sync/ignite_manifold.py >> /home/nbell/santos-sync/logs/manifold_pulse.log
    sleep 1.618
done
