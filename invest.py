import pyhop



def maximum_of_investments_to_buy(account, min_money):
    return int(account/min_money)

def count_earning(time, salary):
    return time * salary

def earn_money(state, account, target):
    if state.money[account] + count_earning(state.time, state.salary) >= state.money[target] and state.time > 0:
        state.money[account] += count_earning(state.time, state.salary)
        state.time = 0
        return state
    return False

def get_money_from_account(state, account, investments, type):
    if maximum_of_investments_to_buy(state.money[account], state.min_money_contribution[type]) != 0 and state.time > 0:
        value = maximum_of_investments_to_buy(state.money[account], state.min_money_contribution[type])
        state.money[investments] += value * state.min_money_contribution[type]
        state.money[account] -= value * state.min_money_contribution[type]
        state.quantity[type] += value
        state.time -= 1
        return state
    return False

def buy(state, investments, type):
    if state.time > state.period[type]:
        while(state.time > state.period[type]):
            state.money[investments] *= state.profit[type]
            state.time -= state.period[type]
        return state
    return False

def get_money_from_investment(state, account, investments, target, type):
    if state.money[investments] > 0 and state.time > 5 and state.money[account] < target:
        state.money[account] += state.money[investments]
        state.money[investments] = 0;
        state.quantity[type] = 0;
        state.time -= 5
        return state
    return False

def pay_employees(state, account, type):
    if state.money[account] > state.quantity[type] * state.employee[type]:
        state.money[account] -= state.quantity[type] * state.employee[type]
        return state
    return False


pyhop.declare_operators(
    earn_money,
    get_money_from_account,
    buy,
    get_money_from_investment,
    pay_employees,
)


def work_in_job(state, account, investments, target):
    result = [('earn_money', account, target)]
    return result


def invest_in_gold(state, account, investments, target):
    result = [('get_money_from_account', account, investments, 'gold'), ('buy', investments, 'gold'),
        ('get_money_from_investment', account, investments, target, 'gold')]
    return result


def invest_in_properties(state, account, investments, target):
    result = [('get_money_from_account', account, investments, 'properties'), ('buy', investments, 'properties'),
            ('get_money_from_investment', account, investments, target, 'properties')]
    return result


def invest_in_shares(state, account, investments, target):
    result = [('get_money_from_account', account, investments, 'shares'), ('buy', investments, 'shares'),
            ('get_money_from_investment', account, investments, target, 'shares')]
    return result


def start_company(state, account, investments, target):
    result = [('get_money_from_account', account, investments, 'cargo'), ('buy', investments, 'cargo'),
            ('pay_employees', account, investments), ('get_money_from_investment', account, investments, target, 'cargo')]
    return result


pyhop.declare_methods('work', work_in_job,  invest_in_gold, invest_in_properties, invest_in_shares, start_company)

state = pyhop.State('state')
state.money = {'account': 100000, 'investments': 0, 'target': 1000000}
state.period = {'gold': 31, 'properties': 365, 'shares': 7, 'cargo': 1}
state.profit = {'gold': 1.1, 'properties': 3.5, 'shares': 1.02, 'cargo': 1.2}
state.min_money_contribution = {'gold': 25000, 'properties': 100000, 'shares': 1000, 'cargo': 200}
state.quantity = {'gold': 0, 'properties': 0, 'shares': 0, 'cargo': 0}
state.employee = {'cargo': 50}
state.salary = 100
state.time = 1000

result = pyhop.pyhop(state, [('work', 'account', 'investments', 'target')], verbose=10)