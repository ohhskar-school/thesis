<script lang="ts">
	import { onMount } from 'svelte';
	import { testSequence } from 'src/store/test-sequence';

	import {
		testSequenceEnteredCharacters,
		testSequenceCharacters,
		testSequenceWrongCharacters,
		keyPressesHistory,
		wrongKeyPressesHistory
	} from 'src/store/metrics';

	const wrongCharacters = $testSequenceEnteredCharacters - $testSequenceCharacters;
	const acc = (
		(($testSequenceEnteredCharacters - wrongCharacters) / $testSequenceEnteredCharacters) *
		100
	).toFixed(2);
	const fpacc = (
		(($testSequenceEnteredCharacters - $testSequenceWrongCharacters) /
			$testSequenceEnteredCharacters) *
		100
	).toFixed(2);
	const hfpacc = Object.entries($keyPressesHistory).map<[string, number]>(([key, value]) => [
		key,
		(((value - $wrongKeyPressesHistory[key]) / value) * 100).toFixed(2)
	]);

	onMount(() => {
		$testSequence = Math.floor(Math.random() * 9);
	});
</script>

<div class="page">
	<div class="holder">
		<h2 class="h2">ACC</h2>
		<p class="metric">{acc}%</p>
	</div>
	<div class="holder">
		<h2 class="h2">FPACC</h2>
		<p class="metric">{fpacc}%</p>
	</div>
	<div class="holder">
		<h2 class="h2">HFPACC</h2>
		{#each hfpacc as value}
			<p class="metric">{value[0]}: {isNaN(value[1]) ? '-' : `${Math.max(0, value[1])}%`}</p>
		{/each}
	</div>
	<a class="button" href="/">New Test Sequence</a>
</div>

<style scoped lang="postcss">
	.page {
		@apply container mx-auto py-32 flex flex-col justify-center items-start;
	}
	.h2 {
		@apply text-xl text-sky-400 pb-4;
	}

	.metric {
		@apply text-lg text-gray-50;
	}

	.holder {
		@apply mb-8;
	}

	.button {
		@apply block mt-4 py-4 px-8 rounded bg-sky-400 hover:bg-sky-600 transition-colors;
	}
</style>
