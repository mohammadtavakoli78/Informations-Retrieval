class InvertedIndex:
    def __init__(self):
        self.doc_id_list = []
        self.all_number_of_repetition = 0
        self.number_of_repetition_each_doc = {}

    def get_doc_id_list(self):
        return self.doc_id_list

    def get_all_number_of_repetition(self):
        return self.all_number_of_repetition

    def get_number_of_repetition_each_doc(self):
        return self.number_of_repetition_each_doc

    def set_doc_id_list(self, doc_id_list):
        self.doc_id_list = doc_id_list

    def set_all_number_of_repetition(self, all_number_of_repetition):
        self.all_number_of_repetition = all_number_of_repetition

    def set_number_of_repetition_each_doc(self, number_of_repetition_each_doc):
        self.number_of_repetition_each_doc = number_of_repetition_each_doc
