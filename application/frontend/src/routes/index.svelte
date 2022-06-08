<script lang="ts">
	import EdgeCoordinatesHandler from 'src/components/@edge-coordinates-handler/index.svelte';
	import FingerTrackingHandler from 'src/components/@finger-tracking-handler/index.svelte';
	import TestArea from 'src/components/@test-area/index.svelte';
</script>

<div class="test">
	<EdgeCoordinatesHandler />
	<TestArea />
	<FingerTrackingHandler />
</div>

<style lang="postcss">
	.test {
		@apply h-screen w-full flex pt-32 justify-center;
	}
</style>
