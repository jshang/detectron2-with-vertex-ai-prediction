FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-devel
USER root
ENV APP /app
WORKDIR $APP

RUN git clone --branch v0.4.1 https://github.com/facebookresearch/detectron2 detectron2_repo && \
	pip install -e detectron2_repo

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python3", "demoapp/app.py", "--config-file", "detectron2_repo/configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml"]
