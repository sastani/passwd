import toml
from app import run

def main():
    confDic = toml.load('config.toml')
    files = confDic['files']
    passwd_path = files['users']['path']
    users_path = files['groups']['path']
    port = confDic['port']
    run(passwd_path, users_path, port)

if __name__ == "__main__":
    main()