FROM gitpod/workspace-full

USER gitpod

RUN sudo apt-get install python3.8 && sudo apt install python3-pip
RUN pip3 install poetry && poetry install
RUN sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libatspi2.0-0
RUN playwright install
