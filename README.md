### Support request classification 

## Dependencies
- Install [docker](https://docs.docker.com/get-docker/) and [docker compose](https://docs.docker.com/compose/install/)
## Installation
1. Clone/Download repository with
3. `docker-compose build`
4. `docker-compose up` or `docker-compose up -d` if you want to run it without terminal
5. unpack model to \tf_serving\models\feed_forward\1\
## Usage

### Predict input image
URL `localhost:80`
POST `v1/predict`  
**Request Body**  
**Content-type:** `form-data`  
| Key           | Required | Value       | Description                      |
|---------------|----------|-------------|----------------------------------|
| text          | string   | Support request to be used for inference. |

## Stopping the container
`docker-compose kill` or `docker-compose down` if you want to delete the container
