import sys

# In order to invoke this script 2 arguments are needed:
#   First argument --> input .txt file
#   Second argument --> Output .txt file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: invalid number of arguments. Callout example: python address_groups_SRX_to_FGT.py <in_file.txt> <out_file.txt>")
        exit(-1)

    input = open(sys.argv[1], mode="r")
    output = open(sys.argv[2], mode="w")

    output.write(f"config firewall addrgrp\n")
    
    lines = input.readlines()
    
    for line in lines:
        split_line = line.strip().split(" ")
        
        match(split_line[0]):
            case "address-set":
                group_name = split_line[1]
                output.write(f"edit \"{group_name}\"\n")
                output.write(f"set member")
            case "address":
                address = split_line[1].strip(";")
                output.write(f" \"{address}\"")
            case "}":
                output.write("\nnext\n")
            
    output.write("end")