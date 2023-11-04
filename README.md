# TableQA

[Table Question Answering][1] based on [Camelot][2] and DAMO's [TableQA][3].


## Prerequisites

```bash
conda create -n tableqa
conda activate tableqa
pip3 install -r requirements.txt
```


## Run

```bash
python3 -m tableqa.api
```


## Test

```bash
bash ask.sh data/集团利润表.pdf 利润总额的变动比率是多少？
```


[1]: https://huggingface.co/tasks/table-question-answering
[2]: https://github.com/camelot-dev/camelot
[3]: https://www.modelscope.cn/models/damo/nlp_convai_text2sql_pretrain_cn/
