import os
import hashlib
import getpass
import random
import string
import subprocess

users = {}
logged_user = None
memory = [0] * 100
file_ownership = {}  # Para armazenar o dono de cada arquivo/diretório

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha512((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def check_password(stored_password, input_password):
    salt, hashed = stored_password.split('$')
    return hash_password(input_password, salt).split('$')[1] == hashed

def create_user():
    global logged_user
    username = input("Crie um nome de usuário: ")
    while username in users:
        username = input("Usuário já existe. Crie outro nome de usuário: ")
    password = getpass.getpass("Crie uma senha: ")
    users[username] = hash_password(password)
    logged_user = username
    print(f"Usuário '{username}' criado e logado com sucesso.")

def login():
    global logged_user
    if not users:
        create_user()
        return
    username = input("Nome de usuário: ")
    if username not in users:
        print("Usuário não encontrado.")
        return
    password = getpass.getpass("Senha: ")
    if check_password(users[username], password):
        logged_user = username
        print(f"Usuário '{username}' logado com sucesso.")
    else:
        print("Senha incorreta.")

def allocate_memory():
    for i in range(len(memory)):
        if memory[i] == 0:
            memory[i] = 1
            return i
    raise MemoryError("Memória insuficiente.")

def deallocate_memory(index):
    if 0 <= index < len(memory):
        memory[index] = 0

def execute_command(command, file_path=None):
    global file_ownership
    pid = os.fork()
    if pid == 0:
        # Processo filho
        os.execvp(command[0], command)
    else:
        # Processo pai
        os.wait()
        print(f"Processo {pid} executado com sucesso.")
        if file_path:
            file_ownership[file_path] = logged_user  # Definir propriedade do arquivo/diretório

def list_dir(directory=None):
    directory = directory or os.getcwd()
    if os.path.exists(directory):
        for item in os.listdir(directory):
            print(item)
    else:
        print("Diretório não encontrado.")

def create_file(file_path):
    directory, filename = os.path.split(file_path)
    directory = directory or os.getcwd()
    if not os.path.exists(directory):
        print("Diretório não encontrado.")
        return
    if os.path.exists(file_path):
        print("Arquivo já existe.")
        return
    allocate_memory()
    with open(file_path, "w") as file:
        file.write("".join(random.choices(string.ascii_letters + string.digits, k=50)))
    file_ownership[file_path] = logged_user
    print(f"Arquivo {file_path} criado.")

def delete_file(file_path):
    if file_path in file_ownership and file_ownership[file_path] != logged_user:
        print("Permissão negada.")
        return
    if os.path.exists(file_path):
        os.remove(file_path)
        del file_ownership[file_path]
        print(f"Arquivo {file_path} removido.")
    else:
        print("Arquivo não encontrado.")

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        file_ownership[dir_path] = logged_user
        print(f"Diretório {dir_path} criado.")
    else:
        print("Diretório já existe.")

def delete_directory(dir_path, force=False):
    if dir_path in file_ownership and file_ownership[dir_path] != logged_user:
        print("Permissão negada.")
        return
    if os.path.exists(dir_path):
        if force:
            subprocess.call(['rm', '-rf', dir_path])
        else:
            try:
                os.rmdir(dir_path)
            except OSError:
                print("Diretório não está vazio.")
                return
        del file_ownership[dir_path]
        print(f"Diretório {dir_path} removido.")
    else:
        print("Diretório não encontrado.")

if __name__ == "__main__":
    while True:
        if logged_user is None:
            login()
        command = input(f"{logged_user}@MiniSO> ").strip()
        if command.startswith("listar"):
            _, *args = command.split()
            list_dir(args[0] if args else None)
        elif command.startswith("criar arquivo"):
            _, _, path = command.split(maxsplit=2)
            create_file(path)
        elif command.startswith("apagar arquivo"):
            _, _, path = command.split(maxsplit=2)
            delete_file(path)
        elif command.startswith("criar diretorio"):
            _, _, path = command.split(maxsplit=2)
            create_directory(path)
        elif command.startswith("apagar diretorio"):
            _, _, path, *flags = command.split(maxsplit=3)
            delete_directory(path, force="--force" in flags)
