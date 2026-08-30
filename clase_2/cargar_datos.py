import json
def load_data():
    with open('data/data.json', 'r') as data:
        return json.load(data)

class TransactionManager:
    def __init__(self, transactions ):
        self.transactions  = transactions

    def get_transactions(self):
        return self.transactions
    def total_transactions(self):
        return len(self.transactions)
    def get_amount_average(self):
        total_amount = 0
        for transaction in self.transactions:
            total_amount += transaction['amount']
        return total_amount / len(self.transactions)
    def get_max_transaction(self):
        return max(self.transactions, key=lambda x: x['amount'])
    def get_min_transaction(self):
        return min(self.transactions, key=lambda x: x['amount'])



transactions= load_data()
manager = TransactionManager(transactions)
print('Total de transacciones: ', manager.total_transactions())
print('Promedio de transacciones: ', manager.get_amount_average())
print('-----Maxima transaccion -----------: ')
for key, value in manager.get_max_transaction().items():
    print(key, ': ', value)
print('--------Minima transaccion -------: ')
for key, value in manager.get_min_transaction().items():
    print(key, ': ', value)
