# Deep Research: Windows 11 Pro firewall configuration for developer workstations
**Domain:** Security Hardening
**Researched:** 2026-05-22 01:20
**Source:** Google Deep Research via Chrome Automation

---

Security Hardening of Windows 11 Pro Firewall Configurations for Autonomous Agent Developer Workstations
Strategic [[ARCHITECTURE|Architecture]] and Operational Context

The deployment, management, and orchestration of autonomous Artificial Intelligence (AI) agent systems demand an exceptionally hardened operational environment, particularly at the workstation level where core development and local testing occur. In the context of the Keystone Sovereign architecture—a multifaceted autonomous system managing construction business operations, multimedia content distribution across YouTube channels, and an expansive health content empire—the developer workstation acts as the central nervous system. As of May 2026, securing these Windows 11 Pro developer nodes requires a rigorous orchestration of the Windows Defender Firewall with Advanced Security (WDFAS), Windows Subsystem for Linux (WSL) 2 networking, Docker containerization boundaries, and strict outbound traffic regulation.

The Keystone Sovereign system introduces unique security challenges. The construction management [[AGENTS|agents]] routinely pull and process proprietary architectural blueprints, bid data, and API-driven project timelines. The multimedia [[AGENTS|agents]] handle high-bandwidth rendering and uploading of YouTube videos, requiring stable, unimpeded connections to Google's ingestion servers. Concurrently, the health content empire relies on scraping and processing massive datasets, demanding strict adherence to data privacy principles adjacent to HIPAA compliance standards. Because the workstation continuously ingests external dependencies—ranging from Python packages via pip to Node.js modules via npm and Docker images from public repositories—a compromised dependency poses a systemic risk. Traditional network perimeter firewalls are entirely insufficient when threats manifest via compromised dependencies pulled directly into the host machine. Consequently, the host-based firewall must serve as the primary, highly granular defense mechanism against data exfiltration, lateral movement, and unauthorized internal API queries.

This report delivers an exhaustive technical analysis of the optimum firewall configuration strategies for such workstations. Moving significantly beyond default parameters, this analysis evaluates the implementation of a "Zero Trust" host-level paradigm, where inbound and outbound traffic are implicitly denied, and authorized communication channels are explicitly brokered through application-aware, port-specific, and IPsec-secured rules. The synthesis incorporates the latest compliance frameworks, notably the Center for Internet Security (CIS) Microsoft Windows 11 STIG Benchmark v1.1.0 and Enterprise Benchmark v5.0.1, reflecting the consensus-based best practices established up to April and May 2026.   

Foundational Firewall Mechanics and Policy Management
The Windows Filtering Platform (WFP) and Service Dependencies

The Windows Defender Firewall is fundamentally built upon the Windows Filtering Platform (WFP), a comprehensive set of API and system services that provide a robust platform for creating network filtering applications. WFP operates at multiple layers of the TCP/IP stack, allowing for deep packet inspection, connection tracking, and the enforcement of network policies before packets are passed to the application layer. This deep integration means that the firewall is not merely a peripheral application but an integral component of the Windows 11 operating system kernel and network stack.   

A critical operational directive for security hardening is that the Windows Firewall Service, identified by the service name MpsSvc, must never be stopped or disabled via the Services snap-in or through command-line service termination. Microsoft explicitly states that disabling this service places the operating system into an unsupported [[STATE|state]] that triggers catastrophic systemic failures across the Windows 11 OS environment. When MpsSvc is halted, modern Universal Windows Platform (UWP) applications fail to install or update, the Start menu frequently ceases to function, Windows activation mechanisms fail, and network protection mechanisms relying on IPsec and network fingerprinting are entirely nullified.   

Furthermore, non-Microsoft firewall software should programmatically disable only the specific rule types of Windows Firewall that require disabling for compatibility reasons, rather than attempting to shut down the service. If a specific operational requirement dictates that the firewall must logically permit all traffic—an anti-pattern for secure developer workstations but occasionally necessary during isolated debugging—the correct methodology is to disable the Windows Firewall Profiles (Domain, Private, and Public) while leaving the underlying MpsSvc service actively running.   

