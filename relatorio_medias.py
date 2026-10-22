from pathlib import Path

import pandas as pd

from validacao_notas import analisar_alunos, calcular_resultado


def gerar_relatorio():
    resultados = analisar_alunos()
    linhas = []

    for resultado in resultados:
        # Registros com pendências ficam no relatório de revisão.
        if resultado["pendencias"]:
            continue

        dados = resultado["dados"]
        periodo_1, periodo_2, media, situacao = calcular_resultado(dados)

        linhas.append({
            "linha_csv": resultado["linha"],
            "ra": dados["RA"],
            "nome": dados["Nome"],
            "periodo_1": str(periodo_1),
            "periodo_2": str(periodo_2),
            "media_final": str(media),
            "situacao_simulada": situacao
        })

    pasta = Path(__file__).resolve().parent / "relatorios"
    pasta.mkdir(exist_ok=True)

    relatorio = pd.DataFrame(
        linhas,
        columns=[
            "linha_csv",
            "ra",
            "nome",
            "periodo_1",
            "periodo_2",
            "media_final",
            "situacao_simulada"
        ]
    )

    caminho = pasta / "medias_simuladas.csv"
    relatorio.to_csv(caminho, sep=";", index=False, encoding="utf-8-sig")

    print(f"Relatório salvo em: {caminho}")
    print(f"Alunos incluídos: {len(linhas)}")
    print("Regra simulada: notas de 0 a 10, pesos 8 e 2 e aprovação a partir de 6.")


if __name__ == "__main__":
    gerar_relatorio()