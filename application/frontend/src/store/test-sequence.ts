import { writable } from 'svelte/store';

export const testSequence = writable<number>(Math.floor(Math.random() * 9));
export const timeElapsed = writable<number>(0);
export const totalCharactersTyped = writable<number>(0);
export const inputData = writable<{ coordinates: TeeCubed.Key | null; key: string }>({
	coordinates: null,
	key: 'z'
});
