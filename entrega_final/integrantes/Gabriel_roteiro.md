# Guia de apresentação de Gabriel

Gabriel Damante Frias. Responsabilidade de material: Folder. Tema de fala: Random Forest e baseline. Slides 9 a 13, aproximadamente 9 minutos.

## O que conferir antes do ensaio

Abra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.

## Slide 9 Uma árvore de decisão

Tempo sugerido: 2 min.

Uma árvore pode ser entendida como uma sequência de perguntas. Em cada nó, o treinamento procura uma variável e um ponto de corte que separe melhor os exemplos. Um exemplo didático seria Amount menor que um valor, seguido de V14 menor que outro. Esses cortes do exemplo são ilustrativos; não estamos afirmando que sejam os cortes reais do modelo. Ao chegar a uma folha, o modelo usa os rótulos dos exemplos de treino que chegaram ali para formar seu score. O critério padrão usado é Gini, uma medida de mistura das classes. Uma folha com exemplos de uma só classe tem impureza menor. Se deixarmos a árvore detalhar demais o treino, ela pode aprender particularidades que não se repetem em novos dados. Limitamos profundidade e tamanho mínimo das folhas para controlar parte dessa complexidade.

Fontes e evidências: Breiman (1996, 2001), em docs/referencias.md; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.

## Slide 10 Bagging e amostras bootstrap

Tempo sugerido: 2 min.

A analogia é um conjunto de revisores que analisam versões diferentes do material de treinamento. A técnica de bagging cria amostras com reposição: sorteamos registros, e o mesmo registro pode aparecer mais de uma vez na amostra de uma árvore. Cada árvore aprende com uma combinação diferente. Todas as amostras vêm apenas do treino. A validação e o teste não entram nesse sorteio. O objetivo da combinação é reduzir a instabilidade de uma árvore isolada, que pode mudar bastante se o treinamento mudar. Usamos 100 árvores. Mais árvores podem estabilizar a agregação, mas também consomem mais tempo e memória, e não garantem corrigir dados ruins ou ausência de sinal. Breiman descreve o bagging como fundamento da agregação de modelos; a floresta acrescenta mais uma fonte de diversidade.

Fontes e evidências: Breiman (1996, 2001), em docs/referencias.md; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.

## Slide 11 Aleatoriedade entre variáveis

Tempo sugerido: 1.5 min.

Além de variar os registros de treino, a floresta varia as variáveis candidatas em cada divisão. Com max_features igual a sqrt, o algoritmo considera aproximadamente a raiz quadrada do número de entradas a cada nó. Isso ajuda a evitar que todas as árvores sigam sempre o mesmo componente dominante. A escolha do melhor corte continua sendo aprendida a partir dos candidatos daquele nó. Não é simplesmente uma divisão aleatória de tudo. Na ablação, o número de entradas muda de 30 para 27, mas a regra sqrt é mantida. A combinação é útil quando as árvores trazem informações parcialmente diferentes. Se o conjunto inteiro não contém um padrão capaz de distinguir determinada fraude, combinar 100 árvores não cria essa informação.

Fontes e evidências: Breiman (1996, 2001), em docs/referencias.md; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.

## Slide 12 Do score das árvores ao alerta

Tempo sugerido: 2 min.

Uma simplificação comum é dizer que as árvores votam. Isso ajuda na intuição, mas precisamos explicar a implementação usada. No RandomForestClassifier do scikit-learn, cada árvore produz probabilidades baseadas nas classes presentes em suas folhas, considerando os pesos quando existem. A floresta calcula a média desses scores. Nosso protótipo compara a média com o limiar escolhido: score maior ou igual ao limiar produz alerta. Por exemplo, numa ilustração com três árvores dando 0,2, 0,6 e 0,8, a média seria aproximadamente 0,533 e haveria alerta com limiar 0,50. Esse exemplo é didático, não é uma medição do dataset. Sem calibração e avaliação apropriada, não podemos concluir que score de 0,8 representa 80% de chance de fraude na prática. A tela mostra a contribuição das 100 árvores para tornar essa agregação visível.

Fontes e evidências: Breiman (1996, 2001), em docs/referencias.md; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.

## Slide 13 Baseline e configuração de referência

Tempo sugerido: 1.5 min.

O baseline principal é uma árvore com profundidade máxima 12, mínimo de duas amostras por folha e pesos balanced. A floresta de referência usa os mesmos três parâmetros, além de 100 árvores, bootstrap e max_features sqrt. O balanced dá mais peso aos exemplos da classe rara durante o ajuste. Isso pode mudar os cortes e os scores, mas não garante melhorar todas as métricas. O número de árvores foi mantido constante nos três experimentos. Não fazemos uma busca sem limite por combinações, nem reamostragem com SMOTE. A ideia é permitir que outra pessoa identifique qual fator mudou em cada comparação. Até aqui, explicamos o modelo e a preparação. André vai mostrar como as hipóteses foram testadas e como chegamos à configuração final.

Fontes e evidências: Breiman (1996, 2001), em docs/referencias.md; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.

## Perguntas que você deve dominar

## Por que Random Forest?

O tema foi sorteado. A técnica é adequada para investigar combinações não lineares em dados tabulares e permite comparação direta com uma árvore. Isso justifica o estudo, sem provar que seja a melhor técnica disponível.

## Por que usar uma árvore como baseline?

Ela usa a mesma família de regras e torna observável o valor da agregação de 100 árvores. A comparação usa a mesma separação de dados. Sempre normal é uma referência adicional para mostrar a armadilha da acurácia.

## Por que retirar balanced se fraude é rara?

Foi uma hipótese controlada, não uma regra geral. Na validação, reduziu FP de 15 para 8, elevou precisão e F1, mas baixou recall. O objetivo escolhido foi F1 no limiar 0,50.

## A votação é por maioria?

Na implementação usada, predict_proba calcula a média dos scores de classe das árvores. O protótipo compara esse score médio com o limiar. A analogia de votação é apenas introdutória.
