import os

import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
import keras

tf.keras.backend.set_learning_phase(0)

## Convert frozen graph to tensorrt 
'''
[<tf.Tensor 'softmax_2/truediv:0' shape=(?, 144, 144, 4) dtype=float32>]
[<tf.Tensor 'input_4:0' shape=(?, 144, 144, 3) dtype=float32>]
'''

def get_frozen_graph(graph_file):
  """Read Frozen Graph file from disk."""
  with tf.gfile.FastGFile(graph_file, "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
  return graph_def

def main():
  frozen_graph_def = get_frozen_graph('/home/goodgame/Downloads/tf_model.pb')

  output_nodes = ['predictions/concat:0']
  output_dir = 'tensorrt_dir'

  trt_graph_def = trt.create_inference_graph(
    frozen_graph_def,
    output_nodes,
    max_batch_size=1,
    #max_workspace_size_bytes=(2 << 10) << 20,
    max_workspace_size_bytes = 1 << 32,
    precision_mode='FP16',
    minimum_segment_size = 5
    )
  with tf.gfile.FastGFile("/media/goodgame/3332-323312/SSD/ssd_0312.pb", 'wb') as f:
    f.write(trt_graph_def.SerializeToString())
  print("TensorRT model is successfully stored!")

  # check how many ops of the original frozen model
  all_nodes = len([1 for n in frozen_graph_def.node])
  print("numb. of all_nodes in frozen graph:", all_nodes)

  # check how many ops that is converted to TensorRT engine
  trt_engine_nodes = len([1 for n in trt_graph_def.node if str(n.op) == 'TRTEngineOp'])
  print("numb. of trt_engine_nodes in TensorRT graph:", trt_engine_nodes)
  all_nodes = len([1 for n in trt_graph_def.node])
  print("numb. of all_nodes in TensorRT graph:", all_nodes)


if __name__ == '__main__':
  main()