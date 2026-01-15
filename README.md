<<<<<<< HEAD
# Guia rápido: como criar e entender um agente de IA

Este repositório serve como um ponto de partida para **entender o funcionamento de um agente de IA** e o **processo de desenvolvimento**. Abaixo está um roteiro prático e direto para você criar o seu agente e compreender cada etapa.

## 1) O que é um agente de IA?
Um agente é um sistema que:
1. **Recebe um objetivo** (por exemplo, “responder perguntas” ou “executar tarefas”).
2. **Planeja e decide ações** com base em um modelo de linguagem (LLM).
3. **Executa ações** via ferramentas (APIs, banco de dados, navegador, scripts).
4. **Observa resultados** e **ajusta o plano** até concluir o objetivo.

## 2) Fluxo básico de funcionamento
1. **Entrada do usuário** → texto, comandos ou eventos.
2. **Raciocínio/planejamento** → o LLM interpreta o pedido e decide os próximos passos.
3. **Ação** → chama ferramentas (ex: buscar dados, escrever arquivos, consultar APIs).
4. **Observação** → lê o resultado da ação.
5. **Iteração** → repete o ciclo até finalizar.

## 3) Componentes essenciais do agente
- **LLM (modelo de linguagem)**: o “cérebro” que interpreta e planeja.
- **Memória**:
  - *Curta duração*: contexto da conversa.
  - *Longa duração*: base de dados, embeddings ou logs.
- **Ferramentas**: funções ou APIs para executar tarefas reais.
- **Controlador (orquestrador)**: define o loop de execução e regras de segurança.

## 4) Passo a passo para criar seu agente
1. **Defina o objetivo**: o que o agente deve fazer?
2. **Escolha um LLM** (ex: GPT, Claude, Llama).
3. **Monte o loop do agente**:
   - entrada → planejamento → ação → observação → repetir.
4. **Integre ferramentas** (APIs, banco de dados, web scraping).
5. **Adicione memória**:
   - logging simples ou base vetorial para contexto.
6. **Implemente segurança**:
   - limites de chamadas, validação de entradas, filtros.
7. **Teste e avalie**:
   - crie casos reais e meça erros/acertos.

## 5) Exemplo de “loop” em pseudocódigo
```
while not done:
  objetivo = ler_entrada_usuario()
  plano = llm_planeja(objetivo)
  resultado = executar_ferramentas(plano)
  done = avaliar_resultado(resultado)
```

## 6) Próximos passos sugeridos
- Criar um protótipo simples em Python com um LLM.
- Adicionar duas ferramentas:
  1. busca de dados (ex: API pública)
  2. persistência (ex: salvar em arquivo ou banco)
- Medir desempenho com perguntas reais.

## 7) Como continuar evoluindo
- **Aprimorar planejamento**: usar “chain-of-thought” ou “plan-and-execute”.
- **Multiagentes**: dividir tarefas entre subagentes especializados.
- **Melhorar memória**: embeddings e recuperação (RAG).

---

Se quiser, posso ajudar você a:
- montar um exemplo em Python;
- integrar APIs específicas;
- criar um agente com memória longa e ferramentas reais.
=======
# README.md

## Setup
pip install -e .
playwright install chromium
uvicorn app.main:app --reload

## Test
POST http://127.0.0.1:8000/api/run

Body:
{
  "rfq": (conteúdo de app/data/rfqs/sample_rfq.json),
  "dry_run": true,
  "channel": "whatsapp"
}

Resultado em:
app/data/runs/<run_id>.json
>>>>>>> e784e71 (primeiro commit local)
