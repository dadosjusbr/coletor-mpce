import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('output_test/expected_2018.json', 'r') as fp:
            expected = json.load(fp)

        files = ['output_test/2018_01_remu.html', 'output_test/2018_01_vi.html']
                 
        dados = load(files, '2018', '01')

        result_data = parse(dados, 'mpce/01/2018', '01', '2018')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        # with open('output_test/expected_2018.json', 'w') as fp:
        #     json.dump(result_to_dict, fp, indent=4, ensure_ascii=False)
        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
