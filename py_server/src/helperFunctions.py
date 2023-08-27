#helperFunctions.py

def read_config_file(whatIneed):
    import os
    import sys

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to config.txt
    config_path = os.path.join(script_dir, '../..', 'config.txt')

    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('#'):  # skip comment lines
                continue
            if '=' in line:
                key, value = line.strip().split('=')
                if key == whatIneed:
                    if whatIneed == "Server-IP" and not value:
                        print("Please set the server's IP address in the config.txt file. \n[Example: Server-IP=192.168.123.123]")
                        sys.exit(1)
                        return None
                    return value

    print(f"Unable to find value for {whatIneed}")
    return None

