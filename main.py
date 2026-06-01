import sys
import numpy as np
import cv2




def make_fake_runway():
    
    img = np.zeros((480, 640, 3), np.uint8)
    img[:240] = (120, 90, 60)     # "sky/ground" top
    img[240:] = (40, 40, 40)      
    cv2.line(img, (180, 480), (300, 250), (220, 220, 220), 6)
    cv2.line(img, (460, 480), (340, 250), (220, 220, 220), 6)
    # dashed center line
    for y in range(260, 480, 40):
        cv2.line(img, (320, y), (320, y + 20), (230, 230, 0), 3)
    return img


def detect(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 200)

    # only look at bottom half 
    mask = np.zeros_like(edges)
    mask[h // 2:, :] = 255
    edges = cv2.bitwise_and(edges, mask)

    # find straight lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength=60, maxLineGap=40)

    left_x, right_x = [], []
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            if x2 == x1:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.3:   
                continue
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # sort lines into left edge vs right edge by slope direction
            (left_x if slope < 0 else right_x).append((x1 + x2) / 2)

    # estimate runway center and the plane's offset from it
    if left_x and right_x:
        center = (np.mean(left_x) + np.mean(right_x)) / 2
        offset = center - w / 2
        cv2.line(img, (int(center), h), (int(center), h // 2), (0, 200, 255), 2)
        txt = f"runway center off by {offset:+.0f}px  ->  steer {'right' if offset>0 else 'left'}"
        cv2.putText(img, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
    else:
        cv2.putText(img, "runway not found", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return img


def main():
    # use the image you pass, otherwise the fake runway
    if len(sys.argv) > 1:
        img = cv2.imread(sys.argv[1])
    else:
        img = make_fake_runway()

    result = detect(img)
    cv2.imshow("runway detection (any key to close)", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
