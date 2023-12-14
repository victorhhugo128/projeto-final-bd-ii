from pymongo import MongoClient
from random import randint
from datetime import datetime
import utils

def criar_conta_cliente(nome, cpf, data_nasc=None, email=None, telefone=None, endereco=None, valor=None):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    conta_cliente = db.conta_cliente
    
    for conta in conta_cliente.find():
        if conta['cpf'] == cpf:
            return False
    
    conta_cliente.insert_one({'nome': nome, 'cpf': cpf, 'data_nasc': data_nasc, 'email': email, 'telefone': telefone, 'endereco': endereco, 'valor': valor, 'cartoes': []})
    
    return True
    
def realizar_saque(cpf, valor):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    conta_cliente = db.conta_cliente
    
    for conta in conta_cliente.find():
        if conta['cpf'] == cpf:
            saldo_atual = conta.get('saldo', 0)
            if saldo_atual >= valor:
                novo_saldo = saldo_atual - valor
                conta_cliente.update_one({'cpf': cpf}, {'$set': {'saldo': novo_saldo}})
                
                conta_cliente.update_one({'cpf': cpf}, {'$push': {'historico': {'tipo': 'saque', 'valor': valor, 'data': datetime.now()}}})
                return True
            else:
                return False
    return False

def realizar_deposito(cpf, valor):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    conta_cliente = db.conta_cliente
    
    for conta in conta_cliente.find():
        if conta['cpf'] == cpf:
            saldo_atual = conta.get('saldo', 0)
            novo_saldo = saldo_atual + valor
            conta_cliente.update_one({'cpf': cpf}, {'$set': {'saldo': novo_saldo}})
            
            conta_cliente.update_one({'cpf': cpf}, {'$push': {'historico': {'tipo': 'deposito', 'valor': valor, 'data': datetime.now()}}})
            return True
    return False
    
def adicionar_cartao_conta(cpf, senha):
    client = MongoClient("localhost", 27017)
    db = client.projeto_final_bd
    conta_cliente = db.conta_cliente
    
    for conta in conta_cliente.find():
        if conta['cpf'] == cpf:
            numero_cartao = utils.gerar_numero_cartao()
            conta_cliente.update_one({'cpf': cpf}, {'$push': {'cartoes': {'numero_cartao': numero_cartao, 'senha': senha, 'validade_cartao': '12/35', 'status': True}}})
            return True
    return False
    
    
    
if __name__ == "__main__":
    print(criar_conta_cliente("Victor", "000.000.000-00"))
    print(adicionar_cartao_conta("000.000.000-00", "1234"))
