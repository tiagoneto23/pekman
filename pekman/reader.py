import csv
from collections import Counter 

path = r"C:/Users/traba/PROG/MyModules/archive/"
file_name = "Tweets.csv"
data = path + file_name

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
def airlines(data):
    airlines = []
    try:
        with open(data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'airline' in row and row['airline'] not in airlines:
                    airlines.append(row['airline'])
        return airlines
    except FileNotFoundError:
        print(f"Erro: O arquivo '{data}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return []

def tweets_neg(data):
    Ntweets = Counter()
    try:
        with open(data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('airline_sentiment') == 'negative':
                    Ntweets[row['airline']] += 1

        if Ntweets:
            airline, total = Ntweets.most_common(1)[0]
            return airline, total
        else:
            return None
    except FileNotFoundError:
        print(f"Ficheiro {data} não encontrado.")

def tweets_p_airline(data):
    contador_tweets = Counter()
    try:
        with open(data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'airline' in row:
                    contador_tweets[row['airline']] += 1

        return dict(contador_tweets)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{data}' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return {}

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

def airline_filter(data):
    tweets = []
    airline = input("Companhia aérea que deseja pesquisar: Virgin America, United, Southwest, Delta, US Airways, American")
    try:
        with open(data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('airline') == airline:
                    tweets.append(row)
        return tweets
    except FileNotFoundError:
        print(f"Erro: O arquivo '{data}' não foi encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return []
