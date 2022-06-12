import { writable } from 'svelte/store';

export const testSequence = writable<number>(0);
export const timeElapsed = writable<number>(0);
export const totalCharactersTyped = writable<number>(0);
export const inputData = writable<{
	coordinates: TeeCubed.Key | null;
	key: string;
	currentLetter: number;
}>({
	coordinates: null,
	key: 'Z',
	currentLetter: 0
});
