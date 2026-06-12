import unittest
import datastructure

class TestDataStructure(unittest.TestCase):

    def test_data_storage_initialization(self):
        ds = datastructure.DataStorage()
        self.assertIsNotNone(ds)

    def test_add_and_get_patient(self):
        ds = datastructure.DataStorage()
        name = "John Doe"
        patient = datastructure.Patient(name)
        ds.add_patient(patient)
        retrieved_patient = ds.get_patient(patient.id)
        self.assertEqual(name, retrieved_patient.name)
        self.assertEqual(patient.id, retrieved_patient.id)

    def test_add_and_get_experiment(self):
        ds = datastructure.DataStorage()
        name = "Walking Test"
        experiment = datastructure.Experiment(name)
        ds.add_experiment(experiment)
        retrieved_experiment = ds.get_experiment(experiment.id)
        self.assertEqual(name, retrieved_experiment.name)
        self.assertEqual(experiment.id, retrieved_experiment.id)

    def test_get_unknown_id_returns_none(self):
        ds = datastructure.DataStorage()
        self.assertIsNone(ds.get_patient("does-not-exist"))
        self.assertIsNone(ds.get_experiment("does-not-exist"))

if __name__ == '__main__':
    unittest.main()