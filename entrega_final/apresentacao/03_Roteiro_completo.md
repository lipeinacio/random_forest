# Roteiro da apresentação do Caçador de Fraudes

Núcleo de aproximadamente 40 minutos, com cinco integrantes. Os tempos incluem leitura dos gráficos, interação e demonstração. As falas são um roteiro de estudo. O grupo precisa ensaiar, explicar com suas palavras e conferir o tempo real. Os slides 24 e 25 são apêndices.

## Distribuição e transições

Lavinia: slides 1 a 4, de 0 a 5 minutos. Material: Resumo expandido e Instagram.
Maicon: slides 5 a 8, de 5 a 12 minutos. Material: Vídeo e Model Card.
Gabriel: slides 9 a 13, de 12 a 21 minutos. Material: Folder.
André: slides 14 a 19, de 21 a 31 minutos. Material: Ficha de experimentos.
Felipe: slides 20 a 23, de 31 a 40 minutos. Material: GitHub e protótipo.

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

## Slide 5 Dados ULB e Worldline

Tempo sugerido: 2 min.

A fonte é a base Credit Card Fraud Detection, publicada pela colaboração ULB e Worldline no Kaggle. Ela contém transações de titulares europeus em dois dias de setembro de 2013. São 284.807 registros e 492 fraudes. Cada transação tem 30 entradas numéricas. Time representa segundos desde a primeira transação. Amount é o valor. V1 a V28 são componentes de uma PCA que os autores já forneceram. Nós não conhecemos as variáveis comerciais originais nem podemos chamar V17 de localização, idade ou qualquer outro atributo. Class é o gabarito: zero para normal e um para fraude. Excluímos Class da entrada do modelo. Essa anonimização ajuda a disponibilizar a base, mas restringe a interpretação e a criação de entradas: o protótipo precisa receber dados já nesse espaço de componentes.

Fontes e evidências: data/README.md; results/auditoria.json; https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud.

## Slide 6 Auditoria e preparação

Tempo sugerido: 1.5 min.

Antes do treino, conferimos o esquema, a ausência de valores não finitos, os rótulos e o hash SHA-256 do arquivo. A base utilizada não apresentou valores ausentes. Encontramos 1.081 cópias completas adicionais e removemos essas cópias antes de separar os conjuntos. Restaram 283.726 registros, com 473 fraudes. Essa decisão evita que uma entrada idêntica apareça no treino e na avaliação. Não permite afirmar que os titulares são diferentes, porque a base não fornece identificadores de cartão. Investigamos extremos no treino com limites de IQR, mas não os removemos automaticamente: uma transação extrema pode ser justamente relevante para fraude. Não aplicamos uma nova normalização. Os dois modelos dividem cada variável por limiares e não dependem de distâncias entre escalas.

Fontes e evidências: data/README.md; results/auditoria.json; https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud.

## Slide 7 Treino, validação e teste

Tempo sugerido: 2 min.

Treino é o conjunto usado para ajustar as árvores. Validação serve para comparar configurações e escolher uma delas. Teste serve para medir o modelo depois que essa decisão está fechada. Fizemos uma divisão estratificada em 60%, 20% e 20%, com semente 42. A estratificação mantém uma proporção semelhante da classe rara, mas não faz as fraudes de treino e avaliação se tornarem iguais. Além de verificar índices separados, comparamos hashes das entradas para detectar repetições entre conjuntos. A exploração detalhada e a escolha dos componentes para a ablação vieram do treino. O teste só foi avaliado após salvar o plano e a decisão final. Ressalva: a separação é aleatória. Como os dados têm dois dias e não há identificador de titular, isso não reproduz necessariamente a chegada de novas transações no futuro.

Fontes e evidências: data/README.md; results/auditoria.json; https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud.

## Slide 8 Três descobertas sobre os dados

Tempo sugerido: 1.5 min.

A primeira descoberta é o desbalanceamento: ele explica por que devemos acompanhar a classe fraude separadamente. A segunda é que a mediana do valor das fraudes no treino foi 11,855, enquanto nas transações normais foi 22,05. Portanto, não faz sentido usar uma regra simplista de que compra cara é fraude. O gráfico usa log de um mais Amount para mostrar a distribuição, mas essa transformação foi usada na visualização, não como uma entrada nova do modelo. A terceira descoberta foi o destaque de V17, V14 e V12 na diferença de médias entre classes em unidades do desvio do treino. Isso é uma associação descritiva. Não estabelece causa nem revela o significado comercial dos componentes. Com os dados contextualizados, Gabriel vai explicar o funcionamento da árvore e da floresta.

Fontes e evidências: data/README.md; results/auditoria.json; https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud.

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

