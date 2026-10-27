# Diário de uso de IA generativa

Grupo 3 | 20/10/2026

Ferramenta: Codex; fornecedor: OpenAI; modelo/versão exibida: não informado; acesso: aplicativo. Horários dos prompts não registrados.

Este registro descreve as ações verificáveis da IA. A adoção das respostas, a utilidade percebida e a reflexão pertencem ao grupo e precisam ser revisadas por ele.

## Registro 1

Etapa: Planejamento

Objetivo: Organizar requisitos, prazos e decisões do grupo.

Prompt exato:

```text
preciso que me ajude a me organizar para esses projeto!
meu grupo e o de random forest, então primeiro veja tudo, organize seu pensamento sobre, traga perguntas caso queira, ja tenho uma definição para algumas coisas e vou te passar depois de tudo
```

Resposta: A IA leu os materiais e consolidou entregas e checkpoints.

Validação: Conferência cruzada dos documentos fornecidos; inconsistência de duração da palestra identificada.

Uso e revisão: Uso proposto: apoiar o planejamento; o grupo precisa confirmar sua adoção.

## Registro 2

Etapa: Escolha do dataset

Objetivo: Avaliar a adequação do dataset indicado no checkpoint.

Prompt exato:

```text
esse dataset ta ok?
```

Resposta: A IA verificou a fonte ULB no Kaggle, o desbalanceamento e a anonimização por PCA. Propôs adaptar a demonstração ao esquema real da base.

Validação: Descrição oficial obtida pela API pública do Kaggle e documentação de métricas consultada. A análise do CSV ainda não havia ocorrido nessa interação.

Uso e revisão: A decisão de manter a base está sendo utilizada nesta implementação; o grupo deve revisar as limitações.

## Registro 3

Etapa: Código e análise

Objetivo: Preparar as evidências e os documentos do Checkpoint 1.

Prompt exato:

```text
preciso que me ajude a completar tudo isso, tenho que entregar!
```

Resposta: Foram produzidos scripts, auditoria, gráficos, comparação de modelos, documentos e instruções de reprodução.

Validação: Dataset baixado da fonte oficial e hash registrado; pipeline executado; métricas recalculadas a partir das previsões; modelo recarregado; CSV inválido rejeitado.

Uso e revisão: Aceitação e modificações pelos integrantes ainda devem ser registradas após revisão. A execução com apoio da IA não comprova domínio do grupo.

## Registro 4

Etapa: Organização técnica

Objetivo: Verificar acesso ao repositório privado.

Prompt exato:

```text
git@github.com:lipeinacio/random_forest.git

ele ta privado, tu consegue acessar mesmo assim?
```

Resposta: SSH retornou Permission denied (publickey); acesso HTTPS funcionou e o repositório foi clonado vazio.

Validação: git ls-remote e git clone por HTTPS, sem expor credenciais.

Uso e revisão: Conferir a publicação e o convite ao professor. Não registrar tokens ou chaves no diário.
