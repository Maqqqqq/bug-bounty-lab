# Penetration Testing Report: DVWA on Metasploitable 2

**Assessment date:** 2026-02-15  
**Target:** Metasploitable 2 (DVWA) at `192.168.56.101`  
**Testing type:** Authorized lab penetration test (controlled environment)  
**DVWA security level:** Medium (see evidence)

## Executive Summary

A penetration test was performed against DVWA hosted on an unmodified Metasploitable 2 VM. The assessment identified multiple high-impact weaknesses that enable account compromise, sensitive data extraction from the backend database, and server-side code execution that can be escalated to root privileges.

Key outcomes:

- Successful credential compromise of a non-admin DVWA user via brute forcing.
- SQL injection enabling enumeration of database schemas, extraction of user records, and identification of the backend database version.
- File upload weakness enabling attacker-controlled file placement in a web-accessible directory, culminating in code execution and privilege escalation to root.

## Methodology

The assessment followed a standard web and host enumeration workflow:

- Environment verification (DVWA reachable, security set to Medium).
- Reconnaissance and service enumeration against the target host.
- Web application testing focused on the required attack classes:
  - Brute force authentication weakness
  - SQL injection
  - File upload
- Post-exploitation validation (privilege level verification) and evidence collection.
- Documentation of results, limitations, and recommendations.

## Environment Setup

- Hypervisor: VirtualBox
- Network: Host-only adapter (`vboxnet0`)
- Target host: Metasploitable 2
- DVWA security level: Medium

Evidence:

- DVWA security set to Medium: `proof/dvwa.png`

## Reconnaissance

### Port and Service Discovery

A service/version scan identified multiple exposed services, including FTP, SSH, Telnet, SMTP, DNS, HTTP, SMB, databases, and additional legacy services.

Evidence:

- Nmap outputs: `recon/recon_initial.nmap`, `recon/recon_initial.gnmap`, `recon/recon_initial.xml`

### Network Map (Single Host)

Target: `192.168.56.101` (Metasploitable 2)

Exposed services (high-level):

- `21/tcp` FTP (anonymous login allowed)
- `22/tcp` SSH (legacy server)
- `23/tcp` Telnet (cleartext remote login)
- `25/tcp` SMTP
- `53/tcp` DNS
- `80/tcp` HTTP (Apache)
- `139,445/tcp` SMB (Samba)
- `3306/tcp` MySQL
- `5432/tcp` PostgreSQL
- `8180/tcp` Tomcat

Potential weaknesses from recon:

- Multiple legacy/cleartext services (e.g., Telnet) increase credential exposure risk.
- Several services appear outdated, increasing the likelihood of known vulnerabilities.
- Broad attack surface increases overall compromise likelihood.

## Findings

### Finding 1: Brute Force (Authenticated) Allows Credential Compromise

**Risk rating:** High  
**Category:** Authentication / Password Security  
**Affected component:** DVWA Brute Force module (Medium)

**Description**

The application allows repeated login attempts against user accounts without effective rate limiting, lockout, or additional verification. This enables an attacker with access to the brute force functionality to guess passwords using a dictionary and identify valid credentials.

**Evidence / Results**

- Successful credential discovery for non-admin account `gordonb`.
- Evidence (tool output): `proof/hydra/hydra_bruteforce_gordonb_2026-02-15.txt`
- Evidence (application login): `proof/brute_force.png`

**Steps to Reproduce (High Level)**

- Ensure DVWA security is set to Medium.
- Access the DVWA Brute Force functionality as an authenticated user.
- Select a non-admin target username.
- Perform repeated credential attempts using a dictionary/wordlist approach.
- Identify a successful attempt by a response change indicating authentication success.
- Validate by logging in with the recovered credentials.

Screenshots:

- DVWA security Medium: `proof/dvwa.png`
- Successful login using recovered credentials: `proof/brute_force.png`

**Impact**

- Account takeover of DVWA users.
- In real deployments, similar weaknesses can enable unauthorized access to sensitive data.

**Recommendations**

- Enforce strong password policies (length, complexity, banned common passwords).
- Implement rate limiting and account lockout/backoff on repeated failures.
- Add 2FA for administrative and high-risk actions.
- Add monitoring and alerting for anomalous login attempts.

### Finding 2: SQL Injection Enables Database Enumeration and Data Extraction

**Risk rating:** Critical  
**Category:** Injection  
**Affected component:** DVWA SQL Injection module (Medium)

**Description**

User-controlled input is handled in a way that allows SQL injection techniques. This enables attackers to enumerate database structure and extract sensitive records, including user data. The database banner/version was also retrieved.

**Evidence / Results**

- Database banner/version extracted: MySQL `5.0.51a-3ubuntu5`.
  - Evidence: `proof/sqlmap/sqlmap_banner_2026-02-15.txt`
- Database names (schemas) enumerated.
  - Evidence: `proof/sqlmap/sqli_dbs_2026-02-15.txt`
- DVWA users table dumped (all users retrieved).
  - Evidence: `proof/sqlmap/sqli_users_dump_2026-02-15.txt`

