# Detecção de transações fraudulentas com Random Forest

Felipe Inácio de Paula; Gabriel Damante Frias; Maicon Manoel Rodrigues dos Santos; André Luiz Jeremias Pereira Junior; Lavinia Zanata Alves

Faculdades Integradas de Bauru | Ciência da Computação | Inteligência Artificial II

## Introdução

A identificação de fraudes em cartões exige reconhecer uma classe rara sem gerar alertas excessivos sobre transações legítimas. O desbalanceamento e a evolução dos padrões tornam a avaliação parte central do problema (Dal Pozzolo et al., 2014). Random Forest combina árvores construídas com aleatoriedade para produzir uma decisão conjunta (Breiman, 2001). Este estudo compara essa abordagem com uma Árvore de Decisão em uma base pública de transações.

## Objetivos

Desenvolver um fluxo reproduzível para identificar transações potencialmente fraudulentas e comparar Random Forest com uma Árvore de Decisão, considerando precisão, recall, F1 e Average Precision. Como aplicação futura, será construído um painel educacional para inspeção de transações no formato da base.

## Relevância do estudo

A relevância está em investigar o custo dos erros: um falso negativo deixa uma fraude passar; um falso positivo sinaliza uma transação legítima. O estudo procura mostrar por que alta acurácia não basta e transformar as evidências em uma demonstração compreensível.

## Materiais e métodos preliminares

Utilizou-se Credit Card Fraud Detection, da colaboração ULB/Worldline, com 284.807 transações de dois dias de setembro de 2013, 492 delas fraudulentas (Machine Learning Group - ULB; Worldline, s.d.). Há 30 entradas numéricas: Time, Amount e V1 a V28, componentes de PCA previamente disponibilizados. Class é o alvo. A auditoria encontrou zero valores ausentes e 1.081 cópias completas adicionais. A remoção conservadora dessas cópias resultou em 283.726 registros, sendo 473 fraudes, evitando repetição de entradas entre conjuntos.

A base foi separada de forma estratificada em treino (60%), validação (20%) e teste (20%), com semente 42. O treino contém 170.235 registros e 284 fraudes; a validação, 56.745 e 94; o teste reservado, 56.746 e 95. A exploração detalhada foi feita no treino. Valores extremos foram investigados e preservados. Não há categorias para codificar; não se aplicou normalização por se tratar de modelos que dividem variáveis por limiares. O alvo foi excluído das entradas, sem transformações aprendidas na validação ou no teste (Scikit-learn Developers, s.d.).

Ambos os modelos usam profundidade máxima 12, mínimo de duas amostras por folha e pesos de classe balanced. A floresta possui 100 árvores e max_features=sqrt. As métricas preliminares são calculadas na validação, preservando o teste para a avaliação final. Average Precision resume a curva Precision-Recall; a escolha considera a avaliação de classes raras discutida por Saito e Rehmsmeier (2015).

## Resultados preliminares e discussão

A EDA mostrou forte desbalanceamento, mediana de Amount de 11,855 em fraudes contra 22,05 em transações normais no treino, e diferenças descritivas destacadas nos componentes V17, V14 e V12. As distribuições dos valores se sobrepõem; valores altos não definem fraude por si só. Os componentes não permitem interpretar diretamente características comerciais da compra.

Na validação, a floresta identificou 80 das 94 fraudes, deixando passar 14 e gerando 15 falsos alertas. A árvore identificou 75, deixou passar 19 e gerou 285 falsos alertas. O classificador que sempre prevê normal tem acurácia de 99,8343% e recall zero, ilustrando a insuficiência da acurácia isolada. A vantagem observada da floresta limita-se a essa configuração e divisão; não demonstra superioridade em outros períodos ou populações.

Métricas completas: ../results/metricas_validacao.csv

## Considerações parciais

O primeiro pipeline funciona da leitura dos dados à previsão, com resultados reproduzíveis. Os próximos experimentos investigarão pesos de classe, profundidade e remoção de componentes. Ainda faltam validação temporal, análise de incerteza e avaliação final no teste. A base antiga, o período curto, a anonimização e a ausência de calibração limitam o uso dos resultados; a aplicação é educacional e não substitui revisão humana.

## Referências

BREIMAN, L. Random Forests. Machine Learning, v. 45, p. 5-32, 2001. DOI: 10.1023/A:1010933404324. https://doi.org/10.1023/A:1010933404324

SAITO, T.; REHMSMEIER, M. The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. PLOS ONE, v. 10, n. 3, e0118432, 2015. DOI: 10.1371/journal.pone.0118432. https://doi.org/10.1371/journal.pone.0118432

DAL POZZOLO, A.; CAELEN, O.; LE BORGNE, Y.-A.; WATERSCHOOT, S.; BONTEMPI, G. Learned lessons in credit card fraud detection from a practitioner perspective. Expert Systems with Applications, v. 41, n. 10, p. 4915-4928, 2014. DOI: 10.1016/j.eswa.2014.02.026. https://doi.org/10.1016/j.eswa.2014.02.026

MACHINE LEARNING GROUP - ULB; WORLDLINE. Credit Card Fraud Detection. Kaggle. Base de transações de setembro de 2013. Acesso em: 20 out. 2026. https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

SCIKIT-LEARN DEVELOPERS. RandomForestClassifier. Documentação oficial. Versão executada: 1.9.1. Acesso em: 20 out. 2026. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

SCIKIT-LEARN DEVELOPERS. Common pitfalls and recommended practices. Documentação oficial. Acesso em: 20 out. 2026. https://scikit-learn.org/stable/common_pitfalls.html