PowerShell Object-Oriented Management vs. Legacy Netsh

Historically, Windows firewall management was conducted utilizing the netsh.exe command-line utility. While netsh remains functional, modern management of Windows 11 Pro firewalls must be executed via the NetSecurity PowerShell module. The fundamental difference lies in data handling: netsh utilizes string-token based inputs, whereas PowerShell utilizes an object-oriented approach that provides significantly greater granularity and programmatic flexibility.   

In the PowerShell implementation, common conditions such as IP addresses or ports are not merely attributes of a rule; they are represented in separate objects called filters, such as NetFirewallAddressFilter, NetFirewallPortFilter, or NetFirewallApplicationFilter. This object-oriented structure allows administrators to query and pipe objects systematically. For example, a security engineer can filter all rules applying to a specific port and dynamically alter their remote address scope in a single pipeline execution.   

Additionally, PowerShell introduces the ability to manage rules on remote developer workstations via the -CimSession parameter, a capability that is not dynamically possible in netsh. For environments managing multiple workstations via Active Directory Group Policy Objects (GPOs), modifying rules one-by-one directly on the domain controller can overload the network. The PowerShell NetSecurity module introduces GPO caching through the Open-NetGPO and Save-NetGPO cmdlets. This allows an administrator to load a GPO session locally, apply all necessary rule creations or modifications to the cached object, and then commit the changes simultaneously, drastically reducing the load on the domain controller.   

Implementing CIS Benchmark Baselines

Establishing a secure foundation requires aligning the workstation with recognized cybersecurity standards. As of April 2026, the Center for Internet Security (CIS) published the Windows 11 STIG Benchmark v1.1.0 and the Windows 11 Enterprise Benchmark v5.0.1. These benchmarks represent a consensus-driven effort by global cybersecurity experts to define prescriptive configuration baselines.   

The CIS benchmarks are structured into two primary profiles:

Level 1 Profile: Recommends essential basic security requirements that can be configured on any system with minimal operational interruption or reduced functionality.   

Level 2 Profile: Recommends highly restrictive security settings designed for environments requiring greater security, which may result in reduced functionality and require significant tuning.   

For a developer workstation orchestrating an autonomous enterprise system like Keystone Sovereign, where a compromise could expose YouTube authentication tokens, proprietary health data, and construction financial bids, Level 2 configurations are mandatory. When deploying these baselines at scale, administrators often utilize Microsoft Endpoint Configuration Manager (MECM) to package the configuration baselines into categories such as Account, Firewall, Network, Services, and System.   

To validate and deploy these baselines, organizations rely on the Microsoft Security Compliance Toolkit (MSCT), which provides the Policy Analyzer and the Local Group Policy Object (LGPO.exe) tool. The Policy Analyzer allows administrators to compare their current GPOs against Microsoft or CIS-recommended baselines, highlighting redundant settings, conflicts, and inconsistencies. However, it is critical to note that following the April 2026 security updates, the Microsoft Policy Analyzer 4.0 experienced significant instability and application crashes, resulting in Just-In-Time (JIT) debugging errors across the community. Consequently, current best practices suggest utilizing the LGPO.exe tool directly for policy injection or relying on third-party comparison tools like SDM Software's Group Policy Reporting Pak until a stable patch for Policy Analyzer is released. Alternatively, automated scanning can be achieved using CIS-CAT Pro or the free CIS-CAT Lite v4 tool, which provides immediate compliance scoring against tailored CIS Benchmarks.   

A baseline configuration script leveraging PowerShell provides immediate enforcement of the core profiles without relying on unstable GUI utilities. The following command structure establishes the baseline posture by enforcing the firewall across all network profiles and explicitly defining default actions:

