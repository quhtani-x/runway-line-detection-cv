# Runway Line Detection (landing assist CV)

A computer-vision landing aid that finds the runway edges and center line from a
camera image, the way a vision-based landing system would. It uses Canny edge
detection + a Hough line transform, sorts the lines into the left and right
runway edges, then works out the runway center and how far off-center the plane
is — and which way to steer.

If you don't pass an image it generates a fake runway so you can see it work
right away.

## run

```bash
pip install opencv-python numpy

python detect.py              # runs on a generated synthetic runway
python detect.py runway.jpg   # runs on your own image
```

tags: ai, computer-vision, opencv, aviation, landing-assist

edge detection + hough lines is a classic CV combo, perfect for lane/runway finding.
