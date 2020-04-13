from flask import Flask, render_template, jsonify, redirect,request, url_for, flash
import csv    

app = Flask(__name__)

name_pass = {'stanley@gmail.com':'1234'}
auth = 0

@app.route("/")
def home():
	if auth == 1:
		return redirect(url_for('profile'))
	return render_template("index.html")
    
@app.route("/profile")
def profile():
	if auth == 0:
		return redirect(url_for("login"))
	return render_template("profile.html")

@app.route("/product")
def product():
	if auth == 0:
		return redirect(url_for("login"))
	return render_template("product.html")

@app.route("/overall")
def overall():
	if auth == 0:
		return redirect(url_for("login"))
	return render_template("overall.html")

@app.route("/login")
def login():
	if auth == 1:
		return redirect(url_for('profile'))
	return render_template("login.html") 

@app.route("/logout")
def logout():
	global auth
	auth = 0
	return redirect(url_for('home'))

@app.route("/process",methods=['POST'])
def process():
	# print(resource)
		if(request.method == 'POST'):
			username = request.form['email']
			password = request.form['password']
			for key,value in name_pass.items():
				if key == username and value == password:
					global auth
					auth = 1
					return url_for('profile')
		return render_template("login.html")

@app.route("/chart_1")
def chart_1():
	filename = "data.csv"
	fields = []
	rows = []
	data_1 = []
	data_2 = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	count_order = float(rows[0][3])
	count_sales = float(rows[0][8])
	for i in range (1,len(rows)):
		if(rows[i][1] == rows[i-1][1]):
			count_order = count_order + float(rows[i][3])
			count_sales = count_sales + float(rows[i][8])
		else:
			data_1.append(int(count_order))
			data_2.append(int(count_sales))
			count_order = float(rows[i][3])
			count_sales = float(rows[i][8])
	data_1.append(count_order)
	data_2.append(count_sales)
	print(data_1)
	print(data_2)

		# print("Total no. of rows: %d"%(csvreader.line_num)) 
  
	# print('Field names are:' + ', '.join(field for field in fields))
	return jsonify({'order':data_1,'sales':data_2})

@app.route("/chart_2")
def chart_2():

	filename = "data2.csv"
	fields = []
	rows = []
	data_1 = []
	data_2 = []
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	for i in rows:
		if(i[0] not in dictt):
			dictt[i[0]] = 0
	for i in rows:
		dictt[i[0]] = dictt[i[0]] + int(i[1])
	
	summ = sum(dictt.values())
	print(100-((dictt['Art & Sculpture']/summ) + (dictt['Basket']/summ) + (dictt['Christmas']/summ) + (dictt['Home Decor']/summ) + (dictt['Recycled Art']/summ) + (dictt['Jewelry']/summ) + (dictt['Skin Care']/summ) + (dictt['Kitchen']/summ)))
	# print(dictt['Basket'])
	# print((dictt['Basket']+summ)/summ)

	return jsonify({'results':[{
            'name': 'Art & Sculpture',
            'y': (dictt['Art & Sculpture']/summ)*100
            
        }, {
            'name': 'Basket',
            'y': (dictt['Basket']/summ)*100
        }, {
            'name': 'Christmas',
            'y': (dictt['Christmas']/summ)*100
        }, {
            'name': 'Home Decor',
            'y': (dictt['Home Decor']/summ)*100
        }, {
            'name': 'Recycled Art',
            'y': (dictt['Recycled Art']/summ)*100
        }, {
            'name': 'Jewelry',
            'y': (dictt['Jewelry']/summ)*100
        }, {
            'name': 'Skin Care',
            'y': (dictt['Skin Care']/summ)*100
        }, {
            'name': 'Kitchen',
            'y': (dictt['Kitchen']/summ)*100
        }, {
            'name': 'Other',
            'y': (1-((dictt['Art & Sculpture']/summ) + (dictt['Basket']/summ) + (dictt['Christmas']/summ) + (dictt['Home Decor']/summ) + (dictt['Recycled Art']/summ) + (dictt['Jewelry']/summ) + (dictt['Skin Care']/summ) + (dictt['Kitchen']/summ)))*100 
        }]
    })

@app.route("/chart_3")
def chart_3():

	filename = "data.csv"
	fields = []
	rows = []
	data_1 = []
	data_2 = []
	data_3 = []
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)

	for i in rows:
		if(i[1] == '2019'):
			data_1.append(int(i[2]))
			data_2.append(int(abs(float(i[4]))))
			data_3.append(int(abs(float(i[5]))))
	print(data_1,data_2,data_3)

	return jsonify({'order':data_1,'disc':data_2,'sales':data_3})


@app.route("/stats_home")
def stats_home():

	filename = "data.csv"
	fields = []
	rows = []
	sales_sum=0
	ordersum = 0
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)

	for i in rows:
		if(i[1] == '2019'):
			ordersum = ordersum + int(i[2])
			sales_sum = sales_sum + int(float(i[8]))

	return jsonify({'sales':sales_sum,'order':ordersum})

