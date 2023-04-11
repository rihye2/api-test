# For more information, please refer to https://aka.ms/vscode-docker-python
FROM nvidia/cuda:12.0.1-cudnn8-runtime-ubuntu22.04

RUN apt-get update && \
    apt-get -y install libgl1-mesa-glx && \
    apt-get install --no-install-recommends -y curl

#install python 3.8 on miniconda
ENV CONDA_AUTO_UPDATE_CONDA=false\
    PATH=/opt/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/miniconda \
    && rm ~/miniconda.sh \
    && sed -i "$ a PATH=/opt/miniconda/bin:\$PATH" /etc/environment

RUN python3 -m pip --no-cache-dir install --upgrade pip


RUN mkdir workdir
ENV WORKSPACE /workdir
WORKDIR ${WORKSPACE}

COPY requirements.txt ${WORKSPACE}/requirements.txt
COPY . ${WORKSPACE}

RUN pip install -r /workdir/requirements.txt
#Docker 외부의 파일을 복사하여 내부에 추가
EXPOSE 80

# COPY run_server /bin/run_server
# ENTRYPOINT ["bash", "-l", "run_server"]

#컨데이너로 띄울 때, 디폴트로 실행할 커맨드
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]



# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8

# RUN mkdir workdir
# ENV WORKSPACE /workdir
# WORKDIR ${WORKSPACE}

# COPY requirements.txt ${WORKSPACE}/requirements.txt
# COPY . ${WORKSPACE}

# RUN apt-get update && apt-get -y install libgl1-mesa-glx

# RUN pip install -r /workdir/requirements.txt
# #Docker 외부의 파일을 복사하여 내부에 추가
# EXPOSE 80

# # COPY run_server /bin/run_server
# # ENTRYPOINT ["bash", "-l", "run_server"]

# #컨데이너로 띄울 때, 디폴트로 실행할 커맨드
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]


