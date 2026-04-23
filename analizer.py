import csv
import matplotlib.pyplot as plt
import random
import statistics
from datetime import date


dict_tipo_veículo = {
    "01": "Automóvel",
    "02": "Bicicleta/Bicicleta elétrica",
    "03": "Bonde",
    "04": "Caminhão",
    "05": "Caminhão-trator",
    "06": "Caminhonete",
    "07": "Camioneta",
    "08": "Carro de mão",
    "09": "Carroça",
    "10": "Charrete",
    "11": "Ciclo",
    "12": "Ciclomotor",
    "13": "Micro-ônibus",
    "14": "Motocicleta",
    "15": "Motoneta",
    "16": "Motorcasa (Motorhome)",
    "17": "Ônibus",
    "18": "Quadriciclo",
    "19": "Reboque",
    "20": "Semirreboque",
    "21": "Trailer",
    "22": "Trator",
    "23": "Treminhão",
    "24": "Triciclo",
    "25": "Utilitário",
    "26": "Veículo articulado",
    "27": "Veículo conjugado",
    "28": "Veículo misto",
    "29": "Patinete/Patinete elétrico",
    "30": "Metrô",
    "31": "Trem",
    "32": "Trólebus",
    "33": "Veículo de serviço",
    "99": "Desconhecido"
}
dict_mes = {
    "1": "janeiro",
    "2": "fevereiro",
    "3": "março",
    "4": "abril",
    "5": "maio",
    "6": "junho",
    "7": "julho",
    "8": "agosto",
    "9": "setembro",
    "10": "outubro",
    "11": "novembro",
    "12": "dezembro"
}
veiculo_arr = [0] * 34
media_mes = []
total_mes22 = [0] * 12
total_mes23 = [0] * 12
total_mes24 = [0] * 12
# cidade, tipo_veiculo, dia_da_semana, fase_do_dia, data_acidente
class Acidente:
    def __init__(self, identificacao_acidente, cidade, tipo_veiculo, data_acidente):
        self.identificacao_acidente = identificacao_acidente
        self.cidade = cidade
        self.tipo_veiculo = tipo_veiculo
        self.data_acidente = data_acidente


def obter_mes(data_acidente, mes_referencia=None):
    data = data_acidente.strip()
    if not data.isdigit() or data == "000000":
        return None

    def data_valida(ano, mes, dia):
        try:
            date(ano, mes, dia)
            return True
        except ValueError:
            return False

    if len(data) == 8:
        dia = int(data[0:2])
        mes = int(data[2:4])
        ano = int(data[4:8])
        if data_valida(ano, mes, dia):
            return mes
        return None

    if len(data) == 7:
        ano = int(data[3:7])
        candidatos = []

        # Opção 1: DMMYYYY (dia com 1 dígito, mês com 2 dígitos)
        dia_dmmyyyy = int(data[0:1])
        mes_dmmyyyy = int(data[1:3])
        if data_valida(ano, mes_dmmyyyy, dia_dmmyyyy):
            candidatos.append(("dmmyyyy", mes_dmmyyyy))

        # Opção 2: DDMYYYY (dia com 2 dígitos, mês com 1 dígito)
        dia_ddmyyyy = int(data[0:2])
        mes_ddmyyyy = int(data[2:3])
        if data_valida(ano, mes_ddmyyyy, dia_ddmyyyy):
            candidatos.append(("ddmyyyy", mes_ddmyyyy))

        if len(candidatos) == 1:
            return candidatos[0][1]

        if len(candidatos) == 2:
            meses_candidatos = sorted([candidatos[0][1], candidatos[1][1]])

            # Se houver mês anterior conhecido, usa a ordem cronológica para desempatar.
            if mes_referencia is not None:
                meses_na_frente = [m for m in meses_candidatos if m >= mes_referencia]
                if meses_na_frente:
                    return meses_na_frente[0]
                return meses_candidatos[-1]

            return meses_candidatos[0]

        return None

    return None


