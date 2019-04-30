Repository for the development of a arcade game controlled in real-time by voice

NOTE: The gym environment used to work only on UNIX machines (Linux, MAC), so if you can try to run it in these machines and not on Windows, you'll be happier sooner!

In order to run the game the following steps have to be taken:

1. Clone repository

Run the following command on your desired folder

`git clone https://git.rwth-aachen.de/iks-rtap-ss2019/group-b-project.git`

Your credentials will be asked, simply input them and you're good to go =D

2. Create a virtualenv for the project

If you have the virtualenv command installed in a linux machine, run

`virtualenv -p python3.6 audioLabEnv`

If you have python installed with conda, the following link might help

https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

3. Activate the environment

If installed with `virtualenv`, run

`source ~/audioLabEnv/bin/activate`

4. Install python dependencies

Move into the project directory

`cd group-b-project`

and install the libraries in requirements.txt

`pip install -r requirements.txt`

5. Play the game in arrow mode

From the command line simply run

`python GameEnvironment/game_environment.py`

The game takes a little while to start, have fun! :D