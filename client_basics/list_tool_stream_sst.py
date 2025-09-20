import requests

# URL = "http://localhost:8000/mcp/"

# payload= {
#     "jsonrpc":"2.0",
#     "method":"tools/list",
#     "params":{},
#     "id":2
# }

# headers = {
#     'Content-Type':'application/json',
#     "Accept":"application/json, text/event-stream"
# }

# response = requests.post(URL, json=payload, headers=headers, stream=True)

# for line in response.iter_lines():
#     if line:
#         print('line: ', line.decode('utf-8'))