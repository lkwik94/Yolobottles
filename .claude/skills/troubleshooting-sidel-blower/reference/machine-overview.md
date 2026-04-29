# Machine Overview — Sidel Matrix Blower

The Sidel Matrix Blower transforms PET preforms into finished bottles through a synchronized high-speed flow across four CPUs. Three CPUs handle the core process (Oven, Transfer, Wheel), and a fourth handles aseptic functions when equipped.

## Phase 1: Infeed & Heating (Oven CPU — `13_OVEN`)



The preform journey starts here:

1. **Feeder** delivers preforms into the system
2. **Infeed Starwheel** receives preforms, equipped with:
   - Stress Guide for detecting loading issues
   - Optional modules: Deduster, Predis (preform disinfection)
3. **Spindle Loading** places preforms onto the Spindle Chain
   - If loading fails, the "Before Oven" ejection triggers after 3 consecutive ejected preforms
4. **Heating** applies infrared lamps according to the active recipe
5. **Tracking** uses the `Item_Oven` shift register to follow each preform through the oven

### Key signals in this phase

- Spindle chain encoder and synchronization
- Lamp power feedback
- Preform presence sensors at loading and ejection points
- Stress guide displacement sensor

## Phase 2: Transfer (Transfer CPU — `11_TRANSFERT`)

The Transfer Arm picks the heated preform from the spindle and places it into the mold on the blowing wheel. This CPU is the **Maestro** — it orchestrates the overall machine synchronization.

### Key signals in this phase

- Transfer arm position and servo feedback
- Preform detection at pickup and drop-off
- Synchronization between oven chain speed and wheel speed

## Phase 3: Blowing & Outfeed (Wheel CPU — `12_WHEEL`)

1. **Stretching** — Linear motors (LinMot) push the stretch rod into the preform
2. **Pre-blowing** — Low-pressure air shapes the preform
3. **Blowing** — High-pressure air expands the preform into the mold shape
4. **Degassing** — Pressure is released
5. **Outfeed** — Finished bottles exit to the air conveyor or downstream Combi equipment

### Key signals in this phase

- LinMot position and force feedback
- Blowing pressure sensors (pre-blow, blow, degas)
- Mold lock confirmation
- Outfeed bottle detection

## Shift registers and item tracking

Each CPU maintains shift registers that track individual items (preforms or bottles) through its zone:

| CPU | Shift Register | Tracks |
|-----|---------------|--------|
| 13_OVEN | `Item_Oven` | Preform from infeed through heating |
| 11_TRANSFERT | `Item_Transfer` | Preform during transfer arm movement |
| 12_WHEEL | `Item_Wheel` | Bottle through blow-mold-outfeed cycle |

These registers carry quality flags, recipe data, and fault markers that follow each item. When diagnosing faults, checking the shift register state at the moment of the alarm provides context about which station and which item triggered it.

## Aseptic Module (ASEPT CPU)

When the machine is configured for aseptic production, the ASEPT CPU manages sterilization and decontamination functions. This CPU is part of the main Automation Studio project.

## Preform Distribution (PRFD — separate project)

The PRFD CPU at `192.168.20.4` handles preform distribution upstream of the blower. It runs its own independent Automation Studio project and is not part of the main blower project files. When troubleshooting PRFD-related issues, a separate project archive is needed.
