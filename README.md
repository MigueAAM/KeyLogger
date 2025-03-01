!Disclamer:
This is a open-source project, any bad use of this program I'm not responsible for it.
All this script is for try to document how cybercriminals develops the malware and test all the phases of infect 
a PC or server, and how it collects information about passwords, usernames and emails, using social engeniering.
I'm open and happy to recieve any recomendation.

=== Modules for use ===
- pynput
- logging
- thread
- os
- winreg or schtasks

=== Steps for planning ===

PHASE 1 Creating keylogger: Inputs should be save on .txt file and store it on the windows registry (In progress...). 
Features of Phase 1:
  - Inputs should be saved on .txt file
  - Use the reg path: HKEY_CURRENT_USER\Console\%%Startup for make a persistance software when it starts
  - OR schtasks module to create a schedule task like:
    if user opens the browser:
      open(script.py)
    
PHASE 2 Connection: Estabish a connection using a reversal connection for transfer the .txt file to the attacker (not started) 
  - Investigate about paramiko and connections

PHASE 3 delivery: use obfuscation techniques for hide the keylogger into a image, pdf or docx. (not started)
  - It could be a .exe file transformed to a .pdf file and execute it when the user interacts with the infect file.
  
PHASE 4 Testing: test all connection, how works the keylogger, repair any bugs, etc. (not started) 
  -Create a VM for test the keylogger and delivery of the same
  -Use wireshark for see how works the packets
  -Fix any bug founded

PHASE 6 Clean up:. After establish the connection, the port should close and delete any registry from infected pc or clean up any registry (not started)
  
  -Document all the results and changes for investigation purpose
