curl -X POST -u sms:F63VRxdn \
  -H "Content-Type: application/json" \
  -d '{ "message": "Hello, doctors!", "phoneNumbers": ["0976646510"] }' \
  http://192.168.2.208:8080/message
