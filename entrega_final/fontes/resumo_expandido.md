# Detecção de transações fraudulentas com Random Forest

Felipe Inácio de Paula; Gabriel Damante Frias; Maicon Manoel Rodrigues dos Santos; André Luiz Jeremias Pereira Junior; Lavinia Zanata Alves

## Grupo de trabalho

Ciência da Computação.

## Palavras-chave

Random Forest; detecção de fraudes; desbalanceamento; classificação; avaliação de modelos.

## Introdução

A detecção de fraudes exige reconhecer uma classe rara sem gerar alertas excessivos sobre transações legítimas. O desbalanceamento e a mudança dos padrões limitam avaliações simplistas (Dal Pozzolo et al., 2014). Random Forest combina árvores construídas com aleatoriedade (Breiman, 2001), utilizando amostras bootstrap relacionadas ao bagging (Breiman, 1996). O estudo compara a técnica com uma árvore isolada e comunica os resultados por meio de um protótipo educacional.

## Objetivos

Investigar o efeito de pesos de classe, profundidade e remoção de componentes sobre a detecção de fraudes. Comparar Random Forest com uma Árvore de Decisão e disponibilizar uma aplicação para inspeção de scores, alertas e falhas.

## Relevância do Estudo

Um falso positivo aumenta a carga de revisão; um falso negativo deixa uma fraude passar. O projeto relaciona escolhas metodológicas a esses dois tipos de erro, sem inferir impacto financeiro não medido.

## Material e Métodos

Utilizou-se Credit Card Fraud Detection, da ULB/Worldline, com 284.807 transações de dois dias de setembro de 2013 e 492 fraudes. Há 30 entradas: Time, Amount e V1 a V28, componentes de PCA fornecidos pelos autores; Class é o alvo e foi excluído das entradas. Removeram-se 1.081 cópias completas adicionais, restando 283.726 registros e 473 fraudes. A divisão estratificada, com semente 42, reservou 60% para treino, 20% para validação e 20% para teste. A exploração detalhada foi restrita ao treino. Valores extremos foram preservados e não se aplicou nova normalização. O baseline é uma árvore com profundidade 12, duas amostras mínimas por folha e pesos balanced. A floresta de referência mantém esses parâmetros, com 100 árvores e max_features=sqrt. A implementação utiliza scikit-learn (Pedregosa et al., 2011).

## Material e Métodos

Registraram-se previamente três hipóteses: retirar pesos poderia reduzir falsos alertas; limitar a profundidade poderia simplificar o modelo; remover V17, V14 e V12 poderia retirar informação útil. Cada comparação alterou um fator em relação à referência. Selecionou-se a configuração de maior F1 da classe fraude na validação, com limiar 0,50 e AP para desempate. A AP complementa a análise da classe rara (Saito; Rehmsmeier, 2015). O teste foi avaliado após salvar a decisão, sem ajustes posteriores.

## Resultados e discussões

Na validação, a referência obteve F1 de 0,8466. Sem pesos, os falsos positivos caíram de 15 para 8, os falsos negativos subiram de 14 para 17 e o F1 aumentou para 0,8603. A profundidade 6 elevou recall a 88,30%, mas gerou 138 falsos positivos, com F1 de 0,5270. A remoção dos três componentes manteve recall em 85,11%, elevou F1 a 0,8511 e reduziu AP de 0,8611 para 0,8540, contrariando uma piora uniforme. Selecionou-se a configuração sem pesos. No teste reservado, com 56.746 transações e 95 fraudes, a floresta identificou 68 fraudes, perdeu 27 e gerou 4 falsos positivos: precisão 94,44%, recall 71,58%, F1 0,8144 e AP 0,7867. A árvore identificou 71, perdeu 24 e gerou 256 falsos positivos, com F1 0,3365. Os intervalos de Wilson de 95% foram 86,57–97,82% para precisão e 61,81–79,67% para recall da floresta. Foram examinados quatro erros reais da validação. O protótipo permite entrada manual, CSV e exploração do limiar.

## Conclusão

A floresta apresentou maior precisão, F1 e AP que a árvore neste protocolo, com recall menor. O resultado favorece uma triagem mais seletiva e não demonstra superioridade em todas as métricas. A base antiga, a divisão aleatória, a ausência de identificação de titulares e os scores sem calibração impedem generalizar para uso operacional. Validação temporal, calibração e custos reais são próximos passos. A aplicação é educacional e mantém a revisão humana.

## Referências

BREIMAN, L. Random Forests. Machine Learning, v. 45, p. 5–32, 2001. DOI: 10.1023/A:1010933404324.

BREIMAN, L. Bagging predictors. Machine Learning, v. 24, p. 123–140, 1996. DOI: 10.1007/BF00058655.

DAL POZZOLO, A. et al. Learned lessons in credit card fraud detection from a practitioner perspective. Expert Systems with Applications, v. 41, p. 4915–4928, 2014. DOI: 10.1016/j.eswa.2014.02.026.

PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. JMLR, v. 12, p. 2825–2830, 2011.

SAITO, T.; REHMSMEIER, M. The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. PLOS ONE, v. 10, e0118432, 2015. DOI: 10.1371/journal.pone.0118432.

ULB; WORLDLINE. Credit Card Fraud Detection. Kaggle. Disponível em: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud. Acesso em: 13 nov. 2026.