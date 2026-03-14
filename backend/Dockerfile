FROM python:3.9-slim

WORKDIR /app

# 配置阿里云apt源
RUN if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources ; \
        sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources ; \
    elif [ -f /etc/apt/sources.list ]; then \
        sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list ; \
        sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list ; \
    fi

COPY requirements.txt .
# 配置阿里云pip镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]