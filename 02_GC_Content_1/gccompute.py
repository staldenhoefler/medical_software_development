import sys
def main():
    args = sys.argv[1:]
    try:
        with open(args[0]) as f:
            file = f.read()
        sequences = file.split('>')[1:]
        for sequence in sequences:
            sequence = sequence.replace('\n', '')
            sequence = sequence.replace(']', ' ')
            sequence = sequence.replace('[', ' ')
            seq_id = sequence.split(' ')[0]
            counter = 0
            for c in sequence.split(' ')[-1]:
                if c == 'G' or c == 'C':
                    counter += 1
            #print(f'{sequence.split(' ')[-1]} \n\n\n\n\n')
            print(f'Answer for {seq_id}: {counter / len(sequence.split(' ')[-1]) * 100}%')
        return 1
    except Exception as e:
        print(f'Something went wrong')
        print(e)
        return 0

if __name__ == '__main__':
    sys.exit(main())