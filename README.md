#  CO-modeling
This is a project to model late-time CO formation in SNe

## Installation
0. Make sure you have the model code or else the docker will not correctly install.
1. Install [Docker](https://docs.docker.com/get-docker/).
2. Install [docker-compose](https://docs.docker.com/compose/install/)
3. Clone this repository: `git clone https://github.com/scottfdavis/CO-modeling`
4. Within the repository folder put the model code in a directory called `CO`
5. Build the Docker image: `docker build -t sfdavis/co_modeling CO-modeling`
6. Set your environment variables to point to where you want to store data and catalogs.
   You may want to add these lines to your `.bashrc` (usually Linux) or `.bash_profile` (usually macOS) file
   so that you don't have to set them in every new terminal session.
   ```
   export CODIR=/your/data/directory
   ```  
7. Startup your "pipeline server".
   ```
   docker-compose -f docker-compose.yml up &
   ```
8. Run the Docker instance.
   ```
   docker exec -it co_modeling /bin/bash
   ```
