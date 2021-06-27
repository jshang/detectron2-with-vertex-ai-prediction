import io
import time
from base64 import b64decode, b64encode

import flask
import numpy as np
from demo import VisualizationDemo, get_parser, setup_cfg
from detectron2.utils.logger import setup_logger
from flask import Flask, request
from PIL import Image

logger = setup_logger()
logger.info("Start initializations...")
app = Flask(__name__)
logger.info("Created app...")
args = get_parser().parse_args()
logger.info("Created args...")
cfg = setup_cfg(args)
logger.info("Created cfg...")
demo = VisualizationDemo(cfg)
logger.info("Created demo... Initialization has done!")


def b64_to_nparray(b64img: str) -> np.array:
    raw = b64decode(b64img)
    buf = io.BytesIO(raw)
    img = Image.open(buf)
    np_img = np.array(img)
    return np_img


def nparray_to_b64(np_img: np.array) -> str:
    img = Image.fromarray(np_img)
    buf = io.BytesIO()
    img.save(buf , format="JPEG")
    byte_b64img = b64encode(buf.getvalue())
    b64img = byte_b64img.decode("utf-8")
    return b64img


@app.route('/predict', methods=["POST"])
def peredict():
    data = request.json["data"]
    b64img = data['b64']
    np_img = b64_to_nparray(b64img)

    start_time = time.time()
    predictions, visualized_output = demo.run_on_image(np_img)
    logger.info(
        "{} in {:.2f}s".format(
        "detected {} instances".format(len(predictions["instances"])) if "instances" in predictions else "finished",
        time.time() - start_time
    ))

    np_img = visualized_output.get_image()
    b64img = nparray_to_b64(np_img)
    boxes = predictions["instances"].pred_boxes.tensor.detach().cpu().numpy().tolist()
    pred_classes = predictions["instances"].pred_classes.detach().cpu().numpy().tolist()
    scores = predictions["instances"].scores.detach().cpu().numpy().tolist()

    return flask.json.jsonify(
        num=len(predictions["instances"]) ,
        boxes=boxes,
        pred_classes=pred_classes,
        b64img=b64img,
        scores=scores)


@app.route('/healthcheck')
def healthcheck():
    return 'alive'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
