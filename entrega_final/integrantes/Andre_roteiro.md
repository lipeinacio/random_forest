# Guia de apresentação de André

André Luiz Jeremias Pereira Junior. Responsabilidade de material: Ficha de experimentos. Tema de fala: Hipóteses, experimentos e métricas. Slides 14 a 19, aproximadamente 10 minutos.

## O que conferir antes do ensaio

Abra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.

## Slide 14 Como lemos as métricas

Tempo sugerido: 1.5 min.

Precisão responde: entre os alertas gerados, quantos eram fraudes? Recall responde: entre todas as fraudes, quantas o sistema encontrou? F1 é a média harmônica dessas duas medidas e fica baixa se uma delas for muito baixa. Usamos sempre a classe fraude como positiva. AP significa Average Precision e resume a relação precisão-recall ao variar o limiar. Ela não é a mesma coisa que acurácia e não deve ser confundida com uma integração trapezoidal idêntica da curva. Nosso critério principal de escolha foi F1 no limiar 0,50. Não comparamos F1 da validação com F1 do teste como se fossem o mesmo conjunto. Para cada experimento, a hipótese foi registrada antes da execução, alteramos um fator em relação à referência e interpretamos o resultado, inclusive quando ele contrariou a expectativa.

Fontes e evidências: Saito e Rehmsmeier (2015), em docs/referencias.md; https://scikit-learn.org/stable/modules/model_evaluation.html.

## Slide 15 E1 Retirar os pesos de classe

Tempo sugerido: 1.5 min.

O primeiro experimento retirou os pesos de classe, mantendo os demais parâmetros e os dados. A hipótese era reduzir falsos alertas, possivelmente sacrificando parte do recall. Foi isso que observamos nesta validação. Os falsos positivos caíram de 15 para 8. As fraudes não identificadas aumentaram de 14 para 17. A precisão passou de 84,21% para 90,59%, o recall caiu de 85,11% para 81,91% e o F1 subiu de 0,8466 para 0,8603. A AP também aumentou de 0,8611 para 0,8748. A leitura correta é que a configuração ficou mais seletiva nessa avaliação. Não podemos resumir o resultado dizendo que retirar pesos é sempre melhor para classes raras. Se a prioridade operacional fosse recall, a decisão poderia ser diferente.

Fontes e evidências: results/final/plano_pre_execucao.json; results/final/experimentos.csv; results/final/decisao_antes_do_teste.json.

## Slide 16 E2 Limitar a profundidade a seis níveis

Tempo sugerido: 1.5 min.

No segundo experimento, alteramos apenas a profundidade máxima de 12 para 6 na configuração de referência. Os pesos balanced foram mantidos. A hipótese era que um modelo mais simples pudesse reduzir o sobreajuste, com risco de perder padrões complexos. O resultado observado não foi uma melhora geral. O recall ficou em 88,30%, com 83 fraudes encontradas, mas houve 138 falsos positivos. A precisão caiu para 37,56% e o F1 para 0,5270. A AP foi 0,8164. Portanto, encontramos mais fraudes nesse limiar, porém à custa de muitos alertas sobre transações normais. Como não avaliamos uma curva de aprendizagem nem múltiplas sementes, não afirmamos que demonstramos a causa exata em termos de sobreajuste. Demonstramos o efeito dessa mudança nas métricas da validação.

Fontes e evidências: results/final/plano_pre_execucao.json; results/final/experimentos.csv; results/final/decisao_antes_do_teste.json.

## Slide 17 E3 Remover três componentes destacados

Tempo sugerido: 1.5 min.

O terceiro experimento é uma ablação: retiramos V17, V14 e V12 porque eles se destacavam na comparação descritiva feita no treino. A hipótese era uma queda de desempenho por remover informação útil. O resultado foi misto. O recall permaneceu igual, com 80 fraudes identificadas. O número de falsos positivos caiu de 15 para 14 e o F1 aumentou levemente para 0,8511. Ao mesmo tempo, a AP caiu para 0,8540. Isso mostra por que uma conclusão não pode se apoiar em uma única frase sobre importância. Outros componentes podem carregar sinais relacionados, e o efeito pode variar entre a métrica num limiar e o ranking ao longo dos limiares. A hipótese de uma piora uniforme não foi sustentada. Também não concluímos que esses componentes sejam inúteis.

