from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    # URL sem semantica, tem que ser feito uma rapagem na página
    # para encontrar a URL de download.
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.RASPAGEM_DIFICULTADA
    metadado.extensao = Coleta.Metadados.Extensao.HTML
    metadado.estritamente_tabular = True
    metadado.formato_consistente = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO

    return metadado
