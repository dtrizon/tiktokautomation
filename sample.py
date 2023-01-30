import cv2
from datetime import datetime

video1 = cv2.VideoCapture("""d:\Downloads\Snaptik.app_7179120535735962923.mp4""")
video2 = cv2.VideoCapture("""D:\Videos\AceHighlights\Clutch2.mp4""")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
now = datetime.now()
currentTime = now.strftime("%H-%M-%S")
fps = video1.get(cv2.CAP_PROP_FPS)

if not video1.isOpened():
    print("error")
else:
    retwhat, firstF = video1.read()
    print(firstF.shape[1])
    video_writer = cv2.VideoWriter(f"{currentTime}.avi", fourcc, fps, (firstF.shape[1], firstF.shape[0]))

while video1.isOpened():
    ret1, img = video1.read()
    ret2, frame2 = video2.read()

    if ret1 == False:
        print("what")
        break
    """
    frame1 = cv2.resize(frame1, (1080,960))
    frame2 = cv2.resize(frame2, (1080,960))
    vid_comb = cv2.vconcat([frame1, frame2])

    cv2.imshow('Frame', vid_comb)
    #video_writer.write(vid_comb)
    """
    scale_percent = 125 # percentage of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # Resize the image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    # Crop the image to get the zoomed portion
    start_row, start_col = int((height - img.shape[0]) / 2), int((width - img.shape[1]) / 2)
    end_row, end_col = start_row + img.shape[0], start_col + img.shape[1]
    end_rowF = int((img.shape[0] * .67) + start_row)
    #print(img.shape[0])
    zoomed = resized[start_row:end_rowF, start_col:end_col]
    #print(zoomed.shape[1])
    end_rowF2 = int(img.shape[0] * .33)
    #print(end_rowF2)
    frame2 = cv2.resize(frame2, (img.shape[1],end_rowF2))

    vid_comb = cv2.vconcat([zoomed, frame2])
    #print(vid_comb.shape[0])
    

    if vid_comb.shape[0] != img.shape[0]:
        vid_comb = cv2.resize(vid_comb, (img.shape[1], img.shape[0]))
    video_writer.write(vid_comb)
    #cv2.imshow('Frame', vid_comb)
        
    if cv2.waitKey(25) & 0xff == ord('q'):
        break

video_writer.release()
video1.release()
video2.release()
cv2.destroyAllWindows()

# Calculate the scaling factor