## Slide 20 Falhas reais na validação

Tempo sugerido: 2 min.

Escolhemos casos reais da validação para não usar o teste como coleção de exemplos para ajustar a solução. Na linha 50537, uma fraude de valor 1 recebeu um score muito baixo e passou sem alerta. Na linha 118308, outra fraude, de valor 30,14, também recebeu score muito baixo. Esses casos mostram que não basta baixar um pouco o limiar para capturar toda fraude. Na linha 14920, uma transação rotulada normal recebeu score 0,8228 e gerou um falso alerta. Vários componentes desse caso têm valores extremos, mas isso é uma hipótese descritiva para investigação, não uma explicação causal validada. Também temos a linha 164955, normal de valor 119,99, com score 0,813. As falhas mostram os limites da informação disponível e do modelo. A ação do protótipo é revisão, sem autorização automática de bloqueio.

Fontes e evidências: results/final/casos_erros.csv. Linhas identificam o índice original do CSV, não pessoas.

## Slide 21 Importância e incerteza

Tempo sugerido: 1.5 min.

Para complementar a importância por impureza, calculamos importância por permutação na validação, com três repetições. Embaralhamos uma variável e medimos a queda de AP. V14 teve a maior queda média. Isso mede dependência preditiva nessa avaliação, não causalidade, e pode ser afetado por informação compartilhada entre variáveis. Os intervalos de Wilson no teste foram de 86,57% a 97,82% para precisão e de 61,81% a 79,67% para recall. O bootstrap estratificado de mil repetições produziu intervalo aproximado de F1 de 0,7468 a 0,8721. Esses intervalos são condicionais ao modelo e à divisão utilizados. Não cobrem mudança dos padrões ao longo do tempo nem a variabilidade de novos treinos. A base tem apenas dois dias de 2013 e os scores não foram calibrados.

Fontes e evidências: results/final/importancia_permutacao.csv; results/final/teste.json.

## Slide 22 Demonstração do protótipo

Tempo sugerido: 3.5 min.

Comece com a aplicação já aberta. Selecione o primeiro exemplo normal e clique em analisar. Mostre que o score é agregado das 100 árvores. Escolha o quarto exemplo, uma fraude conhecida, e analise. Explique o alerta no limiar 0,50. Escolha o sétimo exemplo, um falso negativo, e mostre que mesmo uma fraude real pode receber score próximo de zero. Selecione um falso positivo e aumente o limiar, observando se o alerta muda. Diga que a métrica oficial permanece no limiar 0,50. Convide alguém a alterar Amount ou um componente, deixando claro que a nova combinação pode não representar uma compra real e não tem gabarito. Em seguida, abra a opção de CSV, carregue demo_final.csv, analise e baixe o resultado. Se a plateia fornecer dados válidos no esquema da base, teste-os. Se faltar coluna ou houver Class, mostre a mensagem de validação. Para falha de rede, a aplicação é local. Para falha do servidor, use o vídeo e as capturas, anunciando que são gravações.

Fontes e evidências: README.md; docs/referencias.md; results/final/conclusao.json.

## Slide 23 Conclusões e próximos passos

Tempo sugerido: 2 min.

Respondendo à pergunta inicial: nesta base e nesta divisão, a floresta acrescentou valor em precisão e F1 em relação à árvore. Ela gerou quatro falsos alertas, mas deixou 27 das 95 fraudes passarem. Portanto, o resultado não sustenta um uso autônomo nem superioridade em todas as métricas. A seleção por F1 produziu uma configuração mais seletiva. Se a prioridade for encontrar mais fraudes, será necessário definir uma meta de recall, estudar limiares na validação e medir o custo de novos alertas, com outro conjunto independente para confirmar qualquer nova decisão. Como continuidade, propomos validação temporal, calibração dos scores e análise da capacidade humana de revisão. Essas etapas não foram realizadas neste trabalho. A principal aprendizagem foi que avaliar uma IA exige explicitar a escolha, contar os erros e mostrar os casos em que ela falha. Abrimos para perguntas.

Fontes e evidências: README.md; docs/referencias.md; results/final/conclusao.json.

## Perguntas e respostas para o grupo

## Por que Random Forest?

O tema foi sorteado. A técnica é adequada para investigar combinações não lineares em dados tabulares e permite comparação direta com uma árvore. Isso justifica o estudo, sem provar que seja a melhor técnica disponível.

## Por que usar uma árvore como baseline?

Ela usa a mesma família de regras e torna observável o valor da agregação de 100 árvores. A comparação usa a mesma separação de dados. Sempre normal é uma referência adicional para mostrar a armadilha da acurácia.

## Por que retirar balanced se fraude é rara?

