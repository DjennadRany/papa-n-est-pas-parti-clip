"""Remove filename cartouches baked into transition storyboard JPGs 25–48.

Only the original image's top-left *white label glyphs* are targeted; natural
scene titles (e.g. writing inside a notebook) elsewhere remain untouched.
Keeps original files unmodified; outputs prepared JPG files for AI generation.
"""
from pathlib import Path
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"public/assets/images"
DEST=ROOT/"public/assets/prepared"
DEST.mkdir(parents=True,exist_ok=True)

def clean(source,target):
    image=cv2.imread(str(source))
    if image is None: raise RuntimeError(f"Unreadable image: {source}")
    h,w=image.shape[:2]
    roi=image[:int(h*0.24),:int(w*0.50)]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    white=((hsv[:,:,1]<80)&(hsv[:,:,2]>190)).astype("uint8")*255
    n,labels,stats,_=cv2.connectedComponentsWithStats(white)
    mask=np.zeros((h,w),dtype=np.uint8)
    for component in range(1,n):
        x,y,cw,ch,area=stats[component]
        # Exact visible filenames NN.jpg occupy the first upper-left quadrant.
        if 3<=area<=450 and y<h*0.18 and x<w*0.43 and ch<=h*0.14:
            section=mask[y:y+ch,x:x+cw]
            section[:]=np.maximum(section,(labels[y:y+ch,x:x+cw]==component).astype("uint8")*255)
    mask=cv2.dilate(mask,np.ones((7,7),dtype=np.uint8),iterations=1)
    prepared=cv2.inpaint(image,mask,3,cv2.INPAINT_TELEA)
    if not cv2.imwrite(str(target),prepared,[cv2.IMWRITE_JPEG_QUALITY,96]):
        raise RuntimeError(f"Could not save {target}")
    return int(np.count_nonzero(mask))

if __name__=="__main__":
    for i in range(25,49):
        src=SOURCE/f"{i:02d}.jpg"
        if not src.is_file():raise SystemExit(f"Missing illustration {src}")
        pixels=clean(src,DEST/src.name)
        print(f"Prepared scene {i:02d}; removed {pixels} filename/text pixels",flush=True)
