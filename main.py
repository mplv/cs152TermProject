import re
import argparse
import sys

# Require a file with regular expressions in it passed as a paramater
parser = argparse.ArgumentParser()
parser.add_argument("file", help="File of regexp to run over the input", type=str)
parser.add_argument("-e", "--emp", action=("store_true"), help="Bold the match")
parser.add_argument("-p", "--print-match", action=("store_true"), help="Print just the match")

# not implemented!
# parser.add_argument("--context", "-c", type=int, help="Print CONTEXT number of lines")

# not implemented!
# parser.add_argument("-rt", "--replace-text", type=str, help="Replace non-matched text with REPLACE_TEXT")

args = parser.parse_args()

# a list to hold the regular expression objects that are in the file
regexps = []

# print the regular expressions
print "\n\nRegular expressions to match:"
print "-----------------------------"

# open the file specified as the cmd line arg and name it inputfile
with open(args.file, "r") as inputFile:
    # for each line in inputFile
    for line in inputFile:
        # read a line and convert it to a regular expression
        print line.replace("\n","")
        regexps.append(re.compile(str(line).replace("\n","")))

# print the matches
print "\n\nMatches:"
print "---------"

# read each line of input from stdin
for line in sys.stdin:
    # for each line run each regular expressions over the line
    for r in regexps:
        # get the match object and if we have a match print it
        match = r.search(line)
        if not match is None:
            # print the line with highlight or not
            if args.print_match:
                # print just the match
                if args.emp:
                    # \033[1m causes the match to be bolded on the terminal
                    # \033[0m causes the rest of the text to not be bolded
                    print ("\033[1m" + match.group(0) + "\033[0m").replace("\n","")
                else:
                    print match.group(0)
            else:
                # print the entire line
                if args.emp:
                    # \033[1m causes the match to be bolded on the terminal
                    # \033[0m causes the rest of the text to not be bolded
                    print line.replace(match.group(0),"\033[1m" + match.group(0) + "\033[0m").replace("\n","")
                else:
                    print line.replace("\n","")
