import sys

# In order to invoke this script 2 arguments are needed:
#   First argument --> input .txt file
#   Second argument --> Output .txt file

'''
# SERVICE GROUPS IN SRX
application-set app_set_name {
    application app1_name;
    application app2_name;
    application app3_name;
}

# SERVICE GROUPS IN FGT
config firewall service group
    edit "service_group_name"
        set member "SERVICE1" "SERVICE2" "SERVICE3"
    next
end
'''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: invalid number of arguments. Callout example: python service_groups_SRX_to_FGT.py <in_file.txt> <out_file.txt>")
        exit(-1)

    input = open(sys.argv[1], mode="r")
    output = open(sys.argv[2], mode="w")

    output.write(f"config firewall service group\n")
    
    lines = input.readlines()
    
    for line in lines:
        split_line = line.strip().split(" ")
        
        match(split_line[0]):
            case "application-set":
                service_group_name = split_line[1]
                output.write(f"edit \"{service_group_name}\"\n")
                output.write("set member")
            case "application":
                service_name = split_line[1].strip(";")
                if service_name.find("junos") == -1:
                    output.write(f" \"{service_name}\"")
                else:
                    uppercased_service = service_name.upper()
                    # WARNING: It does NOT erase de "JUNOS-" part of the service name. It is necessary to remove it manually
                    output.write(f" \"{uppercased_service}\"")
            case "}":
                output.write("\nnext\n")
            
    output.write("end")