PowerShell
# Enable Windows Defender Firewall across all network profiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Establish the Zero-Trust Default Action Baseline
Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultInboundAction Block -DefaultOutboundAction Block 

# Configure Advanced Profile Behaviors to mitigate fingerprinting and noise
Set-NetFirewallProfile -Profile Domain,Public,Private -NotifyOnListen False -AllowUnicastResponseToMulticast False 

# Establish comprehensive WFP diagnostic logging required for Level 2 auditing
Set-NetFirewallProfile -Profile Domain,Public,Private -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" -LogBlocked True -LogAllowed False -LogMaxSize 20480


The configuration of DefaultOutboundAction Block is a severe deviation from the standard Windows deployment, which typically allows all outbound traffic by default. However, this configuration is fundamental to mitigating supply chain attacks, ensuring that if a developer accidentally executes a malicious script or pulls a poisoned Docker image, the malware cannot easily establish an outbound command-and-control (C2) connection.   

Navigating the "Block Outbound" Paradigm

Implementing an implicit deny rule for all outbound connections provides unparalleled security but introduces significant friction into standard developer workflows. Under this paradigm, every application, background service, OS updater, and dependency manager requires an explicitly defined allowlist rule to communicate with external servers. According to the internal evaluation logic of the Windows Defender Firewall, explicit block rules always take precedence over conflicting allow rules, and more specific rules take precedence over less specific ones, except when overridden by explicit blocks. Therefore, careful curation of the outbound allowlist is critical to prevent self-inflicted denial of service.   

Advanced AppID Tagging and Firewall Sentinel

Traditional firewall rules rely heavily on port numbers and IP addresses. However, modern cloud infrastructure relies on dynamic Content Delivery Networks (CDNs), making IP-based whitelisting highly volatile and prone to failure. To address this, organizations are increasingly leveraging App Control for Business (formerly Windows Defender Application Control, WDAC) integrated with the firewall.   

Emerging hardening frameworks, such as the open-source Harden-Windows-Security repository on GitHub (specifically the Firewall Sentinel module), utilize AppID tagging in policies to create [[Brand_Constitution/protocol/IDENTITY|identity]]-based allowlisting. Firewall Sentinel offers three distinct profiles to manage a default-block outbound environment efficiently:   

Default Windows: Restricts internet access exclusively to programs, services, and applications native to the Windows OS.   

Allow Microsoft: Expands the default profile to permit network connectivity for any application cryptographically signed with a valid Microsoft code-signing certificate.   

Signed and Reputable: Further extends connectivity by authorizing applications verified by the Intelligent Security Graph cloud verdicts as reputable and signed.   

By leveraging Group Policy to enforce Block Rule Merging (preventing local users from circumventing policies) and defining the default outbound action as Block across all profiles, administrators can ensure that only cryptographically verified binaries communicate externally.   

Managing Developer Package Managers (Pip, NPM, Git)

For a workstation orchestrating AI [[AGENTS|agents]], Python and Node.js are foundational technologies. The Keystone Sovereign system relies on constant ingestion of external libraries for data scraping and local LLM fine-tuning. When the firewall is configured to block outbound traffic, essential developer tools like pip, npm, and git will fail to resolve connections.   

Because Windows Firewall operates strictly at the Network and Transport layers (IP and Port) and does not natively support Layer 7 (Application) URL filtering or deep packet inspection of HTTP host headers, administrators cannot simply create a rule allowing traffic to URLs like pypi.org or npmjs.com. Attempting to whitelist the IP addresses associated with these domains is futile, as they constantly shift behind load balancers.   

The most stable and secure approach is to restrict communication by the application binary executable path combined with required cryptographic protocols (specifically restricting traffic to TCP Port 443 for HTTPS). While some automated solutions exist, such as the WindowsFirewallRuleset by Metablaster or the Block-OutboundFW module, which attempt to recursively find executables in a directory and generate rules automatically, these can inadvertently create overly permissive environments. Manual, explicitly defined binary paths represent the required standard for an autonomous systems environment.   

