---
name: scalance-skill
description: Helps with a specific scalance related troubleshooting and configuration tasks
---

# SCALANCE SC646-2C Troubleshooting & Configuration Skill

## Overview
This skill provides comprehensive CLI commands and best practices for troubleshooting and configuring Siemens SCALANCE SC646-2C industrial security appliances using SSH access. This skill is optimized for use with Antigravity automation and manual troubleshooting workflows.

## Device Information
- **Product Line**: SCALANCE SC-600 Series
- **Specific Model**: SC646-2C (also applicable to SC622-2C, SC626-2C, SC632-2C, SC636-2C, SC642-2C)
- **Access Method**: SSH CLI (Command Line Interface)
- **Firmware Version**: V3.1+
- **IP**: 192.168.20.12
- **Username**: admin
- **Password**: Sidel123!

## Handling Scalance CLI Pagination

The only way to deal with the pagination is the space flood fallback

The terminal type or shell does not support the standard commands like :

```bash
terminal length 0
OR

no cli paging
```

Send the command (e.g., show running-config).
Immediately send a long string of space characters or newlines to the input buffer. This simulates pressing the Spacebar repeatedly to advance the --More-- prompt.

## Essential CLI Commands for Troubleshooting

### 1. System Status & Information

#### Device Identification
```bash
# Show complete device information
show device information

# Show hardware details
show hardware

# Show firmware versions
show versions

# Show coordinates (location/naming)
show coordinates
```

#### System Health
```bash
# Show digital input status (physical inputs)
show digital input

# Show digital output status
show digital output

# Show digital input messages/events
show digital input messages

# Show system time
show time

# Show session timeout settings
show web-session-timeout
show cli-console-timeout
```

### 2. Network Interface Status

#### Basic Interface Commands (Already Used)
```bash
# Show all interfaces status and configuration
show interfaces

# Show specific interface with details
show interfaces gigabitethernet <1-6>

# Show interface descriptions
show interfaces description

# Show flow control status
show interfaces flowcontrol

# Show storm control settings
show interfaces stormcontrol

# Show port status summary
show interfaces status

# Show interface statistics/counters
show interfaces counters

# Show specific interface counters
show interfaces gigabitethernet <1-6> counters

# Clear interface counters (for baseline testing)
clear counters
```

#### IP Configuration
```bash
# Show IP interface configuration
show ip interface

# Show IP interface for specific VLAN
show ip interface vlan <vlan-id>

# Show IPv6 interface configuration
show ipv6 interface

# Show IPv6 neighbors (ND table)
show ipv6 neighbors

# Show IPv6 traffic statistics
show ipv6 traffic
```

### 3. VLAN Configuration (Already Used)

```bash
# Show VLAN summary
show vlan

# Show VLAN brief overview
show vlan brief

# Show specific VLAN(s)
show vlan id <vlan-range>

# Show VLAN summary statistics
show vlan summary

# Show VLAN device information
show vlan device info

# Show VLAN learning parameters
show vlan learning params

# Show VLAN port configuration
show vlan port config

# Show VLAN protocol groups
show vlan protocols-group
```

### 4. Routing Information (Already Used + Extended)

```bash
# Show IP routing table
show ip route

# Show IP routing configuration
show ip routing

# Show static routes only
show ip static route

# Show default gateway
show ip gateway

# Show IPv6 routing table
show ipv6 route

# Show IPv6 routing summary
show ipv6 route summary

# Show IPv6 static routes
show ipv6 static route

# Show IPv6 PMTU (Path MTU Discovery)
show ipv6 pmtu
```

#### OSPF Routing (if enabled)
```bash
# Show OSPF configuration
show ip ospf

# Show OSPF routing table
show ip ospf route

# Show OSPF database summary
show ip ospf database summary

# Show OSPF database details
show ip ospf database

# Show OSPF border routers
show ip ospf border-routers

# Show OSPF interface status
show ip ospf interface

# Show OSPF neighbors
show ip ospf neighbor

# Show OSPF virtual links
show ip ospf virtual-links

# Show OSPF area range
show ip ospf area-range
```

### 5. ARP and MAC Address Tables

```bash
# Show ARP table
show ip arp

# Show MAC address table aging time
show mac-address-table aging-time

# Show MAC address table aging status
show mac-address-table aging-status
```

### 6. Running Configuration (Already Used)

```bash
# Show complete running configuration
show running-config

# Show startup configuration
show startup-config

# Show configuration backup
show configbackup

# Save configuration to startup
write startup-config

# Write memory (alternative)
write memory
```

### 7. DNS and DHCP

```bash
# Show DNS configuration
show ip dns

# Show DHCP client status
show ip dhcp client

# Show DHCP server bindings (if DHCP server enabled)
show ip dhcp-server bindings

# Show DHCP server pools
show ip dhcp-server pools
```

