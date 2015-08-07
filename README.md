# A simple IPython kernel for odpscmd

This is a IPython kernel for [odpscmd](http://odps.aliyun.com), modified from [bash_kernel](https://github.com/takluyver/bash_kernel).

## Requirement

- IPython 3
- Command odpscmd in PATH
- File odps_config.ini should be found in current folder and is properly configured

## Download
- git clone git@github.com:lyman/odpscmd_kernel.git

## Run

Install with `pip install .`, and then run one of:

- `ipython notebook`, In the notebook interface, select Bash from the 'New' menu
- `ipython console --kernel odpscmd`

## Debug

Just run `./debug.sh`

## License

Licensed under the [BSD License](http://www.linfo.org/bsdlicense.html)
