# Projeto acadêmico realizado com o objetivo de criar uma aplicação de controle de estoque de uma empresa.  
## O projeto consiste em:
- Controle de entrada e saída de produtos;
- Cadastro de produtos, bem como a edição ou exclusão (somente administradores);
- Permissões de modificações no estoque para os usuários administradores;
- Cadastros de usuários, comum ou administrador (somente administradores);
- Usuário Comum somente visualiza o estoque;
- Conexão com o banco de dados;
- Criação de tabelas (usuários, produtos e movimentação de estoque) no MySQL Workbench.
  
# MODELO CONCEITUAL
![Design sem nome (3)](https://github.com/user-attachments/assets/de725c03-ddfb-4902-bbd0-3ad9cb45cbef)

Entidades e Atributos  
• **Produtos:** representa os itens do estoque.  
o Atributos:  
▪ id: Identificador único.  
▪ nome: Nome do produto.  
▪ valor: Preço unitário do produto.  
▪ quantidade: Quantidade em estoque.  
▪ quantidade_minima: Estoque mínimo permitido.  

• **Usuários:** representa os usuários do sistema.  
o Atributos:  
▪ id: Identificador único.  
▪ nome: Nome do usuário.  
▪ senha_hash: senha armazenada de forma criptografada.  
▪ perfil: Perfil do usuário (administrador ou comum).  

• **Movimentação de Estoque:** Registra as entradas e saídas de estoque.  
o Atributos  
▪ id: Identificador único.  
▪ quantidade: Quantidade movimentada.  
▪ tipo: Tipo da movimentação (entrada ou saída).  
▪ data: Data e hora da movimentação.  
▪ produto_id: Referência ao produto movimentado,  
▪ usuario_id: Referência ao usuário que realizou a movimentação.  
  
# MODELO LÓGICO
![Modelo lógico](https://github.com/user-attachments/assets/366890a2-0491-4e7e-8ac1-74e90acd5033)

Explicação dos campos e tipos de dados:  
### ➢ Tabela produtos 
|Campo               |Tipo de Dado           |Descrição                        |
|:-------------------|:----------------------|:--------------------------------|
|id                  |INT (PRIMARY KEY)      |Identificador único do produto.  |
|nome                |VARCHAR(100)           |Nome do produto.                 |
|valor               |FLOAT                  |Preço do produto.                |
|quantidade          |INT                    |Quantidade em estoque.           |
|quantidade_minima   |INT                    |Estoque mínimo permitido.        |

### ➢ Tabela usuarios 
|Campo               |Tipo de Dado          |Descrição                         | 
|:-------------------|:---------------------|:---------------------------------|
|id                  |INT (PRIMARY KEY)     |Identificador único do usuário.   |
|nome                |VARCHAR(30)           |Nome do usuário.                  |
|senha_hash          |VARCHAR(255)          |Senha criptografada.              |
|perfil              |VARCHAR(20)           |Tipo de usuário (admin/comum).    | 

### ➢ Tabela movimentacoes_estoque 
|Campo               |Tipo de Dado          |Descrição                            |
|:-------------------|:---------------------|:------------------------------------|
|id                  |INT (PRIMARY KEY)     |Identificador único da movimentação. |
|quantidade          |INT                   |Quantidade movimentada.              |
|tipo                |VARCHAR(10)           |Tipo de movimentação (entrada/saída).|
|data                |DATETIME              |Data e hora da movimentação.         |
|usuarios_id         |INT (FOREIGN KEY)     |ID do usuário responsável.           |
|produtos_id         |INT (FOREIGN KEY)     |ID do produto movimentado.           |

# FLUXOGRAMA
![Fluxograma drawio](https://github.com/user-attachments/assets/b92f41e6-eddd-46df-8ffb-c781a430863f)  

# TECNOLOGIAS UTILIZADAS 
Tecnologias utilizadas no projeto para a criação do sistema de controle de estoque:  
• BrModelo – para a criação do modelo conceitual.  
• MySQL Workbench – para a criação do banco de dados e criação do modelo lógico.  
• Visual Studio Code.  
• Python, Flask, html, CSS – para a implementação e criação do sistema.  

# CONSIDERAÇÕES FINAIS  

A criação deste sistema de controle de estoque visa solucionar os desafios enfrentados na gestão de mercadorias, proporcionando maior organização, eficiência operacional e redução de perdas. Através de um modelo bem estruturado, com base nos conceitos de modelagem de dados e boas práticas de desenvolvimento, o sistema atende às principais demandas da empresa, como o cadastro de produtos, controle de movimentações de estoque, geração de relatórios e diferentes permissões de acesso aos usuários.  

O processo de desenvolvimento do sistema envolveu diversas etapas, incluindo a definição de requisitos, modelagem de dados, conceitual e lógico, bem como a construção de fluxograma, facilitando a compreensão do fluxo do sistema.  

Espera-se que com a implementação deste sistema, reduza significativamente os custos associados à má gestão de estoque e melhore a capacidade de atender clientes, aumentando a eficiência operacional.  

Este projeto demonstra a importância de unir tecnologia, planejamento e entendimento das necessidades do cliente para criar soluções que realmente agreguem valor ao negócio. A criação deste sistema trouxe muito aprendizado e lógica para pensar e pôr em prática tudo o que foi pedido.