The following PowerShell commands demonstrate how to construct granular outbound rules for developer package managers:

PowerShell
# Allow Python outbound for pip operations exclusively over HTTPS
New-NetFirewallRule -DisplayName "Dev: Python PIP Outbound HTTPS" -Direction Outbound -Program "C:\Python312\python.exe" -Protocol TCP -RemotePort 443 -Action Allow

# Allow Node.js outbound for NPM package fetching over HTTPS
New-NetFirewallRule -DisplayName "Dev: Node NPM Outbound HTTPS" -Direction Outbound -Program "C:\Program Files\nodejs\node.exe" -Protocol TCP -RemotePort 443 -Action Allow

# Allow Git operations over HTTPS and explicitly over SSH (Port 22)
New-NetFirewallRule -DisplayName "Dev: Git Outbound HTTPS" -Direction Outbound -Program "C:\Program Files\Git\cmd\git.exe" -Protocol TCP -RemotePort 443 -Action Allow
New-NetFirewallRule -DisplayName "Dev: Git Outbound SSH" -Direction Outbound -Program "C:\Program Files\Git\usr\bin\ssh.exe" -Protocol TCP -RemotePort 22 -Action Allow


By ensuring that pip and npm can only communicate over port 443, the firewall prevents these tools from being exploited to exfiltrate data over unencrypted HTTP (port 80) or alternate protocols.

Hardening Windows Subsystem for Linux (WSL) 2

The integration of Linux environments directly into Windows is vital for the Keystone Sovereign architecture, providing native compatibility for Linux-first AI tooling and build chains. Historically, WSL 2 operated behind a Network Address Translation (NAT) layer managed by the Hyper-V Virtual Switch. This legacy NAT architecture resulted in a dynamic internal IP address being assigned to the Linux subsystem upon every reboot. Furthermore, it prevented external devices on the Local Area Network (LAN) from directly addressing the WSL instance, complicating the testing of microservices.   

As of Windows 11 version 22H2, and heavily refined in subsequent updates through 2026, Microsoft introduced Mirrored Networking for WSL 2. Mirrored networking fundamentally alters the architecture, allowing WSL to share the exact network configuration, interfaces, and IP address range as the Windows host. This enables bidirectional localhost communication, IPv6 support inside WSL distributions, and direct LAN access to Linux-hosted services, effectively making WSL behave like a device natively existing on the physical LAN.   

The .wslconfig Architecture

To enable mirrored networking and its associated advanced security features, administrators must configure the .wslconfig file globally. This file does not exist by default and must be manually created in the user's root profile directory (%UserProfile%\.wslconfig). Changes to this file apply to all installed distributions running on WSL 2.   

A hardened .wslconfig for the developer workstation should include the following [[DIRECTIVES|directives]]:

Ini, TOML
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
firewall=true


The dnsTunneling=true parameter changes how DNS requests are proxied from WSL to Windows, utilizing a virtualization feature to answer DNS requests instead of routing them over standard networking packets, thereby greatly improving compatibility with corporate VPNs. The autoProxy=true setting enforces WSL to seamlessly inherit the Windows HTTP proxy information.   

However, the most critical security enhancement is firewall=true, a feature that became highly stable and active by default on machines running Windows 11 22H2 with WSL 2.0.9 and higher. Prior to this setting, traffic generated inside WSL largely bypassed the Windows host firewall's application-level restrictions. By setting firewall=true, Windows explicitly enforces its firewall rules—including specific Hyper-V traffic filters—onto the WSL network traffic. Ensure that wsl --shutdown is executed via PowerShell after modifying the configuration to guarantee the WSL engine fully terminates and reinitializes with the new parameters.   

Implementing Hyper-V Firewall Rules

