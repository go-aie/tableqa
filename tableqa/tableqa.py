# -*- coding: utf-8 -*-

import tempfile, os, json

from transformers import BertTokenizer
from modelscope.models import Model
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.preprocessors import TableQuestionAnsweringPreprocessor
from modelscope.preprocessors.nlp.space_T_cn.fields.database import Database
from modelscope.utils.constant import ModelFile, Tasks


model_id = 'damo/nlp_convai_text2sql_pretrain_cn'
model = Model.from_pretrained(model_id)
tokenizer = BertTokenizer(os.path.join(model.model_dir, ModelFile.VOCAB_FILE))


class TableQA:
    def __init__(self, tables):
        data = []
        for i, table in enumerate(tables):
            rows = table['rows']
            column_num = len(rows[0])
            data.append(dict(
                table_id=f'table{i}',
                table_name=table['title'],
                header_id=[f'col{j}' for j in range(column_num)],
                header_name=table['rows'][0],
                header_types=['text'] * column_num,
                header_units=[''] * column_num,
                header_attribute=['MODIFIER'] * column_num,
                rows=table['rows'][1:],
            ))

        with tempfile.NamedTemporaryFile() as f:
            for d in data:
                f.write(json.dumps(d, ensure_ascii=False).encode('utf-8'))
                f.write(b'\n')
            f.seek(0, 0)

            db = Database(
                tokenizer=tokenizer,
                table_file_path=f.name,
                syn_dict_file_path=os.path.join(model.model_dir, 'synonym.txt'),
                is_use_sqlite=True)

        preprocessor = TableQuestionAnsweringPreprocessor(model_dir=model.model_dir, db=db)

        self.pipline = pipeline(
            Tasks.table_question_answering,
            model=model,
            preprocessor=preprocessor,
            db=db)

    def chat(self, question):
        output_dict = self.pipline({
            'question': question,
        })[OutputKeys.OUTPUT]
        # print('sql text:', output_dict[OutputKeys.SQL_STRING])
        # print('sql query:', output_dict[OutputKeys.SQL_QUERY])
        # print('query result', output_dict['query_result'])
        result = output_dict['query_result']['rows']
        if result and result[0]:
            return result[0][0]
        else:
            return '未找到相关答案'
