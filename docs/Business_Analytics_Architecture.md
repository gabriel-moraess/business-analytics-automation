# Business Analytics Automation

## Arquitetura Funcional

**Versão:** 1.0.0

**Última atualização:** Agosto de 2026

---

# 1. Visão Geral

O **Business Analytics Automation** é um framework desenvolvido em Python para automatizar o processo de coleta, transformação, validação, armazenamento e disponibilização de dados corporativos para análise de desempenho e suporte à tomada de decisão.

O projeto foi concebido seguindo princípios de Engenharia de Dados e Arquitetura de Software, permitindo integração com diferentes fontes de dados e múltiplas camadas de apresentação, sem depender de um ERP ou sistema específico.

Embora o desenvolvimento inicial utilize uma API pública para fins de demonstração, toda a arquitetura foi planejada para permitir futura integração com plataformas de e-commerce, ERPs, bancos de dados relacionais, planilhas Excel e outras APIs corporativas.

O framework possui uma arquitetura modular, facilitando manutenção, escalabilidade, reutilização de componentes e evolução contínua.

---

# 2. Objetivos

O projeto possui os seguintes objetivos:

* Automatizar processos de ETL (Extract, Transform and Load);
* Reduzir atividades manuais de consolidação de dados;
* Garantir qualidade e consistência das informações através de validações automatizadas;
* Persistir os dados em banco SQLite, permitindo futura migração para PostgreSQL ou SQL Server;
* Disponibilizar os dados em diferentes formatos (CSV, Excel e Parquet);
* Alimentar dashboards executivos automaticamente;
* Servir como base para projetos de Business Intelligence e Analytics;
* Demonstrar boas práticas de desenvolvimento Python para portfólio profissional.

---

# 3. Princípios da Arquitetura

Durante o desenvolvimento foram adotados os seguintes princípios:

* Arquitetura modular;
* Separação de responsabilidades;
* Código reutilizável;
* Configuração centralizada;
* Logging estruturado;
* Tratamento global de exceções;
* Testes automatizados;
* Facilidade de manutenção;
* Escalabilidade para novas integrações;
* Independência entre a camada de dados e a camada de apresentação.

---

# 4. Arquitetura do Sistema

O Business Analytics Automation foi desenvolvido seguindo uma arquitetura em camadas, onde cada módulo possui uma única responsabilidade. Essa abordagem facilita manutenção, reutilização de componentes e futuras expansões do sistema.

## Arquitetura Geral


                ┌──────────────────────────┐
                │      Data Sources        │
                │──────────────────────────│
                │ APIs                     │
                │ Excel                    │
                │ CSV                      │
                │ Banco de Dados           │
                │ ERP                      │
                └─────────────┬────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │     Extract      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Transform     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Validate      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     SQLite       │
                    └────────┬─────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   Exportações                      Dashboard
 (CSV • Excel • Parquet)         (Excel Executivo)


---

# 5. Estrutura do Projeto

A organização dos diretórios segue uma separação por responsabilidade, permitindo evolução do projeto sem acoplamento entre módulos.


Business_Analytics_Automation/

├── dashboard/
├── database/
├── dados/
│   ├── bruto/
│   └── tratado/
├── docs/
├── logs/
├── notebooks/
├── src/
│   ├── api/
│   ├── database/
│   ├── etl/
│   ├── pipeline/
│   ├── reports/
│   └── utils/
├── tests/
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt


---

# 6. Responsabilidade dos Módulos

## src/api

Responsável pela comunicação com APIs externas.

### Componentes

* APIClient
* Endpoints

Responsabilidades:

* Gerenciamento da sessão HTTP;
* Retry automático;
* Timeout;
* Headers;
* Autenticação;
* Consumo de endpoints.

---

## src/etl

Responsável pelo processo de ETL.

### Extract

Realiza a obtenção dos dados a partir das fontes configuradas.

### Transform

Executa o tratamento dos dados:

* normalização;
* padronização;
* remoção de duplicidades;
* inclusão de metadados.

### Validate

Executa validações de qualidade dos dados antes da persistência.

### Load

Exporta os dados para formatos de consumo, como CSV, Excel e Parquet.

---

## src/database

Responsável pela persistência dos dados.

