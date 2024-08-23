## :rocket: competition-uhc-sac

Code for Utah Hockey Club Summer Analytics Challenge.

## :pencil: Authors

- [Jaroslav Bezdek](https://www.github.com/jardabezdek)

## :construction_worker_man: Setup

### Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder: `cd ~/projects/competition-uhc-sac/`
1. Build the docker image with a proper tag: `docker build -t uhc-sac:latest .`
1. Run docker container: `docker run -p 8888:8888 -v $(pwd):/usr/src/app uhc-sac:latest`

### Data download

1. Set the credentials in the `.env` file in the root project directory. Use the [.env.example](./.env.example) file as a refence.
1. Run [this notebook](./notebooks/01_create_datasets.ipynb) to create the datasets.
