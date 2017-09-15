import json, redis
from flask import Flask, request, jsonify
#	#	#	#	#
def is_valid(data):

	if len(data) == 3 and "name" in data and "date" in data and "phone" in data:
		return True
		
	return False
#	#	#	#	#
def put(data):
	my_server = redis.Redis(connection_pool = POOL)
	my_server.rpush('names', data['name'])
	my_server.rpush('dates', data['date'])
	my_server.rpush('phones', data['phone'])
#	#	#	#	#
POOL = redis.ConnectionPool(host = '127.0.0.1', port = 6379, db = 0)
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
#	#	#	#	#
def result():

	if request.method == 'POST':
	
		content = None
		data = {}
		not_valid_message = '{ "result": "Error! Json is not valid!" }'
		success_message = '{ "result": "Data has been successfully put into Redis." }'
		
		try:
			content = request.get_json()
			if not is_valid(content):
				return not_valid_message
				
		except Exception as e:
			return str(e)
			
		data['name'] = content['name'].encode('ascii')
		data['date'] = content['date']
		data['phone'] = content['phone']
		
		put(data)
		
		return success_message
		
	if request.method == 'GET':
		
		my_server = redis.Redis(connection_pool = POOL)
		
		result = request.args.get('type')

		if (result == '1'):
			name = request.args['name']
			names = my_server.lrange('names', 1, -1)
			cur_index = -1
			for i in range(0, len(names)):
				if name == names[i]:
					cur_index = i
					break
			if cur_index == -1:
				return json.dumps({ 'message': '' })
			date = my_server.lrange('dates', cur_index + 1, cur_index + 1)[0]
			phone = my_server.lrange('phones', cur_index + 1, cur_index + 1)[0]
			
			output = name + ', ' + date + ', ' + phone
			print(output)
			return json.dumps({ 'message': output })

		if (result == '2'):
			names = my_server.lrange('names', 1, -1)
			dates = my_server.lrange('dates', 1, -1)
			phones = my_server.lrange('phones', 1, -1)

			output = ''
			for i in range(0, min(len(names), len(dates), len(phones))):
				if output != '':
					output += ';'
				output += names[i] + ', ' + dates[i] + ', ' + phones[i]

			return json.dumps({ 'message': output })

		if (result == '3'):
			names = my_server.lrange('names', 1, -1)
			dates = my_server.lrange('dates', 1, -1)
			phones = my_server.lrange('phones', 1, -1)

			output = ''

			ar = [0] * len(dates)
			for i in range(0, len(dates)):
				ar[i] = [i, dates[i]]
			ar.sort(key = lambda tup: tup[1])

			for i in range(0, len(ar)):
				if output != '':
					output += ';'
				output += names[ar[i][0]] + ', ' + dates[ar[i][0]] + ', ' + phones[ar[i][0]]

			return json.dumps({ 'message': output })

		if (result == '4'):
			names = my_server.lrange('names', 1, -1)
			dates = my_server.lrange('dates', 1, -1)
			phones = my_server.lrange('phones', 1, -1)

			output = ''

			ar = [0] * len(dates)
			for i in range(0, len(dates)):
				ar[i] = [i, dates[i]]
			ar.sort(key = lambda tup: tup[1])
			ar = list(reversed(ar))
			for i in range(0, len(ar)):
				if output != '':
					output += ';'
				output += names[ar[i][0]] + ', ' + dates[ar[i][0]] + ', ' + phones[ar[i][0]]

			return json.dumps({ 'message': output })

		return json.dumps({ 'message': "you shouldn't receive this message" })
	
#	#	#	#	#	
app.run(host = '0.0.0.0')
