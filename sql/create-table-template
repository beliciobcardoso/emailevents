-- Active: 1714247677444@@127.0.0.1@1433@sapiens@dbo#Tables
-- Active: 1714247677444@@127.0.0.1@1433@sapiens@dbo
CREATE TABLE requisicoes(  
    id int IDENTITY(1,1) primary key,
    empresa_id int,
    filial_id int,
    usuario_id int,
    requisicao_id int,
    sequencia int,
    um varchar(255),
    quantidade int,
    produto_id int,
    descricao_produto varchar(255),
    observacao varchar(255),
    deposito varchar(255),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE r999usu(
    id int IDENTITY(1,1) primary key,
    codusu int,
    nomusu varchar(255),
    senha varchar(255),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE r910usu(
    id int IDENTITY(1,1) primary key,
    codent int,
    nomcom varchar(255),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