When firewall=true is enabled, the standard NetFirewallRule cmdlets do not natively catch all inter-VM traffic originating from or destined for the WSL instance. Administrators must specifically utilize the NetFirewallHyperVRule suite of cmdlets to broker traffic for the virtual machine.   

The Hyper-V firewall rules require a strict identifier known as a VMCreatorId to scope the rule to the correct virtual machine. For all WSL 2 instances, this GUID is universally standardized as {40E0AC32-46A5-438A-A0B2-2B479E8F2E90}.   

For example, if the developer workstation is utilizing a local web server compiled inside WSL 2 to render the front-end dashboard for the construction management agent, an explicit Hyper-V inbound rule must be created. Conversely, outbound traffic from the WSL environment must be scrutinized to prevent lateral movement by potentially compromised containers.

PowerShell
# Allow inbound TCP Port 8080 from the LAN to the WSL 2 Dashboard
New-NetFirewallHyperVRule -Name "WSL2-Inbound-8080" -DisplayName "Allow Inbound to WSL2 Dashboard" -Direction Inbound -VMCreatorId '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -Protocol TCP -LocalPorts 8080 -Action Allow

# Block outbound SSH (Port 22) from within WSL 2 to prevent lateral movement
New-NetFirewallHyperVRule -Name "WSL2-Block-Outbound-SSH" -DisplayName "Block WSL Outbound SSH" -Direction Outbound -VMCreatorId '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -Protocol TCP -RemotePorts 22 -Action Block


The interaction between local user-defined Hyper-V rules and Enterprise policies (applied via Group Policy or Intune CSP) can be managed using the Set-NetFirewallHyperVVMSetting cmdlet. The AllowLocalFirewallRules property determines whether locally defined Hyper-V rules are processed alongside enterprise rules. Setting this to False ensures that developers cannot manually override centrally deployed security boundaries.   

Management Cmdlet	Primary Function and Capabilities	Key Parameter Targets
New-NetFirewallHyperVRule	

Generates explicitly scoped inbound/outbound rules exclusively for Hyper-V or WSL containers, segregating host traffic from VM traffic. 

	

-VMCreatorId, -Protocol, -LocalPorts, -Action 


Get-NetFirewallHyperVRule	

Audits and retrieves properties of existing VM-specific rules for compliance validation. 

	

-Direction, -EnforcementStatus, -Enabled 


Set-NetFirewallHyperVVMSetting	

Configures global firewall enforcement states, active profiles, and default actions for specific VM Creators. 

	

-DefaultInboundAction, -Enabled, -AllowLocalFirewallRules 

  
Containerization Security: Docker Desktop and vpnkit

Docker Desktop on Windows introduces significant firewall complexity, distinct from both native application management and WSL 2 configurations. Unlike native Linux installations where the iptables utility natively intercepts and manages port forwarding at the kernel level, Docker Desktop operates a lightweight Linux utility VM. To bypass traditional enterprise VPN and Hyper-V NAT routing issues, Docker Desktop forwards all network traffic at the user level via a sophisticated TCP/IP stack written in OCaml, known as vpnkit.   

When a container publishes a port (for instance, utilizing -p 80:80 in a docker run command), it is not a virtual network adapter that listens. Instead, the com.docker.backend.exe process running directly on the Windows host binds to that specified port. Consequently, the Windows Defender Firewall does not see traffic directed at an abstract "container" or a "virtual IP address"; from the perspective of the WFP, it sees inbound network traffic directed at the local com.docker.backend.exe executable.   

Resolving Port Exposure Failures

A frequent and highly disruptive issue for developers is the inability to access containerized services from the LAN, even when the port is explicitly published and an inbound port rule is seemingly created in the Windows firewall. This failure [[STATE|state]] occurs because the Windows Firewall associates the listening port strictly with the Docker executable application path, and default block rules (or conflicts between network profiles such as Public versus Private) supersede the simple port-based allow rule.   

