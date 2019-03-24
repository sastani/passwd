import toml

def main():
    confDic = toml.load('config.toml')
    files = confDic['files']
    passwd_path = files['users']['path']
    users_path = files['groups']['path']




if __name__ == "__main__":
    main()