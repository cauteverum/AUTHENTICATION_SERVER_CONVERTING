from netmiko import Netmiko
from getpass import getpass


def userSettings(): 
    ip_ = input("Ip: ")
    username_ = input("Username: ")
    password_ = getpass("Password: ").lower()
    device_type_ = input("Device Type: ")

    info = {"host":ip_,
            "username":username_,
            "password":password_,
            "device_type":device_type_
            }

    print("Connection is being established...")
    connection = Netmiko(**info)
    print("Connection was established !")

    res = connection.send_command("show user local")
    with open(file="Old_Users.txt",mode="w",encoding="utf-8") as file: 
        file.write(res)


    middle = int(len(res)/2)
    res_first = res[:middle]
    res_last = res[middle:]
    used_server = input("which server do you use (ldap,radius): ")
    desired_server = input("Which server do you want to use (ldap,radius):")
    name_used_server = input(f"{used_server} name: ")
    name_desired_server = input(f"{desired_server} name: ")

    res_first = res_first.replace(f"set type {used_server}",f"set type {desired_server}")
    res_first = res_first.replace(f'set {used_server}-server "{name_used_server}"',f'set {desired_server}-server "{name_desired_server}"')
    res_last = res_last.replace(f"set type {used_server}",f"set type {desired_server}")
    res_last = res_last.replace(f'set {used_server}-server "{name_used_server}"',f'set {desired_server}-server "{name_desired_server}"')

    res = res_first + res_last    

    with open(file="New_Users.txt",mode="w",encoding="utf-8") as file: 
        file.write(res)
    
    connection.send_config_from_file("New_Users.txt")
    print("New users was created.")


userSettings()