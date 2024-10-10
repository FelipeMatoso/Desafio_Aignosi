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
    Observa-se então que são dados referentes a um processo de análise de conteudo mineral de uma mineradora.