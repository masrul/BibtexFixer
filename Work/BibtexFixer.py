import sys
from collections import deque, defaultdict
import argparse

sys.tracebacklimit = 0


class BibtexFixer:
    def __init__(self, file_name):
        if not file_name.endswith(".bib"):
            raise RuntimeError("File must be *.bib type")

        bibFH = open(file_name, "r")
        self.bibLines = bibFH.readlines()
        bibFH.close()

        self.Entries = defaultdict(dict)

    def tokenize(self, entryType):

        entryType = entryType.upper()
        self.currentLineID = 0

        while self.currentLineID < len(self.bibLines):
            line = self.bibLines[self.currentLineID]

            if line.upper().startswith(entryType):
                blockLineStart = self.currentLineID + 1
                brakets = ""
                blockLines = []
                blockLines.append(line)

                while self.currentLineID < len(self.bibLines):
                    brakets += self.getBrackets(line)
                    if not self.isBalanced(brakets):
                        self.currentLineID += 1
                        line = self.bibLines[self.currentLineID]
                        blockLines.append(line)

                        if line.strip().startswith("@"):
                            blockID = self.getBlockID(blockLines)
                            raise RuntimeError(
                                f"Imbalanced bracket detectd for {entryType:s}->{blockID:s} at line number {blockLineStart:d}"
                            )

                    else:
                        blockID = self.getBlockID(blockLines)
                        self.current_entry[blockID] = blockLines
                        break

            self.currentLineID += 1

    def getEntryTypes(self):
        def parseEntryTypes(line):
            entryType = ""

            save = False
            for char in line:
                if char in "@":
                    save = True
                elif char in "({":
                    break
                elif save:
                    entryType += char
            return entryType.strip().upper()

        self.entryTypes = []
        for line in self.bibLines:
            if line.strip().startswith("@"):
                entryType = parseEntryTypes(line)
                if entryType not in self.entryTypes:
                    self.entryTypes.append(entryType)

    def parseBib(self):

        self.getEntryTypes()

        for entryType in self.entryTypes:
            self.current_entry = self.Entries[entryType]
            self.tokenize("@" + entryType)

    def write(self, outFile):

        outFH = open(outFile, "w")

        for key1 in self.entryTypes:
            for key2 in self.Entries[key1].keys():
                item = self.Entries[key1][key2]

                outFH.write(item[0])
                for line in item[1:]:
                    if line.strip() == "}":
                        line = line.strip() + "\n\n"
                    else:
                        line = "    " + line.strip() + "\n"
                    outFH.write(line)
        outFH.close()

    @staticmethod
    def getBrackets(line):

        brakets = ""

        for char in line:
            if char in "(){}[]":
                brakets += char

        return brakets

    @staticmethod
    def isBalanced(String):
        braDict = dict()
        braDict[")"] = "("
        braDict["}"] = "{"
        braDict["]"] = "["

        stack = deque()
        for char in String:
            if char in "({[":
                stack.append(char)
            else:
                if len(stack) == 0:
                    return False
                else:
                    if stack.pop() != braDict[char]:
                        return False

        if len(stack) == 0:
            return True
        else:
            return False

    @staticmethod
    def getBlockID(block):
        blockString = ""
        blockID = ""
        for line in block:

            blockString += line

        save = False
        for char in blockString:
            if char in "({":
                save = True
            elif char in "=,":
                break
            elif save:
                blockID += char
        return blockID


def main():
    ArgParser = argparse.ArgumentParser(
        description="Remove duplicate entries and check imbalanced braket in a BibTex file"
    )

    ArgParser.add_argument(
        "-i",
        "--inputFile",
        metavar="",
        type=str,
        help="Name of the input file",
        required=True,
    )

    ArgParser.add_argument(
        "-o",
        "--outputFile",
        metavar="",
        type=str,
        help="Name of the output file [Default: Clean.bib]",
    )

    args = ArgParser.parse_args()

    inputFile = args.inputFile
    if args.outputFile:
        outputFile = args.outputFile
    else:
        outputFile = "Clean.bib"

    fixer = BibtexFixer(inputFile)
    fixer.parseBib()
    fixer.write(outputFile)


main()
