<script>
	import '../app.css';
</script>

<main class="layout">
	<slot />
</main>

<style lang="postcss">
	.layout {
		@apply min-h-full min-w-full;
	}
</style>
