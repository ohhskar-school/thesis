<script lang="ts">
	export let elapsedTime: number;
</script>

<div class="container" class:opacity-0={elapsedTime === -1} class:opacity-100={elapsedTime > -1}>
	<span class="timer">{elapsedTime}</span>
</div>

<style scoped lang="postcss">
	.container {
		@apply pb-4
     transition-opacity;
	}

	.timer {
		@apply text-sm
     text-sky-400;
	}
</style>
