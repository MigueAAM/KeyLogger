<!DOCTYPE html>
# KeyLogger
<p>Copyright (c) 2025 all rights reserved</p>

# !Disclamer
<p>
This is a open-source project, I'm not responsible for any non-ethical use of this script.
All this script is for try to document how cybercriminals develops the malware and test all the phases of infect 
a PC or server, and how it collects information about passwords, usernames and emails, using social engeniering.
I'm happy to recieve any recomendation.
</p>

<h2> Phase 1, Creating the script: </h2>
Inputs should be save on .txt file and store it on the windows registry (In progress...). 

Features of Phase 1:
  - Inputs should be saved on .txt file
  - Use the reg path: HKEY_CURRENT_USER\Console\%%Startup for make a persistance software when it starts
  - OR schtasks module to create a schedule task like:
    if user opens the browser:
      open(script.py)
    
<h2>Phase 2, Connection:</h2> 
Estabish a connection using a reversal connection for transfer the .txt file to the attacker (not started) 
  
  - Investigate about paramiko and reverse shell connections

<h2>Phase 3, Delivery:</h2> 
use obfuscation techniques for hide the keylogger into a image, pdf or docx. (not started)
  
  - It could be a .exe file transformed to a .pdf file and execute it when the user interacts with the infect file.
  
<h2>Phase 4, Testing:</h2> 
test all connection, how works the keylogger, repair any bugs, etc. (not started) 
  
  - Create a VM for test the keylogger and delivery of the same
  - Use wireshark for see how works the packets
  - Fix any bug founded

<h2>Phase 5, Clean up:</h2> 
After establish the connection, the port should close and delete any registry from infected pc or clean up any registry (not started)
  
  - Document all the results and changes for investigation purpose
