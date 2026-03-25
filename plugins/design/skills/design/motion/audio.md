# Sound Synthesis & Audio Implementation

## Singleton AudioContext

Create one AudioContext per page. Never create a new one per sound — browsers limit the number of simultaneous contexts.

```js
const audioCtx = new AudioContext();
```

## Check and Resume Suspended Context

Browsers suspend AudioContext on page load until user interaction. Always check and resume:

```js
async function playSound() {
  if (audioCtx.state === 'suspended') {
    await audioCtx.resume();
  }
  // then play
}
```

## Disconnect Nodes After Playback

Source nodes are single-use. Disconnect on `onended` to avoid memory leaks:

```js
source.onended = () => source.disconnect();
source.start();
```

## Exponential Ramps for Natural Decay (Never Linear)

Linear volume ramps sound unnatural. Use exponential:

```js
gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
```

**Important:** The target value must be `0.001`, not `0`. Exponential ramp to zero is mathematically undefined.

## Set Initial Value Before Ramping

Always set the current value first, then ramp — otherwise the ramp starts from the previous value:

```js
gainNode.gain.setValueAtTime(gainNode.gain.value, audioCtx.currentTime);
gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
```

## Filtered Noise for Percussive Sounds

Use `createBuffer` + noise for clicks, taps, and percussion:

```js
const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
const data = buffer.getChannelData(0);
for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
```

Pass through a `BiquadFilterNode` with type `bandpass` to shape the character.

## Oscillators with Pitch Sweep for Tonal Sounds

```js
const osc = audioCtx.createOscillator();
osc.type = 'sine';
osc.frequency.setValueAtTime(440, audioCtx.currentTime);
osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
```

## Click Sound Parameters

- Duration: 5-15ms
- Filter: BiquadFilter type `bandpass`, frequency 3000-6000Hz
- Gain: under 1.0

## Filter Q Value

Use Q between 2-5 for character without resonance artifacts.

## Gain Safety

Keep gain nodes under 1.0 to prevent clipping. Use 0.3 as the default starting point:

```js
gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
```

## Create a New Source for Each Replay

Source nodes are single-use — `currentTime` on an `AudioContext` is read-only and cannot be reset. For sounds that can replay rapidly (button clicks), create a new `BufferSource` node each time:

```js
// Best practice: create a new source each time
const source = audioCtx.createBufferSource();
source.buffer = myBuffer;
source.connect(gainNode);
source.start();
```

## Preload Audio Files

Load audio assets at startup, not on demand:

```js
const response = await fetch('/sounds/confirm.mp3');
const arrayBuffer = await response.arrayBuffer();
const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
```

## Default Volume

Start at 0.3 (subtle, not startling). Let users adjust independently from system volume.

## prefers-reduced-motion and Audio

When `prefers-reduced-motion` is active, suppress or silence audio feedback — motion-sensitive users often have auditory sensitivity too:

```js
const shouldReduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!shouldReduceMotion) playConfirmationSound();
```

For behavioral guidelines on when to use audio → `ui-design/audio-feedback.md`
For PRM CSS/animation implementation → `motion/performance.md`
