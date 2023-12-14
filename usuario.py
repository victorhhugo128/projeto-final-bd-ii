from pymongo import MongoClient
from random import randint
from datetime import datetime
import utils


def cadastrar_cliente(nome, cpf, logradouro, cidade, estado, tipo_conta, saldo_inicial):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    cadastro_cliente = db.Cliente
    id_cliente = 1
    
    for conta in cadastro_cliente.find():
        if conta['cpf'] == cpf:
            return False
        id_cliente = conta["id"]
    id_cliente += 1
    
    cadastro_cliente.insert_one({'id': id_cliente, 'nome': nome, 'cpf': cpf,'endereco': {"logradouro": logradouro, "cidade": cidade, "estado": estado}})
    
    conta_cliente = db.Conta
    
    conta_cliente.insert_one({'cliente_id': id_cliente, 'numero': utils.gerar_numero_conta(), 'tipo': tipo_conta, 'saldo': saldo_inicial})
    
    return True
    
def realizar_saque(cpf, valor):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    cliente = db.Cliente
    
    instancia_cliente = cliente.find_one({'cpf': cpf})
    
    conta = db.Conta
    
    conta.update_one({'cliente_id': instancia_cliente['id']}, {'$inc': {'saldo': valor}})
    
    
    return False

def realizar_deposito(cpf, valor):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    cliente = db.Cliente
    
    instancia_cliente = cliente.find_one({'cpf': cpf})
    
    conta = db.Conta
    
    conta.update_one({'cliente_id': instancia_cliente['id']}, {'$inc': {'saldo': -valor}})
    
    return True
    
def adicionar_cartao_conta(cpf, tipo_cartao, limite):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    cliente = db.Cliente
    
    cliente_instancia = cliente.find_one({'cpf': cpf})
    
    cartao = db.Cartao
    
    cartao.insert_one({"cliente_id": cliente_instancia['id'], 'numero': utils.gerar_numero_cartao(), 'tipo': tipo_cartao, 'limite': limite})
    
    return True
    
    
    
# if __name__ == "__main__":
#     # print(criar_conta_cliente("Victor", "000.000.000-00"))
#     # print(adicionar_cartao_conta("000.000.000-00", "1234"))
#     # print(realizar_deposito("000.000.000-00", 10500))
#     # print(realizar_saque("000.000.000-00", 5000))
