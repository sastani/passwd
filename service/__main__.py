import toml
#from app import run

def main():
    '''
    #read config file
    conf_dic = toml.load('config.toml')
    #determine if program set for testing or deployment
    if(conf_dic['use_test'] == True):
        files = conf_dic['files']['test']
    else:
        files = conf_dic['files']['deploy']
    #extract paths for passwd and group files and port for webserver
    passwd_path = files['passwd']
    users_path = files['group']
    port = conf_dic['port']
    run(passwd_path, users_path, port)
    '''
    ex = toml.load('example.toml')
    print(ex["servers"]["alpha"]["ip"])


if __name__ == "__main__":
    main()