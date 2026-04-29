# Analysis Methodology

## Reverse engineering protocol

When investigating a fault, trace backward from the symptom to the root cause. Follow these steps for each variable encountered:

### Step 1: Identify the trigger variable

Start from the alarm logic (in `XX_ALARMS`). Find the condition that raises the alarm. This gives you the trigger variable(s).

```
Example alarm logic:
IF DI_BrokenRollerDetection AND TMR_RollerDebounce.Q THEN
    Alarm_BrokenRoller := TRUE;
END_IF;
```

The trigger variables here are `DI_BrokenRollerDetection` and `TMR_RollerDebounce.Q`.

### Step 2: Verify the variable's meaning

Check the `.var` file where the variable is declared. Read the comment and data type. Do not rely on the variable name alone — names can be misleading or reused.

```bash
grep -rn "DI_BrokenRollerDetection" Logical/MODULE/**/*.var
```

If the `.var` file lacks a clear comment, ask the user what this variable represents physically.

### Step 3: Find the source of the value

Locate where the variable receives its value:

- For **Digital Inputs (DI_)**: Check `IoMap.iom` — the value comes directly from a physical sensor
- For **Internal variables (VAR_)**: Search for `:=` assignments in `.st` files
- For **Timer outputs (.Q, .ET)**: Find the timer instance and check what drives its `IN` and `PT` inputs
- For **SFC outputs**: Find the SFC step or action that writes the variable

```bash
# For internal variables
grep -rn "VAR_MachineStep :=" Logical/MODULE/**/*.st

# For timers
grep -rn "TMR_RollerDebounce" Logical/MODULE/**/*.st
```

### Step 4: Build the causal chain

Document the chain from physical cause to alarm:

```
Physical sensor (card X67-DI-2452A0, Input 05)
  → DI_BrokenRollerDetection (TRUE when roller broken)
    → TMR_RollerDebounce (debounce timer, PT = 500ms)
      → TMR_RollerDebounce.Q (TRUE after 500ms of continuous detection)
        → Alarm_BrokenRoller raised
```

## Hardware mapping protocol

When you need to confirm which physical I/O card and channel a variable is connected to:

### Step 1: Check comments (hint only)

```bash
grep -rn "DI_BrokenRollerDetection" Logical/MODULE/**/*.var
```

Comments may mention a card or pin number, but treat this as a hint, not proof.

### Step 2: Verify in IoMap.iom (proof)

```bash
grep -rn "DI_BrokenRollerDetection" Physical/OVEN/PLC1/IoMap.iom
```

Expected result format:
```
DI_BrokenRollerDetection AT %IX."X67-DI-2452A0".DigitalInput05;
```

This confirms: card `X67-DI-2452A0`, channel `DigitalInput05`.

### Step 3: Cross-reference with electrical drawings

If available, ask the user to confirm the mapping matches the electrical schematic. This catches cases where the code was updated but the drawing was not (or vice versa).

## Variable verification checklist

Before concluding that a variable means what you think it means:

```
Variable Verification:
- [ ] Found declaration in .var file with type and comment
- [ ] Confirmed physical mapping in IoMap.iom (for I/O variables)
- [ ] Located all assignments (:=) in .st or .sfc files
- [ ] Checked for any conditional logic that modifies its behavior
- [ ] Asked user for confirmation if any ambiguity remains
```

## Recommending traces and PAR_IDs

When proposing diagnostic traces:

1. **Identify the relevant motion or process** (e.g., stretch rod movement, pre-blow timing)
2. **Find the associated PAR_IDs** by searching the `help/` folder:
   ```bash
   grep -rn "stretch" help/
   grep -rn "PAR_ID" help/ | grep -i "blow"
   ```
3. **Suggest both the PAR_IDs and the related process variables** to monitor simultaneously
4. **Specify the trigger condition** for the trace (e.g., "trigger on station N reaching the blow position")

### Trace recommendation format

Present trace recommendations clearly. Note that B&R trace files (`.tc`) are binary configs found in `Diagnosis/<CPU>/PLC1/`. Existing traces in the project can serve as templates.

```
Recommended trace for [issue description]:

Variables to monitor:
- VAR_StretchPhysicalPosInPoints[station] (actual stretch position in encoder points)
- VAR_EncoderPosition (wheel encoder, 36000 pts/rev)
- DI_MoldLockConfirm (mold closed confirmation)

PAR_IDs to check:
- PAR_MoldNumber: Number of molds on the wheel
- PAR_EndCloseMoldDeg: End of closing cam angle
- PAR_BeginLockingDeg: Start of locking cam angle

Trigger: Station reaching blow start angle
Existing trace reference: Diagnosis/WHEEL/PLC1/*.tc
```

## Best practices

- Start with the alarm list: it tells you exactly what the machine considers wrong
- Work backward from the alarm to the physical world, not forward from assumptions
- Check multiple stations when a fault is intermittent — the shift register can tell you which station triggered it
- Compare parameter values against the recipe to detect drift
- When in doubt about a variable's role, reading the surrounding code context (5-10 lines before and after) often clarifies its purpose
