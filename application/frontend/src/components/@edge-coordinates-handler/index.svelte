<script lang="ts">
	import { photo, edgeCoordinates } from 'src/store/edge-coordinates';
	import Camera from 'src/components/@edge-coordinates-handler/camera.svelte';

	const fetchCoordinates = async () => {
		const startTime = Date.now();
		try {
			const response = await fetch('http://127.0.0.1:5000/edge-coordinates', {
				method: 'POST',
				cache: 'no-cache',
				headers: {
					'Content-Type': 'application/json'
				},
				mode: 'cors',
				body: JSON.stringify({
					image: $photo
				})
			});
			const json = await response.json();
			$edgeCoordinates = json.coordinates;
			// 			console.log(Date.now() - startTime);
		} catch (err) {
			console.log(err);
		}
	};

	$: {
		if ($photo !== null) {
			fetchCoordinates();
		}
	}
</script>

{#if !$edgeCoordinates}
	<div class="coordinates-handler">
		<div class="modal">
			{#if !$photo}
				<Camera />
			{/if}
			{#if $photo}
				<h2 class="loading">Calculating Edge Coordinates</h2>
			{/if}
		</div>
	</div>
{/if}

<style lang="postcss">
	.coordinates-handler {
		@apply fixed inset-0 bg-gray-900/50 flex items-center justify-center z-50;
	}

	.modal {
		@apply p-8 bg-gray-800 rounded shadow min-h-[60%] min-w-[60%] flex items-center justify-center;
	}

	.loading {
		@apply text-lg text-gray-50;
	}
</style>
