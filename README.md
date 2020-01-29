# Boticário API

A **API Boticário** foi criada para servir como hub para o cadastro de usuários, registro de pedidos e cálculo do cashback de acordo com o montante vendido. Ela funciona como uma **API RESTful** e a descrição dos recursos expostos ao usuário, bem como o passo a passo para a instalação, encontram-se a seguir


# Recursos

## Endpoint: /users
### Métodos = ['GET', 'POST']
### GET
O método **GET** neste endpoint retornará uma lista com todos os usuários cadastrados e suas respectivas informações.
#### Autenticação JWT: Não
#### Corpo da requisição: N/A
#### Retorno: JSON 
------
### POST
O método **POST** é responsável pela criação de novos usuários no banco de dados. 
#### Autenticação JWT: Não
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro.
	{
		"full_name": <Nome completo do usuário>,
		"cpf": <Número do CPF - Sem pontos ou traços>,
		"email": <E-mail do usuário>
		"password": <Senha do usuário>
	}
#### Retorno: JSON 
------
## Endpoint: /login
### Métodos = ['GET']
Este é o recurso de validação do usuário. É necessário informar um CPF e uma senha no JSON do corpo (ver abaixo). Se as informações forem válidas, ele gera e retorna um **token JWT** do usuário, que deve ser utilizado para acessar os recursos que necessitam de autenticação JWT. 
**ATENÇÃO:** O token JWT expira em 30 minutos e após este período, deixa de ser válido e um novo precisa ser gerado.
#### Autenticação JWT: Não
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro.
{
	"cpf": <Número do CPF - Sem pontos ou traços>,
	"password": <Senha do usuário do CPF informado>
}
#### Retorno: JSON
-------
## Endpoint: /order
### Métodos: ['POST', 'GET', 'PUT', 'DELETE']
### POST
Este método é usado para a inserção de uma nova compra no banco de dados. Não é possível haver mais de uma compra com o mesmo código de compra e a tentativa de criar uma nova com código repetido é recusada. Por padrão, o status de todas as compras é definido como "Em validação" pela API, com exceção das realizadas pelo CPF 153.509.460-56, quando são salvas com o status "Aprovado".
#### Autenticação JWT: Sim
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro.
{
	"order_code": <Código da compra>,
	"order_value": <Valor da compra - Obrigatório float ou int>,
	"order_date": < Data da compra no formato YYYY-MM-DD>,
	"seller_cpf": <Número do CPF - Sem pontos ou traços>,
}
#### Retorno: JSON
--------------
### GET
Este método retorna todas as vendas cadastradas dentro do período especificado sob o CPF informado. Um CPF pode ver apenas as suas compras. Aqui também é cálculado o percentual e o montante do cashback de cada compra, baseando-se no valor total das compras no período especificado.
#### Autenticação JWT: Sim
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro.
{
	"cpf": <Número do CPF - Sem pontos ou traços>,
	"password": <Senha do usuário do CPF informado>
}
#### Retorno: JSON
### PUT
Este método é responsável por atualizar compras existentes com os parâmetros informados. Só é possível alterar os pedidos do CPF informado e se o status for "Em aprovação".
#### Autenticação JWT: Sim
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro. 
**Atenção:** Caso não queira atualizar algum dos campos, passar uma string vazia ("") como valor do respectivo campo.
{
	"seller_cpf": <Número do CPF - Sem pontos ou traços>,
	"order_code": <Código da compra>,
	"updated_fields": {
		"seller_cpf": <Novo número do CPF - Sem pontos ou traços ou string vazia>,
		"order_code": <Novo código da compra ou string vazia>,
		"order_date": < Nova data no formato YYYY-MM-DD ou string vazia>,
		"order_value": < Novo valor da compra em int ou float ou string vazia>
		
	}
}
#### Retorno: JSON
-------
### DELETE
Este recurso encontrará a compra com os parâmetros especificados e a removerá do banco. Essa exclusão é **permanente** e só será realizada caso o status do pedido seja "Em validação".
#### Autenticação JWT: Sim
#### Corpo da requisição: JSON
#### Exemplo de corpo:
Todos os campos são obrigatórios e a ausência de algum deles resultará em erro. 
{
	"cpf": <Número do CPF - Sem pontos ou traços>,
	"password": <Senha do usuário do CPF informado>
}
#### Retorno: JSON
-------
## Endpoint: /get_cashback
### Método: ['GET']
Este método faz uma requisição à API externa do Boticário e retorna o valor de cashback acumulado informado pelo recurso.
#### Autenticação JWT: Sim
#### Corpo da requisição: N/A
#### Retorno: JSON
---------
# Instalação do projeto
## Pré-requisitos:
- Python 3+
- Virtualenv
- Docker
1) Na raiz do projeto, rode o shell script `./first_run.sh`. Ele configurará o ambiente virtual do projeto e instalará todas as dependências necessárias. Depois, ele criará a imagem do MongoDB no Docker e subirá o container que será utilizado pela API. Pode ser necessário rodar com **SUDO** e liberar permissões para o script com o comando `chmod 775 ./first_run.sh`

2) Com o ambiente devidamente configurado, rode o script `./start_local.sh` para inicializar a API. Novamente, pode ser necessário rodar com **SUDO** e liberar permissões para o script com o comando `chmod 775 ./start_local.sh`

**Todo o desenvolvimento e testes foi realizado na distro LinuxMint 19 do Ubuntu**
**Responsável pelo projeto:** Renato Silva
**E-mail do responsável:** renatohss@yahoo.com.br
