# Demonstração — Caçador de Fraudes

Gravação real da aplicação, com diagramas didáticos e narração sintética em português do Brasil (Microsoft Maria Desktop).

## Capítulos

- 00:00 — Uma ajuda para revisar transações
- 00:22 — Uma árvore é uma sequência de perguntas
- 00:53 — A floresta combina 100 árvores
- 01:28 — O índice vem da média dos scores
- 02:01 — O que entra na análise
- 02:35 — Treino, validação e teste têm papéis diferentes
- 03:10 — Na prática: uma compra comum
- 03:44 — Na prática: uma fraude conhecida
- 04:09 — Mudar o corte muda o alerta, não o índice
- 04:41 — Quando uma fraude passa sem alerta
- 05:11 — Quando uma compra legítima gera alerta
- 05:32 — Editar dados cria um cenário sem gabarito
- 05:57 — Os scores das árvores, por dentro
- 06:22 — Analisando várias transações em um CSV
- 06:57 — O resultado no teste reservado
- 07:31 — Precisão e recall respondem perguntas diferentes
- 08:07 — Menos alarmes falsos, com uma troca
- 08:37 — Uma ferramenta para aprender e revisar

## Uma ajuda para revisar transações

Este é o Caçador de Fraudes, um aplicativo educacional que usa inteligência artificial para analisar transações.

A pergunta principal é: esta compra merece uma revisão humana?

Vamos entender a árvore de decisão, a floresta e o significado dos resultados, acompanhando o aplicativo de verdade.

## Uma árvore é uma sequência de perguntas

Uma árvore de decisão funciona como uma sequência de perguntas sobre os números de uma transação.

Neste desenho fictício, a primeira pergunta separa compras pelo valor. Outra pergunta examina um componente dos dados.

Cada resposta leva a um galho. O caminho termina em uma folha, que produz um score para a classe fraude.

As perguntas e os valores de corte são aprendidos durante o treinamento. Não escrevemos manualmente todas essas regras.

## A floresta combina 100 árvores

Uma árvore sozinha pode decorar particularidades do treino e falhar em transações diferentes. Isso é chamado de sobreajuste.

A floresta do projeto combina cem árvores. No treinamento, cada uma recebe uma amostra aleatória, com repetições.

Além disso, cada nova pergunta considera apenas parte dos campos disponíveis, escolhida aleatoriamente.

Isso cria caminhos diferentes. Combinar os scores das árvores ajuda, mas não garante que a floresta sempre acerte.

## O índice vem da média dos scores

Para simplificar, imagine apenas três árvores com scores de zero vírgula dois, zero vírgula sete e zero vírgula nove.

A média desses valores é zero vírgula seis. Multiplicando por cem, o aplicativo mostra um índice sessenta.

No modelo real, a média usa cem árvores. Um índice oitenta e três não significa oitenta e três votos em fraude.

O índice também não comprova uma probabilidade real de fraude. Os scores não foram calibrados para isso.

## O que entra na análise

O aplicativo recebe trinta números. Amount é o valor da transação. Time é o tempo desde a primeira transação da base.

Os outros vinte e oito campos são componentes numéricos de uma transformação chamada pê cê a, já fornecida na base.

Não conhecemos seus significados comerciais originais. Não podemos chamar um desses componentes de loja ou localização.

Existe ainda o gabarito, chamado Class: zero para compra legítima e um para fraude. Ele não entra na previsão.

## Treino, validação e teste têm papéis diferentes

O treinamento aconteceu antes de abrir o aplicativo. A base histórica foi limpa, removendo registros duplicados.

Sessenta por cento dos dados foram usados para ensinar os modelos. Vinte por cento serviram para comparar configurações.

Os vinte por cento restantes ficaram reservados para o teste final, depois de escolher a configuração na validação.

O modelo treinado foi salvo em um arquivo. Clicar em analisar apenas aplica esse modelo: não acontece um novo treinamento.

## Na prática: uma compra comum

Agora vamos usar o aplicativo. Na tela de análise, escolho compra comum. Os dados do exemplo já vêm preenchidos.

Clico em analisar transação. A floresta avalia os trinta campos e o resultado aparece à direita.

O índice ficou abaixo do corte cinquenta, então não houve alerta. O gabarito confirma que este exemplo é legítimo.

Sem alerta não é garantia de segurança. É apenas a sugestão do modelo para estes dados e este corte.

## Na prática: uma fraude conhecida

Agora escolho compra com fraude e peço outra análise. Este exemplo tem fraude confirmada no gabarito da base.

O índice ficou em oitenta e três, acima do corte cinquenta. A sugestão é enviar para revisão humana.

Neste caso o modelo acertou. Mas o alerta, sozinho, não confirma fraude e não autoriza bloquear uma compra.