**Steps to Reproduce (High Level)**

- Ensure DVWA security is set to Medium.
- Access the DVWA SQL Injection functionality.
- Confirm the injectable parameter by observing application response differences when altering input.
- Enumerate database schemas.
- Retrieve the database banner/version.
- Extract user records from the DVWA database.

Screenshots:

- DVWA security Medium: `proof/dvwa.png`

**Identified version-matched exploit reference**

Based on the discovered DB banner (`5.0.51a-3ubuntu5`), the following version-targeted exploit reference was recorded:

- Oracle MySQL < 5.1.50 privilege escalation (replication/slave prerequisite)
  - Evidence: `proof/exploit-research/mysql_searchsploit.txt`

**Impact**

- Confidentiality breach: attackers can extract user records and potentially other sensitive application data.
- Enables further attacks by revealing credentials/hashes and internal schema information.

**Recommendations**

- Use parameterized queries (prepared statements) everywhere.
- Apply server-side input validation as defense-in-depth (not a replacement for parameterization).
- Restrict database account permissions (least privilege).
- Monitor for SQLi patterns and consider a WAF as an additional control.

### Finding 3: File Upload Weakness Enables Code Execution and Privilege Escalation

**Risk rating:** Critical  
**Category:** Unrestricted File Upload / Remote Code Execution  
**Affected component:** DVWA Upload module (Medium)

**Description**

The upload functionality relies on weak validation (e.g., client-controlled MIME type and size threshold), allowing attacker-controlled content to be placed into a web-accessible directory. This can lead to server-side code execution depending on server configuration and file handling.

In this lab, code execution was achieved and then escalated to root using a local privilege escalation path.

**Evidence / Results**

- Reverse connection established and privilege escalation to root demonstrated.
  - Evidence: `proof/become_root.png`

Supporting note:

- A safe test JPEG was generated to validate DVWA Medium upload constraints.
  - Artifact: `proof/upload/test_10x10.jpg`

**Steps to Reproduce (High Level)**

- Ensure DVWA security is set to Medium.
- Use the DVWA Upload feature to upload a file that passes the server-side checks (Medium).
- Confirm the server stores the uploaded file in a web-accessible location.
- Validate server-side execution was possible in this environment.
- Establish an initial shell as the web server context and verify privileges.
- Escalate privileges to root via a local misconfiguration and verify root.

Screenshots:

- Root verification and chain evidence: `proof/become_root.png`

**Impact**

- Remote code execution as the web server user (e.g., `www-data`).
- Full system compromise when combined with a privilege escalation vector.

**Recommendations**

- Enforce strict server-side allowlists based on verified file content (magic bytes), not client `Content-Type`.
- Store uploads outside the web root and serve via a safe download handler.
- Disable directory listing on upload directories.
- Apply least privilege and remove unsafe SUID binaries; continuously audit SUID/SGID files.
- Add runtime monitoring (process execution from web context, suspicious outbound connections).

## Tools Used and Effectiveness

- Nmap: effective for identifying exposed services and versions.
- Hydra: effective for validating brute-force susceptibility and recovering weak credentials.
- SQLMap: effective for extracting DB banner, schemas, and application user data.
- Custom Python script: `scripts/dvwa_bruteforce.py` reproduced brute-force behavior for the lab.

## Recommendations (Prioritized)

Short-term (quick fixes):

- Add rate limiting/backoff and lockout controls to authentication flows.
- Disable directory listing and ensure uploaded files are not directly executable.
- Remove unsafe SUID/SGID permissions and audit SUID/SGID binaries.

Long-term (strategic improvements):

- Migrate all database access to parameterized queries and enforce least-privilege DB accounts.
- Implement centralized logging/monitoring for authentication and web execution events.
- Establish patch management for OS and third-party services.

## Limitations

- This was a lab assessment against a deliberately vulnerable target. Findings and impact are representative of real vulnerability classes, but exact exploitability depends on configuration in real-world environments.
- Evidence collection in this repo focuses on key success criteria. Additional screenshots for intermediate failures can be added to strengthen the audit trail.

## Appendices

### Appendix A: Recon Outputs

- `recon/recon_initial.nmap`
- `recon/recon_initial.gnmap`
- `recon/recon_initial.xml`

### Appendix B: Brute Force Outputs

- `proof/hydra/hydra_bruteforce_gordonb_2026-02-15.txt`
- `proof/brute_force.png`
- Custom script: `scripts/dvwa_bruteforce.py`

### Appendix C: SQL Injection Outputs

- `proof/sqlmap/sqlmap_banner_2026-02-15.txt`
- `proof/sqlmap/sqli_dbs_2026-02-15.txt`
- `proof/sqlmap/sqli_users_dump_2026-02-15.txt`
- Exploit research note: `proof/exploit-research/mysql_searchsploit.txt`

### Appendix D: File Upload / Privilege Escalation Evidence

- `proof/become_root.png`
- Safe upload test file: `proof/upload/test_10x10.jpg`
