# 💰 Motor de Conciliação Financeira (Fintech Architecture)

Este projeto resolve um problema real, crítico e diário enfrentado por e-commerces, fintechs e empresas de médio/grande porte: a **automação da auditoria financeira (conciliação)**. 

Diariamente, setores financeiros perdem horas cruzando planilhas de vendas internas com os extratos reais enviados pelos bancos para garantir que cada centavo vendido realmente entrou no caixa. Inconsistências manuais geram prejuízos ocultos gigantescos. Este sistema automatiza esse processo de ponta a ponta.

---

## 🚀 Funcionalidades Principais

* **Ingestão de Dados Resiliente:** Lê e valida arquivos `.csv` de vendas e de extratos bancários, aplicando validações rigorosas de cabeçalho e tratamento de tipos de dados.
* **Processamento de Alta Performance:** Utiliza tabelas de espelhamento hash (Dicionários Python) para garantir busca em tempo linear ($O(1)$), permitindo processar milhares de linhas em milissegundos, evitando loops aninhados lentos ($O(n^2)$).
* **Auditoria de Precisão (Fix de Centavos):** Identifica automaticamente transações ausentes no banco (possíveis fraudes ou falhas de integração) ou divergências de valores, corrigindo problemas nativos de ponto flutuante do Python (precisão de centavos com `round()`).
* **Exportação Automatizada:** Gera um relatório consolidado em `.csv` (`divergencias.csv`) com todas as inconsistências prontas para a equipe financeira auditar no Excel.

---

## 🛠️ Tecnologias e Conceitos Aplicados

* **Python 3.x** nativo (foco em performance e zero dependências externas pesadas).
* **Programação Orientada a Objetos (POO):** Divisão clara de responsabilidades em camadas utilizando classes dedicadas (`Transacao`, `LeitorCSV`, `Conciliador`).
* **Tratamento de Exceções Robusto:** Proteção contra arquivos corrompidos, caminhos inválidos, colunas ausentes (`KeyError`) ou dados mal formatados (`ValueError`).
* **Testes Automatizados (Test-Driven Mindset):** Cobertura de cenários críticos e regras de negócio usando o módulo nativo `unittest`.

---

## 📂 Estrutura do Projeto

```text
├── conciliador.py          # Código principal do motor e ingestão de dados
├── test_conciliador.py     # Conjunto de testes unitários automatizados
├── .gitignore              # Proteção para não subir dados sensíveis de produção
└── README.md               # Documentação técnica do projeto
