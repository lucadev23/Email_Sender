from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class sendMail:
	host = ""
	port  = 0
	username = ""
	password = ""
	from_mail = username
	mail_list=[]
	html_txt=""
	email_conn=SMTP()
	def __init__(self):
		self.host = "smtp.gmail.com"
		self.port  = 587
		self.username = ""
		self.password = ""
		self.from_mail = self.username
		self.mail_list=[]
		self.html_txt=""
		self.email_conn=SMTP(self.host,self.port)
	def initSetting(self):
		self.host=input("Insert service address: ")
		self.port=input("Insert service port: ")
		self.username=input("Insert your email: ")
		self.password=input("Insert your password:")
	def initSettingWithGoogleService(self):
		self.host = "smtp.gmail.com"
		self.port  = 587
		self.username=input("Insert your email: ")
		self.password=input("Insert your password:")
	def setUsernamePassword(self,username,password):
		self.username=username
		self.password=password
		self.from_mail = self.username
	def reset(self):
		self.host = ""
		self.port  = 0
		self.username = ""
		self.password = ""
		self.from_mail = self.username
		self.mail_list=[]
		self.html_txt=""
	def createMailList(self):
		i = 0
		self.mail_list=[]
		while 1:
			mail = input("Insert email "+str(i+1)+" or digit 'X' to stop: ")
			if mail == 'X':
				break
			self.mail_list.append(mail)
	def resetMailList(self):
		self.mail_list=[]
	def addMailToList(self):
		mail = input("Insert email: ")
		self.mail_list.append(mail)
	def uploadHtmlFile(self):
		path_file=input("Insert path of html file: ")
		file=open(path_file,'r')
		if file.readable()==False:
			print("Error read file:"+path_file)
			return
		self.html_txt=file.read()
		file.close()
	def connectToService(self):
		try:
			self.email_conn = SMTP(self.host,self.port)
			self.email_conn.ehlo()
			self.email_conn.starttls()
		except:
			print("An error occured while try to connect to service")
			return False
		return True
		print("Connected to service!")
	def loginToService(self):
		try:
			self.email_conn.login(self.username,self.password)
		except SMTPAuthenticationError:
			print("Could not login")
			return False
		except:
			print("An error occured while try to login to service")
			return False
		return True
		print("Connected!")
	def connect(self):
		if self.connectToService() == True:
			if self.loginToService() == True:
				return True
		return False
	def disconnected(self):
		self.email_conn.quit()
		print("Disconnected!")
	def sendMail(self):
		if len(self.mail_list) < 1:
			self.email_conn.quit()
			print("Lista email vuota")
			quit()
		for i in range(len(self.mail_list)):
			msg = MIMEMultipart("alternative")
			msg["Subject"] = "Oggetto del messaggio"
			msg["From"] = self.from_mail
			msg["To"] = self.mail_list[i]
			plain_txt = ""#Messaggio in chiaro da inviare
			part_1 = MIMEText(plain_txt,'plain')
			part_2 = MIMEText(self.html_txt, "html")
			msg.attach(part_1)
			msg.attach(part_2)
			try:
				self.email_conn.sendmail(self.from_mail, self.mail_list[i], msg.as_string())
			except SMTPException:
				print("Error sending message to "+self.mail_list[i])
			print("Message to "+self.mail_list[i]+" sended!")
	def importListFromFile(self):
		path_file=input("Insert path of email file: ")
		file=open(path_file,'r')
		if file.readable()==False:
			print("Error read file:"+path_file)
			return
		self.mail_list=file.readlines()
		self.mail_list=self.filterList(self.mail_list)
		#print(self.mail_list)
		file.close()
	def filterList(self,list_to_filter):
		for i in range(len(list_to_filter)):
			list_to_filter[i] = list_to_filter[i][:len(list_to_filter[i])-1] #this because i want to delete the '\n' character from strings
		if list_to_filter[len(list_to_filter)-1]== "": #this to remove the last element of file
			list_to_filter.pop(len(list_to_filter)-1)
		return list_to_filter
	def loginFromFile(self):
		file=open("login.txt",'r')
		if file.readable()==False:
			return False
		try:
			login=file.readlines()
			login=self.filterList(login)
			self.setUsernamePassword(login[0],login[1])
		except:
			file.close()
			return False
		file.close()
		return True
#testing sendMail class
s = sendMail()
if s.loginFromFile() == False:
	s.initSettingWithGoogleService()
if s.connect() == True:
#	s.createMailList()
	s.importListFromFile()
	s.uploadHtmlFile()
	s.sendMail()
else:
	print("End program")
