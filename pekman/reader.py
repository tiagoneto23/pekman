import os

base_path = r"C:\Users\traba\PROG\MyModules\archive"
file_name = "Tweets.csv"

file_path = os.path.join(base_path, file_name)

if os.path.exists(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:  # Certifique-se de usar o encoding correto
        linha = file.readline()  # Ler o cabeçalho (primeira linha)
        print("Linha:", linha.strip())

        print("\nAlgumas linhas do arquivo:")
        for i, line in enumerate(file):
            print(line.strip())
            if i >= 4:  # Limitar a leitura a 5 linhas (para não sobrecarregar o console)
                break
else:
    print(f"Arquivo '{file_name}' não encontrado no diretório '{base_path}'.")