Furthermore, Docker Desktop utilizes wsl-vpnkit to generate an additional network interface for WSL 2 guests named wsltap, reconfiguring their default routing behavior and launching the wsl-gvproxy.exe process to receive and forward networking traffic. This complex routing means that standard IP-based firewalling is often circumvented internally but blocked externally.   

To ensure that autonomous [[AGENTS|agents]] running in Docker containers—such as scalable video rendering nodes for the YouTube channels or independent database instances for the health content empire—are accessible to other authorized devices on the internal network, inbound rules must be established that explicitly permit the Docker backend processes rather than just the abstract port number.   

PowerShell
# Allow inbound connections to Docker containers exposed via the backend process
New-NetFirewallRule -DisplayName "Docker Backend Inbound" -Direction Inbound -Program "C:\Program Files\Docker\Docker\resources\com.docker.backend.exe" -Action Allow -Profile Private,Domain

# Required when DefaultOutboundAction is Block to allow containers to pull images
New-NetFirewallRule -DisplayName "Docker Backend Outbound" -Direction Outbound -Program "C:\Program Files\Docker\Docker\resources\com.docker.backend.exe" -Action Allow

# Allow vpnkit to successfully proxy connections for internal DNS and routing
New-NetFirewallRule -DisplayName "Docker VPNKit Outbound" -Direction Outbound -Program "C:\Program Files\Docker\Docker\resources\vpnkit.exe" -Action Allow


It is a strict security best practice to bind these rules exclusively to the Private and Domain firewall profiles. If the workstation is ever connected to a Public network profile, these rules will not apply, preventing the exposure of developmental containers to untrusted networks. If developers experience issues pulling container images while behind an enterprise proxy, ensure that proxy authentication settings are configured, as vpnkit can log HTTP 407 Proxy Authentication Required errors if traffic is blocked before reaching the Docker Hub.   

Local AI Orchestration: Securing Ollama

The Keystone Sovereign system integrates local Large Language Models (LLMs) to parse dense construction blueprints, autonomously draft health articles, and summarize large datasets without relying on external, cloud-based APIs. This localized execution ensures complete data privacy and eliminates latency. The industry standard tool for hosting and serving these models locally on developer workstations is Ollama.

By default, the Ollama service binds strictly to the loopback interface (127.0.0.1) on TCP port 11434. This is a highly secure default posture that prevents any external network access. However, in an orchestrated multi-agent environment, secondary devices (e.g., an iPad used by project managers on a construction site, or a secondary rendering PC on the local network) may need to execute API queries against the central workstation's locally hosted LLM.   

To facilitate this architecture safely, two specific configuration changes are mandatory. First, the Ollama service must be reconfigured to listen on all available network interfaces rather than just the loopback. This is achieved by setting the system environment variable OLLAMA_HOST to 0.0.0.0:11434. Second, the Windows Firewall must be modified to accept inbound API queries explicitly on this port.   

Some documentation suggests utilizing netsh interface portproxy add v4tov4 to map an external interface port to the internal localhost port. While effective, port proxying introduces additional routing complexity and can obscure the origin IP of the requesting client, hindering detailed auditing. The preferred method is direct binding coupled with a highly restrictive Windows Firewall rule.   

PowerShell
# 1. Set the system environment variable for Ollama global binding
::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434',::Machine)

# 2. Restart the Ollama service to apply the new binding configuration
Restart-Service -Name "Ollama" -ErrorAction SilentlyContinue

# 3. Create a restrictive inbound firewall rule scoped explicitly to the internal subnet
New-NetFirewallRule -DisplayName "Inbound - Ollama Local LLM API" -Direction Inbound -Protocol TCP -LocalPort 11434 -RemoteAddress "192.168.10.0/24" -Action Allow -Profile Private,Domain


