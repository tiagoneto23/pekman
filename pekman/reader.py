import csv

def open_arq(data):
    try:
        with open(data, encoding='utf-8') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rows = list(readCSV)
            header = rows[0]
            data_dict = {
                int(row[0]): dict(zip(header[1:], row[1:]))
                for row in rows[1:]
            }
            return data_dict

    except FileNotFoundError:
        print(f"Erro: O arquivo '{data}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao abrir o arquivo: {e}")


path = r"C:/Users/traba/PROG/MyModules/archive/"
file_name = "Tweets.csv"
data = path + file_name


print(open_arq(data))
