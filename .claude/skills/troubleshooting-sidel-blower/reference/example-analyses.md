# Example Analyses

Complete alarm-to-resolution walkthroughs for common Sidel Matrix Blower faults.

## Example 1: Broken Roller Detection — Oven CPU

### Alarm

`Alarm_BrokenRoller` triggers intermittently during production on the 13_OVEN CPU.

### Investigation

**Step 1 — Locate alarm logic:**

```bash
grep -rn "Alarm_BrokenRoller" Logical/MODULE/13_OVEN/13_ALARMS/
```

Found in `AlarmOven.st`:
```
IF DI_BrokenRollerDetection AND TMR_RollerDebounce.Q THEN
    Alarm_BrokenRoller := TRUE;
END_IF;
```

**Step 2 — Verify DI_BrokenRollerDetection:**

```bash
grep -rn "DI_BrokenRollerDetection" Logical/MODULE/13_OVEN/**/*.var
```

Result: `DI_BrokenRollerDetection : BOOL; (* Spindle chain roller breakage sensor *)`

**Step 3 — Confirm hardware mapping:**

```bash
grep -rn "DI_BrokenRollerDetection" Physical/OVEN/PLC1/IoMap.iom
```

Result: `DI_BrokenRollerDetection AT %IX."X67-DI-2452A0".DigitalInput05;`

Confirmed: Card X67-DI-2452A0, channel DigitalInput05.

**Step 4 — Check the debounce timer:**

```bash
grep -rn "TMR_RollerDebounce" Logical/MODULE/13_OVEN/**/*.st
```

Found: `TMR_RollerDebounce(IN := DI_BrokenRollerDetection, PT := T#500ms);`

The alarm requires 500ms of continuous detection before triggering.

### Causal chain

```
Physical sensor on spindle chain (Card X67-DI-2452A0, Input 05)
  → DI_BrokenRollerDetection = TRUE
    → TMR_RollerDebounce runs for 500ms
      → TMR_RollerDebounce.Q = TRUE
        → Alarm_BrokenRoller raised
```

### Resolution

Since the alarm is intermittent, the sensor signal is bouncing near the threshold. Check:
1. Sensor mounting and alignment on the spindle chain
2. Sensor cable for intermittent contact or EMI
3. Whether a roller is actually worn and triggering brief detections

### Recommended trace

```
Variables to monitor:
- DI_BrokenRollerDetection (raw sensor state)
- TMR_RollerDebounce.Q (debounced output)
- TMR_RollerDebounce.ET (elapsed time — shows how close to triggering)

Trigger: DI_BrokenRollerDetection rising edge
```

---

## Example 2: Before-Oven Ejection — Infeed Problem

### Alarm

`Alarm_BeforeOvenEjection` triggers repeatedly. Machine stops after 3 consecutive ejected preforms.

### Investigation

**Step 1 — Locate alarm logic:**

```bash
grep -rn "Alarm_BeforeOvenEjection" Logical/MODULE/13_OVEN/13_ALARMS/
```

Found in `AlarmOven.st`:
```
IF CNT_EjectedPreforms >= 3 THEN
    Alarm_BeforeOvenEjection := TRUE;
END_IF;
```

**Step 2 — Trace the counter:**

```bash
grep -rn "CNT_EjectedPreforms" Logical/MODULE/13_OVEN/**/*.st
```

Found:
```
IF DI_PreformPresenceAfterLoading = FALSE AND VAR_SpindleAtCheckPosition THEN
    CNT_EjectedPreforms := CNT_EjectedPreforms + 1;
ELSE
    CNT_EjectedPreforms := 0;  (* Reset on successful load *)
END_IF;
```

The counter increments when a preform is expected but not detected after spindle loading. It resets on any successful load.

**Step 3 — Investigate DI_PreformPresenceAfterLoading:**

```bash
grep -rn "DI_PreformPresenceAfterLoading" Physical/OVEN/PLC1/IoMap.iom
```

Result: `DI_PreformPresenceAfterLoading AT %IX."X67-DI-2452A1".DigitalInput02;`

**Step 4 — Investigate VAR_SpindleAtCheckPosition:**

```bash
grep -rn "VAR_SpindleAtCheckPosition :=" Logical/MODULE/13_OVEN/**/*.st
```

