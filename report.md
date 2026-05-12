<img src='uminho.png' width="30%"/>

<h3 align="center">Licenciatura em Engenharia Informática <br> Trabalho prático de Processamento de Linguagens <br> 2025/2026 </h3>

---
# Introdução

Este projeto consistiu na implementação de um compilador para a linguagem Fortran 77.

O compilador traduz programas escritos na linguagem de entrada para código destinado a uma máquina virtual stack-based fornecida (EWVM) no contexto da unidade curricular.

O compilador foi desenvolvido e organizado nas seguintes 4 fases principais:
- Análise léxica
- Análise sintática
- Análise semântica
- Geração de código para máquina virtual

---
# 1. Análise Léxica 

## Descrição Geral

A análise léxica constitui a primeira fase do compilador, sendo responsável por transformar o código fonte numa sequência linear de tokens. Cada token representa uma unidade lexical significativa da linguagem, como palavras-chave, identificadores, operadores ou constantes.

Esta fase tem como principal objetivo simplificar o processamento posterior, eliminando ambiguidades do texto original e fornecendo uma representação estruturada que será utilizada pela análise sintática.

Neste projeto, a análise léxica foi implementada utilizando a biblioteca `ply.lex`, que permite definir tokens através de expressões regulares.

## Estrutura e Funcionamento

O lexer percorre o código fonte sequencialmente, identificando padrões lexicais com base em expressões regulares previamente definidas. Cada padrão corresponde a um tipo de token específico.

Os tokens foram organizados em várias categorias, de acordo com o seu papel na linguagem.

## Palavras-Chave

As palavras-chave correspondem a elementos reservados da linguagem, sendo utilizadas para definir a estrutura e o comportamento dos programas.

Incluem-se nesta categoria:
- `PROGRAM`, `END`
- `INTEGER`, `REAL`, `LOGICAL`
- `IF`, `THEN`, `ELSE`, `ENDIF`
- `DO`, `CONTINUE`, `GOTO`
- `READ`, `PRINT`

Estas palavras não podem ser utilizadas como identificadores, sendo reconhecidas explicitamente pelo lexer para evitar ambiguidades.

## Identificadores

Os identificadores representam nomes definidos pelo utilizador, como variáveis ou arrays.
São reconhecidos através de uma expressão regular genérica que aceita sequências alfanuméricas iniciadas por uma letra. Esta abordagem permite flexibilidade na definição de nomes, mantendo compatibilidade com a sintaxe da linguagem.


## Constantes Numéricas 

O compilador suporta dois tipos de constantes numéricas:

- **Inteiros (`INT`)**: sequências de dígitos convertidas diretamente para o tipo `int`.
- **Reais (`FLOAT`)**: números com parte decimal opcional e suporte para notação científica, convertidas para o tipo `float`.

Estas conversões são efetuadas durante a análise léxica, simplificando o processamento nas fases seguintes.


## Sequência de caracteres

As sequências de caracteres (`STRING`) são delimitadas por aspas simples (`'`), seguindo a convenção da linguagem Fortran.
Também é suportado o uso de aspas simples dentro da string através da duplicação do caractere (`''`).

## Valores Lógicos

Os valores lógicos são representados utilizando a sintaxe:
- `.TRUE.`
- `.FALSE.`

Estes são reconhecidos como tokens específicos (`BOOL`) e numa fase posterior convertidos para uma representação interna baseada em inteiros (1 para verdadeiro, 0 para falso).

## Operadores Aritméticos

Incluem os operadores:
- `+` (adição)
- `-` (subtração)
- `*` (multiplicação)
- `/` (divisão)

Estes operadores são utilizados na construção de expressões matemáticas.

## Operadores Relacionais

A linguagem utiliza uma notação inspirada em Fortran para operadores de comparação:

- `.EQ.` (igual)
- `.NE.` (não igual)
- `.LT.` (menor que)
- `.LE.` (menor ou igual)
- `.GT.` (maior que)
- `.GE.` (maior ou igual)

Estes operadores são fundamentais para a construção de expressões condicionais.

## Operadores Lógicos

Incluem:
- `.AND.`
- `.OR.`
- `.NOT.`

São utilizados para combinar e manipular expressões booleanas, sendo essenciais em estruturas de controlo como instruções `IF`.

## Símbolos e Pontuação

Foram definidos tokens para os principais símbolos estruturais da linguagem:

