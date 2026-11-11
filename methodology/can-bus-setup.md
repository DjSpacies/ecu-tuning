---
id: methodology/can-bus-setup
title: CAN bus setup, decoding and verification
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup, methodology/sensors-io-calibration]
supersedes: []
---

# CAN bus setup, decoding and verification

## Claim
CAN is used to move data between the ECU, dash, wideband controllers, keypads, expanders, power modules and factory modules. It works reliably when four things are right: the physical bus (a twisted pair, a trunk with short stubs, exactly two terminators, one bit rate per bus); addressing (ID, number base, standard or extended format); frame layout (offset, length, byte order); and scaling (multiplier, divisor, offset, units). Each must be verified against a live known value, because the receiver has no idea what the numbers mean. CAN suits slow or many-channel data. It does not suit crank or cam position, knock, or other signals that need very fast or edge-accurate sampling. Replacing a factory ECU on a CAN-integrated car can break other vehicle systems unless their messages are reproduced.

## Why (derivation)
### Physical layer
CAN high and CAN low carry the same signal inverted on a twisted pair. The receiver reads the difference, so noise that lands equally on both wires cancels; this gives strong immunity to ignition noise. Terminators at both trunk ends absorb the signal energy so it is not reflected back to corrupt frames. Two 120 Ω terminators in parallel measure about 60 Ω across CAN-H and CAN-L with power off. One terminator measures about 120 Ω.

### Bit rate
Every node on a bus samples at the same bit timing. A single node at the wrong rate does not just fail itself: it corrupts frames for everyone, and can take down a whole bus, including a factory one. It generally causes no damage. The common rates are 1 Mbit/s for aftermarket devices and 500 or 250 kbit/s on OE buses. Devices that must run at different rates go on separate buses. Transmit rate (how often a frame is sent) can differ between devices; bit rate cannot.

### Addressing and arbitration
Standard 11-bit IDs give about 2000 addresses; extended 29-bit IDs give over 500 million. When frames collide the lowest ID wins, which is why safety-critical OE data such as ABS wheel speeds sits on low IDs. Brands differ in which format they default to, so the format must be matched when mixing brands. IDs are documented in either decimal or hexadecimal (0x prefix). Confusing the two silently points the receiver at the wrong message.

### Frame packing and scaling
A frame carries 8 bytes. One byte (0–255) suits throttle, temperatures and similar. Two bytes (0–65535) are needed for rpm, wheel speed or lambda resolution. Four bytes are needed for GPS coordinates. Single bits carry status flags (limiter active, launch armed). Only integers are sent. Decimals are carried by scaling (lambda 0.902 sent as 902, decoded ÷1000), and negative ranges by offset (temperature sent as T + 50, decoded with −50). Multi-byte values have a byte order, variously called big/little endian, MSB/LSB first, or Motorola/Intel. A wrong order makes a smooth quantity jump randomly. The physical value is (raw × multiplier ÷ divisor) + adder, and most ECUs build their messages in metric units regardless of display units.

### Latency and what not to send
A CAN path adds processing stages and is updated at a frame rate (commonly 10 to 50 Hz for ECU-to-dash streams). Crank and cam signals are acted on at the tooth edge in an interrupt routine, and knock needs fast raw signal processing. Suspension position needs at least about 1000 Hz sampling. None of these suit a CAN expander chain. Slow, many-channel data such as tyre temperature arrays are ideal for it.

## Assumptions
- Device documentation gives the bit rate, ID, number base and address format, plus per-channel offset, length, byte order and scaling, or the bus can be sniffed.
- At least one device on each link allows user-defined receive or transmit templates, or ready-made templates exist for the device pair.
- A trusted reference reading exists for each channel: the transmitting device's own display, a scan tool or a dyno value.

## Breaks when
- Two or more devices carry fixed internal terminators that cannot be switched off, or an unknown internal terminator sits mid-bus. This is a common time-wasting fault, and choosing different hardware is the cleanest fix.
- Stubs run long because nodes sit in the engine bay while the trunk is in the cabin.
- Bit rates are mixed on one bus, for example a 1 Mbit/s keypad or expander on a 500 kbit/s factory bus.
- The ECU accepts CAN only in fixed formats, for example lambda only from its own brand's modules, and the devices chosen cannot be configured to match.
- A factory ECU is removed. The cluster, transmission, ABS, air conditioning or fans may depend on its broadcasts. In one case fans ran constantly because fan requests were CAN messages, and the tacho and coolant gauge died.
- The CAN link fails while a power module is holding outputs the ECU commanded. Without a defined per-output default, outputs may stay on or off.
- A third-party device transmits onto a factory bus (for example through the OBD port) on an ID that clashes with an OE message. Factory modules may then misbehave.
- A benchtop setup tolerates poor practice (untwisted wires, missing or extra terminators) that will fail in the noisy car.
- Emulated I/O-expander streams update slowly. One logged at nearer 5 Hz than its nominal 10 Hz, which is too slow for paddle-shift requests, so those were hardwired instead.
- A cheap CAN-to-USB adapter is unreliable, or is set to the wrong bus speed, so the sniffer shows nothing.

