curl -X 'POST' \
  'http://localhost:3000/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "datetime": "",
  "count_per_label": 100,
  "labels": [
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
  ]
}'