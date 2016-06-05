import json
import re
manufacturer_match_threshold=5
model_match_threshold=8
price_threshold=80
def lcs(string1,string2):
	dp = [ [0 for x in range(len(string1)+1)] for x in range(len(string2)+1)]
	index1 = len(string1)-1
	index2 = len(string2)-1
	while index1 >= 0:
		while index2 >= 0:
			if string2[index2] == string1[index1]:
				dp[index2][index1] = 1+dp[index2+1][index1+1]
			else:
				dp[index2][index1] = max(dp[index2+1][index1],dp[index2][index1+1])
			index2-=1
		index2 = len(string2)-1
		index1-=1
	return dp[0][0]
def lcsubstring(string1,string2):
	long_string = ""
	short_string = ""
	if len(string1) < len(string2):
		long_string = string2
		short_string = string1
	else:
		long_string = string1
		short_string = string2
	index1 = 0
	index2 = 0
	max_length = 0
	while index1 < len(long_string):
		if long_string[index1]==short_string[0]:
			runner = 0
			while runner < len(short_string) and index1+runner < len(long_string):
				if short_string[runner] == long_string[index1+runner]:
					# print "matched ",short_string[runner],long_string[index1+runner],"at index",index1+runner
					if max_length < runner+1:
						max_length = runner+1
				else:
					break
				runner+=1
		index1+=1
	return max_length

# string1 = raw_input()
# string2 = raw_input()
# print lcsubstring(string1,string2)


f = open("listings.txt")
listings=[]
for x in f:
	listings.append(json.loads(x))
f.close()
f = open("products.txt")
for x in f:
	response = {}
	data = json.loads(x)
	response["product_name"] = data["product_name"]
	matches = []
	models = re.split('-|_| ',data["model"].lower())
	# print models
	# print "matching ",data
	# print "listings "
	for y in listings:
		if lcs(y["manufacturer"].lower(),data["manufacturer"].lower()) >= min(manufacturer_match_threshold,len(data["manufacturer"])):
			isValid = True
			for z in models:
				if lcsubstring(z,y["title"].lower()) == len(z):
					continue
				else:
					isValid=False
					break
			if isValid == False:
				continue
			if float(y["price"]) > price_threshold:
#				print y
				matches.append(y)
	response["listings"] = matches
	print json.dumps(response)
f.close()