## Practical use
### Physical build
- Use twisted CAN-H/CAN-L. The sources give a twist about every 20 to 30 mm and call the exact pitch not critical. Light-gauge wire (about 22 to 24 AWG) is enough because CAN carries almost no current.
- Run a trunk with nodes tapped off on short stubs. Stub limits quoted range from about 200 mm to 300 to 500 mm. Total length limits quoted range from about 15 m to 40 m. A car rarely approaches either.
- To reach distant nodes (engine-bay lambda modules, wheel-corner sensors), run the trunk out to them and back unbroken rather than using a long stub.
- Terminate both trunk ends exactly once, about 120 Ω (some makers specify 100 Ω; either has worked in the sources), rated at least a quarter watt. On a bus under about 2 m one terminator may work, but never none. Meter each device across CAN-H/CAN-L before wiring to find built-in terminators. Enable or disable software terminators so that exactly two exist, at the ends. A device with a fixed terminator must sit at an end. If a dash at the far end has one built in, nodes between the ECU and the dash need no extra resistor.
- Build a terminator into the harness by soldering short leads, folding a leg back for strain relief, covering it with glue-lined heat shrink, and crimping it in parallel at the end device's connector. Solder joints crack under vibration unless rigidly supported.
- Add spare CAN ports to a new harness (CAN-H, CAN-L, 12 V, power ground) so later devices plug in.
- Before buying, check that each device allows user templates or has ready templates for the others. Some dashes and ECUs are fixed-format.

### Configuration
1. Choose the bus or channel that matches the physical wiring. Multi-bus ECUs make it easy to send data on the wrong one.
2. Set the bit rate on every node on that bus. Keep 1 Mbit/s aftermarket devices on their own bus if the factory bus is 500 kbit/s.
3. Enter the ID in the number base the tool uses. Convert with a programmer calculator (for example 1000 decimal = 0x3E8, 0x640 = 1600 decimal) rather than in your head. Some receivers require a base ID that is a multiple of 16. Set standard or extended format to match.
4. Lay out the channels: message number, byte offset and length, with no overlap. Some tools define widths in bits and others in bytes (16 bits = 2 bytes). Offset each channel's start by the width of the previous one. Where transmit channel and stream numbers must match, match them. Apply and save, or nothing is sent.
5. Set scaling. If the receiver's base resolution equals the transmitted resolution, no multiplier is needed. Pre-calibrated channels use the transmitter's resolution (for example 0.01 G, 0.1 °C). Raw voltages from an expander ignore scale and need a sensor calibration table like a hard-wired input. Decode metric first and convert units for display afterwards.
6. Pick a transmit rate to suit the data: faster for rpm, MAP and TPS, slower for temperatures. Switch and keypad streams in the sources run at 10 to 50 Hz.
7. Check that a chosen ID does not clash with existing traffic on that bus.
8. Reboot devices after configuration changes where required, and confirm they show online.

### Verify every channel
- With the system powered, engine off or idling, scroll through every received channel and compare it with the source device's own reading. Ready-made templates can still hold surprises, such as ignition timing with a −1 multiplier or values off by one decimal place.
- Toggle every switch or keypad button and watch the bit change in a built-in CAN monitor before relying on it. Then calibrate raw values to positions.
- Send a channel already known to be correct as a reference alongside new ones, to separate layout errors from scaling errors.
- Cross-check CAN-received channels on the dash against the ECU's tuning software before track use.

### Using CAN to save inputs and hardware
- Analog sensors wired into a dash (fuel, oil and coolant pressure, exhaust back pressure, trim pots) can be sent to the ECU for compensation and protection, freeing ECU inputs. The dash's built-in G sensor or GPS can feed ECU strategies such as traction control.
- Factory ABS modules already broadcast calibrated wheel speeds, and often brake pressure and steering angle. Receive them instead of fitting sensors. No pulse-per-revolution calibration is needed, but confirm that all four wheels agree with the car rolling slowly.
- Steering-wheel switches can go through a wheel-mounted display or keypad, so only power, ground and CAN cross the wheel connector. Have the dash show the selected mode whenever a switch moves.
- A flexible dash or gateway can translate between fixed formats. For example, it can receive a third-party wideband or keypad in its published template and retransmit the data in the exact format the ECU expects from its own brand's modules.
- An ECU can request power-module outputs (for example the fuel pump) over CAN. Confirm with the module's CAN monitor while toggling the function. Set each output's behaviour on CAN loss (hold last state, force off, or force on) by what is safest for that device. Holding the last state is most common.
- A transmission controller needs an accurate engine torque figure to set clutch pressure. Under-reporting gives clutch slip and gradual damage, and over-reporting gives harsh shifts, so one maker's guidance errs slightly high. Use a CAN torque signal if the ECU provides an accurate one; otherwise configure the controller's internal torque model.

