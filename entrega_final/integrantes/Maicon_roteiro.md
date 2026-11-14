# Guia de apresentação de Maicon

Maicon Manoel Rodrigues dos Santos. Responsabilidade de material: Vídeo e Model Card. Tema de fala: Público, dataset e qualidade. Slides 5 a 8, aproximadamente 7 minutos.

## O que conferir antes do ensaio

Abra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.

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

## Perguntas que você deve dominar

## Qual foi o maior problema nos dados?

O desbalanceamento extremo é o principal desafio de avaliação. A auditoria também encontrou 1.081 cópias completas adicionais e a PCA pronta restringe a interpretação e o uso de entradas novas.

## Por que remover duplicados antes da divisão?

Para impedir que uma entrada idêntica influencie o treino e a avaliação. A decisão mudou o universo de 492 para 473 fraudes. Sem titular/cartão, não podemos assegurar independência por cliente.

## Precisaram padronizar?

Não para esses classificadores de árvores, que usam cortes por variável. Time e Amount têm escalas diferentes, mas isso não cria o problema de distância encontrado em outros algoritmos. O gráfico de Amount usa log só na visualização.

## O que são V1 a V28?

Componentes de PCA disponibilizados pelos autores. Não temos a transformação original nem o significado comercial. Não é possível converter livremente uma compra bruta em entrada válida do modelo.
