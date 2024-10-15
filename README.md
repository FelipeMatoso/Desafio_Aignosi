# Relatório Projeto Desafio de Dados Aignosi**

Este é o espaço dedicado ao relatório do desenvolvimento do projeto "Desafio de Dados da aignosi", realizado como parte do processo seletivo do candidato Felipe Amaral Matoso ao possível ingresso do mesmo a empresa Aignosi. 

**1- Entendimento do Problema**
    O primeiro paço para começar a desenvolver um projeto é buscar entender o problema proposto. No caso:
        * O objetivo é transformar dados não estruturados, que estão em um banco de dados MongoDB, em dados estruturados e criar uma API para consulta;
        * Será preciso aplicar técnicas de ETL para limpeza, normalização e estruturação dos dados para torná-los acessíveis e analisáveis;
    Desta forma, iniciei o processo procurando saber um pouco mais sobre essas técnicas e tecnologias que serião utilizadas e definir um breve conceito sobre elas:
        * Dados não estruturados: são dados que não estão organizados em um modelo tabular ou uma estrutura projetada. Geralmente, são armazenados em softwares de Banco de Dados NoSQL ("Não só SQL", ou um tipo de BD não-relacional);
        * MongoDB: é um exemplo de software de Banco de Dados NoSQL, orientado a documentos livres, open-source e escrito em C++. Diferente de SGBD's tabulares famosos como postgreSQL e MySQL, o MongoDB foi feito para armazenar dados não estruturados, formatados como Binary JSON (Java Script Object Notation);
        * API(Application Programming Interface): é um "meio de campo" entre os softwares, que possibilita a comunicação e compartilhamento de dados entre 2 ou mais softwares;
        * Técnicas de ETL(Extract, Transform, Load): processo que consiste em combinar dados de várias fontes em um só repositóro;
    Defini-se então um caminho para resolução do problema:
        MongoDB -> Análise dos dados (python) -> ETL(Pandas...) -> API(?)

**2- Definição do Ambiente de Desenvolvimento**
    Como IDE a ser utilizada no projeto, escolhi o VSCode, por ter mais afinidade com o mesmo e por ter diversas funcionalidades e extensões que podem facilitar o processo de desenvolvimento. Como a linguagem a ser utilizada, primeiramente verifiquei a instalação e versão do Python na minha máquina utilizando o comando *python --version*.
    Confirmada a instalação, criei um repositório no GitHub chamado "Desafio_Aignosi" e clonei o repositório no VSCode. Voltando ao VSCode, criei um ambiente virtual (virtualenv), a fim de manter as dependências isoladas, com os comandos *python -m venv venv* e *venv\Scripts\activate*.

