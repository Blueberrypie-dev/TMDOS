from System.Core.Boot import clear
from System.Core.Paths import AppDir
import json

# =========================================
# FUNÇÃO PARA EDITAR USUÁRIO E SENHA
# =========================================

def edit_account():

    usuario = input("Username: ")
    nova_senha = input("New password: ")

    file_path = AppDir / "Settings" / "users.json"

    try:
        # Abre o arquivo JSON
        with open(file_path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Verifica se o usuário existe
        if usuario in dados:

            # Altera a senha
            dados[usuario] = nova_senha

            # Salva o arquivo atualizado
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4)

            print("✅ Senha atualizada com sucesso!")

        else:
            print("❌ Usuário não encontrado.")

    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")

    except json.JSONDecodeError:
        print("❌ JSON inválido.")
    clear()