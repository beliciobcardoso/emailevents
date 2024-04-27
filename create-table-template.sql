-- Active: 1714247677444@@127.0.0.1@1433@sapiens@dbo#Tables
-- Active: 1714247677444@@127.0.0.1@1433@sapiens@dbo
CREATE TABLE requisicoes(  
    id_seque int IDENTITY(1,1) primary key,
    requisicao_id int,
    empresa_id int,
    filial_id int,
    usuario_id int,
    quantidade int,
    um varchar(255),
    produto_id int,
    descricao_produto varchar(255),
    observacao varchar(255),
    deposito varchar(255)
);
