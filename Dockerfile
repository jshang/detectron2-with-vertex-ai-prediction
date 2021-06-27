FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-devel
USER root
ENV APP /app
WORKDIR $APP

RUN apt-get update && apt-get install -y --no-install-recommends locales \
	binutils \
	apt-utils \
	libproj-dev \
	libgdal-dev \
	libgl1-mesa-glx \
	git \
	&& pip install --no-cache-dir \
    autopep8 \
    flake8 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install detectron2 -f \
    https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.8/index.html

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python3", "demoapp/app.py", "--config-file", "detectron2/configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml"]
