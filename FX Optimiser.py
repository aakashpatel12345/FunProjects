# -*- coding: utf-8 -*-
"""
@author: Aakash
"""

import pandas as pd

best_chain = None
best_value = 0.0
currency_summary = {}
path_summary = {}

def build_rates_dict(data):
    global currency_summary
    rates_dict = dict.fromkeys(data['Quote'].unique())
    for currency1 in rates_dict:
        rates = []
        for row in data[data['Quote'] == currency1][['Base', 'Rate']].itertuples(index=False, name=None):
            rates.append(row)

        rates_dict[currency1] = rates
        currency_summary = dict((currency, 0) for currency in rates_dict.keys())
        path_summary = dict((currency, 0) for currency in rates_dict.keys())
        
    return rates_dict



def build_chain(start_currency, current_currency, rates_dict, depth, max_depth, chain=None, value=1):
    global best_value, best_chain, currency_summary
    
    if max_depth < 2:
        return

    if chain is None:
        chain = []
        chain.append(current_currency)

    if depth != max_depth:
        for dest_currency, rate in rates_dict[current_currency]:
            if dest_currency not in chain:  # check if a currency is not part of a chain yet
                chain.append(dest_currency)
                new_depth = depth + 1
                new_value = value * rate
                build_chain(start_currency, dest_currency, rates_dict, new_depth, max_depth, chain, new_value) #use recursion
                chain.pop()
    else:
        # final conversion, thus find currency that matches with start_currency
        currencies, rates = zip(*rates_dict[current_currency]) #unzips and tuple unpacked
        if start_currency in list(currencies):
            idx = currencies.index(start_currency)
            chain.append(start_currency)
            final_chain = ' -> '.join(chain)
            value *= rates[idx]

            #print('Max Depth: {}, Chain: {}, Final Value: {}'.format(max_depth, final_chain, value)) 
            #uncomment above line to see all possible conversions
            
            if value > currency_summary[start_currency]:
                currency_summary[start_currency] = value
                path_summary[start_currency] = final_chain
            

            if value > best_value:
                best_value = value
                best_chain = final_chain

            chain.pop()


def optimize_conversion(data):
    rates_dict = build_rates_dict(data)
    
    #maximum_chain_len = int(input("Please enter the maximum number of conversions : "))
    
    for max_depth in range(2, 3):
        print('Analyzing chain depth {}...'.format(max_depth))
        for currency in rates_dict:
            build_chain(currency, currency, rates_dict, 1, max_depth)
            
    
    
def show_summary(currency_summary, path_summary):
    for key, value in currency_summary.items():
        print(f"For {key} the best rate is {value}")
        print(f"The path for this is {path_summary[key]}")
        print('\n')

def main():
    data = pd.read_csv('FX Rates Sample.csv')
    optimize_conversion(data)
    show_summary(currency_summary, path_summary) #uncomment to see the best conversion for each currency
    print('Best Chain: {}'.format(best_chain))
    print('Best Value: {}'.format(best_value))


if __name__ == '__main__':
    main()
