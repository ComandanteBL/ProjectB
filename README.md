# Requirements:

* requirements file (all anaconda dependencies)
    * conda env export > environment.yml
* tensorflow-gpu 1.14.0 (because of the Keras CuDNNLSTM) https://www.tensorflow.org/install/gpu
* NVIDIA CUDA 10.0 (because of *_100.dll files in /CUDA/v10.0/bin/)
* cuDNN SDK (it is separate installation -> just extract zip to C:\tools\cuda...)

# Adding %PATHS%

Tensorflow will not load without cuDNN64_7.dll file. Add CUDA, CUPTI (comes with CUDA Toolkit) and cuDNN to %PATH% environmental variable.
For example, if the CUDA Toolkit is installed to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1 and cuDNN to C:\tools\cuda, update your %PATH% to match:

```
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras\CUPTI\libx64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\include;%PATH%
SET PATH=C:\tools\cuda\bin;%PATH%
```

If not working add manually in windows paths (user)