Atualmente utiliza SQLite, mas foi projetado para permitir futuras integrações com bancos relacionais como PostgreSQL e SQL Server.

---

## src/pipeline

Responsável pela orquestração do fluxo ETL.

O Pipeline coordena todas as etapas do processamento, mantendo baixo acoplamento entre os módulos.

---

## src/reports

Responsável pela camada de apresentação.

Seu objetivo é atualizar automaticamente o Dashboard Excel sem alterar a lógica do ETL.

---

## src/utils

Centraliza funcionalidades compartilhadas pelo sistema.

Inclui:

* configurações;
* logging;
* utilitários;
* constantes globais.

---

## tests

Contém os testes automatizados do projeto.

Atualmente são executados testes unitários para:

* Transform;
* Validate;
* SQLiteManager;
* Load.

Essa estrutura permite validar continuamente a estabilidade da aplicação durante sua evolução.

---

# 7. Fluxo de Execução do Sistema

A execução do Business Analytics Automation é iniciada pelo arquivo `main.py`, responsável por instanciar o Pipeline e iniciar todo o processo de ETL.

O fluxo completo ocorre conforme o diagrama abaixo.

                         main.py
                            │
                            ▼
                    Inicialização
                            │
                            ▼
                      Pipeline ETL
                            │
                            ▼
                       Extract (API)
                            │
                            ▼
                     Transform (Pandas)
                            │
                            ▼
                   Validate (Qualidade)
                            │
                            ▼
                 Persistência (SQLite)
                            │
                            ▼
                 Exportação de Arquivos
             (CSV • Excel • Parquet)
                            │
                            ▼
              Atualização do Dashboard
                            │
                            ▼
                     Fim da Execução

---

# 8. Etapas do Pipeline

## 8.1 Inicialização

O arquivo `main.py` é responsável por:

* inicializar a aplicação;
* criar a instância do Pipeline;
* iniciar o processo ETL;
* registrar o início e o fim da execução;
* tratar exceções não previstas.

---

## 8.2 Extração (Extract)

Nesta etapa o sistema realiza a comunicação com a fonte de dados.

Responsabilidades:

* abrir conexão com a API;
* enviar requisições HTTP;
* tratar autenticação;
* controlar timeout;
* realizar tentativas automáticas (Retry);
* retornar os dados em formato JSON.

Saída:

Lista de dicionários (JSON)

---

## 8.3 Transformação (Transform)

Os dados são convertidos para um DataFrame do Pandas e passam pelas seguintes etapas:

* normalização do JSON;
* padronização dos nomes das colunas;
* remoção de registros duplicados;
* inclusão de metadados técnicos.

Metadados adicionados:

* `data_coleta`
* `data_processamento`

Saída:

Pandas DataFrame

---

## 8.4 Validação (Validate)

Antes de qualquer persistência, o DataFrame é validado.

Validações implementadas:

* existência das colunas obrigatórias;
* valores nulos;
* registros duplicados;
* resumo estatístico.

Caso qualquer inconsistência seja encontrada, o Pipeline é interrompido imediatamente, evitando persistência de dados inválidos.

---

## 8.5 Persistência (SQLite)

Após a validação, o DataFrame é gravado em banco SQLite.

Características:

* criação automática do banco;
* criação automática das tabelas;
* suporte aos modos:

  * `replace`;
  * `append`;
  * `fail`.

O banco SQLite funciona como camada intermediária entre o ETL e os relatórios.

---

## 8.6 Exportação

Após a persistência, os dados são disponibilizados em diferentes formatos.

Atualmente são gerados:

* CSV;
* Excel (.xlsx);
* Parquet.

Essa etapa permite integração com diferentes ferramentas analíticas sem necessidade de nova extração.

---

## 8.7 Dashboard

Na última etapa, o Dashboard Excel é atualizado automaticamente.

A arquitetura foi projetada para manter independência entre:

* processamento dos dados;
* armazenamento;
* camada de apresentação.

Dessa forma, novas ferramentas de visualização poderão ser adicionadas futuramente sem alterações no Pipeline.

---

# 9. Artefatos Gerados

Ao final da execução, o sistema produz automaticamente os seguintes artefatos.

## Banco de Dados


database/
└── olist.db

---

## Arquivos Tratados

