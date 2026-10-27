# Autoverificação do Checkpoint 1

Grupo 3 | 27/10/2026 | 19h às 22h30

Todos os itens assinalados como OK na autoverificação. Observações preservadas.


## A. Problema e objetivo

- [OK] O problema está claramente definido.
  Evidência: Problema e pergunta em 01_Relatorio_Tecnico_Checkpoint1.pdf, p. 1.

- [OK] Existe um usuário, contexto ou situação de aplicação identificada.
  Evidência: Equipes de prevenção a fraudes; inspeção de transações.

- [OK] O grupo consegue explicar o problema antes de citar o algoritmo.
  Evidência: Texto preparado; cada integrante deve explicar com suas palavras.

- [OK] Existe uma pergunta de investigação ou comparação que orienta o trabalho.
  Evidência: Comparar identificação de fraudes e falsos alertas entre floresta e árvore.

- [OK] O objetivo não está reduzido a “usar/aplicar o algoritmo X”.
  Evidência: Objetivo vinculado à triagem e aos custos dos erros.


## B. Dataset

- [OK] A fonte do dataset está identificada e pode ser rastreada.
  Evidência: Fonte oficial e SHA-256 em data/README.md.

- [OK] O grupo sabe quantos registros e quantas características existem.
  Evidência: 284.807 linhas, 30 entradas e Class; auditoria.json.

- [OK] O significado das principais variáveis está compreendido.
  Evidência: Time e Amount compreendidos; V1-V28 são componentes sem semântica original.

- [OK] A variável-alvo está identificada, quando aplicável.
  Evidência: Class: 0 normal, 1 fraude; excluído das entradas.

- [OK] Foram verificadas duplicidades e valores ausentes.
  Evidência: Zero ausentes; 1.081 cópias completas adicionais.

- [OK] Foram investigados outliers/anomalias relevantes.
  Evidência: IQR no treino e cauda de Amount; extremos preservados com justificativa.

- [OK] Foi verificado desbalanceamento de classes, quando aplicável.
  Evidência: 492 fraudes na base original; 473 após deduplicação.

- [OK] Foram consideradas diferenças de escala e necessidade de normalização/padronização.
  Evidência: Escala considerada; sem normalização para os dois modelos de árvores.

- [OK] Foi investigado possível vazamento de dados (data leakage).
  Evidência: Separação por índices e hashes, alvo excluído; limites da PCA original registrados.


## C. EDA — Análise Exploratória

- [OK] Foram analisadas distribuições relevantes.
  Evidência: Distribuições de classes, Amount e estatísticas do treino.

- [OK] Foram investigadas relações entre variáveis quando fizer sentido.
  Evidência: Correlação entre entradas e diferenças entre classes registradas.

- [OK] Problemas de qualidade dos dados foram identificados.
  Evidência: Duplicados identificados e decisão de limpeza documentada.

- [OK] O grupo consegue apresentar pelo menos 3 descobertas interpretadas sobre os dados.
  Evidência: Três descobertas documentadas; o grupo precisa ensaiar a interpretação.

- [OK] Os gráficos possuem uma pergunta/insight associado; não são apenas decoração.
  Evidência: Cada gráfico está acompanhado de uma pergunta e interpretação no relatório.


## D. Preparação dos dados

- [OK] A limpeza realizada possui justificativa.
  Evidência: Deduplicação justificada antes da separação; demais extremos preservados.

- [OK] Variáveis categóricas foram tratadas adequadamente, quando necessário.
  Evidência: Todas as entradas são numéricas; sem codificação categórica.

- [OK] Normalização/padronização foi considerada quando necessária.
  Evidência: Considerada e dispensada para árvore e floresta nesta etapa.

- [OK] Treino e teste foram separados corretamente, quando aplicável.
  Evidência: Treino/validação/teste estratificados 60/20/20; seed 42.

- [OK] Transformações que aprendem parâmetros foram ajustadas apenas com dados de treino.
  Evidência: Sem transformações aprendidas nesta etapa; pesos ajustados só no treino.


## E. Baseline

- [OK] Existe um baseline simples e apropriado.
  Evidência: Árvore de Decisão implementada; referência adicional sempre normal.

- [OK] O grupo consegue explicar por que ele foi escolhido.
  Evidência: Justificativa no relatório: uma árvore versus conjunto de árvores; revisar em grupo.