Foi uma hipótese controlada, não uma regra geral. Na validação, reduziu FP de 15 para 8, elevou precisão e F1, mas baixou recall. O objetivo escolhido foi F1 no limiar 0,50.

## Por que o modelo final encontrou menos fraudes que a árvore no teste?

A configuração escolhida é mais seletiva no limiar usado. Encontrou 68 de 95, contra 71 da árvore. A melhora em F1 e precisão não implica melhora de recall. Não ajustamos após avaliar o teste.

## Vocês melhoraram o resultado olhando o teste?

Não. O plano registra hipóteses e a decisão é salva em decisao_antes_do_teste.json antes das previsões no teste. A configuração foi escolhida somente pela validação. Mudanças futuras exigem outro protocolo e avaliação independente.

## Qual foi o maior problema nos dados?

O desbalanceamento extremo é o principal desafio de avaliação. A auditoria também encontrou 1.081 cópias completas adicionais e a PCA pronta restringe a interpretação e o uso de entradas novas.

## Por que remover duplicados antes da divisão?

Para impedir que uma entrada idêntica influencie o treino e a avaliação. A decisão mudou o universo de 492 para 473 fraudes. Sem titular/cartão, não podemos assegurar independência por cliente.

## Por que não usar SMOTE?

Não era obrigatório. Mantivemos as distribuições e isolamos os efeitos de pesos, profundidade e remoção de componentes. SMOTE seria outro experimento, restrito ao treino e com avaliação separada.

## Precisaram padronizar?

Não para esses classificadores de árvores, que usam cortes por variável. Time e Amount têm escalas diferentes, mas isso não cria o problema de distância encontrado em outros algoritmos. O gráfico de Amount usa log só na visualização.

## O que são V1 a V28?

Componentes de PCA disponibilizados pelos autores. Não temos a transformação original nem o significado comercial. Não é possível converter livremente uma compra bruta em entrada válida do modelo.

## A votação é por maioria?

Na implementação usada, predict_proba calcula a média dos scores de classe das árvores. O protótipo compara esse score médio com o limiar. A analogia de votação é apenas introdutória.

## O que é AP?

Average Precision resume precisão ao longo das mudanças de recall. É útil para classe rara e ranking, mas não substitui contagem de erros num limiar. Não é acurácia nem uma área trapezoidal necessariamente idêntica.

## Por que não selecionar só recall?

Recall isolado pode chegar a 100% classificando todas as transações como fraude. É preciso considerar alertas falsos e capacidade de revisão. Um requisito operacional poderia impor um recall mínimo, mas não foi o critério deste estudo.

## Um score 0,8 significa 80% de chance?

Não podemos assumir isso. Os scores não foram calibrados nem validados para a população atual. Servem para classificação e comparação dentro do protocolo estudado.

## O que aconteceu ao remover V17, V14 e V12?

Na validação, recall permaneceu em 85,11%, F1 subiu levemente e AP caiu. O efeito misto contraria uma piora uniforme. Pode haver sinal compartilhado com outros componentes, mas não testamos a causa dessa compensação.

## Por que permutação e impureza não são causa?

São medidas de dependência preditiva do modelo. Correlação, variáveis substitutas e o protocolo de amostragem afetam esses números. Nenhuma intervenção causal foi realizada.

## O que significam os intervalos de confiança?

Wilson descreve a incerteza de proporções de precisão e recall nesta amostra. O bootstrap estratificado reamostra positivos e negativos do teste fixo para estimar F1. Não inclui drift nem variabilidade de diferentes treinos.

## O protótipo funciona sem internet?

Sim, após instalar dependências e ter o modelo salvo. Não precisa baixar a base para fazer inferência. Antes da apresentação, abra o servidor local e teste o navegador. O vídeo e os PDFs são o plano B.

## Qual é a limitação mais importante?

A avaliação é aleatória em dois dias de 2013, com poucos positivos e sem separação por titular. Não demonstra desempenho futuro. Além disso, os componentes anonimizados e a falta de calibração limitam a aplicação.

## O que o grupo precisa estudar antes de apresentar?

Todos devem explicar problema, fonte, separação, métricas, três experimentos e limitações. Cada pessoa conduz sua parte, mas deve responder sobre o conjunto. O ensaio e a confirmação de domínio são tarefas reais do grupo.

## Plano B da demonstração

Instale as dependências antes de ir à sala. A inferência usa o modelo já salvo e não exige internet nem a base completa. Abra o servidor antes da fala. Mantenha o vídeo, o PDF dos slides e as capturas disponíveis localmente. Se mostrar a gravação, identifique-a como gravação. Para uma pergunta sem evidência, explique o limite e como faria o experimento.
