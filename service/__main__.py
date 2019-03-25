import toml
from app import run

def main():
    conf_dic = toml.load('config.toml')
    if(conf_dic['test'] == True):
        files = conf_dic['files']['test']
    else:
        files = conf_dic['files']['deploy']
    passwd_path = files['users']['path']
    users_path = files['groups']['path']
    port = conf_dic['port']
    run(passwd_path, users_path, port)

if __name__ == "__main__":
    main()