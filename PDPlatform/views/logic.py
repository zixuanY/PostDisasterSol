import sqlite3
import math
import numpy as np
# import sys
# sys.path.append("../..")
import PDPlatform
from PDPlatform.views.secrets import GOOGLE_API_KEY
#from PDPlatform.views.siamese_net_face_inference import similarity

#weight = [name, age, height, location]
weight = [0.35,0.2,0.15,0.3]

def get_loc_google(loc):
	geocode_url = "http://maps.google.cn/maps/api/geocode/json?address={}".format(loc)
	geocode_url = geocode_url + "&key={}".format(GOOGLE_API_KEY)
		
	results = requests.get(geocode_url)
	results = results.json()
	
	if len(results['results']) == 0:
		lati = 181
		longi= 181
	else:    
		answer = results['results'][0]
		lati = answer.get('geometry').get('location').get('lat')
		longi = answer.get('geometry').get('location').get('lng')
		return (lati, longi)

def get_distance(relative_loc, rescue_loc, c):
	if(relative_loc==rescue_loc): 
		return 0
	query = "SELECT * FROM coordinate_info WHERE LOCATION = "+"'"+relative_loc+"'"
	result = c.execute(query).fetchall()
	#print(result)
	if (len(result)==0):
		rela_long, rela_lati = get_loc_google(relative_loc)
	else:
		rela_long = result[0]['LONGITUDE']
		rela_lati = result[0]['LATITUDE']
	query = "SELECT * FROM coordinate_info WHERE LOCATION = "+"'"+rescue_loc+"'"
	result = c.execute(query).fetchall()
	if (len(result)==0):
		resc_long, resc_lati = get_loc_google(rescue_loc)
	else:
		resc_long = result[0]['LONGITUDE']
		resc_lati = result[0]['LATITUDE']
	if (rela_long==181 or rela_lati==181 or resc_long==181 or resc_lati==181):
		return float('-inf')
	return (resc_long-rela_long) ** 2 + (resc_lati-rela_lati) ** 2

def calc_influence(dic,result,c):
	possible_res = []
	print(result)
	for entry in result:
		cur_weight = np.zeros(4)
		NAME = entry['NAME']
		if(dic['name'] and NAME and dic['name']!=NAME): # different name
			continue
		if(not NAME): 
			cur_weight[0]=0

		AGE = entry['AGE']
		if(not AGE or not dic['age']):
			cur_weight[1] = 0
		elif abs(int(AGE)-int(dic['age']))>10: 
			cur_weight[1] = -0.1
		else:
			cur_weight[1] = math.exp(0.4*-(abs(int(AGE)-int(dic['age']))))

		# AGE_w = 1.0/(abs(AGE-dic['age'])) if (not entry[3]) 0 elif (entry[3] and abs(AGE-dic['age'])<10)  else 0
		# cur_weight[1] = AGE_w

		HEIGHT = entry['HEIGHT']
		if(not HEIGHT or not dic['height']):
			cur_weight[2] = 0
		elif abs(int(HEIGHT)-int(dic['height']))<10: 
			cur_weight[2] = -0.1
		else:
			cur_weight[2] = math.exp(-0.4*(abs(int(HEIGHT)-int(dic['height']))))

		LOCATION = entry['LOCATION']
		#print((LOCATION,dic['location']))
		if(not LOCATION or not dic['location']):
			cur_weight[3]=0
		else:
			distance = get_distance(dic['location'], LOCATION, c)
			if(distance == float('-inf')):
				cur_weight[3]=0
			elif(distance > 10):
				cur_weight[3]=-0.2
			else:
				cur_weight[3]= math.exp(-0.4*distance)

		coeff = 0
		for i in range(len(cur_weight)):
			if cur_weight[i]!=0:
				coeff+=weight[i] 
		w = -100
		if coeff!=0:
			w = np.dot(weight, cur_weight)/coeff
		possible_res.append((w, entry))
		print(cur_weight)

	possible_res.sort(key=lambda pair: pair[0], reverse = True)
	possible_res = possible_res[:9]

	#print(possible_res)

	# for pair in possible_res:
	#   if(not dic['photo']): continue
	#   sim = similarity(dic['photo'],pair[1][9])
	#   pair[0]=0.3*sim + 0.7*pair[0]

	possible_res.sort(key=lambda pair: pair[0], reverse = True)
	possible_res = possible_res[:4]

	ret = []
	for (coef,res) in possible_res:
		diction = {}
		diction['id']=res['ID']
		diction['age']=res['AGE']
		diction['gender']=res['GENDER']
		diction['photo']=res['PHOTO']
		diction['height']=res['HEIGHT']
		diction['location']=res['LOCATION']
		diction['condition']=res['CONDITION']
		diction['contact']=res['CONTACT']
		ret.append(diction)
	#print(ret)
	#to be checked
	insertion = ()

	return ret

	#PHOTO = entry[10]

def logic(dic):
	"""
	Input: form dict from html
	"""
	sqldb = PDPlatform.model.get_db()
	c = sqldb.cursor()
	# if id is provided
	id_ = dic['id']
	name = dic['name']
	gender = dic['gender']
	if id_:
		query = "SELECT * FROM rescue_side_info WHERE id = "+"'"+id_+"'"
		result = c.execute(query).fetchall()
		# if id matches, directly return the result
		if result:
			return [{"id":dic['id'],"age":dic['age'],"gender":dic['gender'],"contact":dic['contact'],"photo":dic['photo'],'height':dic['height'],'location':dic['location'],'condition':dic['condition']}]
	# if id is not provided
	# gender and name are required to be nonempty from relative side"
	insertion = ('', gender, name)
	query = "SELECT * FROM rescue_side_info WHERE ID = "
	query+= "? and GENDER = ? and (NAME = ? or NAME = '');"
	result = c.execute(query, insertion).fetchall()
	if not result:
		print("not found") # no data match in the database
		return []
	return calc_influence(dic, result, c)
	

if __name__=='__main__':
	#logic("310105198809032254", "小丽", 31, "女", 165, 50, "宜宾", "1318888879999", "糖尿病", "")
	#logic("", "小丽", 31, "女", 165, 50, "宜宾", "1318888879999", "糖尿病", "")
	# logic("31010519991003224", "XiaoMing", 20, "male", 175, 70, "Wenchuan", "131888888888", "None", "")
	logic({"id":"310105199909032244", "name":"XiaoHua", "age":20, "gender":"female", "height":171, "weight":60, "location":"重庆市", "contact":"1318888889999", "health_cond":"Heart Disease", "photo":""})
	# logic("310105198809032254", "XiaoLi", 31, "female", 165, 50, "Yibin", "1318888879999", "None", "")
	# logic({"id":"310105196809032244", "name": "LaoWang", "age": 51, "gender":"male", "height":178, "weight":70, "location":"Wenchuan", "contact":"1318588879999", "health_cond":"None", "photo":""})

