/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace TeeCubed {
	type Coordinate = [number, number];
	type Key = [Coordinate, Coordinate, Coordinate, Coordinate];
	type Map = Record<string, Key>;
	// interface Locals {}
	// interface Platform {}
	// interface Session {}
	// interface Stuff {}
}
