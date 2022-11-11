#!/bin/bash

files="aa ab ac ad ae af ag ah ai aj ak al am"

# Iterate the string variable using for loop
for f in $files; do
    python clean_context.py wikipedia_$f &
done