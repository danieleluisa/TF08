# Projeto de lançamento de notas

Projeto de RPA para ler notas de um arquivo CSV, validar os dados e
preencher um formulário usando Python e PyAutoGUI.

## Funcionalidades

- Leitura dos dados mantendo o RA como texto.
- Busca de aluno por RA ou nome completo.
- Identificação de dados ausentes, inválidos ou que precisam de revisão.
- Cálculo de médias e situação em uma simulação.
- Preenchimento e envio supervisionado ao formulário.
- Controle local de envios confirmados para evitar duplicatas.
- Relatórios de pendências e médias simuladas.

## Regra de cálculo simulada

Para demonstrar o projeto, foi considerada uma escala de 0 a 10,
com peso 8 para a nota e peso 2 para o TF:

- Período 1: `(Nota01 * 8 + TF01 * 2) / 10`
- Período 2: `(Nota02 * 8 + TF02 * 2) / 10`
- Média final: `(Período 1 + Período 2) / 2`

A aprovação foi simulada com média mínima 6,0. A escala, a média mínima
e a combinação dos períodos precisam de confirmação do professor.

## Execução no Windows

Instale as dependências no ambiente virtual:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Analise os dados:

    .\.venv\Scripts\python.exe validacao_notas.py

Gere o relatório de médias:

    .\.venv\Scripts\python.exe relatorio_medias.py

Execute o robô:

    .\.venv\Scripts\python.exe bot_notas.py

O robô pede acompanhamento durante o preenchimento e o envio.
Para interromper o PyAutoGUI, mova o mouse para um canto da tela.

## Arquivos de dados e relatórios

O arquivo original fica em `dados/notas_alunos.csv`. Os relatórios ficam
na pasta `relatorios`. Registros com pendências precisam ser revisados;
o programa não inventa valores ausentes.

O arquivo `relatorios/enviados.csv` controla os RAs confirmados
localmente. Antes de retomar uma execução, confira se ele corresponde
às respostas do formulário.