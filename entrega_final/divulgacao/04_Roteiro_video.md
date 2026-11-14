# Vídeo demonstrativo

Narração sintética em português, sem imitar a voz de um integrante. Capturas do protótipo executado localmente.

## 01_problema

Como identificar fraudes sem gerar alertas demais? Nosso projeto usa uma floresta de cem árvores para apoiar a revisão de transações. O resultado é um score, e a comparação com um limiar indica se uma entrada merece análise.

## 02_normal

Este é o protótipo funcionando localmente. Selecionamos um exemplo normal da validação e pedimos a análise. A tela mostra o score da primeira transação e a contribuição de cada árvore. O score da floresta é a média desses valores.

## 03_fraude

Agora escolhemos uma fraude conhecida da validação. Com limiar de zero vírgula cinquenta, o sistema pode gerar um alerta de revisão. Também podemos editar Time, Amount e os componentes anonimizados. Uma combinação editada não tem gabarito e pode não representar uma compra real.

## 04_falha

O modelo também falha. Este exemplo é uma fraude que recebeu score muito baixo e passou sem alerta. Outro caso normal recebeu score alto e gerou um falso positivo. Reduzir o limiar tende a aumentar alertas, mas não garante encontrar todas as fraudes.

## 05_metricas

Três experimentos compararam pesos, profundidade e remoção de componentes. A configuração foi escolhida pelo F um na validação, antes do teste. No teste reservado, a floresta encontrou sessenta e oito das noventa e cinco fraudes, perdeu vinte e sete e gerou quatro falsos alertas. A árvore encontrou setenta e uma fraudes e gerou duzentos e cinquenta e seis falsos alertas. A floresta teve precisão de noventa e quatro vírgula quarenta e quatro por cento, recall de setenta e um vírgula cinquenta e oito por cento e F um de zero vírgula oito um quatro quatro.

## 06_limites

O ganho em precisão veio com recall menor que o da árvore. A base contém apenas dois dias de dois mil e treze, e os scores não foram calibrados. O protótipo é educacional e mantém revisão humana. O repositório reúne código, resultados e instruções para executar. Grupo três, Inteligência Artificial dois, FIB.