- `(` e `)` para agrupamento de expressões
- `,` para separação de argumentos
- `=` para atribuição

Estes elementos contribuem para a organização sintática do código.

## Comentários e Espaços em Branco

Os comentários são iniciados pelo símbolo `!` e estendem-se até ao final da linha. Estes são ignorados pelo lexer.

Espaços em branco e tabulações são igualmente ignorados, sendo utilizados apenas para separação visual do código.

As quebras de linha são contabilizadas para efeitos de controlo de erros, permitindo identificar a linha onde ocorre um problema.


## Formato da Linguagem

Apesar da linguagem alvo ser baseada no Fortran 77, foi adotado o formato *free-form* em vez do formato tradicional baseado em colunas fixas.

No Fortran 77 clássico, o código segue regras rígidas de posicionamento, onde existem colunas específicas para rótulos, colunas reservadas para continuação de linha e limites na largura das instruções.

Neste projeto, optou-se por um formato mais flexível (*free-form*), no qual não existem restrições de colunas, podendo o código ser escrito de forma mais natural e obtendo uma análise léxica significativamente simplificada

Esta decisão permitiu reduzir a complexidade do lexer, evitando a necessidade de tratar alinhamentos e posições específicas de caracteres, focando-se apenas na identificação de padrões lexicais através de expressões regulares.

---
# 2. Análise Sintática

## Descrição Geral

A análise sintática tem como objetivo verificar se a sequência de tokens produzida pela análise léxica respeita a gramática da linguagem, construindo simultaneamente uma representação estruturada do programa.

Neste projeto, foi utilizada a biblioteca `ply.yacc`, recorrendo a um parser do tipo **LALR(1)** (Left-to-right, Rightmost derivation with 1 lookahead), no qual a gramática é definida através de regras associadas a funções Python.

Cada regra gramatical inclui ações semânticas responsáveis pela construção de uma **Árvore de Sintaxe Abstrata (AST)**, que representa o programa de forma hierárquica.

## Construção da AST

A AST é composta por nós da classe `Node`, onde cada nó contém:
- um tipo (ex: `program`, `assign`, `if`, `do`, etc.)
- um conjunto de argumentos (filhos)

Esta representação permite desacoplar a estrutura sintática da execução, sendo posteriormente utilizada nas fases de análise semântica e geração de código.

## Estrutura da Gramática

A regra principal da gramática é:

`program : PROGRAM ID decl_list stmt_list END`

Um programa é composto por:
- identificador do programa
- lista de declarações
- lista de instruções

Esta estrutura define o ponto de entrada da análise sintática.

As declarações seguem a forma:

`decl_list : decl_list declaration`

`decl_list :`

`declaration : type id_list`

`type : INTEGER` 
`| REAL`
`| LOGICAL`

Cada declaração pode ser do tipo INTEGER, REAL e LOGICAL. Declarações do mesmo tipo podem ser feitas conjuntamente em lista de identificadores ou arrays (ex.: INTEGER X, Y, A(5)).

A lista de identificadores desenvolve-se assim:

`id_list : id_element more_ids`

`more_ids : COMMA id_element more_ids`

`more_ids :`

`id_element : id_literal`
`| ID LPAREN expr_list RPAREN`

`id_literal : ID`

Os arrays são suportados através da segunda regra de `id_element`, existe a necessidade da produção `id_literal`, já que numa instrução `do` (iremos ver à frente) não é sintaticamente válido um elemento de um array ser usado como iterador, ou seja `id_element` não poderia ser usado diretamente.

As instruções são representadas por:

`stmt_list : stmt_list statement`

`stmt_list :`

`statement : opt_label basic_statement`

`opt_label : INT`

`opt_label :`

`basic_statement : assignment`
`| print_stmt`
`| read_stmt`
`| do_loop`
`| if_stmt`
`| goto_stmt`
`| continue_stmt`


Após as declarações o programa resume-se num conjunto de instruções até ao final da sua execução. Cada instrução é antecedida opcionalmente por uma etiqueta (label) que é um valor inteiro. Esta é utilizada conjuntamente com a instrução `goto` que permite avançar para uma determinada zona etiquetada no programa. Isto permite o desenvolvimento de ciclos condicionais com o conjunto da instrução `if`.

As instruções suportadas são:

- atribuição (`=`)
- leitura (`READ`)
- escrita (`PRINT`)
- ciclos DO (`DO`)
- condicionais (`IF`)
- saltos (`GOTO`)
- placeholder (`CONTINUE`)

