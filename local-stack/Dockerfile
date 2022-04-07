FROM serverless_base:0.0.1 as base

WORKDIR /authorization_server
COPY ./package-lock.json ./package-lock.json ./pyproject.toml ./poetry.lock ./serverless.yml.local /authorization_server/
RUN npm install
RUN poetry export -f requirements.txt --output requirements.txt && pip3 install -r requirements.txt
RUN cp serverless.yml.local serverless.yml -v