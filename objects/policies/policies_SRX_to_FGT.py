import sys

# In order to invoke this script 2 arguments are needed:
#   First argument --> input .txt file
#   Second argument --> Output .txt file

'''
# POLICIES IN SRX
from-zone SRC_ZONE to-zone DST_ZONE {
            policy policy_name {
                match {
                    source-address SRC_ADDR;
                    destination-address DST_ADDR;
                    application [ junos-app1 app2 ];
                }
                then {
                    permit;
                    log {
                        session-init;
                    }
                }
            }
}


# POLICIES IN FGT
config firewall policy
    edit 0
        set name "Test_policy"
        set srcintf "portX"
        set dstintf "portY"
        set action <accept/deny>
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "service1" "service2"
    next
end

# Logtraffic option sets by default
'''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: invalid number of arguments. Callout example: python policies_SRX_to_FGT.py <in_file.txt> <out_file.txt>")
        exit(-1)
        
    input = open(sys.argv[1], mode="r")
    output = open(sys.argv[2], mode="w")
    
    srcintf = None
    dstintf = None
    
    output.write("config firewall policy\n")
    
    lines = input.readlines()
    
    for line in lines:
        split_line = line.strip().split(" ")
        
        match(split_line[0]):
            case "from-zone":
                srcintf = split_line[1]
                dstintf = split_line[3]
            case "policy":
                output.write("edit 0\n")
                policy_name = split_line[1]
                output.write(f"set name \"{policy_name}\"\n")
                output.write(f"set srcintf \"{srcintf}\"\n")
                output.write(f"set dstintf \"{dstintf}\"\n")
            case "source-address":
                output.write("set srcaddr")
                for field in split_line:
                    if field != "any;" and field != "source-address" and field != "[" and field != "];":
                        if field.find(";") != -1:
                            srcaddr = field.strip(";")
                            output.write(f" \"{srcaddr}\"\n")
                        else:
                            srcaddr = field
                            output.write(f" \"{srcaddr}\"")
                    elif field == "any;":
                        output.write(f" \"all\"\n")
                    elif field == "];":
                        output.write("\n")
            case "destination-address":
                output.write("set dstaddr")
                for field in split_line:
                    if field != "any;" and field != "destination-address" and field != "[" and field != "];":
                        if field.find(";") != -1:
                            dstaddr = field.strip(";")
                            output.write(f" \"{dstaddr}\"\n")
                        else:
                            dstaddr = field
                            output.write(f" \"{dstaddr}\"")
                    elif field == "any;":
                        output.write(f" \"all\"\n")
                    elif field == "];":
                        output.write("\n")
            case "application":
                output.write("set service")
                for field in split_line:
                    if field != "any;" and field != "application" and field != "[" and field != "];":
                        if field.find("junos") != -1:
                            if field.find(";") == -1:
                                service = field.upper()
                                output.write(f" \"{service}\"")
                            else:
                                service = field.strip(";").upper()
                                output.write(f" \"{service}\"\n")
                        else:
                            if field.find(";") == -1:
                                service = field
                                output.write(f" \"{service}\"")
                            else:
                                service = field.strip(";")
                                output.write(f" \"{service}\"\n")
                    elif field == "any;":
                        output.write(" \"ALL\"\n")
                    elif field == "];":
                        output.write("\n")
            case "permit;":
                output.write("set action accept\n")
                output.write("set schedule \"always\"\n")
                output.write("next\n")
            case "deny;":
                output.write("set action deny\n")
                output.write("set schedule \"always\"\n")
                output.write("next\n")
    output.write("end\n")
            