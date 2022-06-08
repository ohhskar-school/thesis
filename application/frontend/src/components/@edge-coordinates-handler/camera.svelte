<script lang="ts">
	import { onMount } from 'svelte';
	import { photo } from 'src/store/edge-coordinates';

	const width = 1280;
	const height = 720;

	let video: HTMLVideoElement;
	let canvas: HTMLCanvasElement;

	const clearPhoto = () => {
		const context = canvas.getContext('2d');

		if (!context) {
			return;
		}

		context.fillStyle = '#AAA';
		context.fillRect(0, 0, canvas.width, canvas.height);

		$photo = canvas.toDataURL('image/png');
	};

	const takePicture = () => {
		const context = canvas.getContext('2d');

		if (!context) {
			clearPhoto();

			return;
		}

		canvas.width = width;
		canvas.height = height;
		context.drawImage(video, 0, 0, width, height);

		$photo = canvas.toDataURL('image/png');
	};

	const click = () => {
		takePicture();
	};

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
				video.srcObject = stream;
				video.play();
			})
			.catch((err) => {
				console.error(err);
			});
	});
</script>

<div class="camera">
	<video bind:this={video} {width} {height} />
	<button class="button" on:click={click}>Capture</button>
	<canvas class="hidden" {width} {height} bind:this={canvas} />
</div>

<style lang="postcss">
	.holder {
		@apply fixed inset-0 bg-gray-900/50 flex items-center justify-center z-50;
	}

	.camera {
		@apply flex items-center justify-center flex-col;
	}

	.button {
		@apply mt-4 py-4 px-8 rounded bg-sky-400 hover:bg-sky-600 transition-colors;
	}
</style>