**3- Acessando a Base de Dados**
    Primeiro, escolhi realizar um teste de conexão a Base de Dados fornecida. Utilizando pymongo e suas bibliotecas, como no caso MongoClient, criei um folder denomindado *teste_conexao.py*, que tem como funcionalidade acessar a base de dados via link, guardando as informações na variavel *string_conexao*. Criando um Client a partir dessa variavel, consegui listar o nome dos dos bancos de dados disponiveis e a partir desse nome, criei uma variavel *db* que armazena as informações do banco de dados, obtendo assim o nome das coleções presentes nessa base. Dessa forma, temos:
        * Banco de Dados: 'MiningProccess';
        * Collections: 'airflow', 'levels', 'laboratory', 'processvariables';
    Sabendo assim como os dados estão organizados, agora preciso saber a formatação dos documentos que esses dados foram armazenado para cada collection. Assim, utilizando a função *.find_one()*, imprimi um exemplo para cada collection, podendo identificar a maneira em que os dados foram armazenados:
        * Todos os documentos possuem uma chave de identificação única *_id* em hexadecimal;
        * Airflow: possui também como informação a data em que provavelmente o dado foi extraido e a medição do fluxo de ar em 7 colunas de flotuação;
        * Levels: parecido com o airflow, só que ao envez de fluxo de ar, mede-se o nível de líquidos nas 7 colunas de flutuação;
        * Laboratory: possui também as porcentagens de sílica e de ferro presentes no material analisado;
        * Processvariables: possui a data e a hora da coleta dos dados, as taxas de fluxo de amido, amina e polpa de minério no processo analisado e o pH e a densidade dessa polpa de minério;
    Foi realizado um método *.info()* presente na biblioteca de manipulação de dados do python chamada Pandas, com o objetivo de categorizar o tipo de dados de cada collection, tendo como resultado:
        *Airflow:
            RangeIndex: 737453 entries, 0 to 737452
            Data columns (total 9 columns):
            #   Column                        Non-Null Count   Dtype
            ---  ------                        --------------   -----
            0   _id                           737453 non-null  object
            1   date                          737453 non-null  datetime64[ns]
            2   Flotation Column 01 Air Flow  737453 non-null  object
            3   Flotation Column 02 Air Flow  737453 non-null  object
            4   Flotation Column 03 Air Flow  737453 non-null  object
            5   Flotation Column 04 Air Flow  737453 non-null  object
            6   Flotation Column 05 Air Flow  737453 non-null  object
            7   Flotation Column 06 Air Flow  737453 non-null  object
            8   Flotation Column 07 Air Flow  737453 non-null  object
            dtypes: datetime64[ns](1), object(8)
            memory usage: 50.6+ MB
        *Levels:
            RangeIndex: 737453 entries, 0 to 737452
            Data columns (total 9 columns):
            #   Column                     Non-Null Count   Dtype
            ---  ------                     --------------   -----
            0   _id                        737453 non-null  object
            1   date                       737453 non-null  datetime64[ns]
            2   Flotation Column 01 Level  737453 non-null  object
            3   Flotation Column 02 Level  737453 non-null  object
            4   Flotation Column 03 Level  737453 non-null  object
            5   Flotation Column 04 Level  737453 non-null  object
            6   Flotation Column 05 Level  737453 non-null  object
            7   Flotation Column 06 Level  737453 non-null  object
            8   Flotation Column 07 Level  737453 non-null  object
            dtypes: datetime64[ns](1), object(8)
            memory usage: 50.6+ MB
        *Laboratory:
            RangeIndex: 737453 entries, 0 to 737452
            Data columns (total 3 columns):
            #   Column         Non-Null Count   Dtype
            ---  ------         --------------   -----
            0   _id            737453 non-null  object
            1   % Iron Feed    737453 non-null  object
            2   % Silica Feed  737453 non-null  object
            dtypes: object(3)
            memory usage: 16.9+ MB
        *ProcessVariables:
            RangeIndex: 737453 entries, 0 to 737452
            Data columns (total 7 columns):
            #   Column            Non-Null Count   Dtype
            ---  ------            --------------   -----
            0   _id               737453 non-null  object
            1   date              737453 non-null  object
            2   Starch Flow       737453 non-null  object
            3   Amina Flow        737453 non-null  object
            4   Ore Pulp Flow     737453 non-null  object
            5   Ore Pulp pH       737453 non-null  object
            6   Ore Pulp Density  737453 non-null  object
            dtypes: object(7)
            memory usage: 39.4+ MB
