import os
import numpy as np
import tensorflow as tf
from decimal import Decimal


class ModelInterface():
  
  session = None
  graph_file = "graph.pb"
  inference_tensor = None
  input_tensor = None
  input_mapper = [
    "feature_1",
    "feature_2"
  ]
  output_mapper = [
    "output_1",
    "output_2"
  ]
  
  def __init__(self):  
    with tf.Session() as session:    
      # Load the graph.
      with tf.gfile.FastGFile(self.graph_file, "rb") as f:
          graph_def = tf.GraphDef()
          graph_def.ParseFromString(f.read())
          tf.import_graph_def(graph_def, name="")
  
      # Get the model's variables.
      W = sess.graph.get_tensor_by_name("model/W:0")
      b = sess.graph.get_tensor_by_name("model/b:0")
  
      # Load the saved variables from the checkpoint back into the session.
      saver = tf.train.Saver([W, b])
      saver.restore(session, "model")
      
      # Session Information
      self.session = session
      self.input_tensor = sess.graph.get_tensor_by_name("inputs/x-input:0")
      self.inference_tensor = session.graph.get_tensor_by_name("inference/inference:0")
    
  
  def prediction(self, input):
    # Map Input
    input_tensor = []
    for feature in self.input_mapper:
      input_tensor.append(input[feature])
      
    # Fetch Inference
    inference = self.session.run(self.inference_tensor, feed_dict={
      self.input_tensor: [input_tensor]
    })[0]
    
    # Map Output
    output = {}
    for i, feature in enumerate(inference):
      feature_name = self.output_mapper[i]
      output[feature_name] = Decimal(str(feature))
      
    return {}

