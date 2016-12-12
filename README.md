# encfile
fastest file enc tool

##Purpose
* Encode/decode a file/files simply and fast
* Support multi-layer encode/decode.

##Priciple
By modifying file header, one could not open it properly.
(normal txt file wont be affected, while compress it would be better)

##Drawback
Simple,too simple.

##Usage
```
chmod 755 encfile.py
ln -s encfile.py /usr/bin/encfile
#encode a file
encfile enc /path/to/the/file.ext
#decode
encfile dec /path/to/the/encoded_file.ixb
#encode files in a folder recursively
encfile enc -R /path/to/folder
#decode files in a folder recursively
encfile dec -R /path/to/folder
```

##Lang
Python
