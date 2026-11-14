# Model Card do Caçador de Fraudes

## Solução e objetivo

Caçador de Fraudes. Apoio educacional à triagem de transações para revisão humana.

## Técnica

RandomForestClassifier, scikit-learn 1.9.1. 100 árvores, max_depth=12, min_samples_leaf=2, max_features=sqrt, bootstrap=True, class_weight=None, seed=42. Limiar oficial 0,50.

## Dados e preparação

ULB/Worldline, dois dias de setembro de 2013. 284.807 transações e 492 fraudes na origem. Após remover 1.081 cópias completas: 283.726 registros e 473 fraudes. Divisão estratificada 60/20/20; treino apenas no primeiro conjunto. Sem normalização nova ou remoção automática de extremos.

## Entradas e saída

Time, Amount e V1 a V28 numéricos e finitos. Class nunca é entrada. A saída contém score sem calibração e sugestão de revisão. V1 a V28 já são PCA e não possuem semântica comercial disponível.

## Seleção e métrica principal

Maior F1 da fraude na validação, com AP como desempate e limiar 0,50. Configuração sem pesos: F1 0,8603 na validação. Decisão gravada antes de avaliar o teste.

## Resultado final no teste

56.746 transações, 95 fraudes. TP=68, FN=27, FP=4, TN=56.647. Precisão 94,44%; recall 71,58%; F1 0,8144; AP 0,7867. Wilson 95%: precisão 86,57–97,82%; recall 61,81–79,67%.

## Baseline e troca observada

Árvore isolada: TP=71, FN=24, FP=256, F1 0,3365 no mesmo teste. A floresta reduz falsos alertas e melhora F1, porém tem recall menor.

## Limitações e riscos

Base antiga e curta; divisão aleatória; poucos positivos; sem independência conhecida por titular; escopo da PCA original desconhecido; sem calibração ou validação temporal. Não foi estimado custo monetário. Alertas podem gerar revisão indevida, e fraudes podem passar.

## Quando não utilizar

Não usar para bloquear compras, decidir sobre pessoas ou operar sem avaliação atual, supervisão e validação apropriada. Não fornecer compras brutas sem a mesma transformação de dados. Cenários editados no protótipo podem não representar transações reais.

## Reprodução e responsáveis

Grupo 3, IA II, FIB. Código e evidências: https://github.com/lipeinacio/random_forest. Script src/finalizar.py; plano, decisão e métricas em results/final/. Modelos salvos em models/final/.