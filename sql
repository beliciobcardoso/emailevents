USE sapiens

SELECT * FROM requisicoes

INSERT INTO sapiens.dbo.requisicoes (requisicao_id,empresa_id,filial_id,usuario_id,quantidade,um,produto_id,descricao_produto,Observacao,deposito ) VALUES (1265, 40, 1, 463,100, 'UN', 110254, 'Vassoura de 1/2', 'Obras e Instalações', 'GERRBA')

INSERT INTO sapiens.dbo.requisicoes (requisicao_id,empresa_id,filial_id,usuario_id,quantidade,um,produto_id,descricao_produto,Observacao,deposito ) VALUES (1265, 40, 1, 463,100, 'UN', 110254, 'Apanhador', 'Obras e Instalações', 'GERRBA')

UPDATE requisicoes SET produto_id = 110365 WHERE id_seque = 2 AND requisicao_id = 1265

UPDATE requisicoes SET quantidade = 50 WHERE id_seque = 2 AND requisicao_id = 1265