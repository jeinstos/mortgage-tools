import argparse
from mortgage import *

def show(m, args):
    header =  '| {:10} | {:10} | {:10} | {:10} | {:10} | {:10} |'.format('Payment #', 'Principal', 'Interest', 'HOI', 'Tax', 'Total')
    divisor = '-'*79
    column_format = '| {:10d} | {:10.02f} | {:10.02f} | {:10.02f} | {:10.02f} | {:10.02f} |'
    columns = []

    monthly_insurance = float(args.insurance) / 12.00
    monthly_tax = ((float(args.tax) / 100.00) * float(args.value)) / 12.00

    cumm_total = 0
    cumm_principal = 0
    cumm_interest = 0
    cumm_tax = 0
    cumm_hoi = 0
    for index, payment in enumerate(m.monthly_payment_schedule()):
        if args.slice and index == int(args.slice): break

        total = sum([float(payment[0]), float(payment[1]), float(monthly_insurance), float(monthly_tax)])
        columns.append(column_format.format(index+1, float(payment[0]), float(payment[1]), float(monthly_insurance), float(monthly_tax), total))

        cumm_total += total
        cumm_principal += float(payment[0])
        cumm_interest += float(payment[1])
        cumm_tax += float(monthly_tax)
        cumm_hoi += float(monthly_insurance)

    print(header)
    for column in columns:
        print(divisor)
        print(column)

    print(divisor)
    print('| {:10} | {:10.02f} | {:10.02f} | {:10.02f} | {:10.02f} | {:10.02f} |'.format('Total', cumm_principal, cumm_interest, cumm_hoi, cumm_tax, cumm_total))
    print(divisor)

def main():
    parser = argparse.ArgumentParser(description='Mortgage Amortization Tools')
    parser.add_argument('-i', '--loan-interest', default=3.5, dest='interest', help='loan interest rate')
    parser.add_argument('-y', '--loan-years', default=30, dest='years', help='loan term in years')
    parser.add_argument('-m', '--loan-months', default=None, dest='months', help='loan term in months')
    parser.add_argument('-a', '--loan-amount', default=75000, dest='amount', help='loan amount')
    parser.add_argument('-v', '--house-value', default=70000, dest='value', help='assesed house value')
    parser.add_argument('-t', '--property-tax', default=4.5, dest='tax', help='total tax rate on property')
    parser.add_argument('-n', '--home-insurance', default=600, dest='insurance', help='cost of a year of home owner\'s insurace')
    parser.add_argument('-s', '--slice', default=60, dest='slice', help='display the first N payments')
    args = parser.parse_args()

    if args.months:
        m = Mortgage(float(args.interest) / 100, float(args.months), args.amount)
    else:
        m = Mortgage(float(args.interest) / 100, float(args.years) * MONTHS_IN_YEAR, args.amount)

    show(m, args)

if __name__ == '__main__':
    main()
