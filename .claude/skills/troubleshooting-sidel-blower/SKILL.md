---
name: troubleshooting-sidel-blower
description: Diagnoses faults on Sidel Matrix Blower machines (4-CPU B&R architecture). Reverse-engineers Structured Text and I/O mappings, then validates live via PVI/ANSL if connected to the machine network. Use when user mentions blower alarm, Matrix blower fault, preform ejection, stretch rod issue, oven heating, blowing pressure, transfer arm, LinMot diagnostic, B&R PLC troubleshooting, blowing curve analysis, or Sidel machine behavior.
---

# Sidel Matrix Blower — Diagnostic v4

Analyze faults on Sidel Matrix Blower machines by combining static code analysis with live PLC data via the MCP Sidel tools.

## Diagnostic workflow

```
Diagnosis Progress:
- [ ] Step 1: Identify the alarm (number, text, or photo)
- [ ] Step 2: Locate trigger logic in XX_ALARMS programs
- [ ] Step 3: Reverse-engineer variables to their physical source
- [ ] Step 4: Confirm hardware mapping via IoMap.iom
- [ ] Step 5: (IF ONLINE) Read live values to validate hypothesis
- [ ] Step 6: (IF ONLINE) Monitor suspect signals for anomalies
- [ ] Step 7: Propose root cause and corrective action
```

## Step 1: Identify the alarm

Determine the alarm number and module. Sources:
- User gives a number directly (e.g., "alarme 129 TRSF")
- User gives a photo of the HMI alarm screen — read the alarm numbers from the image
- User describes a symptom — search by text

**If MCP Sidel is available**, use `search_alarm` to get the full alarm definition including PLC variable, action type, OMAC classification, EIT code, and repair time.

## Step 2: Locate trigger logic

Find the exact `IF` condition that raises the alarm in the project code.

**Where to search:**
```
Logical/MODULE/11_TRANSFERT/11_ALARMS/   (TRSF alarms)
Logical/MODULE/12_WHEEL/12_ALARMS/       (WHEEL alarms)
Logical/MODULE/13_OVEN/13_ALARMS/        (OVEN alarms)
```

**How to search:**
```bash
# By alarm variable from Step 1
grep -rn "VAR_EventTRSF\[129\]" Logical/MODULE/11_TRANSFERT/11_ALARMS/

# By fault variable name
grep -rn "VAR_PreformArmFault" Logical/MODULE/11_TRANSFERT/
```

**Alarm function call patterns:**
```
AlarmCritical(Number:=129, Word:=VAR_WordAlarmCriTrsf);
AlarmAlert(Number:=120, Word:=VAR_WordAlarmAlertOven);
```

For station-specific alarms, number uses offset: `Number:=b+240` where b = station number.

## Step 3: Reverse-engineer variables

Trace backward from the alarm condition to the physical source.

For each variable encountered:
1. **Check declaration** in `.var` file — read type and comment
2. **Find assignments** (`:=`) in `.st` files
3. **If Digital Input (DI_)**: go to Step 4 for hardware mapping
4. **If Internal (VAR_)**: find what drives it — may involve timers, counters, SFC steps
5. **If Timer (.Q)**: find what drives IN and PT inputs

```bash
# Find declaration
grep -rn "DI_TransfPreformArmNotDetected" Logical/MODULE/**/*.var

# Find assignments
grep -rn "CNT_CtrlPrefArm" Logical/MODULE/11_TRANSFERT/**/*.st
```

**Build the causal chain:**
```
Physical sensor (card X20-DI-3402A1, Input 03)
  → DI_TransfPreformArmNotDetected
    → EDGEPOS resets CNT_CtrlPrefArm to 0
      → If 2 machine steps without reset → CNT_CtrlPrefArm > 1
        → VAR_PreformArmFault := TRUE → Alarm 129
```

## Step 4: Confirm hardware mapping

**This is critical. Do not skip.**

```bash
# Check IoMap for the variable
grep -rn "DI_TransfPreformArmNotDetected" Physical/TRSF/PLC1/IoMap.iom
```

Expected result: `DI_TransfPreformArmNotDetected AT %IX."X20-DI-3402A1".DigitalInput03;`

This confirms: card X20-DI-3402A1, channel DigitalInput03.

Cross-reference with Hardware.hw for module type:
```bash
grep -rn "X20-DI-3402A1" Physical/TRSF/Hardware.hw
```

