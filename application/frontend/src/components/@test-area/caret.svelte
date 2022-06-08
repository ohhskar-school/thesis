<script lang="ts">
	export let currentWord = 0;
	export let userInput: (string | null)[][];
	export let focused: boolean = false;

	let clientWidth: number = 0;

	$: totalCharacters =
		userInput.slice(0, currentWord).reduce((acc, curr) => acc + curr.length, 0) + currentWord;

	$: left =
		clientWidth * (totalCharacters + userInput[currentWord].filter((el) => el !== null).length);
</script>

<div class="container">
	<div bind:clientWidth class="caret" style={`left: ${left}px`}>
		<div class="line" class:opacity-0={!focused} />
	</div>
</div>

<style scoped lang="postcss">
	.container {
		@apply absolute inset-0 z-40;
	}

	.caret {
		@apply absolute block w-3 h-6 left-0 top-0;
	}

	.line {
		@apply absolute left-0 inset-y-0 w-px bg-sky-400 transition-opacity;
	}
</style>
