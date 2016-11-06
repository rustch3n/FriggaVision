#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
import os

TEMPLATE_TRAIN = '''
#############################  DATA Layer  #############################
name: "face_train_val"
layer {
  top: "data_1"
  top: "label_1"
  name: "data_1"
  type: "Data"
  data_param {
    source: "../DataPrepare/webface_multi_cropped/%s/train_lmdb"
    backend:LMDB
    batch_size: 128
  }
  transform_param {
     mean_file: "../DataPrepare/webface_multi_cropped/%s/train_mean.binaryproto"
     mirror: true
  }
  include: { phase: TRAIN }
}

layer {
  top: "data_1"
  top: "label_1"
  name: "data_1"
  type: "Data"
  data_param {
    source: "../DataPrepare/webface_multi_cropped/%s/validation_lmdb"
    backend:LMDB
    batch_size: 128
  }
  transform_param {
    mean_file: "../DataPrepare/webface_multi_cropped/%s/train_mean.binaryproto"
    mirror: true
  }
  include: { 
    phase: TEST 
  }
}

#############################  CONV NET 1 #############################
layer {
  name: "conv1_1"
  type: "Convolution"
  bottom: "data_1"
  top: "conv1_1"
  param {
    name: "conv1_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "conv1_b"
    lr_mult: 2
    decay_mult: 0
  }
  convolution_param {
    num_output: 20
    kernel_size: 4
    stride: 1
    weight_filler {
      type: "gaussian"
      std: 0.01
    }
    bias_filler {
      type: "constant"
      value: 0
    }
  }
}
layer {
  name: "relu1_1"
  type: "ReLU"
  bottom: "conv1_1"
  top: "conv1_1"
}
layer {
  name: "norm1_1"
  type: "LRN"
  bottom: "conv1_1"
  top: "norm1_1"
  lrn_param {
    local_size: 5
    alpha: 0.0001
    beta: 0.75
  }
}
layer {
  name: "pool1_1"
  type:  "Pooling"
  bottom: "norm1_1"
  top: "pool1_1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv2_1"
  type: "Convolution"
  bottom: "pool1_1"
  top: "conv2_1"
  param {
    name: "conv2_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "conv2_b"
    lr_mult: 2
    decay_mult: 0
  }
  convolution_param {
    num_output: 40
    kernel_size: 3
    group: 2
    weight_filler {
      type: "gaussian"
      std: 0.01
    }
    bias_filler {
      type: "constant"
      value: 0.1
    }
  }

}
layer {
  name: "relu2_1"
  type: "ReLU"
  bottom: "conv2_1"
  top: "conv2_1"
}
layer {
  name: "norm2_1"
  type: "LRN"
  bottom: "conv2_1"
  top: "norm2_1"
  lrn_param {
    local_size: 5
    alpha: 0.0001
    beta: 0.75
  }
}
layer {
  name: "pool2_1"
  type:  "Pooling"
  bottom: "norm2_1"
  top: "pool2_1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv3_1"
  type: "Convolution"
  bottom: "pool2_1"
  top: "conv3_1"
  param {
    name: "conv3_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "conv3_b"
    lr_mult: 2
    decay_mult: 0
  }
  convolution_param {
    num_output: 60
    kernel_size: 3
    weight_filler {
      type: "gaussian"
      std: 0.01
    }
    bias_filler {
      type: "constant"
      value: 0
    }
  }

}
layer {
  name: "pool3_1"
  type:  "Pooling"
  bottom: "conv3_1"
  top: "pool3_1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv4_1"
  type: "Convolution"
  bottom: "pool3_1"
  top: "conv4_1"
  param {
    name: "conv4_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "conv4_b"
    lr_mult: 2
    decay_mult: 0
  }
  convolution_param {
    num_output: 80
    kernel_size: 2
    stride: 2
    weight_filler {
      type: "gaussian"
      std: 0.01
    }
    bias_filler {
      type: "constant"
      value: 0.1
    }
  }

}
layer{
  name:"flatten_pool3_1"
  type:"Flatten"
  bottom:"pool3_1"
  top:"flatten_pool3_1"
}
layer{
  name:"flatten_conv4_1"
  type:"Flatten"
  bottom:"conv4_1"
  top:"flatten_conv4_1"
}
layer{
  name:"contact_conv"
  type:"Concat"
  bottom:"flatten_conv4_1"
  bottom:"flatten_pool3_1"
  top:"contact_conv"
}
layer {
  name: "deepid_1"
  type:  "InnerProduct"
  bottom: "contact_conv"
  top: "deepid_1"
  param {
    name: "fc6_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "fc6_b"
    lr_mult: 2
    decay_mult: 0
  }
  inner_product_param {
    num_output: 160
    weight_filler {
      type: "gaussian"
      std: 0.005
    }
    bias_filler {
      type: "constant"
      value: 0.1
    }
  }

}
layer {
  name: "relu6_1"
  type: "ReLU"
  bottom: "deepid_1"
  top: "deepid_1"
}
layer {
  name: "drop6_1"
  type:  "Dropout"
  bottom: "deepid_1"
  top: "deepid_1"
  dropout_param {
    dropout_ratio: 0.5
  }
}

layer {
  name: "fc8_1"
  type:  "InnerProduct"
  bottom: "deepid_1"
  top: "fc8_1"
  param {
    name: "fc8_w"
    lr_mult: 1
    decay_mult: 1
  }
  param {
    name: "fc8_b"
    lr_mult: 2
    decay_mult: 0
  }
  inner_product_param {
    num_output: 10575
    weight_filler {
      type: "gaussian"
      std: 0.01
    }
    bias_filler {
      type: "constant"
      value: 0
    }
  }

}

layer {
  name: "accuracy_1"
  type:  "Accuracy"
  bottom: "fc8_1"
  bottom: "label_1"
  top: "accuracy_1"
  include: { phase: TEST }
}
layer {
  name: "loss_1"
  type:  "SoftmaxWithLoss"
  bottom: "fc8_1"
  bottom: "label_1"
  top: "loss_1"
  #loss_weight: 0.5
}

'''


TEMPLATE_SOLVER = '''
net: "%s"
test_iter: 100
test_interval: 1000

#type: "RMSProp"
base_lr: 0.001
lr_policy: "step"
gamma: 0.95
stepsize:  100000
momentum: 0.9
weight_decay: 0.0005

display: 100
max_iter:  500000
snapshot:  100000
snapshot_prefix: "./snapshot_%s_"
solver_mode: GPU
#debug_info: true

'''


def gen_net(patch_name):
    text = TEMPLATE_TRAIN % (patch_name, patch_name, patch_name, patch_name)
    # print text
    fn_net = "webface_train_%s.prototxt" % patch_name
    with open(fn_net, 'w') as f_out:
        f_out.write(text + "\n")
    
    solver_text = TEMPLATE_SOLVER % (fn_net, patch_name)
    fn_solver = "webface_solver_%s.prototxt" % patch_name
    with open(fn_solver, 'w') as f_out:
        f_out.write(solver_text + "\n")
    

if __name__ == "__main__":
    patch_name = sys.argv[1]
    print "gen net: ", patch_name
    gen_net(patch_name)
