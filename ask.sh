# Make a data URL from a file
function make-data-url() {
  TYPE=$(file --mime-type -b $1)
  ENC=$(base64 $1)
  echo "data:$TYPE;base64,$ENC"
}

# 1. Parse tables from PDF
TABLES=$(curl -s -XPOST -H 'Content-Type: application/json' http://127.0.0.1:8081/tables -d '{"file": "'$(make-data-url $1)'"}')

# 2. Add a question
DATA=$(echo $TABLES | python -c 'import json, sys; data = json.load(sys.stdin); data["question"] = "'$2'"; print(json.dumps(data, ensure_ascii=False))')

# 3. Get the answer from TableQA
curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:8081/ask -d "$DATA"
