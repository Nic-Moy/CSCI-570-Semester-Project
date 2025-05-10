#!/bin/bash

# Output files
BASIC_OUT="basic_results.txt"
EFFICIENT_OUT="efficient_results.txt"

# Clear previous outputs
> "$BASIC_OUT"
> "$EFFICIENT_OUT"

# Loop through in1.txt to in15.txt
for i in {1..15}; do
    INPUT="../datapoints/in${i}.txt"
    BASIC_TMP="out_basic_${i}.txt"
    EFFICIENT_TMP="out_efficient_${i}.txt"

    echo "Running on $INPUT..."

    # Run basic
    python3 basic_3.py "$INPUT" "$BASIC_TMP"
    echo "===== in${i}.txt =====" >> "$BASIC_OUT"
    cat "$BASIC_TMP" >> "$BASIC_OUT"
    echo "" >> "$BASIC_OUT"

    # Run efficient
    python3 efficient_3.py "$INPUT" "$EFFICIENT_TMP"
    echo "===== in${i}.txt =====" >> "$EFFICIENT_OUT"
    cat "$EFFICIENT_TMP" >> "$EFFICIENT_OUT"
    echo "" >> "$EFFICIENT_OUT"

    # Clean up temp files
    rm "$BASIC_TMP" "$EFFICIENT_TMP"
done

echo "Done. Outputs saved to $BASIC_OUT and $EFFICIENT_OUT."
