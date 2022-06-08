<script lang="ts">
	import { onDestroy } from 'svelte';

	import { testSequences } from 'src/constants/test-sequences';
	import { keyMap, expectedKeys } from 'src/constants/keymap';

	import { testSequence, inputData } from 'src/store/test-sequence';
	import { fingersDetected, hands, video } from 'src/store/mediapipe';
	import { edgeCoordinates } from 'src/store/edge-coordinates';

	import Input from 'src/components/@test-area/input.svelte';
	import Words from 'src/components/@test-area/words.svelte';
	import Timer from 'src/components/@test-area/timer.svelte';
	import Caret from 'src/components/@test-area/caret.svelte';

	let finished = false;
	let focused = false;

	// Timings
	let startTime = 0;
	let elapsedTime = -1;
	let interval: NodeJS.Timer | null = null;

	const updateElapsedTime = () => {
		elapsedTime = Math.floor((Date.now() - startTime) / 1000);
	};

	$: {
		if (startTime > 0) {
			interval = setInterval(updateElapsedTime, 500);
		}
	}

	onDestroy(() => {
		if (interval) {
			clearInterval(interval);
		}
	});

	const words = testSequences[$testSequence].split(' ');
	const userInput = words.map((word) => Array(word.length).fill(0));
	let currentWord = 0;
	let currentLetter = 0;
	let totalEnteredCharacters = 0;

	const handleInput = (event: Event) => {
		if (finished) {
			return;
		}

		const target = event.target as HTMLInputElement;
		const inputEvent = event as InputEvent;

		if (startTime === 0) {
			target.value = inputEvent.data ?? '';
			startTime = Date.now();
		}

		const actualLen = words[currentWord].length;

		if (
			$video &&
			inputEvent.data &&
			inputEvent.data === words[currentWord][target.value.length - 1]
		) {
			const key = keyMap?.[inputEvent.data as keyof typeof keyMap] ?? inputEvent.data.toUpperCase();
			$inputData = { coordinates: $edgeCoordinates?.[key] ?? null, key: inputEvent.data };

			setTimeout(() => {
				if (!$video) {
					return;
				}

				$hands?.send({ image: $video });
			}, 10);
		}

		totalEnteredCharacters += 1;

		if (inputEvent.data === ' ' && userInput[currentWord].join('') === words[currentWord]) {
			currentWord += 1;
			target.value = '';

			return;
		}

		userInput[currentWord] = target.value.split('');
		currentLetter = target.value.length - 1;
		const difference = actualLen - userInput[currentWord].length;

		if (difference > 0) {
			userInput[currentWord] = userInput[currentWord].concat(Array(difference).fill(0));
		}
	};

	$: {
		if (
			!$fingersDetected.includes(expectedKeys[$inputData.key as keyof typeof expectedKeys]) &&
			startTime > 0
		) {
			userInput[currentWord][currentLetter] = 1;
			console.log(userInput);
		}
	}
</script>

<div class="test-area">
	<Timer {elapsedTime} />
	<div class="container">
		<Words {userInput} />
		<Caret {currentWord} {userInput} {focused} />
		<Input
			on:input={handleInput}
			on:focus={() => (focused = true)}
			on:blur={() => (focused = false)}
		/>
	</div>
</div>

<style scoped lang="postcss">
	.test-area {
		@apply w-3/6;
	}

	.container {
		@apply w-full
     relative
		 h-6;
	}
</style>
