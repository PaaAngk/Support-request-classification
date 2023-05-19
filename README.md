### Support request classification 

## Dependencies
- Install [docker](https://docs.docker.com/get-docker/) and [docker compose](https://docs.docker.com/compose/install/)
## Installation
1. Clone/Download repository
2. Unpack model to folder: \tf_serving\models\feed_forward\1\
3. `docker-compose build`
4. `docker-compose up` 
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
