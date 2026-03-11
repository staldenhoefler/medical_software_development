import pandas as pd
import sys

def main():
    args = sys.argv[1:]
    try:
        df = pd.read_csv(args[0], sep='\t', low_memory=False, usecols=['#tax_id', 'type_of_gene'])
    except Exception as e:
        print(f'Could not read file.')
        print(e)
        return 0

    print(f'MD5 value of the input file')
    print(f'Answer question 1: {df.shape[0]}')
    print(f'Answer question 2: {df[df['#tax_id'] == 9606].shape[0]}')
    print(f'Answer question 3: {', '.join(df['type_of_gene'].unique().tolist())}')
    print(f'Answer question 4: {df['type_of_gene'].value_counts().index[df['type_of_gene'].value_counts().argmax()]}')

    return 1

if __name__ == '__main__':
    sys.exit(main())