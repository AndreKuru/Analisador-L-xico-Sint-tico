# python Formals.py source-text.txt pattern1.txt pattern2.txt pattern3...
import sys
from formals.Scanner import Scanner, printToken_table

source_text = sys.argv[1]
patterns = sys.argv[2:]

scanner = Scanner(patterns)

printToken_table(scanner)