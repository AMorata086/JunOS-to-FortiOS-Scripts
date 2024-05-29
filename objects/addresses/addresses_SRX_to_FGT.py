import sys
# In order to invoke this script 2 arguments are needed:
#   First argument --> input .txt file
#   Second argument --> Output .txt file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: invalid number of arguments. Callout example: python addresses_SRX_to_FGT.py <in_file.txt> <out_file.txt>")
        exit(-1)

    input = open(sys.argv[1], mode="r")
    output = open(sys.argv[2], mode="w")

    lines = input.readlines()
    output.write(f"config firewall address\n")
    for line in lines:
        split_line = line.strip().split(sep=" ")
        name = split_line[1]
        ip = split_line[2].strip(";")
        output.write(f"edit \"{name}\"\n")
        output.write(f"set subnet {ip}\n")
        output.write("next\n")

    output.write("end")