#!/usr/bin/env python3

from cv2 import cv2 as cv
import mediapipe as mp
import numpy as np

from common import DEBUG

# Heavily lifted from https://google.github.io/mediapipe/getting_started/python.html.
# Cited as (Lugaresi et al., n.d.) in the paper
def classifyPressedFinger(
    image: np.ndarray, roiPoints: np.ndarray
) -> tuple[str, str] | None:

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    image_height, image_width, _ = image.shape

    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5
    ) as hands:
        results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            raise Exception("finger_detection: no landmarks found")

        # Get all possible landmarks that fit witihin the ROI. This is because
        # some landmarks such as INDEX_FINGER_PIP may fall within the ROI, and
        # it is highly unlikely that someone will click using that part of the
        # finger. However, if no other matches are to be found, this is taken as
        # the fallback
        possibleMatches: list[tuple[str, str]] = []

        for handIndex, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[handIndex].classification[0].label

            # Flip handedness. Mediapipe expects the images to be flipped
            # horizontally, much like taking a selfie. However, this wont work
            # for our case
            if handedness == "Left":
                handedness = "Right"
            else:
                handedness = "Left"

            for landmarkIndex, landmark in enumerate(hand_landmarks.landmark):
                x = round(landmark.x * image_width)
                y = round(landmark.y * image_height)
                landmarkName = mp_hands.HandLandmark(landmarkIndex).name

                if DEBUG:
                    print(handedness)
                    print(landmarkName)
                    print(x, y)
                    print(landmark)

                # The following if statements check if the landmark is within
                # the ROI. If it fails, the next landmark is tested

                # In the X axis, the landmark's coordinates is greater than one
                # or both of the two coordinates found on the left side of the
                # ROI
                if x < roiPoints[0][0] and x < roiPoints[3][0]:
                    continue

                # In the X axis, tha landmark's coordinates is less than one or
                # both of the two coordinates found on the right side of the ROI
                if x > roiPoints[1][0] and x > roiPoints[2][0]:
                    continue

                # In the Y axis, the landmark’s coordinates is greater than one
                # or both of the two coordinates found of the top side of the
                # ROI
                if y < roiPoints[0][1] and y < roiPoints[1][1]:
                    continue

                # In the Y axis, the landmark’s coordinates is less than one or
                # both of the two coordinates found of the bottom side of the ROI
                # These conditions maximize the total area of the ROI and is not
                # strict about exact accuracy.
                if y > roiPoints[2][1] and y > roiPoints[3][1]:
                    continue

                if DEBUG:
                    print("CLASSIFIED FINGER")
                    print(landmarkName)
                    print(roiPoints)
                    print(x, y)
                possibleMatches.append((handedness, landmarkName))

            if DEBUG:
                print(
                    f"Index finger tip coordinates: (",
                    f"{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, "
                    f"{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})",
                )
                annotated_image = image.copy()

                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

                cv.imshow("debug", annotated_image)
                cv.waitKey(0)

        # Get all fingertip landmarks
        tipLandmarkMatches = [
            identifier
            for identifier in possibleMatches
            if identifier[1].split("_")[-1] == "TIP"
        ]

        if DEBUG:
            print(possibleMatches)
            print(tipLandmarkMatches)
            cv.waitKey(0)

        if len(tipLandmarkMatches) > 0:
            return tipLandmarkMatches[0]

        # Don't consider fallback. Later if naay instances lang
        # if len(possibleMatches) > 0:
        #     return possibleMatches[0]

        # No fingertip is inside the roi
        return None