## Step 5: Read live values (IF ONLINE)

**Before using PVI tools, check network connectivity:**
```
pvi_check_network()
```
The PC is NOT on the machine subnet (192.168.20.x). It connects through a GLI.Net router (192.168.20.160) via DHCP. If ping succeeds for a CPU, PVI can connect to it.

**If CPUs are reachable**, read ALL variables from the causal chain in one pass:
```
pvi_read_multiple("TRSF", [
    "DI_TransfPreformArmNotDetected",
    "CNT_CtrlPrefArm",
    "VAR_MachineStep",
    "VAR_PreformArmFault"
])
```

This immediately tells you:
- Is the fault currently active?
- What is the current sensor state?
- Is the counter at 0 (normal) or climbing (fault building)?

**If the MCP is NOT connected**, skip to Step 7 and recommend the user what to check manually.

## Step 6: Monitor suspect signals (IF ONLINE)

If a signal seems involved in the fault, monitor it for anomalies:
```
pvi_monitor("TRSF", "DI_TransfPreformArmNotDetected", 10)
```

**What to look for:**
- **Signal bouncing (>5 Hz)**: sensor misalignment, cable EMI, or mechanical vibration
- **Signal stuck (0 transitions)**: sensor dead, wiring broken, or wrong config
- **Irregular transitions**: mechanical timing issue, synchronization drift

For blowing issues, use curve tools:
```
pvi_blowing_curve(12)           → read station 12 pressure curve
pvi_all_blowing_curves(20)      → compare all 20 stations at once
pvi_save_blowing_curve(12)      → archive for later comparison
```

## Step 7: Propose root cause and action

Combine all findings into a clear diagnosis:

1. **State the root cause** with confidence level (confirmed by live data / hypothesized from code)
2. **Physical action required** (sensor alignment, cable check, valve replacement...)
3. **Recommended trace** for intermittent faults — list variables, trigger condition, and reference existing traces in `Diagnosis/<CPU>/PLC1/`
4. **Parameters to check** — relevant PAR_IDs with expected values

## Key analysis principles

- **Verify every variable** in its `.var` file before drawing conclusions
- **Always check IoMap** — do not trust variable names or comments alone
- **Check machine personalization** before assuming standard logic:
  ```
  Logical/MODULE/XX_TRANSFERT/XX_MACHINE_PERSONALIZATION/
  → CfgMachine.st, ParameterMachine.st
  ```
- **When unsure about a variable's role**, ask the user rather than guessing
- **Start with the alarm, work backward** — not forward from assumptions

## Reference files

- **Machine overview**: See [reference/machine-overview.md](reference/machine-overview.md)
- **Project structure**: See [reference/project-structure.md](reference/project-structure.md)
- **Methodology**: See [reference/methodology.md](reference/methodology.md)
- **Example analyses**: See [reference/example-analyses.md](reference/example-analyses.md)

## CPU quick reference

| CPU | IP | Prefix | Alarms path |
|-----|----|--------|-------------|
| TRSF | 192.168.20.6 | 11_ | MODULE/11_TRANSFERT/11_ALARMS/ |
| WHEEL | 192.168.20.2 | 12_ | MODULE/12_WHEEL/12_ALARMS/ |
| OVEN | 192.168.20.3 | 13_ | MODULE/13_OVEN/13_ALARMS/ |
| ASEPT | 192.168.20.5 | - | MODULE/ASEPT/ |

## Variable naming conventions

| Prefix | Meaning | Where mapped |
|--------|---------|-------------|
| `DI_` | Digital Input (sensor) | IoMap.iom |
| `DO_` | Digital Output (actuator) | IoMap.iom |
| `AI_` | Analog Input | IoMap.iom |
| `VAR_` | Internal variable | .st assignments |
| `PAR_` | Tunable parameter | Machine personalization |
| `CNT_` | Counter | .st logic |
| `TMR_` | Timer | .st logic |

## Common anti-patterns

- **Ignoring hardware**: analyzing code endlessly when the sensor is simply misaligned
- **Wrong config**: assuming an axis (e.g., M15) is present — always check active options
- **Skipping live verification**: proposing a root cause without reading the actual signal state when PVI is available
- **Trusting variable names**: a variable named "NotDetected" may have inverted logic — always check the `.var` comment and the code context
