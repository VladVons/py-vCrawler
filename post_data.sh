wget \
    --header="Authorization: Basic $(echo -n 'user01:passw01' | base64)" \
    --header="Content-Type: application/json" \
    --post-data='{"_path": "main", "method": "Main", "param":{"key": "value"}}' \
    http://localhost:8082/api/system/test