**4-ETL (Extract, Transform, Load)**
**4.1- Pre processamento (Limpeza dos dados):**
    Também utilizando o Pandas, usei o método *.isnull().sum()* que mostra a quantidade de dados nulos por coluna de cada collection, obtendo o seguinte resultado:
        *Airflow:                                  *Levels:
            _id                             0          _id                          0 
            date                            0          date                         0 
            Flotation Column 01 Air Flow    0          Flotation Column 01 Level    0 
            Flotation Column 02 Air Flow    0          Flotation Column 02 Level    0 
            Flotation Column 03 Air Flow    0          Flotation Column 03 Level    0 
            Flotation Column 04 Air Flow    0          Flotation Column 04 Level    0 
            Flotation Column 05 Air Flow    0          Flotation Column 05 Level    0 
            Flotation Column 06 Air Flow    0          Flotation Column 06 Level    0 
            Flotation Column 07 Air Flow    0          Flotation Column 07 Level    0 
     
        *ProcessVariables:                          *Laboratory
            _id                 0                      _id              0
            date                0                      % Iron Feed      0
            Starch Flow         0                      % Silica Feed    0
            Amina Flow          0
            Ore Pulp Flow       0
            Ore Pulp pH         0
            Ore Pulp Density    0

    Dessa forma, podemos concluir que não há dados faltantes nessa Base de Dados.

    Outra parte da limpeza dos dados é a verificação de dados duplicados. Utilizando a função *.duplicated()*, verifiquei para todas as 4 coleções a existência de dados duplicados, que poderiam influenciar no processo, e foi constatado que não há nenhum em nenhuma das coleções, como mostra a saida da função:

    *Airflow            *Levels             *Laboratory         *ProcessVariables:
    0         False     0         False     0         False     0         False 
    1         False     1         False     1         False     1         False 
    2         False     2         False     2         False     2         False 
    3         False     3         False     3         False     3         False 
    4         False     4         False     4         False     4         False 
              ...                 ...                 ...                 ...   
    737448    False     737448    False     737448    False     737448    False 
    737449    False     737449    False     737449    False     737449    False 
    737450    False     737450    False     737450    False     737450    False 
    737451    False     737451    False     737451    False     737451    False 
    737452    False     737452    False     737452    False     737452    False 
    Length: 737453      Length: 737453      Length: 737453      Length: 737453  

    O último passo seria o tratamento de outliers, valores descrepantes que podem influenciar na análise dos dados. Eu decidi utilizar o método de IQR (Interquartil Range), que dé uma técnica estatística que permite identificar outliers, ou seja, valores que se diferenciam drasticamente dos demais em um conjunto de dados.Um valor é considerado outlier se estiver abaixo do limite inferior (Q1–1,5 * IQR) ou acima do limite superior (Q3 + 1,5 * IQR). Não foi encontrado nenhum outlier para nenhuma das coleções, como mostra a saida:

    Outliers na coleção 'airflow':

    Outliers na coleção 'levels':

    Outliers na coleção 'laboratory':

    Outliers na coleção 'processvariables':

    Concluindo o processo de limppeza dos dados, podemos observar e especular que essa Base de Dados ja pode ter sido pre-processada, pois é muito difícil existir uma base que foi extraida de um minimundo real e não possuir dados faltantes, dados duplicados e nem outliers. Outra possibilidade seria desta base ter sido gerada por algum algoritmo.

    Para realizar a analise da limpeza, que no caso não se mostrou necessária, basta compilar o código *limpeza.py*.

**4.2- Normalização:**
    Em seguida, realizei a normalização dos dados para produzir e assim garantir uma certa consistência das informações. Isso inclui a conversão de colunas de data para um formato padrão e a transformação de colunas numéricas, como os fluxos de ar e os níveis das colunas de flutuação, para valores de tipo *float*. As colunas referentes a alimentação de ferro e sílica, além das variaveis de processo como o fluxo de polpa de minério, pH e densidade, também doram normalizadas para garantir que os dados fossem facilmente utilizaveis em analises futuras.

    Escolhi o método de normalização Min-Max Scaling por ser simples e eficiente, focando na conversão direta de valores numéricos e na padronização das datas. Isso evita problemas com formatos inconsistentes, como o uso da virgula ao inves de pontos, e preserva a integridade dos valores originais. A normalização escolhida garante que os dados estejam prontos para análises detalhadas, sem distorções que poderiam surgir com outros métodos, como a padronização.
    
    O código foi feito de maneira automatizada, usando como referência códigos presentes no stackoverflow e delftstack, permitindo que qualquer campo relevante dentro das collections fosse identificado e ajustado. Isso garante que todos os dados estejam no formato correto.

    Para efetuar a normalização, basta compilar o código *normalizacao.py*.

**4.3- Agregação:**
    Decidi realizar uma agragação entre as 3 collections que possuem a conula em comum 'data'. Para isso, realizei um merge entre as 4 collections existentes, verificando se cada uma continha a coluna em comum 'data', que no casso a collection *laboratory* não possuia. Essa agregação tinha como objetivo juntar essas 3 collections em um só DataFrame para que eu, no futuro, possa analisar e tirar alguma conclusão sobre os dados destas collcetions em conjunto. 
    Entretanto, ao rodar o código, notei que 5 linhas de medição de pH e densidade da polpa de minério apareceram como 'NaN', o que é estranho pois ja havia realizado a análise de dados faltantes e não tinha acusado a presença de nenhum na Base de Dados. Isso pode ser explicada pelo processo de merge (união) das coleções. No meu código, foi utilizada a técnica de outer join para combinar as tabelas, o que preserva todos os dados das coleções mesmo que não haja correspondência exata em determinadas colunas. Assim, se uma linha de uma coleção, por exemplo, airflow, não tiver correspondência direta de data ou ID com outra coleção, como processvariables, as colunas de processvariables terão valores nulos (NaN) nessa linha do resultado final. Por enquanto, não vou realizar nenhum procedimento de limpeza com estes dados faltantes, pois será melhor decidir qual metodo usar quando eu for realizar a análize no futuro.

