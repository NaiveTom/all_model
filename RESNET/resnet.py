import tensorflow as tf
from residual_block import *



# 第二个文件：resnet.py



# 分类数量，这里要分成2类，所以用2
NUM_CLASSES = 2



KERNEL_SIZE = 24 # 基本块大小24
STRIDES = 2 # 隔开2



# 第一类ResNet，适用于18或34
class ResNetTypeI(tf.keras.Model):
    def __init__(self, layer_params):
        super(ResNetTypeI, self).__init__()

        self.conv1 = tf.keras.layers.Conv2D(filters = 64,
                                            kernel_size = (KERNEL_SIZE, 1),
                                            strides = STRIDES,
                                            padding = 'same')
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPool2D(pool_size = (2, 1),
                                               strides = STRIDES,
                                               padding = 'same')

        self.layer1 = make_basic_block_layer(filter_num = 64,
                                             blocks = layer_params[0],
                                             stride = 4)
        self.layer2 = make_basic_block_layer(filter_num = 64,
                                             blocks = layer_params[1],
                                             stride = 4)
        self.layer3 = make_basic_block_layer(filter_num = 64,
                                             blocks = layer_params[2],
                                             stride = 4)
        self.layer4 = make_basic_block_layer(filter_num = 64,
                                             blocks = layer_params[3],
                                             stride = 4)

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        self.fc = tf.keras.layers.Dense(units = NUM_CLASSES, activation = tf.keras.activations.softmax)

    def call(self, inputs, training = None, mask = None):
        x = self.conv1(inputs)
        x = self.bn1(x, training = training)
        x = tf.nn.relu(x)
        x = self.pool1(x)
        x = self.layer1(x, training = training)
        x = self.layer2(x, training = training)
        x = self.layer3(x, training = training)
        x = self.layer4(x, training = training)
        x = self.avgpool(x)
        output = self.fc(x)

        return output


    
# 第二类ResNet，适用于50或101或152
class ResNetTypeII(tf.keras.Model):
    def __init__(self, layer_params):
        super(ResNetTypeII, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(filters = 64,
                                            kernel_size = (7, 7),
                                            strides = 2,
                                            padding = 'same')
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPool2D(pool_size = (3, 3),
                                               strides = 2,
                                               padding = 'same')

        self.layer1 = make_bottleneck_layer(filter_num = 64,
                                            blocks = layer_params[0])
        self.layer2 = make_bottleneck_layer(filter_num = 128,
                                            blocks = layer_params[1],
                                            stride = 2)
        self.layer3 = make_bottleneck_layer(filter_num = 256,
                                            blocks = layer_params[2],
                                            stride = 2)
        self.layer4 = make_bottleneck_layer(filter_num = 512,
                                            blocks = layer_params[3],
                                            stride = 2)

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        self.fc = tf.keras.layers.Dense(units = NUM_CLASSES, activation = tf.keras.activations.softmax)

    def call(self, inputs, training = None, mask = None):
        x = self.conv1(inputs)
        x = self.bn1(x, training = training)
        x = tf.nn.relu(x)
        x = self.pool1(x)
        x = self.layer1(x, training = training)
        x = self.layer2(x, training = training)
        x = self.layer3(x, training = training)
        x = self.layer4(x, training = training)
        x = self.avgpool(x)
        output = self.fc(x)

        return output



# 不同大小的声明函数，注意，到了152就已经到头了，再大意义不大了，所以平时用用50或者101就行了
# 这里的设置以图片为准
def resnet_18():
    return ResNetTypeI(layer_params = [2, 2, 2, 2])

def resnet_34():
    return ResNetTypeI(layer_params = [3, 4, 6, 3])

def resnet_50():
    return ResNetTypeII(layer_params = [3, 4, 6, 3])

def resnet_101():
    return ResNetTypeII(layer_params = [3, 4, 23, 3])

def resnet_152():
    return ResNetTypeII(layer_params = [3, 8, 36, 3])
