
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

import numpy as np
import random

# For our custom calibrator
from calibrator import load_mnist_data, load_mnist_labels, MNISTEntropyCalibrator

# For ../common.py
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], os.path.pardir))
import common

TRT_LOGGER = trt.Logger()


class ModelData(object):
    DEPLOY_PATH = "deploy.prototxt"
    MODEL_PATH = "mnist_lenet.caffemodel"
    OUTPUT_NAME = "prob"
    # The original model is a float32 one.
    DTYPE = trt.float32


# This function builds an engine from a Caffe model.
def build_int8_engine(deploy_file, model_file, calib, batch_size=32):
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network() as network, trt.CaffeParser() as parser:
        # We set the builder batch size to be the same as the calibrator's, as we use the same batches
        # during inference. Note that this is not required in general, and inference batch size is
        # independent of calibration batch size.
        builder.max_batch_size = batch_size
        builder.max_workspace_size = common.GiB(1)
        builder.int8_mode = True
        builder.int8_calibrator = calib
        # Parse Caffe model
        model_tensors = parser.parse(deploy=deploy_file, model=model_file, network=network, dtype=ModelData.DTYPE)
        network.mark_output(model_tensors.find(ModelData.OUTPUT_NAME))
        
        # Build engine and do int8 calibration.
        return builder.build_cuda_engine(network)


def check_accuracy(context, batch_size, test_set, test_labels):
    inputs, outputs, bindings, stream = common.allocate_buffers(context.engine)

    num_correct = 0
    num_total = 0

    batch_num = 0
    for start_idx in range(0, test_set.shape[0], batch_size):
        batch_num += 1
        if batch_num % 10 == 0:
            print("Validating batch {:}".format(batch_num))
        # If the number of images in the test set is not divisible by the batch size, the last batch will be smaller.
        # This logic is used for handling that case.
        end_idx = min(start_idx + batch_size, test_set.shape[0])
        effective_batch_size = end_idx - start_idx

        # Do inference for every batch.
        inputs[0].host = test_set[start_idx:start_idx + effective_batch_size]
        [output] = common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, batch_size=effective_batch_size)

        # Use argmax to get predictions and then check accuracy
        preds = np.argmax(output.reshape(32, 10)[0:effective_batch_size], axis=1)
        labels = test_labels[start_idx:start_idx + effective_batch_size]
        num_total += effective_batch_size
        num_correct += np.count_nonzero(np.equal(preds, labels))

    percent_correct = 100 * num_correct / float(num_total)
    print("Total Accuracy: {:}%".format(percent_correct))

def main():
    _, data_files = common.find_sample_data(description="Runs a TF resnet50 network in Int8 mode", subfolder="./", find_files=["./", "./", "./", ModelData.DEPLOY_PATH, ModelData.MODEL_PATH])
    [test_set, test_labels, train_set, deploy_file, model_file] = data_files

    # Now we create a calibrator and give it the location of our calibration data.
    # We also allow it to cache calibration data for faster engine building.
    calibration_cache = "mnist_calibration.cache"
    calib = MNISTEntropyCalibrator(test_set, cache_file=calibration_cache)

    # Inference batch size can be different from calibration batch size.
    batch_size = 32
    with build_int8_engine(deploy_file, model_file, calib, batch_size) as engine, engine.create_execution_context() as context:
        # Batch size for inference can be different than batch size used for calibration.
        check_accuracy(context, batch_size, test_set=load_mnist_data(test_set), test_labels=load_mnist_labels(test_labels))

if __name__ == '__main__':
    main()