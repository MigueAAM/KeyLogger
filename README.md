<div align="center">
  <h1>🕵️ Endpoint Threat Simulator</h1>
  <p>
    <img src="[https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)" />
    <img src="[https://img.shields.io/badge/Focus-Insider%20Threat-orange?style=for-the-badge](https://img.shields.io/badge/Focus-Insider%20Threat-orange?style=for-the-badge)" />
    <img src="[https://img.shields.io/badge/Tech-Reverse%20Shell-black?style=for-the-badge](https://img.shields.io/badge/Tech-Reverse%20Shell-black?style=for-the-badge)" />
  </p>
  <p><em>A Proof-of-Concept tool to simulate malware persistence and data exfiltration vectors.</em></p>
</div>

<div style="background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 10px; border-radius: 5px;">
  <strong>⚠️ Disclaimer:</strong> This software is for educational purposes and authorized security research only.
</div>

<hr />

<div style="font-family: sans-serif; line-height: 1.6;">

  <h2 style="color: #D35400;">🎯 Purpose of the Project</h2>
  <p>
    To effectively defend an endpoint, a Security Analyst must understand how data is stolen. I developed this simulator to study the lifecycle of an <strong>Insider Threat</strong>. The specific objective was to replicate how malware captures user inputs (Keystrokes) and establishes a persistent connection (C2) to exfiltrate that sensitive data to a remote server.
  </p>

  <h2 style="color: #D35400;">🧠 What I Learned</h2>
  <ul>
    <li><strong>Persistence Mechanisms:</strong> Learned how scripts can run in the background and survive system reboots or user logouts.</li>
    <li><strong>Command & Control (C2):</strong> Built a Linux-based listener to understand how attackers maintain "Reverse Shell" connections to bypass inbound firewall rules.</li>
    <li><strong>Data Exfiltration:</strong> Analyzed how text data is packetized and sent over the network, providing insight into how DLP (Data Loss Prevention) systems might detect this traffic.</li>
  </ul>

  <h2 style="color: #D35400;">🛠️ How I Learned</h2>
  <p>
    I adopted a "Red Team / Blue Team" simulation workflow:
  </p>
  <ol>
    <li><strong>Development (Red Team):</strong> I utilized Python libraries (like <code>pynput</code>) to hook keyboard events and route them to a local file.</li>
    <li><strong>Networking:</strong> I configured a Linux server to listen on specific ports and accept incoming data streams from the client script.</li>
    <li><strong>Analysis (Blue Team):</strong> I monitored the traffic using Wireshark to see what the exfiltration looked like "on the wire," helping me understand what signatures a SOC Analyst would see.</li>
  </ol>

</div>
