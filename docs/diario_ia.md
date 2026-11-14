# Diário de uso de IA generativa

Grupo 3 | Registros iniciados em 20/10/2026 | Revisão em 27/10/2026

Ferramenta: aplicativo Codex. Fornecedor: OpenAI. Modelo/versão exibida: não informado neste registro. Forma de acesso: aplicativo.

Este diário registra o apoio da IA no desenvolvimento do projeto, as verificações técnicas realizadas e a participação do grupo na visualização, discussão e aprovação dos materiais. A revisão do grupo e o aprendizado relatado foram registrados em 27/10/2026.

Integrantes: Felipe Inácio de Paula; Gabriel Damante Frias; Maicon Manoel Rodrigues dos Santos; André Luiz Jeremias Pereira Junior; Lavinia Zanata Alves

Horários individuais das interações anteriores não registrados. A data e o horário da execução técnica estão em results/ambiente.json.

## Registro 1

Etapa: Planejamento

Objetivo: Organizar requisitos, prazos e decisões do grupo.

Prompt exato:

```text
preciso que me ajude a me organizar para esses projeto!
meu grupo e o de random forest, então primeiro veja tudo, organize seu pensamento sobre, traga perguntas caso queira, ja tenho uma definição para algumas coisas e vou te passar depois de tudo
```

Apoio da IA: A IA leu os materiais da disciplina e organizou os requisitos, as entregas e os checkpoints.

Verificação: Conferência cruzada dos documentos fornecidos, com identificação de diferenças nas orientações de duração da apresentação.

Uso pelo grupo: Utilizamos a organização apresentada como apoio ao planejamento. A leitura e a discussão dos materiais contribuíram para compreender as etapas e as entregas do projeto.

## Registro 2

Etapa: Escolha do dataset

Objetivo: Avaliar a adequação do dataset indicado no checkpoint.

Prompt exato:

```text
esse dataset ta ok?
```

Apoio da IA: A IA consultou a descrição oficial do dataset ULB no Kaggle e apresentou características da base, como o desbalanceamento e a anonimização por PCA, além de implicações para a demonstração.

Verificação: Consulta à fonte oficial e à documentação de métricas. Nessa interação, a avaliação ainda se limitava à descrição da base; a análise do CSV foi realizada posteriormente.

Uso pelo grupo: A análise apoiou a manutenção do dataset no projeto e ajudou a compreender suas limitações. Consideramos essas informações na discussão da aplicação e dos resultados.

## Registro 3

Etapa: Código e análise

Objetivo: Preparar as evidências e os documentos do Checkpoint 1.

Prompt exato:

```text
preciso que me ajude a completar tudo isso, tenho que entregar!
```

Apoio da IA: A IA apoiou a implementação e a execução do pipeline, a geração de gráficos, a comparação dos modelos e a preparação da documentação do checkpoint.

Verificação: Verificação técnica realizada com apoio da IA: download da fonte oficial e registro do hash; execução do pipeline; recálculo das métricas a partir das previsões; recarga do modelo salvo; rejeição de CSV com esquema inválido.

Uso pelo grupo: Visualizamos os resultados e os materiais produzidos, discutimos o conteúdo e aprovamos sua utilização no projeto. O processo também contribuiu para nosso aprendizado sobre o trabalho desenvolvido.

## Registro 4

Etapa: Organização técnica

Objetivo: Verificar acesso ao repositório privado.

Prompt exato:

```text
git@github.com:lipeinacio/random_forest.git

ele ta privado, tu consegue acessar mesmo assim?
```

Apoio da IA: A IA verificou o acesso ao repositório privado. A conexão por SSH foi recusada, enquanto o acesso por HTTPS funcionou. O repositório foi utilizado para organizar o código e os materiais.

Verificação: Verificação por git ls-remote e git clone via HTTPS, seguida de publicação dos arquivos. Credenciais não foram incluídas no projeto.

Uso pelo grupo: Utilizamos o repositório para reunir o código, os resultados e os documentos aprovados pelo grupo. O acesso do professor deve ser conferido antes da entrega.

## Síntese do uso de IA no projeto

Utilizamos a IA como apoio à organização, à implementação, à análise e à redação dos materiais. Visualizamos os resultados apresentados, discutimos o conteúdo e aprovamos sua utilização no projeto. Essa interação também fez parte do nosso aprendizado. As verificações técnicas estão documentadas no código e nos resultados, enquanto a participação do grupo incluiu a leitura, a discussão e a avaliação dos materiais. O Diário de IA tem finalidade de acompanhamento e não compõe a nota do projeto.


## Registro 5

Data: 13/11/2026. Etapas: conclusão dos experimentos, protótipo e comunicação. Ferramenta: Codex, OpenAI. Modelo/versão visível ao usuário nesta interação: não informado no registro.

Prompts relevantes enviados pelo usuário: “consegue me trazer tudo pronto?” e “use esse repositorio como exemplo para melhorar qualquer metrica necessaria para a conclusao do nosso seminario!” Referência indicada: https://github.com/ViniciusSilveiraCampos/football-pca-map.

Apoio da IA: leitura do repositório e das exigências; uso do projeto de PCA como referência de organização, sem copiar seus dados ou resultados; implementação de três experimentos com hipóteses previamente gravadas; seleção na validação; avaliação final; protótipo; elaboração dos materiais e roteiros.

Validação técnica: hash da base oficial conferido; reprodução da configuração original; isolamento de registros entre conjuntos; testes automatizados de inferência, rejeição de Class e entradas inválidas; conferência das matrizes e métricas. Resultados e ambiente em results/final/. A seleção foi gravada antes do teste. O recall menor no teste foi preservado na comunicação.

Uso pelo grupo nesta etapa: materiais disponibilizados para leitura, revisão, ensaio e eventual adoção. Não houve declaração de revisão individual ou teste em outro computador nesta interação. Esses fatos só devem ser acrescentados após ocorrerem.

Reflexão dos integrantes e verificação em outra máquina: pendentes de registro real pelo grupo. Não foram simulados depoimentos, participação ou aprovação.
