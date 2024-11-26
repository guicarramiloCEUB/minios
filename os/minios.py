import log
import os
import subprocess

class MiniOs:
    def __init__(self):
        self.user = None                #credenciais
        self.password = None
        self.current_directory = os.getcwd() + "\\users"     #diretorio atual (criar dirs e arquivos no dir atual)
        self.dir_counter = 0     #contador utilizado para evitar a saida do diretorio do usuario
        print('''\033[1;32m
              

              



              
                        ___  ___ _         _   _____  _____ 
                        |  \/  |(_)       (_) |  _  |/  ___|
                        | .  . | _  _ __   _  | | | |\ `--. 
                        | |\/| || || '_ \ | | | | | | `--. |
                        | |  | || || | | || | \ \_/ //\__/ /
                        \_|  |_/|_||_| |_||_|  \___/ \____/ 
                                      Welcome    

              

              Created by: Guilherme Carramilo, Ricardo Bittar and Jamille     
                                 
        ''')
        print("1) Create user\n2) Login\n")
        op = None
        while True:
            op = input("Select option: ")
            if op == "1":
                self.user, self.password = log.create_user()
                self.current_directory = self.current_directory + f'\\{self.user}'
                break
            elif op == "2":
                self.user, self.password = log.login()
                self.current_directory = self.current_directory + f'\\{self.user}'
                break
            print(f"{op} in not an avaible option.")


    def terminal(self):   #abre o terminal do OS, onde receberá os comandos
        while True:
            command = input(f"{self.user}@MiniOS{self.current_directory[self.current_directory.find(f"\\users\\{self.user}"):]}>").strip()
            if command.startswith("create directory"):
                _, _, path = command.split(maxsplit=2)
                self.create_directory(path)
            elif command.startswith("list"):
                if len(command.split()) == 1:
                    self.list_dir(self.current_directory)
                else:
                    self.list_dir(self.current_directory + f'\\{command.split()[1]}')
            elif command.startswith("cd"):
                if len(command.split()) == 1 and self.dir_counter >= 0:
                    if self.dir_counter == 0:
                        print("Cannot return to directory")
                    else:
                        self.dir_counter -= 1
                        self.current_directory = self.current_directory[:(self.current_directory.rfind('\\'))]
                else:
                    _, path = command.split(maxsplit=2)
                    self.goto_directory(path)
            else:
                print("Command does not exist.")

    def create_directory(self, dir_path):
        if not os.path.exists(f"{self.current_directory}\\" + dir_path):
            os.makedirs(f"{self.current_directory}\\" + dir_path)
            print(f"Directory '{dir_path}' created.")
        else:
            print("Directory already exists.")
        
    def list_dir(self, directory):
        if os.path.exists(directory):
            for item in os.listdir(directory):
                print(item)
        else:
            print("Directory not found.")

    def goto_directory(self, directory):
        if os.path.exists(f"{self.current_directory}\\" + directory):
            self.dir_counter += 1    #mantem quantas vezes o user entrou em diretorios, consequentemente sabe quantas vezes pode retornar
            self.current_directory = self.current_directory + f"\\{directory}"
        else:
            print("Directory not found.")
