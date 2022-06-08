import { writable } from 'svelte/store';

import type { Hands } from '@mediapipe/hands';

export const hands = writable<Hands | null>(null);
export const video = writable<HTMLVideoElement | null>(null);
export const result = writable<{
	fingersDetected: string[];
	key: string;
	currentLetter: number;
}>({
	fingersDetected: ['LEFT_PINKY'],
	key: 'Z',
	currentLetter: -1
});