### 8. Security & VPN (IPSec)

#### IPSec VPN Status
```bash
# Show IPSec connection authentication
show ipsec conn-authentication

# Show all IPSec connections
show ipsec connections

# Show IPSec Phase 1 status
show ipsec conn-phase1

# Show IPSec Phase 2 status
show ipsec conn-phase2

# Show IPSec general information
show ipsec information

# Show IPSec remote endpoints
show ipsec remoteend
```

#### Access Control
```bash
# Show HTTP server status
show ip http server status

# Show HTTPS server status
show ip http secure server status

# Show SSH configuration
show ip ssh

# Show active VTY (virtual terminal) sessions
show line vty

# Clear/disconnect VTY line
clear line vty <line-number>
```

### 9. Logging and Events

```bash
# Show logbook (system logs)
show logbook

# Show event configuration
show events config

# Show event severity settings
show events severity

# Show event faults configuration
show events faults config

# Show event faults for power
show events faults config power

# Show event faults for links
show events faults config link
```

### 10. LLDP (Link Layer Discovery Protocol)

```bash
# Show LLDP neighbors
show lldp neighbors

# Show LLDP status
show lldp status
```

### 11. Port Channel / Link Aggregation

```bash
# Show port channel configuration
show interfaces port-channel <1-8>

# Show port channel counters
show interfaces port-channel <1-8> counters
```

### 12. Load/Save Configuration Management

```bash
# Show load/save files available
show loadsave files

# Show minimum config file version required
show loadsave minimum config-file version

# Show TFTP load/save configuration
show loadsave tftp

# Show secure TFTP configuration
show loadsave stftp
```

### 13. Industrial Automation Specific

#### SINEMA Remote Connect (SRC)
```bash
# Show SINEMA configuration
show sinema

# Show SINEMA RC configuration
show sinemarc

# Show SRS (SINEMA Remote Service) configuration
show srs

# Show SRS logon status
show srs logon
```

#### Device Access Service (DAS)
```bash
# Show DAS information
show das info
```

#### Plug Configuration (C-PLUG)
```bash
# Show C-PLUG configuration
show plug
```

#### Industrial Management (IM)
```bash
# Show IM configuration
show im
```

---

## Troubleshooting Workflow

### Initial Connection Issues
1. `show interfaces` - Verify physical link status
2. `show ip interface` - Check IP configuration
3. `show ip route` - Verify routing table
4. `show ip gateway` - Confirm default gateway
5. `show ip arp` - Check ARP resolution

### VLAN Problems
1. `show vlan` - Verify VLAN configuration
2. `show vlan port config` - Check port VLAN assignments
3. `show interfaces gigabitethernet <id>` - Verify port configuration
4. `show vlan device info` - Check VLAN device information

### VPN Connectivity Issues
1. `show ipsec connections` - Check VPN tunnel status
2. `show ipsec conn-phase1` - Verify Phase 1 negotiation
3. `show ipsec conn-phase2` - Verify Phase 2 negotiation
4. `show ipsec information` - Check overall IPSec status
5. `show ip route` - Verify VPN routing
6. `show logbook` - Check for IPSec errors

### Routing Problems
1. `show ip routing` - Verify routing is enabled
2. `show ip route` - Check routing table entries
3. `show ip static route` - Verify static routes
4. `show ip ospf neighbor` (if OSPF) - Check neighbor adjacencies
5. `show ip ospf route` (if OSPF) - Check OSPF routing table

### Performance Issues
1. `show interfaces counters` - Check for errors/discards
2. `show interfaces stormcontrol` - Verify storm control settings
3. `show logbook` - Check for system events
4. `clear counters` - Reset counters for baseline
5. Wait and re-check: `show interfaces counters`

### Configuration Verification
1. `show running-config` - Current active configuration
2. `show startup-config` - Boot configuration
3. `show configbackup` - Check backup configuration
4. `show versions` - Verify firmware version

---

## Navigation Commands

### Mode Changes
```bash
# Enter privileged EXEC mode
enable

# Exit privileged EXEC mode
disable

# Enter global configuration mode
configure terminal

# Exit configuration mode
exit

# Exit to privileged EXEC mode from any config mode
end
```

### Help and Completion
```bash
# Show available commands
?

# Show command parameters
<command> ?

# Command completion
<partial-command><TAB>
```

---

## Best Practices for Antigravity Automation

### 1. Command Sequencing
For comprehensive status check, execute in this order:
```bash
show device information
show interfaces status
show ip interface
show vlan brief
show ip route
show ip arp
show ipsec connections
show logbook
```

