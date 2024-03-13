### PoC ➡️ Demo: Pickle injection

Some light tooling that can add arbitrary code to pickle files and then trick pytorch into running them

- `make venv`
- source the venv
- `make install-reqs`
- `make train-model`
- `make demo`: get location & ip info
- `make demo-helloworld`: basic hello world example
- `make demo-minecraft`: opens minecraft if installed on your system
- `make demo-neofetch`: get system information if neofetch is installed on your system

### TODO

- injections not breaking the model execution
- fix the zipped model example
