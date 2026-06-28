import random
from Bio.Seq import Seq
from utility import Utility


class DNASequenceGenerator:
    alphabet = ['A', 'C', 'G', 'T']

    def create_sequence(self, n):
        return ''.join(random.choice(self.alphabet) for _ in range(n))


# Singleton
class SequenceStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def save(self, name, sequence):
        self._data[name] = sequence

    def read(self, name):
        return self._data[name]

    def names(self):
        return list(self._data.keys())


class DNASequence:
    kind = 'dna'

    def __init__(self, data):
        self.seq = data if isinstance(data, Seq) else Seq(data)

    def to_protein(self):
        rna = Utility.transcribe_dna_to_rna(self.seq)
        protein = Utility.translate_rna_to_protein(rna)
        return ProteinSequence(protein)

    def __str__(self):
        return str(self.seq)


class ProteinSequence:
    kind = 'protein'

    def __init__(self, data):
        self.seq = data if isinstance(data, Seq) else Seq(data)

    def __str__(self):
        return str(self.seq)


# factory
class SequenceFactory:
    @staticmethod
    def create_sequence(data, kind='dna'):
        if kind == 'dna':
            return DNASequence(data)
        elif kind == 'protein':
            return ProteinSequence(data)
        else:
            raise ValueError(f'unknown sequence kind: {kind}')

if __name__ == '__main__':
    dna = Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG')
    rna = Utility.transcribe_dna_to_rna(dna)
    protein = Utility.translate_rna_to_protein(rna)
    print(f'DNA:     {dna}')
    print(f'RNA:     {rna}')
    print(f'Protein: {protein}')

    print('-' * 60)
    storage_a = SequenceStorage()
    storage_a.save('demo', dna)
    storage_b = SequenceStorage()
    print(f'Only one instance exists: {storage_a is storage_b}')
    print(f"Read back from storage:   {storage_b.read('demo')}")

    print('-' * 60)
    cd28 = DNASequence(Utility.read_fasta_file('../02_GC_Content_1/data/gene.fna'))
    cd28_protein = cd28.to_protein()
    SequenceStorage().save('CD28', cd28_protein)
    print(f'CD28 protein: {cd28_protein}')

    print('-' * 60)
    seq_dna = SequenceFactory.create_sequence('ATGAAATAG', kind='dna')
    seq_protein = SequenceFactory.create_sequence('MKVL', kind='protein')
    print(f'{seq_dna.kind} sequence:     {seq_dna}')
    print(f'{seq_protein.kind} sequence: {seq_protein}')
