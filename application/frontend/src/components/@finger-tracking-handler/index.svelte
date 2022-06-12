<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	import type { Results } from '@mediapipe/hands';
	import mpHands from '@mediapipe/hands';

	import { hands, video, result } from 'src/store/mediapipe';
	import { inputData } from 'src/store/test-sequence';

	const width = 1280;
	const height = 720;
	const fingerTips = [4, 8, 12, 16, 20];
	const fingerTipLabel = { 4: 'THUMB', 8: 'INDEX', 12: 'MIDDLE', 16: 'RING', 20: 'PINKY' };

	let canvas: HTMLCanvasElement;

	const onResults = (results: Results): void => {
		const context = canvas.getContext('2d');

		if (!context) {
			return;
		}

		context.save();
		context.clearRect(0, 0, width, height);
		context.drawImage(results.image, 0, 0, width, height);

		const tempResults: string[] = [];

		if (!$inputData.coordinates) {
			console.error('no coords');
			return;
		}

		if (results.multiHandLandmarks && results.multiHandedness) {
			for (let index = 0; index < results.multiHandLandmarks.length; index++) {
				const classification = results.multiHandedness[index];
				const landmarks = results.multiHandLandmarks[index];

				context.fillStyle = 'red';
				for (const point of $inputData.coordinates!) {
					context.fillRect(point[0], point[1], 5, 5);
				}

				for (const landmarkIndex of fingerTips) {
					const landmark = landmarks[landmarkIndex];
					const x = Math.round(landmark.x * width);
					const y = Math.round(landmark.y * height);

					if (x < $inputData.coordinates![0][0] && x < $inputData.coordinates![3][0]) {
						continue;
					}

					if (x > $inputData.coordinates![1][0] && x > $inputData.coordinates![2][0]) {
						continue;
					}

					if (y < $inputData.coordinates![0][1] && y < $inputData.coordinates![1][1]) {
						continue;
					}

					if (y > $inputData.coordinates![2][1] && y > $inputData.coordinates![3][1]) {
						continue;
					}

					context.fillStyle = 'blue';
					context.fillRect(x, y, 5, 5);

					const label = classification.label === 'Right' ? 'LEFT' : 'RIGHT';
					const landmarkName = fingerTipLabel[landmarkIndex as keyof typeof fingerTipLabel];

					tempResults.push(`${label}_${landmarkName}`);
				}
			}

			$result = {
				currentLetter: $inputData.currentLetter,
				key: $inputData.key,
				fingersDetected: tempResults
			};
		}

		context.restore();
	};

	onMount(() => {
		$hands = new mpHands.Hands({
			locateFile: (file: string) => `./mediapipe-hands/${file}`
		});

		if (!$hands) {
			return;
		}

		$hands.setOptions({
			maxNumHands: 4,
			modelComplexity: 1,
			minDetectionConfidence: 0.5,
			minTrackingConfidence: 0.5
		});
		$hands.onResults(onResults);
	});

	onMount(() => {
		navigator.mediaDevices
			.getUserMedia({
				video: {
					width: { ideal: width },
					height: { ideal: height }
				},
				audio: false
			})
			.then((stream) => {
				if (!$video) {
					return;
				}

				$video.srcObject = stream;
				$video.play();

				$hands?.send({ image: $video });
			})
			.catch((err) => {
				console.error(err);
			});
	});

	let interval: NodeJS.Timer | null = null;

	onDestroy(() => {
		if (interval) {
			clearInterval(interval);
		}
	});
</script>

<div class="finger-tracking">
	<video class="" bind:this={$video} {width} {height} />
	<canvas class="canvas" {width} {height} bind:this={canvas} />
</div>

<style lang="postcss">
	.finger-tracking {
		@apply fixed bottom-6 flex items-end justify-center;
	}

	.canvas {
		@apply origin-bottom;
	}
</style>
