#  CO-modeling
This is a project to model late-time CO formation in SNe. This repository does NOT currently include the CO modeling code, just tools to install and navigate it.

## Installation
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

## Testing installation
1. If your Docker instance is not already open run steps 7 and 8 from installation to resume the instance.
2. Once inside Docker, navigate to your folder with CO models
   ```
   cd $CODIR
   cd CO
   ```
3. Compile the modeling code `make -B -f ./Makefile.gfortran`
4. Create a new model with `python CO_wrapper.py`

## Notes
The Docker does not currently support running the jupyter notebook included in this repository. The Docker environment is used for creating new models and not model fitting. It is expected that the model fitting be done outside the Docker.

## How to run the example jupyter notebook
0. This is currently all done outside of the Docker, you will need the following python packages
   ```
   numpy
   pandas
   matplotlib
   scipy
   ```
1. Navigate to your CO directory `cd $CODIR`
2. Create a csv file for each model that exists on your computer `python make_model_df.py` (this will take a while to run)
3. Once that code has run navigate to the example directory `cd example`
4. Open the jupyter notebook `jupyter notebook plot_CO.ipynb`
