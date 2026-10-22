from pathlib import Path

import pandas as pd


# Localiza o CSV a partir da pasta deste script.
CAMINHO_DADOS = Path(__file__).resolve().parent / "dados" / "notas_alunos.csv"


def carregar_alunos():
    # Preserva os valores como texto, incluindo zeros e campos vazios.
    return pd.read_csv(
        CAMINHO_DADOS,
        sep=";",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig"
    )


if __name__ == "__main__":
    alunos = carregar_alunos()

    print("Colunas encontradas:")
    print(alunos.columns.tolist())

    print("\nPrimeiros cinco registros:")
    print(alunos.head().to_string(index=False))

    print(f"\nTotal de registros: {len(alunos)}")