`assignment : id_element ASSIGN condition`

`print_stmt : PRINT MULT COMMA expr_list`

`read_stmt : READ MULT COMMA id_list`

`expr_list : expression more_exprs`

`more_exprs : COMMA expression more_exprs`

`more_exprs :`

`do_loop : DO INT id_literal ASSIGN expression COMMA expression stmt_list INT CONTINUE`

Mais uma vez note-se que no ciclo `do` é apenas sintaticamente válido atribuir um `id_literal` como iterador. O parser necessita de algum tipo de delimitador para saber quando exatamente esta produção termina. Neste caso o delimitador foi a parte final `INT CONTINUE` já que os exemplos padrão não utilizam um delimitador `ENDDO`. Colocar o statement final apenas como a regra `continue_stmt` também não foi viável devido à origem de conflitos já que essa opção traria a ambiguidade de o parser não saber se a instrução faz parte da `stmt_list` do loop ou se é o seu delimitador.

`if_stmt : IF LPAREN condition RPAREN THEN stmt_list else_part ENDIF`

`else_part : ELSE stmt_list`

`else_part :`

Como podemos ver, no caso do `if` já existe o delimitador `ENDIF`.

`goto_stmt : GOTO INT`

`continue_stmt : CONTINUE`

As condições são utilizadas em atribuições e nos `if`. Na construção da gramática foi considerada a precedência de cada operador lógico para eliminar ambiguidades (NOT > AND > OR). 

`condition : or_expr`

`or_expr : or_expr OR and_expr`
`| and_expr`

`and_expr : and_expr AND not_expr`
`| not_expr`

`not_expr : NOT not_expr`
`| rel_expr`

Os operandos das condições são essencialmente condições ou expressões que são derivadas a partir da condição. Existem dois tipos de expressões a expressão aritmética e a expressão relacional (que produzem valores booleanos).

`rel_expr : expression relop expression`
`| expression`

Numa expressão relacional os operadores são :

- igual a (`EQ`)
- não igual a (`NE`)
- menos que (`LT`)
- menos ou igual a (`LE`)
- mais que (`GT`)
- mais ou igual a (`GE`)

`relop : EQ`
`| NE`
`| LT`
`| LE`
`| GT`
`| GE`

A expressão aritmética é constituída pelos operadores aritméticos que são:

- adição/ + (`PLUS`)
- subtração/ - (`MINUS`)
- multiplicação/ * (`MULT`)
- divisão/ / (`DIV`)

A ordem de precedência destes operadores (() > DIV/MULT > MINUS/PLUS) também é estabelecida na construção das expressões para eliminar ambiguidades

`expression : term expression_tail`

`expression_tail : PLUS term expression_tail`

`expression_tail : MINUS term expression_tail`

`expression_tail :`

`term : factor term_tail`

`term_tail : MULT factor term_tail`

`term_tail : DIV factor term_tail`

`term_tail :`

As expressões foram desenvolvidas com o auxílio da regra `factor`. Os fatores têm o maior grau de precedência do programa e descrevem-se na seguinte forma:

`factor : id_element`

`factor : INT`

`factor : FLOAT`

`factor : BOOL`

`factor : STRING`

`factor : LPAREN condition RPAREN`

`factor : MINUS factor`

Note-se que o operador menos unário é tratado como um caso especial na gramática do programa e também terá verificações semânticas associadas.

---
# 3. Análise Semântica

## Descrição Geral

A análise semântica tem como objetivo verificar a correção dos programas para além da sua estrutura sintática, garantindo que as instruções fazem sentido do ponto de vista da linguagem.

Nesta fase são realizadas verificações como:
- declaração prévia de variáveis
- consistência de tipos
- utilização correta de arrays
- validade de labels e saltos (`GOTO`)
- verificação de expressões e condições

O analisador semântico foi implementado recorrendo a uma travessia recursiva da AST, utilizando o padrão *visitor* e métodos específicos para cada tipo de nodo.




## Tabela de Símbolos

Foi implementada uma tabela de símbolos responsável por armazenar informação sobre as variáveis declaradas no programa.

Cada entrada contém:
- tipo (`INTEGER`, `REAL`, `LOGICAL`)
- tipo de entidade (`var` ou `array`)
- endereço de memória
- tamanho (no caso de arrays)

A tabela é também responsável por:
- impedir declarações duplicadas
- garantir que todas as variáveis são declaradas antes da sua utilização

