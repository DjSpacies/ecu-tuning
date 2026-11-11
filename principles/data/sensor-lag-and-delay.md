---
id: principles/data/sensor-lag-and-delay
title: Sensor lag and transport delay
layer: L1
status: draft
confidence: medium
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Sensor lag and transport delay

## Claim
A measurement of lambda arrives later than the events that caused it: first a transport delay through the engine and exhaust, then the sensor's own lag, then any filtering in the controller, the ECU, the logger or the display. Logged channels must be aligned in time before they are compared, and the log rate must be fast enough to show the event at all. Most apparent lambda errors at a step in target, a tip-in or a lift-off are timing artefacts, not calibration errors.

## Why (derivation)
An engine-control textbook models the fuel-to-sensor path as a pure delay followed by a first-order lag, both depending on operating point. The delay is partly a cycle effect (the charge must be induced, burnt and exhausted) and partly gas travel time to the sensor, so it is longest at low speed and low flow and shrinks as exhaust flow rises. Filters in the sensor controller or ECU add further lag.

Three further layers stack on top in practice:
- **Hidden filtering.** Some ECUs filter the lambda input before display or logging, sometimes without saying so, so the trace looks steadier and slower than the sensor really is. Dyno software that receives lambda or boost over a data link is often both filtered and slowly updated; one demonstration showed a dyno boost trace that looked flat while the ECU's own log showed it a few kPa below target.
- **Sampling.** A logger records discrete samples and the viewer draws straight lines between them. Anything shorter than the sample interval is invisible or flattened. In the sources, a pressure channel logged at 10 Hz looked erratic beside the same kind of channel at about 50 Hz, and a lift-off pressure spike logged at 10 Hz was judged to be under-read for the same reason. Live laptop links can be much slower than onboard logging (a few hertz on one ECU shown), which hides the shape of a fast transient.
- **Commanded steps.** When the ECU steps its lambda target (for example from closed-loop stoichiometric to a rich power-enrichment target), the target changes in one sample but measured lambda follows a few tenths of a second later. The logged error in that window can be several percent, and the sources show it reaching over ten percent, although the cell would read near zero if held there.

## Assumptions
A roughly constant delay near a given operating point. A sensor mounted in the usual position near the collector or turbine outlet, not at the tailpipe.

## Breaks when
- Rapid speed or load changes, sensor location changes, and sensors running outside their heater-ready state.
- The sensor is far downstream (tailpipe probe on a dyno): delay grows a lot and may need its own estimate.
- Overrun fuel cut, ignition-cut shifts and limiters: the sensor sees unburnt oxygen and pegs lean. That is a true reading of the exhaust, not lag, but it falls in the same windows and must be removed as well (methodology/data-quality).
- Closed-loop controllers with high gain at slow transport (idle, cruise) correct before they can see their last correction and oscillate; see principles/control/feedback-and-pid.

## Practical use
- Estimate delay from the log using a step: a commanded lambda target step, an injector trim step, or a sharp throttle event. The lag is the time from the step to the measured channel moving.
- Discard samples around transients and target steps unless delay has been handled. Do not attribute a lambda excursion to the table cell that was active at the time of the reading.
- During airflow or VE calibration, a flat lambda target removes target-step artefacts. Enter the real target shape after the airflow model is right (one practitioner's method).
- On full-throttle pulls, let measured lambda settle at the rich target before collecting data, and stop collecting before the throttle is lifted; both ends of a pull otherwise log false lean errors.
- Judge transients from the ECU's internal log, at a rate suited to the event, not from a slow live graph or a data-link channel relayed to another screen.
- Choose a log rate from how fast the signal and sensor can change, not "as fast as possible": fast pressures and lambda at tens of hertz, temperatures at one or two hertz (methodology/log-capture-protocol).

### Diagnostic tests
- **Lag versus real error at a target step.** Look at the error in the samples straight after the step and in samples later in the same cell. If the error decays toward zero within a few tenths of a second, it is lag. If it persists, it is real.
- **Lag versus real error on a tip-in.** A lean dip that lines up with throttle rate and recovers is transient fuelling or lag; a steady offset after the throttle settles is a table error.
- **Filtering hidden in a channel.** Compare the same quantity from two paths (ECU internal log versus dyno screen, or ECU log at two rates). A path that looks smoother and later than the other is filtered.
- **Sample rate too low.** If a peak's shape changes noticeably when the rate is raised, the slower rate was missing it.

## Worked example
At 1000 rpm one four-stroke cycle takes 120 ms, and the delay spans at least several events plus gas travel and sensor response. A lean spike logged at time t was caused by fuelling earlier than t by that delay.

At a switch from closed-loop stoichiometric to a lambda 0.85 target, a log shows the target step at t = 0 and measured lambda reaching 0.86 at about 0.3 s. The samples in between show an apparent lean error of up to about 15 %. Samples from 0.5 s onward in the same cell read within 1 %. Only those later samples are used.

## Disputed / conflicts
- **How large the delay is.** The textbook view, kept above, is that delay is longest at low flow and depends strongly on operating point. One practitioner's view is that the delay to a normally placed sensor is small, especially at higher rpm, so measured lambda should overlay target closely in a log unless the sensor is at the tailpipe. Both agree at high flow; they differ in emphasis at low flow. Discriminating test: step the target at idle and at mid rpm under load and measure the lag at each.
- **Data-link lambda on the dyno.** Some tuners work from the lambda shown on the dyno screen. A demonstration showed that, relayed over a data link, it updated too slowly to judge a ramp, and the ECU's own log was used instead. Whether that holds depends on the link rate of the setup in use.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
