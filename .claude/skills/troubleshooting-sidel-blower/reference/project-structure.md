# Project Structure — B&R Automation Studio

The Sidel Matrix Blower project runs on 4 CPUs within a single Automation Studio project, plus downstream equipment on the same network. A separate PRFD (preform distribution) CPU has its own independent project.

## CPU Architecture

### CPU 1: `11_TRANSFERT` (TRSF) — Maestro / Core — `192.168.20.6`

This is the main orchestrator. It manages machine states, synchronization, and overall coordination.

```
Logical/MODULE/11_TRANSFERT/
├── 11_ALARMS/              # Alarm definitions and logic
├── 11_MACHINE_PERSONALIZATION/  # Options, parameters, machine config
├── 11_CORE/                # Main state machine and sequencing
└── ...
```

### CPU 2: `12_WHEEL` — Blowing Process — `192.168.20.2`

Handles the blowing cycle: stretch, pre-blow, blow, degas, and outfeed.

```
Logical/MODULE/12_WHEEL/
├── 12_MACHINE_MODULE/      # Core blowing process logic
├── 12_ALARMS/              # Wheel-specific alarms
└── ...
```

### CPU 3: `13_OVEN` — Infeed & Heating — `192.168.20.3`

Manages preform feeding, spindle chain, heating lamps, and oven tracking.

```
Logical/MODULE/13_OVEN/
├── 13_ALARMS/              # Oven-specific alarms
├── 13_HEATING/             # Lamp control and recipe management
├── 13_INFEED/              # Feeder and starwheel logic
└── ...
```

### CPU 4: `ASEPT` — Aseptic Module — `192.168.20.5`

Handles aseptic process functions. Shares the same Automation Studio project.

```
Logical/MODULE/ASEPT/
└── ...
```

### Separate project: `PRFD` — Preform Distribution — `192.168.20.4`

The PRFD CPU runs its own independent Automation Studio project. Its programs are not accessible from the main blower project files.

## Network topology

All CPUs and devices share the `192.168.20.x` subnet.

### PLCs

| CPU | IP Address | ANSL |
|-----|-----------|------|
| WHEEL | 192.168.20.2 | Active |
| OVEN | 192.168.20.3 | Active |
| PRFD (separate project) | 192.168.20.4 | Active |
| ASEPT | 192.168.20.5 | Active (if equipped) |
| TRSF | 192.168.20.6 | Active |
| FILLER (downstream) | 192.168.20.11 | Active |
| LABELLER (downstream) | 192.168.20.21 | Active |
| ACTIS (downstream) | 192.168.20.31 | Active |

### Peripherals (on TRSF hardware)

| Device | IP Address | Protocol |
|--------|-----------|----------|
| MainBearing | 192.168.20.186 | ModbusTCP |
| MotionBearing | 192.168.20.188 | ModbusTCP |
| PowerMeter | 192.168.20.8 | ModbusTCP |

### Infrastructure

| Role | IP Address | Device |
|------|-----------|--------|
| Gateway | 192.168.20.12 | Scalance |
| NTP Server / HMI | 192.168.20.1 | HMI |

ANSL (Automation Net Secure Link) is B&R's secure communication protocol. When troubleshooting communication issues, verify ANSL status matches between the CPUs attempting to communicate.

## Alarm system architecture

Alarms are organized by severity and CPU. Each CPU has its own alarm detection programs:

```
XX_ALARMS/
├── XX_AlarmCriticalDetection/    # Machine-stopping faults
├── XX_AlarmAlertDetection/       # Warnings, may degrade operation
├── XX_AlarmInfoDetection/        # Informational messages
├── XX_AlarmMessageDetection/     # Operator messages
├── XX_AlarmHandlerXX/            # Central alarm handler for this CPU
├── XX_ClearingFault/             # Fault acknowledgment logic
├── XX_DiagnosticAlarm/           # Diagnostic messages
└── XX_HistoricDiagnosticAlarm/   # Alarm history
```

Alarm function call pattern (found in .st files):
```
AlarmCritical(Number:=85, Word:=VAR_WordAlarmCriWheel);
AlarmAlert(Number:=120, Word:=VAR_WordAlarmAlertOven);
AlarmInfo(Number:=45, Word:=VAR_WordAlarmInfoTrsf);
```

For station-specific alarms, the number uses an offset pattern:
```
AlarmCritical(Number:=b+240, Word:=VAR_WordAlarmCriWheel);
// Where b = station number (1..N), offset determines fault type:
//   b+0:   Inverter fault station X
//   b+240: Inconsistent Point 10 value station X
//   b+288: Stretch motor temperature too high station X
//   b+336: PT10 discrepancy between station 1 and station X
//   b+384: Stretching drive not ready station X
//   b+431: Inconsistent Point 0 value station X
//   b+480: Stretching down at wrong place station X
```

Alarm word arrays (declared in AlarmHandler.var):