## Verificação de Declarações

Durante a análise das declarações variáveis simples são registadas na tabela de símbolos e arrays são registados com o respetivo tamanho.

A tabela de símbolos já se encarrega de lançar uma exceção no erro semântico de declarar variáveis duplicadas. No caso da variável corresponder a um array é verificado que o valor dentro dos parênteses é um número inteiro. 

Na análise também se verifica que as variáveis não são declaradas com o identificador `MOD`. No programa `MOD` é considerada uma função *built-in* e portanto esse identificador é restrito a identificar essa função.

## Verificação de Atribuições

Nas atribuições verifica-se se os identificadores de variáveis numéricas estão propriamente definidos comparativamente a serem um array versus um escalar, ou seja são considerados erros semânticos um escalar ser escrito com um índice e um array ser escrito sem índice.

Posteriormente é feito type checking entre variável e a expressão que lhe está a ser atribuída. A variável tem de ser do mesmo tipo ou de um tipo compatível à expressão. Os tipos desiguais compatíveis na linguagem são `INTEGER` e `REAL`, sendo que `LOGICAL` não é compatível com nenhum desses dois.  

## Verificação das Expressões

As expressões são analisadas recursivamente, sendo determinado o seu tipo.

As expressões aritméticas (DIV/MULT/MINUS/PLUS) apenas permitem operandos do tipo `INTEGER` ou `REAL`. O seu resultado é `REAL` se pelo menos um operando for `REAL`, `INTEGER` caso contrário.

As expressões lógicas (AND/OR/NOT) requerem operandos do tipo `LOGICAL`. O resultado é sempre `LOGICAL`.

As expressões relacionais requerem operandos do mesmo tipo ou simplesmente ambas de tipo numérico (`INTEGER` e `REAL`).

O menos unário é apenas válido para tipos numéricos (`INTEGER` e `REAL`).

A função `MOD` recebe exatamente dois argumentos, e esses argumentos devem ser tipos numéricos (`INTEGER` e `REAL`).

O índice de um array deve ser do tipo `INTEGER`.

## Verificação de Estruturas de Controlo

Na instrução `IF` a condição deve ser do tipo `LOGICAL`. 

Nos ciclos `DO` as variáveis de controlo devem ser do tipo `INTEGER` e os limites das expressões têm que ter tipo numérico (`INTEGER` e `REAL`). A label inicial do ciclo deve coincidir com a label final. Mais uma vez clarificando a opção de aglomerar a instrução final do ciclo `CONTINUE` como delimitador deste.

Antes da análise principal do programa, é feita uma recolha de todos os labels existentes no programa.

Posteriormente, verifica-se na instrução `GOTO` que de facto a label referenciada está definida.

## Leitura e Escrita

Na instrução `PRINT` as expressões são analisadas para garantir consistência e na instrução `READ` verifica-se que todas as variáveis estão declaradas.

---
# 4. Geração de Código

## Descrição Geral

A fase de geração de código tem como objetivo traduzir a AST produzida nas fases anteriores para instruções executáveis pela máquina virtual stack-based fornecida no contexto da unidade curricular (EWVM). A geração de código foi implementada recorrendo novamente ao padrão *visitor*, onde cada tipo de nodo da AST possui um método responsável pela emissão das instruções correspondentes.

O código gerado é armazenado sequencialmente numa lista de instruções através do método *emit*. No final da geração, esta lista representa o programa completo em código da máquina virtual.

## Estratégia de Geração 

Sendo a máquina virtual utilizada baseada numa arquitetura de pilha, as expressões são avaliadas colocando operandos na pilha e aplicando posteriormente a operação correspondente.

O compilador implementado não utiliza uma representação intermédia (Intermediate Representation / IR) nem fases de otimização.

A geração de código é realizada diretamente a partir da AST construída, emitindo instruções da máquina virtual à medida que a árvore é percorrida.

## Estrutura Geral do Programa

A geração de código inicia-se no nodo `program`. As instruções `START` e `STOP` são emitidas no início e no fim do programa respetivamente.
Estas instruções delimitam a execução do programa na VM.

## Gestão de Memória e Alocações

As variáveis escalares são inicializadas com o valor 0. 

    PUSHI 0
    STOREG addr

Os arrays são implementados utilizando memória dinâmica da heap da VM. Para cada array é reservado espaço com `ALLOCN` e o endereço base é armazenado numa posição global.

    PUSHI size
    ALLOCN
    STOREG addr