### 2. Baseline Collection
Before troubleshooting, capture baseline:
```bash
show running-config
show interfaces counters
show ip arp
show vlan
```

### 3. Error Identification
For error diagnosis:
```bash
show interfaces counters          # Look for: errors, discards, runts, giants
show logbook                      # Check recent events
show events faults config         # Review fault configuration
show ipsec conn-phase1            # VPN Phase 1 errors
show ipsec conn-phase2            # VPN Phase 2 errors
```

### 4. Filtering and Output
- Use specific parameters to reduce output
- Example: `show interfaces gigabitethernet 1` instead of `show interfaces`
- Capture output to files for later analysis

### 5. Configuration Changes
Always save after modifications:
```bash
configure terminal
# ... make changes ...
end
write startup-config
```

### 6. Safe Testing
Before making changes:
```bash
show running-config               # Save current config
# Make test changes
# Test functionality
# If successful: write startup-config
# If failed: reload (loses unsaved changes)
```

---

## Common Issues and Commands

| Issue | Diagnostic Commands |
|-------|-------------------|
| No connectivity | `show interfaces`, `show ip interface`, `show ip route`, `show ip arp` |
| VLAN misconfiguration | `show vlan`, `show vlan port config`, `show interfaces status` |
| VPN tunnel down | `show ipsec connections`, `show ipsec conn-phase1`, `show ipsec conn-phase2`, `show logbook` |
| Routing problems | `show ip route`, `show ip routing`, `show ip gateway`, `show ip ospf neighbor` |
| High errors on interface | `show interfaces counters`, `show interfaces gigabitethernet <id> counters` |
| Configuration loss | `show startup-config`, `show configbackup`, `show loadsave files` |
| Time synchronization | `show time`, configure NTP/SNTP servers |
| Access issues | `show ip ssh`, `show ip http server status`, `show line vty` |

---

## Security Considerations

1. **Always use SSH** for secure access (not Telnet)
2. **Verify session timeouts**: `show cli-console-timeout`, `show web-session-timeout`
3. **Review access logs**: `show logbook`
4. **Check active sessions**: `show line vty`
5. **Monitor failed login attempts**: Check events in logbook
6. **IPSec authentication**: `show ipsec conn-authentication`

---

## Quick Reference: Port Numbering

SCALANCE SC646-2C typically has:
- **6 Gigabit Ethernet ports**: gigabitethernet 1-6
- **2 Combo ports** (SFP/RJ45): Usually ports 5-6
- **Management port**: Separate management interface

Always verify exact port configuration with: `show interfaces`

---

## Output Interpretation Tips

### Interface Status
- **Up/Up**: Interface operational
- **Up/Down**: Physical link up, protocol down (L2/L3 issue)
- **Down/Down**: No physical link
- **Admin Down**: Interface manually disabled

### Counter Monitoring
- **Input/Output Errors**: Physical layer issues, cable problems
- **CRC Errors**: Physical/cable issues, duplex mismatch
- **Runts/Giants**: Packet size issues
- **Discards**: Buffer overflow, QoS dropping

### IPSec Connection States
- **Connected**: VPN tunnel operational
- **Connecting**: Tunnel negotiation in progress
- **Down**: Tunnel not established - check Phase 1/2 status

---

## Configuration Backup Strategy

Regular backup workflow:
```bash
# Create configuration backup
configbackup create

# Verify backup
show configbackup

# Save to TFTP server (if configured)
save filetype config

# Show TFTP configuration
show loadsave tftp
```

---

## Notes for Field Service Engineers

1. **Pre-site visit**: Review previous configurations if available
2. **On-site**: Use `show running-config` to understand current state
3. **Documentation**: Capture all `show` outputs for analysis
4. **Changes**: Always `write startup-config` after verified changes
5. **Rollback**: Keep previous config backup before major changes
6. **Communication**: Note configuration in service report

---

## Antigravity Integration Points

When using Antigravity for automated troubleshooting:

1. **Initial Discovery**: Use `show device information`, `show hardware`, `show interfaces status`
2. **Health Check**: Run `show interfaces counters`, `show logbook`, `show ipsec connections`
3. **Configuration Audit**: Execute `show running-config`, `show vlan`, `show ip route`
4. **Change Validation**: Compare before/after outputs of relevant `show` commands
5. **Documentation**: Export all outputs for historical records

---

## Additional Resources

- **Full CLI Reference**: SCALANCE SC-600 CLI V3.1 Configuration Manual (C79000-G8976-C476-06)
- **Context-sensitive help**: Use `?` after any command for options
- **Tab completion**: Use TAB key for command and parameter completion

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-02-02 | Initial comprehensive skill document for SC646-2C troubleshooting |

---

**End of SCALANCE SC646-2C Skill Document**