dados/
└── tratado/
    ├── usuarios.csv
    ├── usuarios.xlsx
    └── usuarios.parquet

---

## Dashboard

dashboard/
└── Dashboard.xlsx

---

## Logs

logs/
└── automacao.log

Todos esses artefatos são gerados automaticamente a partir de uma única execução do Pipeline.

---

# 10. Modelo Analítico

O Business Analytics Automation foi projetado para atender empresas de diferentes segmentos de mercado.

Embora o desenvolvimento inicial utilize uma API pública para fins de demonstração, a camada analítica foi modelada de forma independente da origem dos dados.

Essa abordagem permite substituir a fonte de dados (API, ERP, planilhas ou banco de dados) sem necessidade de alterações na camada de apresentação.

---

# 11. Modelo de Dados

O modelo analítico segue o conceito de Star Schema (Modelo Estrela), amplamente utilizado em projetos de Business Intelligence.

## Tabela Fato

### Fato_Vendas

Representa os eventos de negócio que serão analisados pelos dashboards.

Campos previstos:

| Campo          | Descrição                       |
| -------------- | ------------------------------- |
| id_pedido      | Identificador do pedido         |
| data_pedido    | Data da venda                   |
| id_cliente     | Cliente responsável pela compra |
| id_produto     | Produto vendido                 |
| categoria      | Categoria do produto            |
| quantidade     | Quantidade vendida              |
| preco_unitario | Valor unitário                  |
| desconto       | Valor de desconto               |
| frete          | Valor do frete                  |
| receita        | Receita da venda                |
| custo          | Custo da venda                  |
| lucro          | Receita - Custo                 |
| status         | Situação do pedido              |

---

## Dimensão Cliente

Informações relacionadas ao cliente.

Campos previstos:

* id_cliente
* nome_cliente
* cidade
* estado
* região
* segmento

---

## Dimensão Produto

Informações referentes aos produtos.

Campos previstos:

* id_produto
* nome_produto
* categoria
* marca
* fornecedor

---

## Dimensão Tempo

Permite análises temporais.

Campos previstos:

* data
* ano
* semestre
* trimestre
* mês
* semana
* dia

---

# 12. Indicadores de Negócio (KPIs)

O Dashboard Executivo será alimentado por indicadores de desempenho calculados automaticamente.

## Indicadores Financeiros

* Receita Total
* Receita Mensal
* Receita Acumulada
* Lucro Total
* Margem de Lucro (%)
* Ticket Médio
* Receita por Cliente
* Receita por Produto

---

## Indicadores Comerciais

* Total de Pedidos
* Produtos Vendidos
* Clientes Ativos
* Novos Clientes
* Produtos Mais Vendidos
* Categorias Mais Vendidas
* Crescimento Mensal

---

## Indicadores Operacionais

* Pedidos Entregues
* Pedidos Cancelados
* Pedidos Pendentes
* Tempo Médio de Processamento
* SLA de Atendimento
* Frete Médio

---

## Indicadores de Clientes

* Ticket Médio por Cliente
* Clientes Recorrentes
* Frequência de Compra
* Valor Médio por Pedido
* Participação dos Maiores Clientes

---

# 13. Regras de Negócio

O cálculo dos indicadores seguirá regras padronizadas.

## Receita

Receita = Quantidade × Preço Unitário

---

## Lucro

Lucro = Receita − Custo

---

## Margem

Margem (%) = Lucro ÷ Receita

---

## Ticket Médio

Ticket Médio = Receita Total ÷ Número de Pedidos

---

## Crescimento

Crescimento (%) =
(Período Atual − Período Anterior)
÷ Período Anterior

Essas regras serão centralizadas no projeto para garantir consistência entre diferentes relatórios e dashboards.

---

# 14. Independência da Fonte de Dados

Um dos princípios fundamentais do Business Analytics Automation é a independência entre a origem dos dados e a camada analítica.

O Dashboard Executivo não possui dependência direta de nenhuma API, ERP ou banco de dados específico.

A única responsabilidade do Pipeline é fornecer uma base padronizada contendo os campos esperados pelo modelo analítico.

Essa abordagem permite que o sistema seja adaptado para diferentes organizações apenas alterando a etapa de extração dos dados, mantendo intactas as regras de negócio, indicadores e dashboards.
