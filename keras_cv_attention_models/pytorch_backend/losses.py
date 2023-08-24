import torch

epsilon = 1e-7


class Loss:
    def __init__(self, reduction="AUTO", name=None):
        pass

    def __call__(self, y_true, y_pred, sample_weight=None):
        pass


def categorical_crossentropy(y_true, y_pred, from_logits=False, label_smoothing=0.0, axis=-1):
    """
    # from_logits=False
    >>> import torch, tensorflow as tf
    >>> from keras_cv_attention_models.pytorch_backend import losses
    >>> xx, yy = tf.random.uniform([24, 10]), tf.one_hot(tf.random.uniform([24], 0, 10, dtype='int32'), 10)
    >>> tf_out = keras.losses.categorical_crossentropy(yy, xx, from_logits=False).numpy().mean()
    >>> torch_out = losses.categorical_crossentropy(torch.from_numpy(yy.numpy()), torch.from_numpy(xx.numpy()), from_logits=False)
    >>> print(tf_out, torch_out, np.allclose(tf_out, torch_out))
    >>> # 2.681877 tensor(2.6819) True
    # from_logits=True
    >>> tf_out = keras.losses.categorical_crossentropy(yy, xx, from_logits=True).numpy().mean()
    >>> torch_out = losses.categorical_crossentropy(torch.from_numpy(yy.numpy()), torch.from_numpy(xx.numpy()), from_logits=True)
    >>> print(tf_out, torch_out, np.allclose(tf_out, torch_out))
    >>> # 2.3364408 tensor(2.3364) True
    """
    if from_logits:
        return torch.nn.functional.cross_entropy(y_pred, y_true.argmax(-1), label_smoothing=label_smoothing)
    else:
        y_pred = y_pred / y_pred.sum(dim=axis, keepdim=True)
        y_pred = y_pred.clamp_(epsilon, 1.0 - epsilon)
        return -(y_true * y_pred.log()).sum(dim=axis).mean()


def sparse_categorical_crossentropy(y_true, y_pred, from_logits=False, label_smoothing=0.0, axis=-1):
    """
    # from_logits=False
    >>> import torch, tensorflow as tf
    >>> from keras_cv_attention_models.pytorch_backend import losses
    >>> xx, yy = tf.random.uniform([24, 10]), tf.random.uniform([24], 0, 10, dtype='int64')
    >>> tf_out = keras.losses.sparse_categorical_crossentropy(yy, xx, from_logits=False).numpy().mean()
    >>> torch_out = losses.sparse_categorical_crossentropy(torch.from_numpy(yy.numpy()), torch.from_numpy(xx.numpy()), from_logits=False)
    >>> print(tf_out, torch_out, np.allclose(tf_out, torch_out))
    >>> # 2.677911 tensor(2.6779) True
    # from_logits=True
    >>> tf_out = keras.losses.sparse_categorical_crossentropy(yy, xx, from_logits=True).numpy().mean()
    >>> torch_out = losses.sparse_categorical_crossentropy(torch.from_numpy(yy.numpy()), torch.from_numpy(xx.numpy()), from_logits=True)
    >>> print(tf_out, torch_out, np.allclose(tf_out, torch_out))
    >>> # 2.3503969 tensor(2.3504) True
    """
    if from_logits:
        return torch.nn.functional.cross_entropy(y_pred, y_true, label_smoothing=label_smoothing)
    else:
        y_pred = y_pred / y_pred.sum(dim=axis, keepdim=True)
        y_pred = y_pred.clamp_(epsilon, 1.0 - epsilon)
        y_true = torch.nn.functional.one_hot(y_true, y_pred.shape[-1])
        return -(y_true * y_pred.log()).sum(dim=axis).mean()
