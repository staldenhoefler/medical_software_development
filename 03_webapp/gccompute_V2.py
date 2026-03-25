import sys
from io import StringIO
def main(input_seq):
    try:
        counter = 0
        for c in input_seq.split(' ')[-1]:
            if c == 'G' or c == 'C':
                counter += 1

        return counter / len(input_seq.split(' ')[-1]) * 100
    except Exception as e:
        print(f'Something went wrong')
        print(e)
        return "0"

def read_fasta_file(file):
    try:
        file = StringIO(file.getvalue().decode("utf-8")).read()
        sequences = file.split('>')[1:]
        sequence_list = []
        for sequence in sequences:
            sequence = sequence.replace('\n', '')
            sequence = sequence.replace(']', ' ')
            sequence = sequence.replace('[', ' ')
            sequence_list.append(sequence)
        return sequence_list[0]
    except Exception as e:
        print(f'Something went wrong')
        print(e)
        return 0