## Mudar o corte muda o alerta, não o índice

Vou abrir o ajuste de sensibilidade e aumentar o ponto de corte de cinquenta para noventa.

Ao analisar a mesma transação, o índice continua oitenta e três. Como ficou abaixo de noventa, o alerta desaparece.

O modelo não mudou. Mudou apenas a exigência para emitir um alerta, e esta fraude passou sem alerta.

Diminuir o corte tende a gerar mais alertas e também mais alarmes falsos. Aumentar o corte pode deixar mais fraudes passarem.

## Quando uma fraude passa sem alerta

Restauro o corte cinquenta e escolho desafie o modelo. Aqui temos um erro real da validação.

O gabarito confirma uma fraude, mas o índice é muito baixo e a floresta não gera alerta.

Esse erro é chamado de falso negativo: uma fraude que não foi detectada.

Neste exemplo, nem o menor corte disponível no aplicativo resolve o erro. Mudar a sensibilidade não garante encontrar todas as fraudes.

## Quando uma compra legítima gera alerta

Avanço para outro caso de erro. Agora o índice é alto e a sugestão é revisar a transação.

Só que o gabarito confirma uma compra legítima. Esse é um falso positivo, ou alarme falso.

Esses dois tipos de erro mostram por que precisamos avaliar o modelo e manter uma revisão humana.

## Editar dados cria um cenário sem gabarito

Também é possível abrir os dados e alterar o valor da transação. Vou fazer uma edição e analisar novamente.

O aplicativo avisa que este cenário não tem gabarito associado, porque os dados já não são os mesmos do exemplo original.

Alterar apenas o valor não garante mudar o resultado. A floresta considera o conjunto dos trinta campos.

## Os scores das árvores, por dentro

Restauro um exemplo de fraude e abro a visualização das árvores. Cada quadradinho representa uma árvore.

Quanto mais escuro, maior o score atribuído por ela. Algumas árvores podem discordar das outras.

A média dos cem scores gera o índice da floresta. Esta visualização mostra os scores, mas não explica a causa de uma compra ser fraudulenta.

## Analisando várias transações em um CSV

Para analisar várias transações, escolho enviar um arquivo de valores separados por vírgula, no formato cê ésse vê.

O arquivo precisa das mesmas trinta colunas numéricas. Não pode incluir Class, porque ela contém o gabarito.

Envio o arquivo de demonstração e clico em analisar. O resumo mostra quantas linhas foram analisadas e quantas precisam de revisão.

O indicador principal se refere à primeira linha. A tabela e o arquivo de resultados permitem consultar as outras transações.

## O resultado no teste reservado

Na seção resultados do modelo, vemos a avaliação em cinquenta e seis mil, setecentas e quarenta e seis transações.

Havia noventa e cinco fraudes conhecidas. A floresta encontrou sessenta e oito e deixou vinte e sete passarem.

Também gerou quatro alarmes falsos, ou seja, quatro compras legítimas que foram encaminhadas para revisão.

Esses resultados usam o modelo escolhido na validação e o corte padrão cinquenta. Mudar o corte na demonstração não altera estas métricas.

## Precisão e recall respondem perguntas diferentes

Precisão pergunta: entre os alertas emitidos, quantos eram realmente fraudes? Foram sessenta e oito de setenta e dois alertas.

Por isso a precisão foi noventa e quatro vírgula quarenta e quatro por cento.

Recall pergunta: entre todas as fraudes existentes, quantas foram encontradas? Foram sessenta e oito de noventa e cinco.

O recall foi setenta e um vírgula cinquenta e oito por cento. O F um combina precisão e recall, e ficou em aproximadamente zero vírgula oito um quatro.

## Menos alarmes falsos, com uma troca

Na comparação deste projeto, a árvore isolada encontrou setenta e uma fraudes e gerou duzentos e cinquenta e seis alarmes falsos.

A floresta final encontrou sessenta e oito fraudes e gerou quatro alarmes falsos. Ela reduziu bastante a revisão indevida, mas encontrou três fraudes a menos.

Também não basta olhar a acurácia geral: como fraude é rara, responder tudo normal daria muitos acertos, sem encontrar uma única fraude.

## Uma ferramenta para aprender e revisar

A base contém apenas dois dias de dois mil e treze. Esses resultados não garantem desempenho em fraudes atuais.

Para usar o aplicativo, escolha um exemplo, peça a análise, leia a sugestão e compare com o gabarito quando ele estiver disponível.

Uma árvore faz perguntas. A floresta combina cem árvores. O índice resume os scores, e o ponto de corte transforma esse índice em alerta.

O objetivo é apoiar a revisão humana. Este é um projeto educacional do grupo três de Inteligência Artificial dois, da FIB.

