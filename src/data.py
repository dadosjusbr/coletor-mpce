import sys
import os

import pandas as pd

# Se for erro de não existir planilhas o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _read(file, year, month):
    try:
        data = pd.read_html(file)
        # A partir de 09/2023, há uma modificação no html (botões para download em outros formatos)
        # Essa modificação torna necessário modificar o índice para acessar a planilha de dados no html 
        data = data[1]
        data = data[: -1]
        data = data.to_numpy()

    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data


def load(file_names, year, month, output_path):
    """Carrega os arquivos passados como parâmetros.
    
     :param file_names: slice contendo os arquivos baixados pelo coletor.
    Os nomes dos arquivos devem seguir uma convenção e começar com 
    Membros ativos-contracheque e Membros ativos-Verbas Indenizatorias
     :param year e month: usados para fazer a validação na planilha de controle de dados
     :return um objeto Data() pronto para operar com os arquivos
    """

    contracheque = _read([c for c in file_names if "contracheque" in c][0], year, month)
    indenizatorias = _read([i for i in file_names if "verbas-indenizatorias" in i][0], year, month)

    return Data(contracheque, indenizatorias, year, month, output_path)


class Data:
    def __init__(self, contracheque, indenizatorias, year, month, output_path):
        self.year = year
        self.month = month
        self.output_path = output_path
        self.contracheque = contracheque
        self.indenizatorias = indenizatorias

    def validate(self):
        """
         Validação inicial dos arquivos passados como parâmetros.
        Aborta a execução do script em caso de erro.
         Caso o validade fique pare o script na leitura da planilha 
        de controle de dados dara um erro retornando o codigo de erro 4,
        esse codigo significa que não existe dados para a data pedida.
        """

        if not (
            os.path.isfile(
                f"{self.output_path}/membros-ativos-contracheque-{self.month}-{self.year}.html"
            )
            or os.path.isfile(
                f"{self.output_path}/membros-ativos-verbas-indenizatorias-{self.month}-{self.year}.html"
            )
        ):
            sys.stderr.write(f"Não existe planilhas para {self.month}/{self.year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)
