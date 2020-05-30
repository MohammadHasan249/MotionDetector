import cv2
from datetime import datetime
import pandas

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # start capturing video
first_frame = None
statuses = [None, None]
times = []
df = pandas.DataFrame(columns=['Start', 'End'])

while True:

    check, frame = video.read()  # read frame by frame
    status = 0  # checking if motion is detected or not
    # make current frame greyed out and blur it for more accuracy
    grayed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayed_frame = cv2.GaussianBlur(grayed_frame, (21, 21), 0)

    # keep the "background" image the same throughout - the first frame read
    # this image is compared to every other frame to detect differences, and
    # thus, motion
    if first_frame is None:
        first_frame = grayed_frame
        continue

    # find the differences between the "background" image and the current frame
    delta_frame = cv2.absdiff(first_frame, grayed_frame)
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 10000:
            continue
        status = 1
        x, y, h, w = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    statuses.append(status)
    if (statuses[-1] == 1 and statuses[-2] == 0) or\
            (statuses[-1] == 0 and statuses[-2] == 1):
        times.append(datetime.now())

    # cv2.imshow("Delta Frame", delta_frame)
    # cv2.imshow("Grayed Frame", grayed_frame)
    # cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Capture", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

# print(statuses)
print(times)

for index in range(0, len(times), 2):
    df = df.append({"Start": times[index], "End": times[index + 1]},
                   ignore_index=True)

df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows()
