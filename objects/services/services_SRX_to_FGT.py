import sys

# In order to invoke this script 2 arguments are needed:
#   First argument --> input .txt file
#   Second argument --> Output .txt file

'''
# SERVICE IN SRX
1)
application app_name {
        protocol tcp;
        destination-port 6666-6668;
    }
2) NOT IMPLEMENTED
application app_name protocol <protocol_number>;

# SERVICE IN FGT
    edit "SERVICE_NAME"
        set category "service_category"
        set udp-portrange 6666-6668
    next
'''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: invalid number of arguments. Callout example: python addresses_SRX_to_FGT.py <in_file.txt> <out_file.txt>\n")
        exit(-1)
        
    input = open(sys.argv[1], mode="r")
    output = open(sys.argv[2], mode="w")
    
    lines = input.readlines()
    
    output.write("config firewall service custom\n")
    
    for line in lines:
        split_line = line.strip().split(" ")

        match(split_line[0]):
            case "application":
                if len(split_line) != 4:
                    service_name = split_line[1]
                    output.write(f"edit \"{service_name}\"\n")
            case "protocol":
                if split_line[1].strip(";") == "tcp":
                    output.write("set tcp-portrange ")
                elif split_line[1].strip(";") == "udp":
                    output.write("set udp-portrange ")
            case "destination-port":
                portrange = split_line[1].strip(";")
                output.write(f"{portrange}\n")
            case "}":
                output.write("next\n")
            
    output.write("end")