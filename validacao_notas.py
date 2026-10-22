from decimal import Decimal, InvalidOperation

from leitor_notas import carregar_alunos

from pathlib import Path

import pandas as pd


CAMPOS_NOTAS = ["Nota01", "Nota02", "TF01", "TF02"]


def validar_aluno(aluno):
    dados = aluno.to_dict()
    pendencias = []

    # Ajusta apenas os espaços, sem alterar o arquivo original.
    dados["Nome"] = " ".join(dados["Nome"].split())
    dados["RA"] = dados["RA"].strip()

    if not dados["Nome"]:
        pendencias.append("Nome ausente")

    if not dados["RA"]:
        pendencias.append("RA ausente")
    elif not dados["RA"].isascii() or not dados["RA"].isdigit():
        pendencias.append("RA contém caracteres diferentes de números")

    for campo in CAMPOS_NOTAS:
        texto = dados[campo].strip()

        if not texto:
            pendencias.append(f"{campo}: valor ausente")
            continue

        try:
            numero = Decimal(texto.replace(",", "."))
        except InvalidOperation:
            pendencias.append(f"{campo}: valor não numérico ({texto})")
            continue

        if not numero.is_finite():
            pendencias.append(f"{campo}: valor não finito")
            continue

        if numero < 0:
            pendencias.append(f"{campo}: valor negativo")
            continue

        if numero > Decimal("10"):
            pendencias.append(
                f"{campo}: valor {texto} acima de 10 na escala simulada"
            )
            continue

        dados[campo] = format(numero, "f")

    return dados, pendencias


def analisar_alunos():
    alunos = carregar_alunos()
    resultados = []

    # Verifica repetições sem escolher qual registro seria o correto.
    registros_ra = alunos["RA"].str.strip()
    registros_nome = alunos["Nome"].map(
        lambda nome: " ".join(nome.split()).casefold()
    )

    for indice, aluno in alunos.iterrows():
        dados, pendencias = validar_aluno(aluno)

        if dados["RA"] and (registros_ra == dados["RA"]).sum() > 1:
            pendencias.append("RA repetido no arquivo")

        nome_comparacao = dados["Nome"].casefold()

        if nome_comparacao and (
            registros_nome == nome_comparacao
        ).sum() > 1:
            pendencias.append("Nome repetido: conferir identificação")

        resultados.append({
            "linha": indice + 2,
            "dados": dados,
            "pendencias": pendencias
        })

    return resultados

def salvar_pendencias(resultados):
    pasta = Path(__file__).resolve().parent / "relatorios"
    pasta.mkdir(exist_ok=True)

    linhas = []

    for resultado in resultados:
        for pendencia in resultado["pendencias"]:
            linhas.append({
                "linha_csv": resultado["linha"],
                "nome": resultado["dados"]["Nome"],
                "ra": resultado["dados"]["RA"],
                "pendencia": pendencia
            })

    relatorio = pd.DataFrame(
        linhas,
        columns=["linha_csv", "nome", "ra", "pendencia"]
    )
    relatorio.to_csv(
        pasta / "pendencias.csv",
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nRelatório salvo em relatorios/pendencias.csv")
    resultados = analisar_alunos()

MEDIA_APROVACAO = Decimal("6.0")


def calcular_resultado(dados):
    nota_1 = Decimal(dados["Nota01"])
    tf_1 = Decimal(dados["TF01"])
    nota_2 = Decimal(dados["Nota02"])
    tf_2 = Decimal(dados["TF02"])

    periodo_1 = (nota_1 * 8 + tf_1 * 2) / 10
    periodo_2 = (nota_2 * 8 + tf_2 * 2) / 10
    media = (periodo_1 + periodo_2) / 2

    situacao = "Reprovado"

    if media >= MEDIA_APROVACAO:
        situacao = "Aprovado"

    return periodo_1, periodo_2, media, situacao

if __name__ == "__main__":
    resultados = analisar_alunos()
    salvar_pendencias(resultados)
    total_pendentes = 0

    for resultado in resultados:
        if resultado["pendencias"]:
            total_pendentes += 1
            print(
                f"\nLinha {resultado['linha']} — "
                f"{resultado['dados']['Nome']}"
            )

            for pendencia in resultado["pendencias"]:
                print(f"  - {pendencia}")

    print(f"\nTotal de registros: {len(resultados)}")
    print(f"Com pendências: {total_pendentes}")
    print(f"Sem pendências básicas: {len(resultados) - total_pendentes}")
    print("Escalas das notas e regras de aprovação ainda não validadas.")