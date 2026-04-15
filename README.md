# DVWA Bug Bounty Lab (Metasploitable 2)

This repository contains artifacts for a penetration testing exercise performed against **Damn Vulnerable Web Application (DVWA)** running on an **unmodified Metasploitable 2** VM.

## Author
- Markus Stamm

## Scope / Ethics

- Target: Metasploitable 2 VM hosting DVWA
- Allowed: Testing only inside this controlled lab
- Not allowed: Using these techniques against systems you do not own or do not have explicit permission to test

## Environment

- Hypervisor: VirtualBox
- Target VM: Metasploitable 2
- DVWA security level: `Medium`

### Network Configuration (VirtualBox)

Recommended isolation:

- `Adapter 1`: `Host-only Adapter` (`vboxnet0`)
- (Optional) `Adapter 2`: `NAT` (only if you need internet access inside the VM)

Target IP used in this lab:

- Metasploitable 2: `192.168.56.101`

To find the target IP from the VM:

```bash
ifconfig
```

To verify connectivity from the host:

```bash
ping 192.168.56.101
```

### DVWA Access

- DVWA base URL: `http://192.168.56.101/dvwa/`
- Security level page: `http://192.168.56.101/dvwa/security.php`

If DVWA needs initialization:

- Setup page: `http://192.168.56.101/dvwa/setup.php`

## Repo Layout

- `recon/`: network reconnaissance outputs
- `proof/`: screenshots and tool outputs used as evidence
- `scripts/`: custom scripts created for this project

## Reconnaissance

Nmap output files are saved in `recon/`:

- `recon/recon_initial.nmap`
- `recon/recon_initial.gnmap`
- `recon/recon_initial.xml`

Example scan command used:

```bash
nmap -sC -sV -oA recon/recon_initial 192.168.56.101
```

## Custom Script (Requirement)

A custom brute-force helper script is included:

- `scripts/dvwa_bruteforce.py`

Usage:

```bash
python3 scripts/dvwa_bruteforce.py --help
```

Note: This script is designed for the DVWA lab and requires valid DVWA session cookies.

## Evidence / Proof

Collected evidence is stored under `proof/`, including:

- `proof/hydra/`: brute-force tool output
- `proof/sqlmap/`: SQL injection tool output
- `proof/exploit-research/`: version-to-advisory/exploit research notes
- `proof/upload/`: safe test upload assets (e.g., a small JPEG)

## Notes / Challenges Encountered

- Got stuck in VirtualBox
- Hydra usage and proper indexing?
- DVWA upload on `Medium` is strict about client-supplied MIME type (`image/jpeg`) and size (< 100 KB). Uploading a PNG will fail even if the file is otherwise valid.
- Firewall? issues when trying to reverse shell
- 
