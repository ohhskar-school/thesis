import { writable } from 'svelte/store';

export const photo = writable<string | null>(null);
export const edgeCoordinates = writable<TeeCubed.Map | null>(null);