## Acesso a variáveis e arrays

O acesso a uma variável consiste apenas em carregar o seu valor da memória global.

    PUSHG addr

Os arrays utilizam indexação baseada em 1, seguindo a convenção típica do Fortran.

Assim, para aceder ao elemento A(i):

- obtém-se o endereço base do array
- calcula-se o deslocamento i - 1
- soma-se o deslocamento ao endereço base
- carrega-se o valor

----                                                                                                                                    
    PUSHG addr
    ...
    PUSHI 1
    SUB
    PADD
    LOAD 0


## Atribuição em variáveis e arrays

Os mesmos princípios descritos acima também são aplicados para atribuições.

Atribuição em variável:

    STOREG addr

Atribuição num array:

    PUSHG addr
    ...
    PUSHI 1
    SUB
    PADD  
    ...
    STORE 0

## Geração de Expressões

As expressões aritméticas são traduzidas diretamente para instruções na máquina virtual:

- `ADD` 
- `SUB`
- `MUL`
- `DIV`

As expressões lógicas também:

- `AND`
- `OR`
- `NOT` 

As expressões relacionais são convertidas para:

- `EQUAL`
- `INF`
- `INFEQ`
- `SUP`
- `SUPEQ`

O não igual é implementado através da composição de `EQUAL` e depois `NOT`.

O menos unário foi implementado multiplicando a expressão por -1:

    PUSHI -1
    MUL


## Leitura e Escrita

Na escrita, strings utilizam `WRITES`, valores numéricos e lógicos utilizam `WRITEI`.

No final da instrução é emitido `WRITELN` para a mudança de linha.

A leitura é realizada através da instrução `READ`. Posteriormente, o valor é convertido para `ATOI` para inteiros e lógicos e `ATOF` para reais.

## Estrutura de Controlo 

As instruções `IF` são implementadas através de labels internas geradas automaticamente.

O fluxo geral consiste em:

- avaliar a condição
- saltar para o bloco `ELSE` se a condição for falsa (`JZ`)
- executar o bloco `THEN`
- saltar para o fim do `IF` (`JUMP`)

Para este efeito são criadas labels dinamicamente através do método `new_label()`.

O fluxo dos ciclos `DO` é:

- inicializar a variável de controlo
- verificar a condição de continuação, saltar para o fim se for falsa (`JZ`)
- executar o corpo do ciclo
- incrementar a variável iteradora (`PUSHI 1` e `ADD`)
- saltar para o início do `DO` (`JUMP`)

A instrução `GOTO` é traduzida diretamente para:

    JUMP label

Permitindo saltos incondicionais para labels previamente definidas no programa. 

---
# Instruções do Compilador

## Estrutura do Projeto

O projeto encontra-se organizado em duas diretorias principais:

- `src/` - contém a implementação do compilador
- `tests/` - contém programas de teste e código VM gerado

A diretoria `tests/` encontra-se organizada da seguinte forma:

        tests/
            ├── programs/    # programas fonte Fortran
            ├── vm/          # código VM gerado
            └── run_tests.py # script auxiliar de compilação


## Requisitos 

O projeto foi desenvolvido em *Python 3*.

Recomenda-se a utilização de um ambiente virtual Python (venv).

Criação do ambiente virtual:

    python -m venv venv

Ativação do ambiente virtual:

    source venv/bin/activate

É também necessária a biblioteca *PLY (Python Lex-Yacc)*, utilizada nas fases de análise léxica e sintática.

Instalação:

    pip install ply

## Compilação de Programas

A compilação é realizada através do script `run_tests.py`.

A partir da diretoria `tests/`, deve executar-se:

    python run_tests.py programs/program.f

O compilador executa:

- análise léxica
- análise sintática
- análise semântica
- geração de código VM

No final é produzido automaticamente o ficheiro:

    vm/program.vm


## Execução na Máquina Virtual

O código gerado pode posteriormente ser executado utilizando a máquina virtual EWVM fornecida no contexto da unidade curricular.

## Conjunto de Testes

Foram desenvolvidos diversos programas de teste cobrindo as funcionalidades suportadas pelo compilador, incluindo:

- expressões aritméticas
- expressões lógicas
- expressões relacionais
- condicionais `IF`
- ciclos `DO`
- arrays
- leitura e escrita
- utilização de `GOTO`

Os testes encontram-se disponíveis na diretoria `tests/programs/`.

