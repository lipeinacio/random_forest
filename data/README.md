# Dados e atribuição

Fonte oficial: Machine Learning Group - ULB e Worldline. **Credit Card Fraud Detection**.
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Base original: transações de titulares europeus em dois dias de setembro de 2013.
284.807 registros, 31 colunas, 30 entradas e alvo `Class` (0 normal, 1 fraude).
`V1` a `V28` são componentes de PCA previamente fornecidos. Seus significados
originais e os parâmetros da transformação não estão disponíveis. `Time` é o tempo
em segundos desde a primeira transação; `Amount` é o valor da transação.

O CSV completo é obtido com `python src/baixar_dados.py`. Ele não entra no Git.
Também é possível baixar pela página oficial e salvar `data/creditcard.csv`.

SHA-256 da versão utilizada:
`76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`

Licença indicada na fonte: Database: Open Database; Contents: Database Contents.
Confira os termos na página oficial antes de redistribuir uma base derivada.
Os pequenos CSVs em `demo/` são extratos anonimizados dessa fonte para demonstração.
A base não contém nomes, números de cartão ou campos de localização interpretáveis.

Referência associada: DAL POZZOLO, A.; CAELEN, O.; JOHNSON, R. A.; BONTEMPI, G.
Calibrating Probability with Undersampling for Unbalanced Classification. IEEE SSCI,
2015, p. 159–166. https://doi.org/10.1109/SSCI.2015.33
