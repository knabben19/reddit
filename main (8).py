import json
import os
from datetime import datetime

DATA_FILE = "reddit_data.json"

# -------------------------
# Carregar ou criar banco
# -------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "posts": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()
current_user = None

# -------------------------
# Usuário
# -------------------------
def register():
    username = input("Novo usuário: ")

    for user in data["users"]:
        if user["username"] == username:
            print("Usuário já existe!")
            return

    data["users"].append({
        "username": username,
        "karma": 0
    })

    save_data(data)
    print("Usuário criado com sucesso!")

def login():
    global current_user
    username = input("Digite seu usuário: ")

    for user in data["users"]:
        if user["username"] == username:
            current_user = user
            print(f"Logado como {username}")
            return

    print("Usuário não encontrado.")

# -------------------------
# Posts
# -------------------------
def create_post():
    if not current_user:
        print("Você precisa estar logado!")
        return

    title = input("Título do post: ")
    content = input("Conteúdo: ")

    post = {
        "id": len(data["posts"]) + 1,
        "author": current_user["username"],
        "title": title,
        "content": content,
        "likes": 0,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    data["posts"].append(post)
    save_data(data)
    print("Post criado com sucesso!")

def list_posts():
    if not data["posts"]:
        print("Nenhum post ainda.")
        return

    for post in sorted(data["posts"], key=lambda x: x["likes"], reverse=True):
        print("\n------------------------")
        print(f"ID: {post['id']}")
        print(f"Título: {post['title']}")
        print(f"Autor: {post['author']}")
        print(f"Karma: {post['likes']}")
        print(f"Data: {post['created_at']}")
        print(f"Conteúdo: {post['content']}")
        print("------------------------")

def like_post():
    if not current_user:
        print("Você precisa estar logado!")
        return

    try:
        post_id = int(input("ID do post para curtir: "))
    except ValueError:
        print("ID inválido.")
        return

    for post in data["posts"]:
        if post["id"] == post_id:
            if post["author"] == current_user["username"]:
                print("Você não pode curtir seu próprio post.")
                return

            post["likes"] += 1

            for user in data["users"]:
                if user["username"] == post["author"]:
                    user["karma"] += 1

            save_data(data)
            print("Post curtido!")
            return

    print("Post não encontrado.")

# -------------------------
# Menu
# -------------------------
def menu():
    while True:
        print("\n====== REDDIT CLI ======")
        print("1 - Registrar")
        print("2 - Login")
        print("3 - Criar Post")
        print("4 - Listar Posts")
        print("5 - Curtir Post")
        print("6 - Ver Meu Karma")
        print("0 - Sair")

        choice = input("Escolha: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            create_post()
        elif choice == "4":
            list_posts()
        elif choice == "5":
            like_post()
        elif choice == "6":
            if current_user:
                print(f"Seu karma: {current_user['karma']}")
            else:
                print("Faça login primeiro.")
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

menu()