Found: Generated from the spindle encoder position matching a specific angle window.

### Causal chain

```
Spindle reaches check position (encoder-based)
  → VAR_SpindleAtCheckPosition = TRUE
    → System checks DI_PreformPresenceAfterLoading
      → If FALSE: preform not loaded → CNT_EjectedPreforms + 1
        → After 3 consecutive: Alarm_BeforeOvenEjection
```

### Resolution

The preforms are not landing correctly on the spindles. Investigate:
1. Feeder output — are preforms arriving consistently?
2. Infeed starwheel timing — is the starwheel synchronized with the spindle chain?
3. Stress guide — is it deflecting and indicating a jam?
4. Preform geometry — does the preform neck fit the spindle mandrel?

### Recommended trace

```
Variables to monitor:
- DI_PreformPresenceAfterLoading (presence sensor)
- VAR_SpindleAtCheckPosition (check window)
- CNT_EjectedPreforms (consecutive count)
- DI_StressGuideDeflection (if available — infeed jam indicator)

PAR_IDs to check:
- PAR_ID related to spindle loading angle window
- PAR_ID related to feeder output speed

Trigger: VAR_SpindleAtCheckPosition rising edge
```

---

## Example 3: Stretch Rod Fault — Blowing Wheel

### Alarm

`Alarm_StretchFault_Station12` triggers on station 12 during blowing. Other stations work fine.

### Investigation

**Step 1 — Locate alarm logic:**

```bash
grep -rn "Alarm_StretchFault" Logical/MODULE/12_WHEEL/12_ALARMS/
```

Found in `AlarmWheel.st`:
```
IF ABS(VAR_StretchActualPos[i] - VAR_StretchSetpointPos[i]) > PAR_StretchPositionTolerance
   AND VAR_StationInBlowPhase[i] THEN
    Alarm_StretchFault[i] := TRUE;
END_IF;
```

The alarm fires when the actual stretch position deviates from setpoint beyond tolerance during the blow phase.

**Step 2 — Check the tolerance parameter:**

```bash
grep -rn "PAR_StretchPositionTolerance" help/
```

Found: This PAR_ID defines the maximum allowed deviation between stretch rod actual and setpoint positions.

**Step 3 — Determine if this is station-specific:**

Since only station 12 faults, the issue is mechanical or electrical on that specific station, not a recipe or parameter problem.

**Step 4 — Check LinMot diagnostics:**

```bash
grep -rn "LinMot" Logical/MODULE/12_WHEEL/**/*.st | grep -i "station\|diag\|error"
```

Look for LinMot status words, error codes, and force feedback variables specific to station 12.

### Causal chain

```
LinMot servo on station 12 cannot follow position setpoint
  → VAR_StretchActualPos[12] deviates from VAR_StretchSetpointPos[12]
    → Deviation exceeds PAR_StretchPositionTolerance
      → Alarm_StretchFault[12] raised
```

### Resolution

Station-specific stretch fault typically points to:
1. LinMot slider mechanical issue (friction, wear, damage)
2. LinMot stator winding problem on that station
3. Electrical connection issue (encoder cable, power supply to station 12)
4. Cooling problem on that specific LinMot

### Recommended trace

```
Variables to monitor:
- VAR_StretchActualPos[12] (actual position)
- VAR_StretchSetpointPos[12] (setpoint)
- VAR_StretchForce[12] (LinMot force — if available)
- VAR_LinMotStatus[12] (servo status word)

PAR_IDs to check:
- PAR_ID for stretch position tolerance
- PAR_ID for stretch speed setpoint
- PAR_ID for stretch start/end angles

Compare station 12 traces with a healthy station (e.g., station 1) to isolate the deviation.

Trigger: Station 12 reaching stretch start angle
```

---

## Example 5: Preform Arm Fault — LockedClosedMold SFC (Real Code)

### Alarm

`VAR_PreformArmFault` is set to TRUE, triggering a critical alarm via the TRSF alarm handler. Occurs sporadically during production.

### Investigation

**Step 1 — Locate the fault source:**

```bash
bash scripts/trace_variable.sh /path/to/project VAR_PreformArmFault
```

