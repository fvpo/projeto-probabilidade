import csv
import matplotlib.pyplot as plt
import random
import statistics
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
total_mes = [0] * 12
# cidade, tipo_veiculo, dia_da_semana, fase_do_dia, data_acidente
class Acidente:
    def __init__(self, identificacao_acidente, cidade, tipo_veiculo, dia_da_semana, fase_do_dia, data_acidente):
        self.identificacao_acidente = identificacao_acidente
        self.cidade = cidade
        self.tipo_veiculo = tipo_veiculo
        self.dia_da_semana = dia_da_semana
        self.fase_do_dia = fase_do_dia
        self.data_acidente = data_acidente


def obter_mes(data_acidente):
    data = data_acidente.strip()
    if not data.isdigit() or data == "000000":
        return None

    if len(data) >= 8:
        mes = int(data[2:4])
        return mes if 1 <= mes <= 12 else None

    if len(data) == 7:
        candidatos = []

        mes_duplo = int(data[1:3])
        if 1 <= mes_duplo <= 12:
            candidatos.append(mes_duplo)

        mes_simples = int(data[2:3])
        if 1 <= mes_simples <= 12:
            candidatos.append(mes_simples)

        if candidatos:
            return candidatos[0]

        return None

    return None


def ler_arquivo():
    with open("./Acidentes.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        for dados in leitor:
            # Ignore empty rows that would otherwise create a 1-item list.
            if not dados:
                continue
            acidente = Acidente(
                identificacao_acidente=dados[0],
                cidade=dados[1],
                tipo_veiculo=dados[2],
                dia_da_semana=dados[3],
                fase_do_dia=dados[4],
                data_acidente=dados[5]
            )
            tipo_veiculo = acidente.tipo_veiculo.strip()
            
            if tipo_veiculo == "99" or tipo_veiculo == "0" or tipo_veiculo == "":    
                veiculo_arr[33] += 1
            else:
                veiculo_arr[int(acidente.tipo_veiculo) - 1] += 1


            mes = obter_mes(acidente.data_acidente)
            if mes is not None:
                total_mes[mes - 1] += 1
          
            

def plot_veiculo():
    ler_arquivo()
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
    
    veiculo_arr_sorted = sorted(veiculo_arr_stringify)
    number_of_incidents = []
    involved_vehicles = []
    for item in veiculo_arr_sorted:
        involved_vehicles.append(str(item[0]))
        number_of_incidents.append((item[1]))
    number_of_incidents = sorted(number_of_incidents, reverse=True)

    plt.bar(involved_vehicles, number_of_incidents)
    plt.xticks(rotation=90)
    plt.xlabel('Tipo de Veículo')
    plt.ylabel('Número de Acidentes')
    
    plt.axhline(media, color='black', linestyle='-', linewidth=1, label='Média (μ)')
    plt.axhline(media + (2 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='+2σ')
    plt.axhline(media + (1 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='+1σ')
    
    plt.legend()
    plt.show()


def plot_mes():
    ler_arquivo()
    media = statistics.mean(total_mes)
    desvio_padrao = statistics.pstdev(total_mes)

    rng = random.Random(42)
    normal_mes = [max(0, round(rng.gauss(media, desvio_padrao))) for _ in total_mes]

    mes_labels = [f'{dict_mes.get(str(i+1), f"Mês {i+1}")}' for i in range(12)]
    plt.bar(mes_labels, total_mes, label='Total de Acidentes', color='blue')
    plt.plot(mes_labels, normal_mes, color='orange', marker='o', linewidth=2, label='Distribuição gaussiana simulada')

    plt.axhline(media, color='black', linestyle='-', linewidth=1, label='Média (μ)')
    plt.axhline(media + (2 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='+2σ')
    plt.axhline(media - (2 * desvio_padrao), color='green', linestyle='--', linewidth=1, label='-2σ')
    plt.axhline(media + (3 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='+3σ')
    plt.axhline(media - (3 * desvio_padrao), color='red', linestyle=':', linewidth=1, label='-3σ')

    plt.xlabel('Mês')
    plt.ylabel('Número de Acidentes')
    plt.legend()
    plt.show()

plot_mes()

plot_veiculo()
