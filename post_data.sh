GetTables()
{
    wget \
    -O - \
    --quiet \
    --header="Authorization: Basic $(echo -n 'user01:passw01' | base64)" \
    --header="Content-Type: application/json" \
    --post-data='{"method": "Get_Tables", "param": {"scheme": "public"}}' \
    http://localhost:8082/api/tables |\
    jq --color-output .
}

GetUserConf()
{
    wget \
    -O - \
    --quiet \
    --header="Authorization: Basic $(echo -n 'user01:passw01' | base64)" \
    --header="Content-Type: application/json" \
    --post-data='{"method": "Get_UserConf", "param": {"user_id": 1}}' \
    http://localhost:8082/api/user |\
    jq --color-output .
}

GetUserId()
{
    wget \
    -O - \
    --quiet \
    --header="Authorization: Basic $(echo -n 'user01:passw01' | base64)" \
    --header="Content-Type: application/json" \
    --post-data='{"method": "Get_UserId", "param": {"login": "user01", "passw": "passw01"}}' \
    http://localhost:8082/api/user |\
    jq --color-output .
}



GetTables
#GetUserConf
#GetUserId