Supplying a strict -RemoteAddress parameter (such as 192.168.10.0/24, representing the trusted internal LAN subnet) rather than allowing Any remote address is critical. This ensures that even if the network profile is incorrectly categorized, arbitrary devices on a larger corporate network cannot execute API calls and consume expensive, finite GPU compute resources assigned to the LLM. Developers can validate connectivity internally using PowerShell's Test-NetConnection <IP> -Port 11434 or by writing simple C# or Python test scripts.   

Advanced Isolation: IPsec and Connection Security Rules

For the highest tier of security—particularly when the developer workstation is handling proprietary construction bids or sensitive, regulated health data—standard port and IP-based filtering is insufficient against advanced persistent threats (APTs) or insider threats operating within the LAN. Windows Defender Firewall integrates natively with Internet Protocol Security (IPsec) through Connection Security Rules (CSR).   

IPsec allows the firewall to demand cryptographic authentication before processing standard firewall allow rules. This architectural concept creates "Domain Isolation" or "Server Isolation" enclaves. By leveraging CSR, traffic must be authenticated, integrity-checked, and optionally encrypted via IPsec. If IPsec fails to authorize the connection, no traffic is allowed to pass to the application.   

For example, if the developer workstation hosts a sensitive staging database that should only be accessible by explicitly authorized administrative servers (e.g., the Keystone Sovereign primary database cluster), an IPsec rule can be configured to drop all traffic that lacks mathematical proof of [[Brand_Constitution/protocol/IDENTITY|identity]] via Kerberos or pre-shared keys (PSK). Recent updates to the Windows Server 2025 security baseline (version 2602), which parallel Windows 11 enterprise guidelines, emphasize cryptographic agility and the prevention of deprecated hashing algorithms like SHA-1 for certificate and Kerberos authentications.   

The following PowerShell implementation demonstrates the creation of an IPsec-secured pathway, requiring Kerberos authentication:

PowerShell
# 1. Create a Kerberos Authentication Proposal
$kerbProp = New-NetIPsecAuthProposal -Machine -Kerberos

# 2. Create the Phase 1 Authentication Set utilizing the Kerberos proposal
$phase1AuthSet = New-NetIPsecPhase1AuthSet -DisplayName "Keystone Kerberos Auth Phase 1" -Proposal $kerbProp

# 3. Create the IPsec Connection Security Rule requiring inbound and outbound authentication
New-NetIPsecRule -DisplayName "Require IPsec Auth for Secure Subnet" -InboundSecurity Require -OutboundSecurity Require -Phase1AuthSet $phase1AuthSet.Name -Endpoint1 "Any" -Endpoint2 "192.168.10.50"


Following the successful establishment of the IPsec tunnel (Main Mode and Quick Mode Security Associations, observable via Get-NetIPsecMainModeSA or netsh advfirewall monitor show mmsa all), an explicit firewall rule can be created that leverages the -Authentication Required and -Encryption Required parameters. If a rogue device attempts to connect to the port without successfully negotiating the underlying IPsec SA, the WFP silently drops the packet before it ever reaches the application layer.   

Auditing, Telemetry, and Continuous Validation

A firewall operating in a strictly hardened "Block Default" configuration will inevitably drop legitimate traffic during the initial operational tuning phase. [[Troubleshooting|Troubleshooting]] in this environment requires robust logging and auditing mechanisms. The standard Windows Firewall log (pfirewall.log) is useful for basic IP and Port correlations but often lacks the deep contextual metadata necessary for forensic analysis or advanced troubleshooting.   

Advanced Audit Policy Configuration

To achieve comprehensive visibility into network flows, administrators must explicitly enable the Windows Filtering Platform audit policies. This is executed via the auditpol.exe command-line utility or through Advanced Audit Policy Configuration in Group Policy. These policies write rich network event data directly into the Windows Security Event Log, which can then be forwarded to SIEM solutions (like Microsoft Sentinel) or queried rapidly via PowerShell for immediate triage.   

DOS
:: Enable Success and Failure logging for WFP Packet Drops (Generates Event ID 5152)
auditpol /set /subcategory:"Filtering Platform Packet Drop" /success:enable /failure:enable