@app.route("/stats_product")
def stats_product():

	filename = "data2.csv"
	fields = []
	rows = []
	sales_sum=0
	ordersum = 0
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	for i in rows:
		if(i[0] not in dictt):
			dictt[i[0]] = 0
	for i in rows:
		dictt[i[0]] = dictt[i[0]] + int(i[1])
	o = max(dictt,key = dictt.get)
	
	dictt1={}
	for i in rows:
		if(i[0] not in dictt1):
			dictt1[i[0]] = 0
	for i in rows:
		dictt1[i[0]] = dictt1[i[0]] + int(abs(float(i[3])))

	d = max(dictt1,key = dictt1.get)

	

	r = min(dictt,key = dictt.get)

	dictt3 = {}
	for i in rows:
		if(i[0] not in dictt3):
			dictt3[i[0]] = 0
	for i in rows:
		dictt3[i[0]] = dictt3[i[0]] + int(float(i[2]))

	s = max(dictt3,key = dictt3.get)

	# for i in rows:
	# 	if(i[0] not in dictt):
	# 		dictt[i[0]] = 0
	# for i in rows:
	# 	dictt[i[0]] = dictt[i[0]] + int(i[1])

	return jsonify({'sales':s,'order':o,'discount':d,'return':r})


@app.route("/chart_1_p")
def chart_1_p():

	filename = "data2.csv"
	fields = []
	rows = []
	returnn = []
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	for i in rows:
		if(i[0] not in dictt):
			dictt[i[0]] = 0
	for i in rows:
		dictt[i[0]] = dictt[i[0]] + int(i[1])

	for key,value in dictt.items():
		if key != '':
			a = []
			a.append(key)
			a.append(value)
			returnn.append(a)
	return jsonify({'result':returnn})


@app.route("/chart_2_p")
def chart_2_p():

	filename = "data2.csv"
	fields = []
	rows = []
	returnn = []
	dictt={}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	for i in rows:
		if(i[0] not in dictt):
			dictt[i[0]] = 0
	for i in rows:
		dictt[i[0]] = dictt[i[0]] + int(float(i[5]))

	for key,value in dictt.items():
		if key != '':
			a = []
			a.append(key)
			a.append(value)
			returnn.append(a)
	return jsonify({'result':returnn})


@app.route("/stats_overall")
def stats_overall():

	filename = "data.csv"
	fields = []
	rows = []
	dictt={}
	o = 0
	s = 0
	d = 0
	r = 0
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	for i in rows:
		if(i[0] not in dictt):
			dictt[i[0]] = 0
	for i in rows:
		o = o + int(i[2])
		s = s + int(float(i[8]))
		d = d + int(abs(float(i[4])))
		r = r + int(float(i[7]))

	return jsonify({'sales':o,'order':s,'discount':d,'return':r})


@app.route("/chart_1_o")
def chart_1_o():
	filename = "data.csv"
	fields = []
	rows = []
	data_1 = []
	data_2 = []
	data_3 = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	count_order = 0
	count_sales = 0
	order = 0
	shipping = 0
	dics = 0
	for i in range (1,len(rows)):
		if(rows[i][1] =='2017'):
			count_order = count_order + float(rows[i][3])
			count_sales = count_sales + float(rows[i][8])
			order = order + int(rows[i][2])
			shipping = shipping + float(rows[i][7])
			dics = dics + abs(float(rows[i][4]))
	data_1.append(int(count_order))
	data_1.append(int(count_sales))
	# data_1.append(int(order))
	data_1.append(int(shipping))
	data_1.append(int(dics))

	count_order = 0
	count_sales = 0
	order = 0
	shipping = 0
	dics = 0
	for i in range (1,len(rows)):
		if(rows[i][1] =='2018'):
			count_order = count_order + float(rows[i][3])
			count_sales = count_sales + float(rows[i][8])
			order = order + int(rows[i][2])
			shipping = shipping + float(rows[i][7])
			dics = dics + abs(float(rows[i][4]))
	data_2.append(int(count_order))
	data_2.append(int(count_sales))
	# data_2.append(int(order))
	data_2.append(int(shipping))
	data_2.append(int(dics))

	count_order = 0
	count_sales = 0
	order = 0
	shipping = 0
	dics = 0
	for i in range (1,len(rows)):
		if(rows[i][1] =='2019'):
			count_order = count_order + float(rows[i][3])
			count_sales = count_sales + float(rows[i][8])
			order = order + int(rows[i][2])
			shipping = shipping + float(rows[i][7])
			dics = dics + abs(float(rows[i][4]))
	data_3.append(int(count_order))
	data_3.append(int(count_sales))
	# data_3.append(int(order))
	data_3.append(int(shipping))
	data_3.append(int(dics))
			
	return jsonify({'a1':data_1,'a2':data_2,'a3':data_3})

@app.route("/chart_2_o")
def chart_2_o():
	filename = "data.csv"
	fields = []
	rows = []
	data_1 = []
	data_2 = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)
	count_order = float(rows[0][2])
	count_sales = float(rows[0][8])
	for i in range (1,len(rows)):
		if(rows[i][1] == rows[i-1][1]):
			count_order = count_order + float(rows[i][2])
			count_sales = count_sales + float(rows[i][8])
		else:
			data_1.append(int(count_order))
			data_2.append(int((count_sales)/100))
			count_order = float(rows[i][2])
			count_sales = float(rows[i][8])
	data_1.append(count_order)
	data_2.append(int((count_sales)/100))
	print(data_1)
	print(data_2)

		# print("Total no. of rows: %d"%(csvreader.line_num)) 
  
	# print('Field names are:' + ', '.join(field for field in fields))
	return jsonify({'order':data_1,'sales':data_2})

if __name__ == "__main__":
    app.run(debug=True)