Fontes e evidências: results/final/plano_pre_execucao.json; results/final/experimentos.csv; results/final/decisao_antes_do_teste.json.

## Slide 18 Escolha feita na validação

Tempo sugerido: 1.5 min.

O gráfico reúne as quatro configurações: a referência e as três alterações. O critério registrado foi selecionar o maior F1 na validação, com AP para eventual desempate. A configuração sem pesos venceu por esse critério. Salvamos essa decisão antes de avaliar o teste. O modelo final continua treinado somente nos 60% de treino, para manter a comparação auditável; não fizemos um novo ajuste com treino mais validação. A exploração não comprova um ótimo global. Foram quatro configurações e uma única semente. O aumento de F1 de cerca de 0,014 na validação é uma evidência localizada. A próxima etapa é medir a configuração escolhida no teste reservado, sem tentar voltar e mudar parâmetros para melhorar aquele resultado.

Fontes e evidências: results/final/plano_pre_execucao.json; results/final/experimentos.csv; results/final/decisao_antes_do_teste.json.

## Slide 19 Resultado no teste reservado

Tempo sugerido: 2.5 min.

Agora estamos em outro conjunto: 56.746 transações, com 95 fraudes. A floresta final identificou 68, deixou passar 27 e gerou 4 falsos alertas. A árvore identificou 71, deixou passar 24 e gerou 256 falsos alertas. A floresta teve precisão de 94,44%, recall de 71,58%, F1 de 0,8144 e AP de 0,7867. Na árvore, o F1 foi 0,3365 e a AP 0,5206. Peçam que a plateia leia a matriz: linhas são rótulos reais e colunas são previsões. A conclusão tem de incluir os dois lados. A floresta melhorou bastante a precisão e o F1, mas perdeu três fraudes adicionais em relação à árvore. O F1 do teste também foi menor que o da validação. Com poucos positivos, a composição das amostras pesa na estimativa. Não ajustamos o modelo depois de olhar esses resultados. Felipe vai apresentar falhas concretas, as limitações e a aplicação.

Fontes e evidências: results/final/teste.json; results/final/conclusao.json.

## Perguntas que você deve dominar

## Por que retirar balanced se fraude é rara?

Foi uma hipótese controlada, não uma regra geral. Na validação, reduziu FP de 15 para 8, elevou precisão e F1, mas baixou recall. O objetivo escolhido foi F1 no limiar 0,50.

## Por que o modelo final encontrou menos fraudes que a árvore no teste?

A configuração escolhida é mais seletiva no limiar usado. Encontrou 68 de 95, contra 71 da árvore. A melhora em F1 e precisão não implica melhora de recall. Não ajustamos após avaliar o teste.

## Vocês melhoraram o resultado olhando o teste?

Não. O plano registra hipóteses e a decisão é salva em decisao_antes_do_teste.json antes das previsões no teste. A configuração foi escolhida somente pela validação. Mudanças futuras exigem outro protocolo e avaliação independente.

## O que é AP?

Average Precision resume precisão ao longo das mudanças de recall. É útil para classe rara e ranking, mas não substitui contagem de erros num limiar. Não é acurácia nem uma área trapezoidal necessariamente idêntica.

## O que aconteceu ao remover V17, V14 e V12?

Na validação, recall permaneceu em 85,11%, F1 subiu levemente e AP caiu. O efeito misto contraria uma piora uniforme. Pode haver sinal compartilhado com outros componentes, mas não testamos a causa dessa compensação.

## O que significam os intervalos de confiança?

Wilson descreve a incerteza de proporções de precisão e recall nesta amostra. O bootstrap estratificado reamostra positivos e negativos do teste fixo para estimar F1. Não inclui drift nem variabilidade de diferentes treinos.