:: Enable Success and Failure logging for WFP Connections (Generates Event ID 5157)
auditpol /set /subcategory:"Filtering Platform Connection" /success:enable /failure:enable


Once these subcategories are enabled, Event ID 5152 represents a definitively dropped packet, and 5157 represents a blocked connection attempt. Crucially, these events include precise details regarding the Source IP, Destination IP, Port, Protocol, and most importantly, the exact Process ID (PID) and Application Path that requested the connection. This application context allows administrators to rapidly identify which obscure developer tool or background service is being hindered by the default outbound deny rule. Furthermore, this auditing ties into broader application whitelisting strategies like AppLocker or WDAC, which log execution attempts under Event IDs 8003 and 8004, providing a holistic view of process behavior and network intent.   

When diagnosing network drops, the diagnostic workflow must follow a strict procedural logic. First, engineers must check the Security log for Event 5157 to confirm the block and identify the source application path. If the source is identified as Docker's com.docker.backend.exe or vpnkit.exe, rules must be applied directly to those host executables rather than the container's mapped ports. Conversely, if the traffic originates from the WSL 2 environment, engineers must evaluate and apply New-NetFirewallHyperVRule cmdlets utilizing the specific WSL VMCreatorId.

Automating Rule Discovery via Event Logs

When a new autonomous agent container is deployed or a developer runs a new npm install command that fails to resolve, the following PowerShell function can be executed locally to parse the Security Log. This script isolates recent outbound connection failures and provides actionable intelligence for writing the requisite New-NetFirewallRule:

PowerShell
# Query the last 50 blocked WFP connection events for rapid triage
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=5157} -MaxEvents 50 | Select-Object TimeCreated, 
    @{Name="Process"; Expression={$_.Properties.Value}},
    @{Name="DestIP"; Expression={$_.Properties.Value}},
    @{Name="DestPort"; Expression={$_.Properties.Value}},
    @{Name="Protocol"; Expression={$_.Properties.Value}} | Format-Table -AutoSize

Continuous Compliance Validation via InSpec

A secure [[STATE|state]] degrades over time. As developers request temporary port exceptions or application whitelists to test new features for the Keystone Sovereign system, these temporary rules often drift into permanent vulnerabilities. Continuous validation against established baselines is an absolute necessity.

Tools such as the dev-sec/windows-baseline InSpec profile (an open-source project maintained on GitHub by the DevSec Hardening Framework Team and Chef compliance teams) allow security administrators to run automated, code-driven compliance scans against the workstation. InSpec utilizes Ruby-based definitions to evaluate the live [[STATE|state]] of the registry, services, and Windows Firewall against frameworks inspired by the CIS Benchmarks.   

By executing the baseline profile locally or over WinRM, the system actively audits whether the required parameters—such as the explicit denial of inbound connections, the enforcement of AppID policies, and the correct log sizing limits—remain intact and untampered:

Bash
# Execute the dev-sec Windows security baseline directly against the local workstation
inspec exec https://github.com/dev-sec/windows-baseline


This automated auditing bridges the critical gap between static policy application (via GPO or PowerShell injection) and dynamic configuration drift over the lifecycle of the workstation. By combining the declarative enforcement capabilities of the NetSecurity PowerShell module with the continuous validation of InSpec and the deep telemetry of WFP auditing, organizations can ensure the developer workstation remains a hardened, resilient asset within the Keystone Sovereign autonomous architecture.   

---
*Auto-ingested into Keystone Brain Vector DB*


---
📁 **See also:** [[Research_Archives/11_Security/INDEX|← Directory Index]]

**Related:** [[20260522_security_hardening_antivirus_recommendations_that_don't_interfere_with_developm]] · [[20260522_security_hardening_vpn_setup_for_accessing_geo-restricted_ai_services]] · [[20260522_security_hardening_github_secret_scanning_and_credential_leak_prevention]]
