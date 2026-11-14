# Guia de apresentação de Lavinia

Lavinia Zanata Alves. Responsabilidade de material: Resumo expandido e Instagram. Tema de fala: Problema, contexto e objetivo. Slides 1 a 4, aproximadamente 5 minutos.

## O que conferir antes do ensaio

Abra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.

## Slide 1 Caçador de Fraudes

Tempo sugerido: 1 min.

Boa noite. Nosso projeto investiga como um Random Forest pode ajudar a selecionar transações para revisão. A pergunta é prática: conseguimos identificar fraudes sem transformar compras legítimas em alertas em excesso? Vamos mostrar os dados, a comparação com uma árvore isolada, três experimentos e um protótipo que aceita novas entradas. O resultado tem uma vantagem e uma limitação importantes: a floresta final reduz bastante os falsos alertas, mas ainda deixa fraudes passarem. Ao longo da apresentação, vamos distinguir o resultado observado de qualquer promessa sobre uma aplicação real. Não desenvolvemos um sistema bancário pronto para uso. Desenvolvemos uma investigação reproduzível e uma demonstração educacional.

Fontes e evidências: README.md; results/metricas_validacao.json; results/final/plano_pre_execucao.json.

## Slide 2 Quem recebe o alerta

Tempo sugerido: 1 min.

O público da solução seria uma equipe de prevenção a fraudes. Para essa equipe, um alerta custa tempo de análise e pode causar incômodo ao cliente. Por outro lado, uma fraude que passa sem alerta pode gerar prejuízo. Esses erros têm consequências diferentes. Antes de escolher o algoritmo, precisamos definir o papel da aplicação: apoiar triagem, com uma pessoa avaliando o caso. Não medimos o prejuízo financeiro real nem sabemos a capacidade de análise de uma equipe. Portanto, vamos comparar quantidades de erros e métricas de classificação, sem inventar uma economia em dinheiro. Perguntem à plateia: vocês prefeririam mais alertas ou mais risco de deixar uma fraude passar? Guardem essa resposta para quando compararmos os resultados.

Fontes e evidências: README.md; results/metricas_validacao.json; results/final/plano_pre_execucao.json.

## Slide 3 99,83% de acurácia pode esconder todas as fraudes

Tempo sugerido: 1.5 min.

Vamos começar com uma armadilha. Se eu disser que um sistema acerta mais de 99,8% das transações, ele parece excelente. Porém, na validação, basta responder normal para todas as entradas para atingir 99,8343% de acurácia. Isso acontece porque as fraudes são muito raras. O sistema acerta as 56.651 transações normais e erra todas as 94 fraudes. O recall da fraude é zero. Peçam à plateia para interpretar esse resultado antes de revelar a última linha. Acurácia é a fração de acertos totais e, sozinha, não responde à pergunta do projeto. Usaremos precisão para avaliar os alertas, recall para avaliar as fraudes encontradas e F1 para resumir o equilíbrio entre essas duas medidas.

Fontes e evidências: README.md; results/metricas_validacao.json; results/final/plano_pre_execucao.json.

## Slide 4 Pergunta de investigação

Tempo sugerido: 1.5 min.

Nossa pergunta é: a floresta consegue melhorar o equilíbrio entre fraudes encontradas e falsos alertas em relação a uma árvore isolada? Para comparar de forma coerente, usamos as mesmas entradas e a mesma divisão dos dados. Uma árvore é um baseline apropriado porque permite investigar o que muda ao combinar várias árvores. Também mantemos a referência que sempre responde normal. O critério de seleção da configuração final foi maior F1 da classe fraude na validação, com limiar de 0,50 e AP como desempate. Esse critério é uma escolha metodológica, não uma afirmação de que F1 representa todos os custos de um banco. A seguir, Maicon vai explicar de onde vieram os dados e o que foi necessário verificar antes de treinar.

Fontes e evidências: README.md; results/metricas_validacao.json; results/final/plano_pre_execucao.json.

## Perguntas que você deve dominar

## Por que Random Forest?

O tema foi sorteado. A técnica é adequada para investigar combinações não lineares em dados tabulares e permite comparação direta com uma árvore. Isso justifica o estudo, sem provar que seja a melhor técnica disponível.

## Por que usar uma árvore como baseline?

Ela usa a mesma família de regras e torna observável o valor da agregação de 100 árvores. A comparação usa a mesma separação de dados. Sempre normal é uma referência adicional para mostrar a armadilha da acurácia.

## Por que não selecionar só recall?

Recall isolado pode chegar a 100% classificando todas as transações como fraude. É preciso considerar alertas falsos e capacidade de revisão. Um requisito operacional poderia impor um recall mínimo, mas não foi o critério deste estudo.

## Qual é a limitação mais importante?

A avaliação é aleatória em dois dias de 2013, com poucos positivos e sem separação por titular. Não demonstra desempenho futuro. Além disso, os componentes anonimizados e a falta de calibração limitam a aplicação.