Found in `11_LockedClosedMold.sfc`, production step:

```
IF CNT_CtrlPrefArm > 1 THEN
    VAR_PreformArmFault := TRUE;
END_IF
```

**Step 2 — Understand the counter logic:**

`CNT_CtrlPrefArm` is incremented on every `EDGEPOS(VAR_MachineStep)` (each station passing), and reset to 0 on `EDGEPOS(DI_TransfPreformArmNotDetected)` (arm passing its sensor).

So the fault means: 2 stations passed the reference point without the preform arm sensor seeing the arm pass. The arm is "missing a beat."

**Step 3 — Check the sensor:**

```bash
bash scripts/trace_variable.sh /path/to/project DI_TransfPreformArmNotDetected
bash scripts/list_io_mapping.sh /path/to/project TRSF DI_TransfPreformArm
```

Confirm the physical card and channel for this sensor.

**Step 4 — Check reset conditions:**

The counter and fault are cleared when:
```
IF DI_WatchDogWheelFault OR VAR_MachineStopped OR BP_ClearingFault.State
   OR NOT(BP_StartMachine.State) THEN
    CNT_CtrlPrefArm := 0;
    VAR_PreformArmFault := FALSE;
END_IF
```

### Causal chain

```
VAR_MachineStep pulses (station passes reference)
  → CNT_CtrlPrefArm increments
    → DI_TransfPreformArmNotDetected should reset counter to 0
      → If arm sensor does NOT trigger between 2 machine steps
        → CNT_CtrlPrefArm > 1 → VAR_PreformArmFault := TRUE
```

### Resolution

The preform arm sensor is not detecting the arm passing. Check:
1. Sensor `DI_TransfPreformArmNotDetected` mounting and alignment
2. Transfer arm mechanical position — is it lagging behind the wheel?
3. Encoder synchronization between transfer arm and wheel
4. Whether `VAR_MpAxisCouplingM15OffsetShift` is active (servo offset mode bypasses the check)

### Recommended trace

```
Variables to monitor:
- DI_TransfPreformArmNotDetected (arm detection sensor)
- CNT_CtrlPrefArm (arm counter — should never exceed 1)
- VAR_MachineStep (station pulse)
- WHEEL_ValEncoder (wheel position, 36000 pts/rev)
- VAR_MemoryCtrlArm (stored encoder value at last arm detection)
- VAR_ValueCtrlArm (calculated step difference)

Trigger: VAR_PreformArmFault rising edge
Existing trace reference: Diagnosis/TRSF/PLC1/
```

---

## Example 6: Transfer Arm Synchronization Loss

### Alarm

`Alarm_TransferSyncLoss` appears during speed ramp-up. Machine fails to reach production speed.

### Investigation

**Step 1 — Locate alarm logic:**

```bash
grep -rn "Alarm_TransferSyncLoss" Logical/MODULE/11_TRANSFERT/11_ALARMS/
```

Found: The alarm triggers when the phase difference between the transfer arm encoder and the wheel encoder exceeds a threshold defined by a PAR_ID.

**Step 2 — Trace the synchronization variables:**

```bash
grep -rn "TransferSync" Logical/MODULE/11_TRANSFERT/**/*.st
```

Identify:
- The actual phase difference variable
- The tolerance PAR_ID
- The speed at which the fault occurs

**Step 3 — Check if speed-dependent:**

If the fault only appears during ramp-up, the servo tuning or mechanical coupling may struggle at higher accelerations.

### Resolution

1. Check transfer arm servo drive parameters (gain, acceleration limits)
2. Inspect mechanical coupling between transfer arm and drive
3. Verify encoder signals from both transfer arm and wheel
4. Review the synchronization tolerance PAR_ID — it may need adjustment for the current recipe/speed

### Recommended trace

```
Variables to monitor:
- VAR_TransferPhaseError (phase difference)
- VAR_WheelSpeed (wheel encoder speed)
- VAR_TransferArmSpeed (transfer arm speed)
- VAR_MachineSpeed (overall speed setpoint)

PAR_IDs to check:
- PAR_ID for sync tolerance
- PAR_ID for ramp-up acceleration rate

Trigger: Machine speed crossing the threshold where fault occurs
```
