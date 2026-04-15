## The student can explain what Penetration Testing is and how it is proactively used in cybersecurity.
Penetration testing is an authorized security assessment where we simulate real attacker behavior to find weaknesses before criminals do. It is proactive because it identifies vulnerabilities, validates impact, and helps prioritize fixes based on real risk.

## The student can explain the ethical guidelines of Penetration Testing.
Ethical pentesting requires explicit permission, a clearly defined scope, and safe handling of data. You avoid harming systems, stop when you reach the agreed objective, document actions truthfully, and report findings responsibly so they can be fixed.

## The student can explain the reasons behind choosing their attacking platform.
An attacking platform is chosen based on tool availability, stability, repeatability, and how well it supports evidence collection. For example, a Linux host (or Kali) is commonly used because it has strong networking tools, scripting support, and mature pentest utilities.

## The student can demonstrate network scanning and explain the provided information.
Network scanning discovers live hosts, open ports, and service versions. The results tell you what is exposed (attack surface), what software is running (potential known CVEs), and which services deserve deeper testing.

## The student can explain the network map and identify potential weaknesses.
A network map is a structured view of hosts, IPs, open ports, and services and how they relate. Weaknesses include unnecessary exposed services, outdated versions, cleartext protocols, default credentials, and services that allow anonymous or remote access.

## The student can explain the principles and methods of brute forcing.
Brute forcing is repeated credential guessing against an authentication mechanism. It uses dictionaries/wordlists, rules/mutations, or targeted guesses to find weak passwords when rate limiting, lockout, and monitoring are insufficient.

## The student can explain how the brute forcing tool identifies valid usernames and passwords.
Tools detect success by comparing responses: success messages, redirects, status codes, response length, or content differences between failed and successful logins. A reliable check is a unique success indicator rather than only the absence of an error (to avoid false positives).

## The student can explain the principles and methods of SQL injection.
SQL injection happens when user input is concatenated into SQL queries without proper parameterization, letting attackers change the query logic. Common methods include error-based, union-based, boolean/time-based blind techniques to extract data when direct output is limited.

## The student can explain what further actions can be taken once the database schemas have been obtained.
With schema names, you can enumerate tables/columns, identify sensitive datasets (users, sessions, secrets), and target high-impact tables for extraction. It also helps prioritize remediation by showing what data is actually at risk.

## The student can explain the principles and methods of file upload attacks.
File upload attacks exploit weak validation in upload features to store attacker-controlled files on the server. Impact ranges from hosting malicious content to server-side code execution if the server processes the uploaded file as executable or in a dangerous parser context.

## The student can explain in detail how their reverse shell works.
We uploaded a server-executed file through DVWA Upload, then triggered it from the browser. The target (Metasploitable 2) initiated an outbound connection back to my listener on the host-only network (`192.168.56.1`), which is why it is called a reverse shell. When the connection was received, I got an interactive shell running as the web user (`www-data`, `uid=33`), verified with `whoami` and `id`. After that initial foothold, I performed local privilege escalation and confirmed root-level context (`euid=0`) in the evidence.

## The student can explain various privilege escalation methods.
Privilege escalation is gaining higher permissions than initially obtained. Common categories include misconfigurations (weak `sudoers`, writable sensitive files), unsafe SUID/SGID binaries, exposed credentials/keys, insecure services, and (when applicable) vulnerable kernels or software versions that allow elevation.

## The student can explain the contents of the report.
The report summarizes what was tested, how it was tested, what vulnerabilities were found, and what evidence proves them. It translates technical results into impact and risk, then provides prioritized fixes and practical guidance for both technical and non-technical stakeholders.

## The student can explain how these recommendations improve the security of the application.
Recommendations improve security by reducing attack surface (disabling unused services), preventing common attack paths (parameterized queries, upload hardening), and adding defensive controls (rate limiting, lockout, monitoring). The goal is to lower likelihood of compromise and reduce blast radius if something fails.