def ler_arquivo():
    id_acidente_anterior = None
    ultimo_mes = None
    with open("./Acidentes24.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        for dados in leitor:
            # Ignore empty rows that would otherwise create a 1-item list.
            if not dados:
                continue
            acidente = Acidente(
                identificacao_acidente=dados[0],
                cidade=dados[1],
                tipo_veiculo=dados[2],
                data_acidente=dados[3]
            )
            tipo_veiculo = acidente.tipo_veiculo.strip()
            
            if tipo_veiculo == "99" or tipo_veiculo == "0" or tipo_veiculo == "":    
                veiculo_arr[33] += 1
            else:
                veiculo_arr[int(acidente.tipo_veiculo) - 1] += 1

            if acidente.identificacao_acidente != id_acidente_anterior:   
                mes = obter_mes(acidente.data_acidente, ultimo_mes)
                if mes is not None:
                    total_mes24[mes - 1] += 1
                    ultimo_mes = mes
            id_acidente_anterior = acidente.identificacao_acidente
    id_acidente_anterior = None
    ultimo_mes = None
    with open("./Acidentes22.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        for dados in leitor:
            if not dados:
                continue
            acidente = Acidente(
                identificacao_acidente=dados[0],
                cidade=0,
                tipo_veiculo=0,
                data_acidente=dados[1]
            )
            if acidente.identificacao_acidente != id_acidente_anterior:   
                mes = obter_mes(acidente.data_acidente, ultimo_mes)
                if mes is not None:
                    total_mes22[mes - 1] += 1
                    ultimo_mes = mes
            id_acidente_anterior = acidente.identificacao_acidente
    with open("./Acidentes23.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        i = 0
        for dados in leitor:
            total_mes23[i] = int(dados[0])
            i += 1
          
def plot_veiculo():
    veiculo_arr_stringify = []
    for i, item in enumerate(veiculo_arr):
        if i < 9:
            label = dict_tipo_veículo['0' + str(i + 1)]
        elif i < 33:
            label = dict_tipo_veículo[str(i + 1)]
        else:
            label = dict_tipo_veículo['99']
        if item != 0:
            veiculo_arr_stringify.append((label, item))
    media = statistics.mean(veiculo_arr)
    desvio_padrao = statistics.pstdev(veiculo_arr)
    
    veiculo_arr_sorted = sorted(veiculo_arr_stringify, key=lambda x: x[1], reverse=True)
    number_of_incidents = []
    vehicle_type = []
    i = 0
    for item in veiculo_arr_sorted:
        vehicle_type.append(item[0])
        number_of_incidents.append((item[1]))
    plt.bar(vehicle_type, number_of_incidents)
    plt.xticks(rotation=90)
    plt.xlabel('Tipo de Veículo')
    plt.ylabel('Número de Acidentes')
    
    plt.axhline(media, color='black', linestyle='-', linewidth=1, label='Média (μ)')
    plt.axhline(media + (3 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='+3σ')
    plt.axhline(media + (2 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='+2σ')
    
    plt.legend()
    plt.show()

def plot_mes(ano_atual, media_anual, titulo):
    media = statistics.mean(media_anual)
    desvio_padrao = statistics.pstdev(media_anual)
    mes_labels = [f'{dict_mes.get(str(i+1), f"Mês {i+1}")}' for i in range(12)]
    plt.bar(mes_labels, ano_atual, label='Total de Acidentes', color='blue')
    plt.plot(mes_labels, media_anual, color='orange', marker='o', linewidth=2, label='Média dos anos de 2022 a 2024')

    plt.axhline(media, color='black', linestyle='-', linewidth=1, label='Média (μ)')
    plt.axhline(media + (2 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='+2σ')
    plt.axhline(media - (2 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='-2σ')
    plt.axhline(media + (3 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='+3σ')
    plt.axhline(media - (3 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='-3σ')

    plt.xlabel('Mês')
    plt.ylabel('Número de Acidentes')
    plt.title(titulo)
    plt.legend()
    plt.show()
def definir_media_mes():
    for i in range(12):
        media_mes.append(statistics.mean([total_mes22[i], total_mes23[i], total_mes24[i]]))
def main():
    ler_arquivo()
    definir_media_mes()
    plot_veiculo()
    plot_mes(total_mes24, media_mes, "Total de Acidentes por Mês em 2024")
main()