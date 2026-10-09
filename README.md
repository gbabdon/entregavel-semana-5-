# entregavel-semana-5-

Sistema de Análise de Dados em Python
Sobre o projeto

Esse projeto foi feito para a atividade da Semana 05. Nele, usei algumas coisas que aprendi nas aulas de Python, como leitura de arquivos, Regex e tratamento de erros.

O programa lê um arquivo CSV com nome, e-mail, CPF, telefone e data de nascimento. Depois, confere os dados e mostra quais estão certos e quais têm erros.

Arquivos
main.py: código principal do programa.
dados.csv: arquivo com os dados para testar.
README.md: arquivo com as informações do projeto.
.gitignore: arquivo para ignorar arquivos desnecessários.
Validações

Usei Regex para conferir o formato do e-mail, CPF, telefone e data de nascimento. Também usei o datetime para conferir se a data existe de verdade.

A validação do CPF confere apenas o formato, não se o número é válido de verdade.

Tratamento de erros

No código, usei:

FileNotFoundError: quando o arquivo não é encontrado.
ValueError: quando acontece um erro com algum valor.
KeyError: quando falta alguma coluna no CSV.
FormatoInvalidoError: erro que criei para os dados que não passam na validação.

Também usei try, except, else e finally para tratar os erros e fechar o arquivo depois do uso.

Como executar

É preciso ter o Python instalado. Deixe o main.py e o dados.csv na mesma pasta e execute no terminal:

python main.py


O programa vai mostrar o resultado da análise e salvar um relatório no arquivo relatorio.txt.

Exemplo de entrada
nome,email,cpf,telefone,data_nascimento
Ana,ana@email.com,123.456.789-09,(11) 91234-5678,15/05/2000
Bruno,bruno-email.com,123.456.789-00,11912345678,31/02/2001

Exemplo de saída
Total de registros: 2
Registros válidos: 1
Registros inválidos: 1
Taxa de aprovação: 50.00%

Conclusão

Com esse projeto, consegui praticar o que aprendi nas aulas e entender melhor como ler arquivos, conferir dados e tratar erros usando Python.
