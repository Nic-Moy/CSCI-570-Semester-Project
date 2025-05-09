if [ "$#" -ne 2 ]; then
    echo "Usage: ./efficient.sh <input_file> <output_file>"
    exit 1
fi

# Run the efficient_3.py script
python3 efficient_3.py "$1" "$2"
