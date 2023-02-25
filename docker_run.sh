export MSYS_NO_PATHCONV=1
# "winpty"
"docker.exe" run --rm -it -v "$PWD/:/" dedlin:latest "$@"
