# Guia de apresentação de Felipe

Felipe Inácio de Paula. Responsabilidade de material: GitHub e protótipo. Tema de fala: Erros, demonstração e conclusão. Slides 20 a 23, aproximadamente 9 minutos.

## O que conferir antes do ensaio

Abra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.

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

## Perguntas que você deve dominar

## Por que o modelo final encontrou menos fraudes que a árvore no teste?

A configuração escolhida é mais seletiva no limiar usado. Encontrou 68 de 95, contra 71 da árvore. A melhora em F1 e precisão não implica melhora de recall. Não ajustamos após avaliar o teste.

## Vocês melhoraram o resultado olhando o teste?

Não. O plano registra hipóteses e a decisão é salva em decisao_antes_do_teste.json antes das previsões no teste. A configuração foi escolhida somente pela validação. Mudanças futuras exigem outro protocolo e avaliação independente.

## Um score 0,8 significa 80% de chance?

Não podemos assumir isso. Os scores não foram calibrados nem validados para a população atual. Servem para classificação e comparação dentro do protocolo estudado.

## Por que permutação e impureza não são causa?

São medidas de dependência preditiva do modelo. Correlação, variáveis substitutas e o protocolo de amostragem afetam esses números. Nenhuma intervenção causal foi realizada.

## O protótipo funciona sem internet?

Sim, após instalar dependências e ter o modelo salvo. Não precisa baixar a base para fazer inferência. Antes da apresentação, abra o servidor local e teste o navegador. O vídeo e os PDFs são o plano B.

## Qual é a limitação mais importante?

A avaliação é aleatória em dois dias de 2013, com poucos positivos e sem separação por titular. Não demonstra desempenho futuro. Além disso, os componentes anonimizados e a falta de calibração limitam a aplicação.