| Array | CPU | Max alarms |
|-------|-----|-----------|
| VAR_WordAlarmCriWheel | WHEEL | 4736 |
| VAR_WordAlarmCriOven | OVEN | 5568 |
| VAR_WordAlarmCriTrsf | TRSF | 3392 |
| VAR_WordAlarmCriAsept | ASEPT | 3072 |

Same pattern for `Alert`, `Info`, and `InfoProd` severities.

| Extension | Purpose | Where to find |
|-----------|---------|---------------|
| `.st` | Structured Text source code | Inside program folders |
| `.var` | Variable declarations with types and comments | Alongside `.st` files |
| `.iom` | I/O mapping (physical card ↔ variable) | `Physical/<CPU>/PLC1/IoMap.iom` |
| `.sfc` | Sequential Function Chart programs | Inside program folders |

## Inter-CPU communication

CPUs share data via `Logical/MODULE/COM_Variable/`:

| File | Direction |
|------|-----------|
| COM_TRSF.var / COM_TRSF_Table.var | Variables sent/received by TRSF |
| COM_WHEEL.var / COM_WHEEL_Table.var | Variables sent/received by WHEEL |
| COM_OVEN.var / COM_OVEN_Table.var | Variables sent/received by OVEN |
| COM_ASEPT.var / COM_ASEPT_Table.var | Variables sent/received by ASEPT |
| COM_PRFD.var / COM_PRFD_Table.var | Variables exchanged with PRFD (external project) |
| COM_SafeLog.var | Safety PLC shared variables |

Each CPU also has local HMI/BP communication vars: `COM_HMI_XX.var`, `COM_XX_BP.var`, `COM_XX_HMI.var`.

## Shared global files

At `Logical/MODULE/` root:

| File | Content |
|------|---------|
| Matrix.typ | Global type definitions (ARTICLE tracking struct, alarm structs, NozzleConfiguration, etc.) |
| Matrix.var | Global parameters (PAR_MoldNumber, PAR_NumberSpindle, nozzle configs, offsets) |
| OMAC.typ | PackML/OMAC state machine types |
| AlarmHandler.var | Alarm word arrays for all 4 CPUs and severity levels |
| BlowerMatrixFault.exe | Compiled fault handler |

## Key file types

| Extension | Purpose | Where to find |
|-----------|---------|---------------|
| `.st` | Structured Text source code | Inside program folders |
| `.var` | Variable declarations with types and comments | Alongside `.st` files |
| `.iom` | I/O mapping (physical card ↔ variable) | `Physical/<CPU>/PLC1/IoMap.iom` |
| `.sfc` | Sequential Function Chart programs | Inside program folders |
| `.typ` | Type definitions (structs, enums) | MODULE root or CPU folders |
| `.tc` / `.td` | Trace configuration / Trace data | `Diagnosis/<CPU>/PLC1/` |
| `.pkg` | Package descriptor (folder contents) | Every folder |
| `.hw` / `.hwl` | Hardware configuration | `Physical/<CPU>/` |

## Navigation commands

### Finding alarm logic

```bash
# List all alarm programs
view Logical/MODULE/11_TRANSFERT/11_ALARMS/
view Logical/MODULE/12_WHEEL/12_ALARMS/
view Logical/MODULE/13_OVEN/13_ALARMS/

# Search for a specific alarm by name or number
grep -rn "Alarm_BrokenRoller" Logical/MODULE/
```

### Tracing variables

```bash
# Find where a variable is declared (type and comment)
grep -rn "DI_BrokenRollerDetection" Logical/MODULE/**/*.var

# Find where a variable is assigned a value
grep -rn "DI_BrokenRollerDetection :=" Logical/MODULE/**/*.st

# Find all usages of a variable
grep -rn "DI_BrokenRollerDetection" Logical/MODULE/
```

### Hardware mapping

```bash
# Check I/O mapping for a specific variable
grep -rn "DI_BrokenRollerDetection" Physical/

# List all I/O cards for a CPU
view Physical/OVEN/PLC1/IoMap.iom
view Physical/TRANSFERT/PLC1/IoMap.iom
view Physical/WHEEL/PLC1/IoMap.iom
```

### Using the help folder

The `help/` directory contains machine documentation, PAR_ID descriptions, and parameter references.

```bash
# Search for a PAR_ID
grep -rn "PAR_ID_5012" help/

# Search for a topic
grep -rn "stretch rod" help/
grep -rn "pre-blow" help/
```

## Variable naming conventions

Sidel projects typically follow these prefixes:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `DI_` | Digital Input | `DI_BrokenRollerDetection` |
| `DO_` | Digital Output | `DO_EjectionValve` |
| `AI_` | Analog Input | `AI_OvenTemperature` |
| `AO_` | Analog Output | `AO_LampPower` |
| `TMR_` | Timer | `TMR_StepTime` |
| `CNT_` | Counter | `CNT_EjectedPreforms` |
| `VAR_` | Internal variable | `VAR_MachineStep` |
| `PAR_` | Parameter (tunable) | `PAR_BlowPressure` |
