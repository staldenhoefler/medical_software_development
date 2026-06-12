from Bio.Seq import Seq


class Utility:
    @staticmethod
    def transcribe_dna_to_rna(dna):
        return dna.transcribe()

    @staticmethod
    def translate_rna_to_protein(rna):
        return rna.translate()

    @staticmethod
    def read_fasta_file(path):
        lines = open(path).read().splitlines()
        # drop the header line(s) starting with '>' and join the rest
        seq = ''.join(line for line in lines if not line.startswith('>'))
        return Seq(seq)
