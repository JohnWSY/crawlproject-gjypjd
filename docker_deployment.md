docker部署说明

服务器：172.18.15.122

文件目录
.
├── app         //存放项目文件
│   └── gjypjd      
│       ├── chromedriver
├── build.sh
├── Dockerfile
├── gjypjd.pth

基础镜像: registry.thunisoft.com:5000/base/webdriver:v3

docker镜像生成

    Dockerfile
        FROM registry.thunisoft.com:5000/base/webdriver:v3
        COPY ["gjypjd.pth","/root/.pyenv/versions/env_pyspider/lib/python3.6/site-packages/"]
        RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
        WORKDIR /root/work_space/
        COPY ["app","pyspider_space/"]
        WORKDIR /root/work_space/pyspider_space/gjypjd/
        ENTRYPOINT [""]
        CMD [""]

    gjypjd.pth
        /root/work_space/pyspider_space

    build.sh
        docker build -t registry.thunisoft.com:5000/scjg/gjypjd_v6:8.8 .
        docker push registry.thunisoft.com:5000/scjg/gjypjd_v6:8.8

    修改/etc/hosts文件
        172.18.15.71  registry.thunisoft.com

    执行./build.sh 生成镜像并push到172.18.15.71服务器

使用镜像
    registry.thunisoft.com:5000/scjg/gjypjd_v7:1.2
    arterydocker页面中的拓扑页签下设置
        镜像选择：gjypjd_v7
        版本选择：1.2
        启动命令: /root/.pyenv/shims/python gcqx_lssj.py


其他说明
    python环境说明
        基础镜像：registry.thunisoft.com:5000/base/webdriver:v3
            工作目录：/root/work_space/pyspider_space
            python路径：/root/.pyenv/shims/python

