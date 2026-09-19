# Sistema HCA G2 — Smart Charging Simulator 🔋🚗

O **HCA G2** é uma aplicação em Python voltada para a simulação, monitoramento e bilhetagem inteligente de estações de carregamento para veículos elétricos (VE). O ecossistema simula o comportamento elétrico e térmico de uma recarga residencial/comercial em tempo real, integrando autenticação e cálculo de **tarifa dinâmica** baseado em faixas de fluxo da rede e incentivos de geração de energia solar microgerada.

---

## 🚀 Funcionalidades Principais

*   **Módulo de Autenticação Interativo:** Login seguro e criação de novas contas diretamente pelo terminal com validações nativas para tratamento de erros (impede falhas caso o usuário digite texto em campos numéricos).
*   **Telemetria Dinâmica de Recarga:** Simulação contínua e realista segundo a segundo de grandezas físicas:
    *   Tensão alternada ($200\text{V}$ a $220\text{V}$) com flutuações de ruído na rede.
    *   Corrente elétrica adaptada à integridade da tensão (até $40\text{A}$).
    *   Cálculo em tempo real de Potência Ativa ($\text{kW}$) e energia acumulada ($\text{kWh}$).
*   **Proteção Ativa e Segurança Elétrica:** Monitoramento térmico indireto e proteção de sobrecorrente/sobrecarga. O sistema interrompe o fornecimento e aciona um bloqueio de segurança caso a potência real ultrapasse a barreira crítica de $8.8\text{kW}$.
*   **Algoritmo de Tarifa Inteligente:** Sistema adaptativo de cobrança indexado pelo dia da semana e hora de início do carregamento:
    *   Separação automatizada em fluxos: `BAIXA`, `REGULAR`, `MEDIANO` e `PICO`.
    *   **Incentivo Solar GoodWe:** Identificação da janela de pico de geração solar das 10h às 14h, aplicando descontos exclusivos no multiplicador de preço por kWh.

---

## 🛠️ Arquitetura de Dados Local

O script opera 100% com módulos padrão do ecossistema Python (sem dependências externas), mas necessita obrigatoriamente de uma base relacional local em formato JSON chamada `veiculos.json` alocada no mesmo diretório de execução.

### Formato esperado para o `veiculos.json`:
```json
[
  {
    "marca": "BYD",
    "modelo": "Dolphin Plus",
    "capacidade_bateria_kwh": 60.48
  },
  {
    "marca": "GWM",
    "modelo": "Ora 03 GT",
    "capacidade_bateria_kwh": 63.0
  },
  {
    "marca": "Volvo",
    "modelo": "EX30",
    "capacidade_bateria_kwh": 69.0
  }
]


| Categoria de Fluxo | Janela Horária Comum            | Fator Padrão | Fator c/ Incentivo Solar (10h - 14h) |
| **BAIXA**          | Madrugadas / Início da Manhã    | 0.90         | 0.70                                 |
| **REGULAR**        | Horários intermediários         | 1.00         | 0.85                                 |
| **MEDIANO**        | Transições de fluxo comercial   | 1.00         | 0.85                                 |
| **PICO**           | Horários de retorno residencial | 1.40         | 1.25                                 |
```

💻 Como Rodar o Projeto
Siga as etapas abaixo no terminal do seu sistema operacional:

1. Clone ou salve o arquivo do projeto

2. Abra o terminal na raiz desta pasta instalada.

3. Execute a aplicação utilizando o interpretador do Python 3:


```bash
python run.py
```


4. **Credenciais de Teste Padrão:**
   * **E-mail:** `p@email`
   * **Senha:** `123`

---

## 📊 Exemplo de Saída (Relatório Final)

```text
========= ESTATÍSTICAS =========
Sessões realizadas: 2
Energia Fornecida:  0.02 kWh
Faturamento:        R$ 0.04
Ticket médio:       R$ 0.02
Maior consumo:      0.01 kWh
Menor consumo:      0.01 kWh
================================
```
---

# Análise de algoritmos
## Busca Sequencial
No projeto, a busca sequencial é utilizada para localizar uma vaga específica informada pelo usuário através do método de busca.Trecho do código que provoca o crescimento:
```Python
def busca_sequencial(vagas, vaga_procurada):
    for i in range(len(vagas)):
        if vagas[i].id_sessao == vaga_procurada:
            return i
    return -1
```
Análise:Para uma lista com $n$ sessões (veículos estacionados), no pior caso (quando o veículo procurado está na última posição ou não existe na lista), o algoritmo precisa percorrer todas as posições do vetor uma a uma. A quantidade de comparações cresce de forma linear em relação ao número de elementos.Complexidade: O(n)


## Bubble Sort
O algoritmo Bubble Sort foi implementado no projeto para ordenar as sessões de acordo com diferentes critérios escolhidos pelo usuário (como bateria atual, status ou tempo restante).Trecho do código que provoca o crescimento:
```Python
def bubble_sort(lista_sessoes, chave):
    n = len(lista_sessoes)
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            val1 = getattr(lista_sessoes[j], chave, 0)
            val2 = getattr(lista_sessoes[j + 1], chave, 0)
```

Análise:Para ordenar $n$ sessões, o algoritmo utiliza laços aninhados. O laço externo executa $n$ vezes e o laço interno executa em média $n/2$ vezes. Isso gera uma quantidade de operações proporcional a $n \times n$, fazendo com que o número de comparações e trocas cresça de forma quadrática.

# Complexidade: O(n²)10. 
## Comparação entre algoritmos
A análise da complexidade demonstra o impacto prático do crescimento dos dados no comportamento do sistema:

### Busca Sequencial
```text
Busca Sequencial — O(n) (Linear)Tamanho da entrada e Quantidade de operações: Se o número de sessões ativas no estacionamento dobrar (por exemplo, de 10 para 20 vagas ocupadas), o número máximo de verificações que o laço for precisará fazer também dobrará proporcionalmente.Desempenho: Como o estacionamento possui um limite físico de vagas reduzido, o impacto no desempenho é imperceptível para o usuário, mantendo a busca extremamente rápida.
```

### Bubble Sort 
```text
Bubble Sort — O(n²) (Quadrática)Tamanho da entrada e Quantidade de operações: Se a quantidade de dados duplicar, o número de operações e comparações não dobra apenas — ele é multiplicado aproximadamente por quatro ($2^2$).Desempenho: Para o contexto de um estacionamento de pequeno/médio porte (com dezenas de vagas), o Bubble Sort executa de forma aceitável. No entanto, se a quantidade de elementos crescesse expressivamente para milhares de registros, o desempenho cairia drasticamente, tornando o sistema lento devido ao alto volume de comparações em cascata.
```