if [ "$#" -ne 2 ]; then
    echo "Usage: ./basic.sh <input_file> <output_file>"
    exit 1
fi

# Run the basic_3.py script
python3 basic_3.py "$1" "$2"
