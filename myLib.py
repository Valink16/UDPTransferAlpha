def ask(msg,pos,neg):
	#simple neg or pos answer asking function
	#args must be string type
	loopInput=True
	while(loopInput):
		reponse=input(msg)
		if(reponse.upper()==pos):
			return True
		elif(reponse.upper()==neg):
			return False
		else:
			print("Enter {} or {}".format(pos,neg))


def log(msg):
        print("[*]"+msg)
