import csv
import logging
from collections import Counter, defaultdict
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s; Line:%(lineno)s; %(levelname)s: %(message)s",
                    datefmt="%d-%b-%Y %H:%M")

# Leitura e Armazenamento do arquivo CSV 
def read_csv(data):
  path = input("Escreva o caminho do ficheiro Tweets.csv: ")
    name = "Tweets.csv"
    path_name = os.path.join(path, name)

    try:
        with open(data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            if not rows:
                logging.warning("O arquivo CSV está vazio.")
            return rows
    except csv.Error as e:
        logging.error(f"Erro ao processar o CSV: {e}")
        return []
    except FileNotFoundError:
        logging.error(f"Erro: O arquivo '{data}' não foi encontrado.")
        return []

def open_arq(data):
    rows = read_csv(data)
    return {index: row for index, row in enumerate(rows, start=1)}

# Analise por sentimento (Vasco)
def cont_sent(data):
    linhas = read_csv(data)
    if not linhas:
        return Counter()

    sentimentos = Counter(linha['airline_sentiment'] for linha in linhas)
    logging.info("Número de tweets por sentimento:")
    for sentimento, quantidade in sentimentos.items():
        logging.info(f"{sentimento.capitalize()}: {quantidade}")
    return sentimentos

def perc_sent(data):
    linhas = read_csv(data)
    if not linhas:
        return

    contagem_por_companhia = defaultdict(Counter)
    contagem_total = Counter()
    total_tweets_geral = len(linhas)

    for linha in linhas:
        companhia = linha['airline']
        sentimento = linha['airline_sentiment']
        contagem_por_companhia[companhia][sentimento] += 1
        contagem_total[sentimento] += 1

    logging.info("\nPercentagem total de sentimentos para todas as companhias aéreas:")
    for sentimento, quantidade in contagem_total.items():
        porcentagem = (quantidade / total_tweets_geral) * 100
        logging.info(f"{sentimento.capitalize()}: {quantidade} tweets ({porcentagem:.2f}%)")

    logging.info("\nPercentagem de sentimentos por companhia aérea:")
    for companhia, contagem_sentimentos in contagem_por_companhia.items():
        total_tweets_companhia = sum(contagem_sentimentos.values())
        logging.info(f"\n{companhia} (Total: {total_tweets_companhia} tweets):")
        for sentimento, quantidade in contagem_sentimentos.items():
            porcentagem = (quantidade / total_tweets_companhia) * 100
            logging.info(f"  {sentimento.capitalize()}: {quantidade} tweets ({porcentagem:.2f}%)")

def twt_pos(data):
    linhas = read_csv(data)
    if not linhas:
        return None, 0
    contagem_positivos = Counter(linha['airline'] for linha in linhas if linha['airline_sentiment'] == 'positive')
    if contagem_positivos:
        companhia_mais_positivos, total_positivos = contagem_positivos.most_common(1)[0]
        logging.info(f"A companhia aérea com mais tweets positivos é {companhia_mais_positivos} com {total_positivos} tweets.")
        return companhia_mais_positivos, total_positivos
    logging.warning("Nenhuma companhia aérea com tweets positivos encontrada.")
    return None, 0

def avg_rt(data):
    linhas = read_csv(data)
    if not linhas:
        return {}
    soma_retweets = defaultdict(int)
    contagem_sentimentos = defaultdict(int)
    for linha in linhas:
        sentimento = linha.get('airline_sentiment')
        retweets = linha.get('retweet_count', '0')
        try:
            retweets = int(retweets)
        except ValueError:
            retweets = 0
        soma_retweets[sentimento] += retweets
        contagem_sentimentos[sentimento] += 1
    medias = {}
    for sentimento, soma in soma_retweets.items():
        if contagem_sentimentos[sentimento] > 0:
            media = soma / contagem_sentimentos[sentimento]
            medias[sentimento] = media
            logging.info(f"{sentimento.capitalize()}: {media:.2f} retweets em média.")
    return medias

# Analise por companhia (Felipe)

def airlines(data):
    rows = read_csv(data)
    return list({row['airline'] for row in rows if 'airline' in row})

def twt_neg(data):
    rows = read_csv(data)
    negtweets = Counter()
    for row in rows:
        if row.get('airline_sentiment') == 'negative':
            negtweets[row['airline']] += 1
    result = negtweets.most_common(1)
    if result:
        logging.info(f"Companhia com mais tweets negativos: {result[0][0]} ({result[0][1]} tweets)")
    else:
        logging.warning("Nenhum tweet negativo encontrado.")
    return result[0] if result else None

def twt_airline(data):
    rows = read_csv(data)
    contador_tweets = Counter(row['airline'] for row in rows if 'airline' in row)
    logging.info(f"Contagem de tweets por companhia: {dict(contador_tweets)}")
    return dict(contador_tweets)

def airline_filter(data):
    rows = read_csv(data)
    airlines = sorted({row['airline'] for row in rows if 'airline' in row})
    if not airlines:
        logging.warning("Nenhuma companhia aérea encontrada nos dados.")
        return []

    logging.info("Companhias disponíveis:")
    for i, airline in enumerate(airlines, start=1):
        print(f"{i}. {airline}")
    try:
        escolha = int(input("Selecione a companhia aérea pelo número: "))
        if 1 <= escolha <= len(airlines):
            airline = airlines[escolha - 1]
            tweets_filtrados = [row for row in rows if row.get('airline') == airline]
            logging.info(f"{len(tweets_filtrados)} tweets encontrados para a companhia aérea '{airline}'.")
            return tweets_filtrados
        else:
            logging.warning("Escolha inválida.")
    except ValueError:
        logging.warning("Entrada inválida. Por favor, insira um número.")
    return []

# Processamento Temporal (Tiago)

data_dict = open_arq(data)

def maxday(data_dict):
    dias = {}
    for row in data_dict.values():
        tweet_created = row["tweet_created"]
        tweet_date = tweet_created.split(" ")[0]

        if tweet_date not in dias:
            dias[tweet_date] = 1
        else:
            dias[tweet_date] += 1

    max_day = max(dias, key=dias.get)
    return max_day, dias[max_day]

def counthour(data_dict):
    contador_horas = {}
    for row in data_dict.values():
        tweet_created = row["tweet_created"]
        hora = tweet_created.split(" ")[1].split(":")[0]

        if hora not in contador_horas:
            contador_horas[hora] = 1
        else:
            contador_horas[hora] += 1

    horas_ordenadas = sorted(contador_horas.items(), key=lambda x: x[1], reverse=True)
    return horas_ordenadas

def count_day(data_dict):
    dias = {}
    for row in data_dict.values():
        tweet_created = row["tweet_created"]
        tweet_date = tweet_created.split(" ")[0]

        if tweet_date not in dias:
            dias[tweet_date] = 1
        else:
            dias[tweet_date] += 1

    dias_ordenados = sorted(dias.items(), key=lambda x:x[1], reverse=True)
    return dias_ordenados

def extrair_mes(data_dict, mes_filtro=None):
    if mes_filtro is None:
        mes_filtro = input('Insira um mês a filtrar (e.g., "02", "04", "11"): ').strip()

    try:
        contador_meses = {}
        for row in data_dict.values():
            tweet_created = row["tweet_created"]
            tweet_date = tweet_created.split(" ")[0]
            mes = tweet_date.split("-")[1]

            if mes not in contador_meses:
                contador_meses[mes] = 1
            else:
                contador_meses[mes] += 1

        if mes_filtro in contador_meses:
            return f"Total de tweets no mês {mes_filtro}: {contador_meses[mes_filtro]}"
        elif mes_filtro.lower() == "all":
            return contador_meses
        else:
            raise ValueError(f"O mês '{mes_filtro}' não foi encontrado nos dados.")

    except KeyError:
        print("Erro: O campo 'tweet_created' está ausente nos dados.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def countyear(data_dict):
    try:
        ano_filtro = input('Insira um ano a filtrar (e.g., "2024", "2023"): ').strip()
        contador_ano = {}

        for row in data_dict.values():
            tweet_created = row["tweet_created"]
            tweet_date = tweet_created.split(" ")[0]
            ano = tweet_date.split("-")[0]

            if ano not in contador_ano:
                contador_ano[ano] = 1
            else:
                contador_ano[ano] += 1

        if ano_filtro in contador_ano:
            return f"Total de tweets no ano '{ano_filtro}': {contador_ano[ano_filtro]}"
        elif ano_filtro.lower() == "all":
            return contador_ano
        else:
            raise ValueError(f"O ano '{ano_filtro}' não foi encontrado nos dados.")

    except KeyError:
        print("Erro: O campo 'tweet_created' está ausente nos dados.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
