import { writable } from 'svelte/store';

const baseHistory = {
	Q: 0,
	A: 0,
	Z: 0,
	W: 0,
	S: 0,
	X: 0,
	E: 0,
	D: 0,
	C: 0,
	R: 0,
	F: 0,
	V: 0,
	T: 0,
	G: 0,
	B: 0,
	Y: 0,
	H: 0,
	N: 0,
	U: 0,
	J: 0,
	M: 0,
	I: 0,
	K: 0,
	',': 0,
	O: 0,
	L: 0,
	'.': 0,
	P: 0,
	';': 0,
	'/': 0,
	"'": 0,
	'[': 0,
	']': 0,
	Spacebar: 0
};

export const testSequenceEnteredCharacters = writable<number>(0);
export const testSequenceWrongCharacters = writable<number>(0);
export const testSequenceCharacters = writable<number>(0);
export const keyPressesHistory = writable<Record<string, number>>({ ...baseHistory });
export const wrongKeyPressesHistory = writable<Record<string, number>>({ ...baseHistory });