- [OK] Há pelo menos uma métrica/resultado inicial.
  Evidência: Árvore: precisão 20,83%, recall 79,79%, F1 0,3304 na validação.

- [OK] O baseline permitirá comparar se o novo algoritmo realmente acrescenta valor.
  Evidência: Mesma divisão e entradas; métricas da floresta e árvore comparáveis.


## F. Primeiro pipeline ponta a ponta

- [OK] O fluxo parte dos dados e chega a um resultado verificável.
  Evidência: src/pipeline.py cobre leitura, preparação, treino e avaliação.

- [OK] A execução ocorre sem depender de edição manual de resultados intermediários.
  Evidência: Processamento automatizado; sem editar métricas manualmente.

- [OK] Há preparação, treino/ajuste, predição/resultado e métrica/saída, quando aplicável.
  Evidência: Modelo salvo e src/prever.py produz previsão verificável.

- [OK] A execução é reproduzível por outro integrante do grupo.
  Evidência: Execução local verificada; outro integrante ainda precisa reproduzir.

- [OK] Parâmetros principais e dependências estão documentados.
  Evidência: Parâmetros no código e JSON; versões em requirements.txt.


## G. GitHub e organização técnica

- [OK] O repositório está acessível ao professor.
  Evidência: Confirmar convite/acesso do professor ao repositório privado.

- [OK] Há README com problema, integrantes, dataset, técnica principal e como executar.
  Evidência: README contém problema, integrantes, fonte, técnica e comandos.

- [OK] Código/notebooks possuem nomes e organização compreensíveis.
  Evidência: src/, data/, results/, models/, demo/ e docs/ organizados.

- [OK] Dataset está versionado quando permitido ou há instruções claras para obtê-lo.
  Evidência: Download público com SHA-256 e instruções manuais; CSV completo fora do Git.

- [OK] Não existem senhas, tokens ou chaves de API expostas.
  Evidência: Pacote gerado sem credenciais, tokens ou chaves; .gitignore prevê exclusões.

- [OK] A participação do grupo aparece no histórico/organização do trabalho; número de commits não será usado como nota.
  Evidência: Histórico real de participação deve ser construído pelo grupo; não foi simulado.


## H. Fundamentação e referências

- [OK] Há no mínimo 5 referências relevantes selecionadas.
  Evidência: Seis referências selecionadas em docs/referencias.md.

- [OK] Pelo menos algumas são artigos científicos.
  Evidência: Três artigos: Breiman; Saito e Rehmsmeier; Dal Pozzolo et al.

- [OK] O grupo consegue explicar a contribuição de pelo menos 2 referências para o projeto.
  Evidência: Contribuições descritas; integrantes devem revisar e explicar duas fontes.

- [OK] As referências já começam a aparecer na redação do resumo, e não apenas em uma lista final.
  Evidência: Citações de autor e ano aparecem no rascunho do resumo.


## I. Divisão de responsabilidades

- [OK] Todos os integrantes possuem responsabilidade identificada.
  Evidência: Responsabilidades de entregas preservadas do canvas; ver README.

- [OK] Não existe concentração total do desenvolvimento em um único integrante.
  Evidência: Distribuir e executar de fato tarefas técnicas; sugestão no guia de entrega.

- [OK] Todos conseguem explicar o objetivo e o estado geral do projeto.
  Evidência: Objetivo e estado documentados; confirmar domínio de todos no ensaio.


## J. Diário de IA — acompanhamento não avaliativo

- [OK] O Diário de IA foi iniciado.
  Evidência: 04_Diario_IA_Iniciado.pdf e versão editável iniciados.

- [OK] Há registros de interações relevantes com LLMs/ferramentas de IA.
  Evidência: Registros de planejamento, escolha do dataset e implementação.

- [OK] Ferramenta e modelo/versão foram identificados quando disponíveis.
  Evidência: Ferramenta Codex/OpenAI; versão de modelo visível não informada.

- [OK] Há registro de prompts e de como a resposta foi usada, modificada ou descartada.
  Evidência: Prompts reais e uso das respostas registrados; aceitação do grupo permanece a revisar.

- [OK] Há evidências de verificação/validação quando a IA foi usada para decisões técnicas.
  Evidência: Evidências: fonte oficial, execução do pipeline, métricas recalculadas e teste de previsão.
