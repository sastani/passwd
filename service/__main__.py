import toml
from app import run

def main():
    #read config file
    conf_dic = toml.load('config.toml')
    #determine if program set for testing or development
    if(conf_dic['test'] == True):
        files = conf_dic['files']['test']
    else:
        files = conf_dic['files']['deploy']
    #extract paths for passwd and group files and port for webserver
    passwd_path = files['users']['path']
    users_path = files['groups']['path']
    port = conf_dic['port']
    run(passwd_path, users_path, port)

if __name__ == "__main__":
    main()