### Decoding an undocumented or factory bus
1. Set the sniffer to the bus speed (try the common rates, or measure with a scope).
2. Change one thing only (unplug a sensor with ignition on, swap a temperature sensor for a variable resistor, force a sensor into fault and change its fault default, move the throttle) and watch which ID and byte changes. The same quantity often appears on several IDs in different formats for different modules; this is normal.
3. Fix byte order: a two-byte field that jumps randomly while the real quantity changes smoothly is in the wrong order or the wrong place.
4. Derive scaling. Record raw values against true values from a scan tool or the dyno, plot them, and fit a line for slope and offset. Force the intercept to zero where raw is zero at rest (wheel speed at standstill) to reduce the effect of scattered points.
5. OBD2 standard PIDs give key values, but often at slow update rates. There is generally no public database of OE messages.

### Replacing a factory ECU on a CAN car
- Decide up front whether the cluster, transmission, ABS, air conditioning and fans will work. Options are: reflash the factory ECU; use a plug-in standalone whose maker replicates the OE messages; decode and reproduce the messages yourself, for example from an aftermarket dash; or budget for an aftermarket dash and gearbox control.
- An adaptor-harness install that breaks OE messaging may be acceptable for a dyno demonstration but not for a road or track car.

### Diagnostic tests
- **Nothing communicates, or the whole bus goes down.** Check in this order: bit rate on every node; CAN-H and CAN-L swapped; termination (60 Ω between the wires with power off; about 120 Ω means one terminator is missing, and much lower means extras); the wrong bus selected on a multi-bus device. On a complex bus, disconnect all nodes and add them back one at a time.
- **One device not detected while others work.** Tolerance to bad termination varies. In one case a wideband failed without a far-end terminator while another brand's module worked, and a second module added to the same bus also needed the terminator. Working with one device does not prove the bus is right.
- **Configured ID shows no data.** Check the number base and the standard/extended format. A receive base ID entered as 16 in hex is 0x16 (22), not 0x10.
- **Value off by an exact factor (×10, ×100).** Scaling is wrong, not position. Examples: oil pressure 17 kPa against a known 170 kPa; rpm reading 100 at 1000 rpm; lateral G of −1 to −2 where the dash showed about 0.01. Correct with the multiplier or divisor.
- **Value offset by a constant, or wrong sign.** The adder or sign is wrong, which is typical for temperatures and timing.
- **Value jumps randomly.** Byte order or byte location is wrong.
- **Two devices with layout conflicts.** Channels share a start position. Offset them.

## Worked example
**Coolant temperature byte.** A factory bus sends coolant temperature in one byte as T + 50. A raw 150 decodes as 150 − 50 = 100 °C. The byte can represent −50 to 205 °C.

**Throttle byte.** Raw 0 at closed and 255 at full throttle: percent = raw ÷ 2.55.

**Lambda.** Lambda is sent ×1000 in two bytes. Raw 0x0386 = 902 decodes as 902 ÷ 1000 = 0.902. If the receiver expects ×100 and is set with divisor 10 instead of 1000, it shows 90.2, an obvious ×100 error.

**Wheel speed fit.** Holding a steady road speed on the dyno, raw readings of about 19,600 at 100 km/h give a slope of about 0.0051 (km/h)/count with the intercept forced to zero.

**Termination check.** With power off, the meter across CAN-H and CAN-L at the ECU connector reads 118 Ω. Only one terminator is present. The far-end resistor is missing, or the dash's built-in terminator is disabled. Fit or enable it, recheck for about 60 Ω, then add nodes.

## Disputed / conflicts
- **Terminator value.** Some makers specify 100 Ω and others 120 Ω. One practitioner reports that either has worked when mixing brands, so the exact value is not critical, but the other sources specify 120 Ω. Matching the existing terminators is the conservative choice.
- **Do short buses need two terminators?** Several sources say one terminator usually suffices under about 2 m. Others say to always fit both. One demonstration showed a single module working with only the ECU's built-in terminator, then failing once more nodes were added. Fit both as good practice.
- **Length limits.** Stub limits are quoted as about 200 mm, 300 mm and 500 mm, and trunk limits as about 15 m and 40 m. These are rules of thumb from different documents, not measured thresholds. Keep stubs as short as practical.
- **Analog versus CAN for lambda.** The sources strongly prefer CAN because it removes ground offsets. One practitioner stresses that CAN guarantees transmission, not the accuracy of the controller, so it still needs a reference cross-check (see methodology/wideband-sensors).
- **Transmission torque model.** One maker's method sets unloaded torque in neutral at about 10 to 20 Nm across idle, 3000 and 5000 rpm, extrapolates upward and smooths the table. After 500 to 1000 km, clutch pressure adaptations near zero mean the table is good, and values of roughly 20 to 40 or more mean it needs work. This is one maker's procedure, shown in one source, and adaptation scaling is controller-specific.
- **Standalone versus reflash on CAN-heavy road cars.** One practitioner's view is that a standalone only makes sense on stripped race cars with an aftermarket dash and gearbox control, and that reflashing is cheaper once the ECU is unlocked. Other sources show plug-in standalones with replicated OE messages working on such cars. The choice depends on whether templates exist for that model.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
