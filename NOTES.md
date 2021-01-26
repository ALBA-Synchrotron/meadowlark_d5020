# Notes

## Waveforms
- Off
- Invariant
- Sinusoid
- Triangle
- Square
- Sawtooth
- T.N.E

## Parameters

- V<sub>1</sub>: 0 - 10V
- V<sub>2</sub>: 0 - 10V
- Period T: 0.5 - infinte seconds
- Phase: -360 - 360
### Parameters of Transient Nematic Effect
- V<sub>TNE</sub> 0 - 10V
- T<sub>TNE</sub> 0 - 255ms


## Monitoring threshold

The I/O connector is monitored, and if less than 2.5V, output = V1. Otherwise, output is V2.

## Trigger

The I/O connector is monitored for pulses. When a pulse is received, if the output is at V1, it switches to V2. If the output is at V2, it switches to V1.