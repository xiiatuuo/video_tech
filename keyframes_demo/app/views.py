from flask import render_template, flash, redirect
from app import app
from .forms import SubmitForm
import time
from hashlib import md5
import os
from video_utils import obtain_online_video
from video_utils import obtain_video_keyframes
from video_utils import obtain_local_frames
from video_utils import obtain_video_ratio 
from entropy_keyframe import obtain_all_entropy_list
from entropy_keyframe import obtain_duration_entropy_list
from config import basedir
from keyframe import KeyFrame




@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

def packge_result(a, b):
    n = max(len(a), len(b))
    new_list = []
    for i in xrange(n):
        d = {}
        if i < len(a):
            d["entropy"] = a[i]
        else:
            d["entropy"] = ""
        if i < len(b):
            d["gray_pixel"] = b[i]
        else:
            d["gray_pixel"] = ""
        new_list.append(d)
    return new_list
    

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        flash('submit requested for url =' + str(form.url.data))
        kf = KeyFrame(form.url.data)
        download_flag , info = kf.download_video()
        if not download_flag:
            return render_template('submit.html', title='Submit', form=form, error=info)

        entropy_images_path, info = kf.entropy_based()
        if not entropy_images_path:
            return render_template('submit.html', title='Submit', form=form, error=info)

        gray_pixel_images_path = []
        gray_pixel_images_path, info = kf.gray_pixel_based()
        if not gray_pixel_images_path:
            return render_template('submit.html', title='Submit', form=form, error=info)

        images_path  = packge_result(entropy_images_path, gray_pixel_images_path)

        return render_template('result.html', title='Result', images_path=images_path)

    return render_template('submit.html', title='Submit', form = form, error="")

'''
if __name__ == "__main__":
    print get_image_path("http://weibo.com/p/230444463048de15f7ff201eba91cfff16ec41")
'''
