
# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import CONTRACHEQUE, INDENIZACOES, HEADERS
import number


def parse_employees(fn, chave_coleta, categoria):
    employees = {}
    counter = 1
    for row in fn:
        matricula = row[0]
        name = row[1]
        if not number.is_nan(name) and not number.is_nan(matricula) and name != "0" and name != "NOME":
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = name
            membro.matricula = str(matricula)
            membro.funcao = row[2]
            membro.local_trabalho = row[3]
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
           
            membro.remuneracoes.CopyFrom(
                cria_remuneracao(row, categoria)
            )
            
            employees[matricula] = membro
            counter += 1
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        remuneracao.valor = float(number.format_value(row[value]))
        remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        if categoria == CONTRACHEQUE and value in [4]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")

        if categoria == CONTRACHEQUE and value in [13, 14, 15]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")

        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        matricula = str(row[0])
        if matricula in employees.keys():
            emp = employees[matricula]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[matricula] = emp
    return employees


def parse(data, chave_coleta, mes, ano):
    employees = {}
    folha = Coleta.FolhaDePagamento()
    try:
        employees.update(parse_employees(
                data.contracheque, chave_coleta, CONTRACHEQUE
            ))
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar contracheque ou indenizações: {}".format(e)
        )
        os._exit(1)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha