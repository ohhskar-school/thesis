<script lang="ts">
	import { testSequences } from 'src/constants/test-sequences';
	import { testSequence } from 'src/store/test-sequence';

	const words = testSequences[$testSequence].split(' ');

	export let userInput: (string | null)[][];
	export let wrongFingers: boolean[][];

	$: console.log(userInput);
</script>

<div class="container">
	<div class="words">
		{#each userInput as word, wordIndex}
			{#each word as letter, letterIndex}
				{#if wrongFingers[wordIndex][letterIndex]}
					<div class="letter text-purple-600">
						{words[wordIndex][letterIndex]}
					</div>
				{:else}
					<div
						class="letter"
						class:text-gray-50={letter === words[wordIndex][letterIndex]}
						class:text-gray-600={letter === null}
						class:text-red-600={letter !== null && letter !== words[wordIndex][letterIndex]}
					>
						{words[wordIndex]?.[letterIndex] ?? letter}
					</div>
				{/if}
			{/each}

			<div class="letter" />
		{/each}
	</div>
</div>

<style scoped lang="postcss">
	.container {
		@apply w-full h-full relative z-0;
	}

	.words {
		@apply absolute inset-0 text-lg flex flex-wrap;
	}

	.letter {
		@apply w-3 block;
	}
</style>
