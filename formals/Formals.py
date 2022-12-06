# python Formals.py source-text.txt pattern1.txt pattern2.txt pattern3...
import sys
from Scanner import Scanner

source_text = sys.argv[1]
patterns = sys.argv[2:]

scanner = Scanner(patterns)
scanner.run(source_text)
