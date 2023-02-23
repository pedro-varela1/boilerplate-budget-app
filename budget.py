class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def check_withdraw(self):
        withdraws = list()
        for op in self.ledger:
            if op['amount'] < 0:
                withdraws.append(op['amount'])
        return sum(withdraws)

    def check_name(self):
        return self.name

    def deposit(self, amount, *description):
        add = {'amount': amount, 'description': ''}
        for d in description:
            add['description'] = d
            break
        self.ledger.append(add)

    def get_balance(self):
        balance = 0
        for dic in self.ledger:
            balance += dic['amount']
        return balance

    def check_funds(self, amount):
        if (self.get_balance()-amount) < 0:
            return False
        else:
            return True

    def withdraw(self, amount, *description):
        if self.check_funds(amount):
            add = {'amount': -amount, 'description': ''}
            for d in description:
                add['description'] = d
                break
            self.ledger.append(add)
        return self.check_funds(amount)

    def transfer(self, amount, bc):
        w = self.withdraw(amount, 'Transfer to %s' % bc.check_name())
        if w:
            bc.deposit(amount, 'Transfer from %s' % self.name)
            return True
        else:
            return False

    def __str__(self):
        layout1 = self.name.capitalize()
        layout1 = layout1.center(30, '*')
        layout2 = ''
        total = 0
        for dic in self.ledger:
            word = dic['description']
            value = dic['amount']
            layout2 += "\n"
            for i in range(23):
                try:
                    layout2 += word[i]
                except:
                    layout2 += ' '
            layout2 += ('%.2f' % value).rjust(7)
        layout2 += "\nTotal: %.2f" % self.get_balance()
        return (layout1 + layout2).rstrip()

def create_spend_chart(categories):
    name = list()
    per = list()
    sum_withdraw = list()

    for c in categories:
        name.append(c.check_name())
        sum_withdraw.append(c.check_withdraw())

    for i in sum_withdraw:
        new_per = round((i/sum(sum_withdraw)),1)
        per.append(new_per)

    i = 100
    line = list()
    while i >= 0:
        aline = str(i).rjust(3) + "| "
        for p in per:
            if p*100 >= i:
                aline += "o  "
            else:
                aline += "   "
        line.append(aline)
        i -= 10

    bline = '    '
    for i in range(len(name)):
        bline += '---'
    bline += '-'
    line.append(bline)

    name_split = list()
    for word in name:
        name_split.append(list(word))

    max_name = 0
    for i in range(len(name_split)):
        max_name = max(len(name_split[i]), max_name)
    cline = '    '
    for i in range(max_name):
        for j in range(len(name_split)):
            try:
                cline += ' ' + name_split[j][i] + ' '
            except:
                cline += '   '
        cline += ' \n' + '    '
    line.append(cline)

    chart = 'Percentage spent by category\n'
    for k in line:
        chart += k + '\n'

    return chart.rstrip()
