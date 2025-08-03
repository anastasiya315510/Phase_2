FROM ubuntu:latest
LABEL authors="esty"

ENTRYPOINT ["top", "-b"]