# Include standard modules
import argparse

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("chase", "chase:volume", help="show program version", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

# Check for --version or -V
if args.chase:
    print("This is myprogram version 0.1")