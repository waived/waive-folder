import sys, os
from cryptography.fernet import Fernet

def _loadKey(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as e:
        print('\n Error reading key:', e)
        return None
    
def _genKey(drop, name):
    _key = Fernet.generate_key()
    
    if not drop.endswith('/'):
        drop += '/'
        
    _myKey = os.path.join(drop, name + '.gate')
    try:
        with open(_myKey, 'wb') as f:
            f.write(_key)
        input('\n Key "' + _myKey + '" generated! Press <ENTER> to return...')
    except Exception as e:
        print('\n Error generating key:', e)

def _encrypt(path, _dir_path):
    _key = _loadKey(path)

    for root, dirs, files in os.walk(_dir_path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if not file.endswith('.lock'):
                    fernet = Fernet(_key)
                    with open(file_path, 'rb') as f:
                         encrypted_data = fernet.encrypt(f.read())
                    with open(file_path, 'wb') as f:
                        f.write(encrypted_data)
                    new_path = os.path.join(root, file + '.lock')
                    os.rename(file_path, new_path)
            except:
                print(' [!] Error locking ' + file_path)
                    
    input('\n Files locked! Press <ENTER> to return...\n')


def _decrypt(path, _dir_path):
    _key = _loadKey(path)

    for root, dirs, files in os.walk(_dir_path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if file.endswith('.lock'):
                    fernet = Fernet(_key)
                    with open(file_path, 'rb') as f:
                         encrypted_data = f.read()
                         decrypted_data = fernet.decrypt(encrypted_data)
                    with open(file_path, 'wb') as f:
                         f.write(decrypted_data)
                    new_path = os.path.join(root, file[:-5])  # Remove '.lock'
                    os.rename(file_path, new_path)
            except:
                print(' [!] Error unlocking ' + file_path)
            
    input('\n Files unlocked! Press <ENTER> to return...\n')
            
def main():
    banner = '''
    ______      __             ____      __   __
   / / / /____ /_/____ ____   / __/____ / /__/ /____ ___
  / / / // . // /| / // -_/  / __// . // // . // -_// _/
 /_____//__,//_/ \__//___/  /_/  /___//_//___//___//_/

 <1> Generate encryption key
 <2> Unlock folder content
 <3> Lock folder content
 <4> Exit WaiveFolder 1.0
'''
    while True:
        os.system('clear')  # Adjust clear command as needed
        print(banner)
        
        try:
            option = int(input(' Option: '))
            print('\n')
            if option == 1:
                drop = input(' Location for key (/home/example): ')
                name = input(' Key name (ex- "secret"): ')
                _genKey(drop, name)
            elif option == 2 or option == 3:
                path = input(' Load key (/home/example/mykey.gate): ')
                _dir_path = input(' Directory to ' + ('unlock' if option == 2 else 'lock') + ' (/home/example): ')
                if option == 2:
                    _decrypt(path, _dir_path)
                else:
                    _encrypt(path, _dir_path)
            elif option == 4:
                break
        except KeyboardInterrupt:
            break
        except:
            pass
            
    sys.exit('\n\n Thank you for using WaiveFolder!\n')
    
if __name__ == "__main__":
    main()

