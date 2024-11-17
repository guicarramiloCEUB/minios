import os
import hashlib
import getpass
import random
import string

users = {}
logged_user = None
memory = [0] * 100

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
        print(f"Login bem-sucedido como '{username}'.")
    else:
        print("Senha incorreta.")

def allocate_memory(size):
    # Simples alocação de memória usando first-fit
    for i in range(len(memory) - size + 1):
        if all(v == 0 for v in memory[i:i+size]):
            for j in range(i, i+size):
                memory[j] = 1
            return i
    raise MemoryError("Não há memória suficiente disponível.")

def deallocate_memory(start, size):
    for i in range(start, start + size):
        memory[i] = 0

def execute_command(command):
    pid = random.randint(1000, 9999)
    print(f"[PID {pid}] Executando: {command}")
    
    try:
        memory_size = random.randint(1, 10)
        start_mem = allocate_memory(memory_size)
        print(f"[PID {pid}] Memória alocada: {memory_size} unidades.")
        if command.startswith("listar"):
            directory = command.split(" ")[1] if len(command.split()) > 1 else "."
            print(f"Conteúdo de '{directory}': {os.listdir(directory)}")
        elif command.startswith("criar arquivo"):
            parts = command.split(" ")
            filepath = parts[2] if len(parts) > 2 else "arquivo.txt"
            with open(filepath, 'w') as f:
                f.write('Conteúdo aleatório.')
            print(f"[PID {pid}] Arquivo '{filepath}' criado.")
        elif command.startswith("apagar arquivo"):
            parts = command.split(" ")
            filepath = parts[2] if len(parts) > 2 else "arquivo.txt"
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"[PID {pid}] Arquivo '{filepath}' apagado.")
            else:
                print(f"[PID {pid}] Arquivo '{filepath}' não encontrado.")
        elif command.startswith("criar diretorio"):
            parts = command.split(" ")
            dirpath = parts[2] if len(parts) > 2 else "novo_diretorio"
            os.makedirs(dirpath, exist_ok=True)
            print(f"[PID {pid}] Diretório '{dirpath}' criado.")
        elif command.startswith("apagar diretorio"):
            parts = command.split(" ")
            dirpath = parts[2] if len(parts) > 2 else "novo_diretorio"
            if os.path.exists(dirpath) and os.path.isdir(dirpath):
                if len(os.listdir(dirpath)) == 0 or "--force" in parts:
                    os.rmdir(dirpath)
                    print(f"[PID {pid}] Diretório '{dirpath}' apagado.")
                else:
                    print(f"[PID {pid}] Diretório '{dirpath}' não está vazio.")
            else:
                print(f"[PID {pid}] Diretório '{dirpath}' não encontrado.")
        else:
            print(f"[PID {pid}] Comando '{command}' não reconhecido.")
    finally:
        deallocate_memory(start_mem, memory_size)
        print(f"[PID {pid}] Memória desalocada.")

def main():
    global logged_user
    while not logged_user:
        login()
    print(f"Bem-vindo ao MiniSO, {logged_user}!")

    while True:
        command = input("MiniSO> ")
        if command.lower() in ("sair", "exit"):
            print("Encerrando o MiniSO.")
            break
        execute_command(command)

if __name__ == "__main__":
    main()
