# CS271P Assignment 1 Walkthrough + CS175 RL Reading Guide

## 1. What RL you actually need from the `cs175` repository

You do **not** need to learn the whole repository to finish this assignment.

For this homework, the RL you need is only the part that explains the **agent–environment loop** clearly enough that the Docker test script makes sense. The assignment is mostly about Docker, not about implementing an RL algorithm.

### Read this first

#### `README.md`
Read the root `README.md` first so you know the chapter map and the intended dependency order. The repo says Chapter 2 is the place to start, and it explicitly says the dependency chain matters.

What this gives you:
- the canonical chapter order,
- the notation convention that the action at time `t` is `A_t`,
- the convention that the reward caused by that action is `R_{t+1}`.

### Required reading

#### `02_problem-setup-and-agent-environment-interaction/README.md`
Read this chapter **carefully**.

This is the most relevant RL material for Assignment 1.

What you need from it:
1. **Decision point / order of events**
   - The agent is at a pre-action decision point.
   - It chooses `A_t`.
   - Then the environment reacts.
   - Then the agent receives `R_{t+1}` and the next observation.

   This is the exact causal order behind the Gymnasium environment loop.

2. **Observation, action, reward**
   - Observation: what the environment reveals now.
   - Action: what the agent chooses now.
   - Reward: the immediate scalar consequence that appears after the environment reacts.

3. **Do not confuse observation with state**
   For this assignment, you do not need a deep state-theory discussion. You just need to avoid sloppy language. The environment gives you an observation; that does not automatically mean you have a complete Markov state in the strong theoretical sense.

4. **Episode timing and termination discipline**
   This matters because the test script runs one episode of `FrozenLake-v1` and stops when the episode terminates or truncates.

### Read next, but only selected parts

#### `04_states-histories-mdps-and-objective/README.md`
You do **not** need the whole chapter for Assignment 1. Read these ideas:

1. **History is the full available pre-action record**
   This helps you understand what information exists at the moment the agent acts.

2. **A state representation is a function of history**
   This is useful so you do not casually treat every observation as a fully justified Markov state.

3. **What the Markov property actually says**
   Read this lightly. You only need enough to understand why environments like FrozenLake are usually discussed as MDP-style problems.

4. **Return and the performance objective**
   You need this only at a high level: RL is not about maximizing one immediate reward in isolation. It is about long-run return.

### Optional for later assignments, not needed now

#### `06_dynamic-programming-monte-carlo-td-sarsa-qlearning/README.md`
This is **optional for Assignment 1**.

Read it only if you want early intuition for the algorithms that often get run on toy environments like FrozenLake.

The only sections worth skimming right now are:
- `epsilon`-greedy action selection,
- SARSA,
- Q-learning.

But be clear: **Assignment 1 does not ask you to train an agent.** The test script only verifies that your Docker environment can run a toy RL environment, produce a plot, and record a video.

### What you can safely skip for this assignment

You can skip Chapters 5, 7, 8, and 9 for now.

Those chapters matter later, but they are not necessary to:
- explain the Dockerfile,
- explain the `docker run` command,
- build the image,
- run the container,
- execute `test.py`,
- capture the screenshot and video frame.

## 2. What the assignment is actually checking

The homework is checking four separate things.

### Part A: setup
Can you install Docker Desktop and get into the starter directory correctly?

### Part B: Dockerfile comprehension
Can you explain what each Dockerfile directive does and why it is present in this starter environment?

### Part C: container launch comprehension
Can you explain what the major pieces of the build/run/exec commands do?

### Part D: environment verification
Can you prove that the environment works by running the provided test and showing the output?

The optional extra-credit part asks you to design your own Dockerfile for a future AI project.

## 3. What is inside the starter archive

In the uploaded starter archive, the files that matter are:
- `Dockerfile`
- `requirements.txt`
- `test.py`

`requirements.txt` lists the Python packages to install.

`Dockerfile` tells Docker how to build the image.

`test.py` is not an RL training script. It is a **sanity check** script. It checks that:
- NumPy works,
- Matplotlib works,
- ImageIO works,
- Gymnasium works,
- video recording works,
- the environment can run one FrozenLake episode successfully.

That means you do **not** need to understand policy evaluation, Bellman equations, or Q-learning in order to finish this assignment.

## 4. MacBook M1 Air note

Your machine should be fine for this assignment.

But there is one required change:

- **Remove `--gpus all`** from the `docker run` command.

Why this check matters:
- your MacBook Air M1 does not have the NVIDIA-style GPU setup expected by that flag,
- leaving it in is the easiest way to make the command fail for no good reason,
- the test script does not need GPU acceleration anyway.

Also use the **Apple silicon** Docker Desktop installer.

## 5. The fastest correct workflow

## Step 1: Install Docker Desktop
Install Docker Desktop for Mac, using the Apple silicon version.

What you are checking here:
- Docker Desktop launches,
- the Docker engine is running,
- the `docker` command works from Terminal.

What success means:
- Docker Desktop opens normally,
- a terminal command like `docker --version` succeeds,
- Docker is ready before you try to build the image.

## Step 2: Unzip the starter archive and enter the correct directory
Unzip `assignment1.zip`.

Then go to the directory that actually contains:
- `Dockerfile`
- `requirements.txt`
- `test.py`

In your uploaded archive, that is the **inner** `assignment1/assignment1` directory, not just the outer folder.

What this check means:
- Docker build uses the **current directory** as the build context,
- if you run `docker build` from the wrong directory, Docker may not see the expected files.

## Step 3: Build the Docker image
Run the image build command from the directory containing the Dockerfile.

Example shape:

```bash
docker build -t assignment1-img .
```

What this step checks, in order:
1. Docker can read the Dockerfile.
2. Docker can pull the base image `python:3.11-slim`.
3. `apt-get` can install `ffmpeg`.
4. `pip` can install the packages from `requirements.txt`.
5. Docker can copy the local files into `/workspace`.
6. The final image is created successfully.

What success means:
- the build completes without an error,
- you now have a named local image.

## Step 4: Run the container
Because you are on an M1 Mac, use the run command **without** `--gpus all`.

Example shape:

```bash
docker run -d --name assignment1-ctr -v "$(pwd)":/workspace assignment1-img sleep infinity
```

What each part is checking:
- `-d` means detached mode, so the container runs in the background.
- `--name assignment1-ctr` gives the container a stable name so you can reference it later.
- `-v "$(pwd)":/workspace` mounts your current host directory into the container at `/workspace`.
- `assignment1-img` is the image to start from.
- `sleep infinity` keeps the container alive so you can enter it later.

What success means:
- the container starts and remains running in the background,
- it does not immediately exit.

## Step 5: Enter the running container
Now open a shell inside the running container.

Example shape:

```bash
docker exec -it assignment1-ctr bash
```

What this step checks:
- the container is still alive,
- Docker can attach an interactive terminal to it,
- you can now run commands inside the container.

What success means:
- your shell prompt changes to a container prompt,
- you are inside `/workspace` or can move there.

## Step 6: Run the provided test
Inside the container, run:

```bash
python3 test.py
```

What this test checks, in order:
1. NumPy imports and basic array operations work.
2. Matplotlib imports and can save a plot.
3. ImageIO can read the saved image back.
4. Gymnasium imports successfully.
5. `FrozenLake-v1` can be created.
6. `RecordVideo` can write an MP4.
7. The environment loop runs until termination or truncation.

What success means:
- the script finishes,
- it prints version information,
- it says a plot was saved,
- it says a video was recorded,
- it ends with `All tests passed!`.

## Step 7: Collect the two deliverables for Part D
You need two pieces of evidence.

### A. Screenshot of console output
Take a screenshot of the terminal after `python3 test.py` finishes successfully.

What the screenshot should show:
- the command you ran,
- the printed output,
- the final success message.

### B. One frame from the recorded video
The video file will be inside the output video directory created by the script.

You need to open the generated MP4 and capture **one frame** from it.

What this proves:
- recording actually worked,
- the environment rendered frames correctly,
- your container has the right non-Python dependency for video encoding.

## 6. Part B — model answers you can study and adapt

These are the answers you should understand well enough to restate in your own words.

### `FROM python:3.11-slim`
This sets the base image for the build. It means the rest of the container will start from a lightweight Python 3.11 environment instead of from an empty filesystem. It fixes the operating-system and Python starting point that every later build step depends on.

### `RUN apt-get update && apt-get install -y ffmpeg`
This executes shell commands while the image is being built. In this Dockerfile, it first refreshes the package index and then installs `ffmpeg`, which is needed because the test script records a video and that video must be encoded correctly inside the container.

### `WORKDIR /workspace`
This sets the default working directory for the later build instructions and for commands run in the container. After this line, relative paths are interpreted from `/workspace`, which keeps the build organized and makes the container behave as though your project lives there.

### `COPY requirements.txt /workspace/requirements.txt`
This copies the dependency list from your host machine into the image so that `pip` can read it during the build. It does not install anything by itself; it only moves the file into the container filesystem.

### `RUN pip install -r requirements.txt`
This installs the Python packages listed in `requirements.txt` into the image. It is the step that makes libraries like Gymnasium, NumPy, Matplotlib, and ImageIO available when you later run `python3 test.py`.

### `COPY . /workspace`
This copies the project files from your local directory into the container’s `/workspace` directory. In this assignment, that includes at least the test script and the dependency file, so the container has the actual project content it needs to run.

### `CMD ["bash"]`
This sets the default command the container would run if no other command were provided at startup. Here, it means the image is prepared to drop into a Bash shell by default, which is useful for interactive work.

## 7. Part C — model answers you can study and adapt

### `docker build -t YOUR_IMAGE_NAME .`
This builds a Docker image from the Dockerfile in the current directory and gives the finished image a name. The final dot means the current directory is the build context, so Docker can see the Dockerfile and the files being copied into the image.

### `-d`
This tells Docker to run the container in detached mode. The container stays running in the background instead of taking over the current terminal.

### `--gpus all`
This tells Docker to expose all available GPUs to the container. On a machine without the expected GPU support, this flag can cause the run command to fail, which is why you should remove it on your MacBook M1 Air.

### `-v PATH_TO_PART_A_DIR:/workspace`
This mounts a directory from your host machine into the container. What is fixed is the host path on the left and the container path on the right. The effect is that files in your homework folder can be shared directly with the container without rebuilding the image every time something changes.

### `sleep infinity`
This keeps the container process alive indefinitely. That matters because a container stops when its main process ends. If you want to enter it later with `docker exec`, you need the container to still be running.

### `docker exec -it YOUR_CONTAINER_NAME bash`
This opens an interactive Bash shell inside the already running container. `-i` keeps standard input open, and `-t` allocates a terminal, so you can type commands normally inside the container.

## 8. What RL understanding maps directly onto `test.py`

This is the minimum RL interpretation you should have in your head while running the test.

### Observation
The environment gives the agent an observation after reset and after each step.

### Action
At each decision point, the agent selects one action from the environment’s action space.

In this script, the action is sampled randomly. That means there is **no learning algorithm** here.

### Reward
After the action, the environment returns a reward. That reward is the immediate consequence of the last action, not the entire training objective.

### Episode end
The episode ends when either:
- the environment terminates naturally, or
- the environment is truncated.

The script stops when one of those conditions becomes true.

### Why FrozenLake appears here
FrozenLake is being used as a lightweight toy RL environment so the script can verify that Gymnasium, rendering, and video recording all work.

It is not being used here to test whether you know dynamic programming, SARSA, or Q-learning.

## 9. Common failure modes and what each one means

### Failure mode: Docker build cannot find `requirements.txt` or `test.py`
Meaning: you are probably building from the wrong directory.

Check:
- are you inside the folder that actually contains the Dockerfile?
- do `requirements.txt` and `test.py` sit next to it?

### Failure mode: `docker run` fails with a GPU-related error
Meaning: you left `--gpus all` in the command on a machine that should not use it.

Fix:
- remove the GPU flag.

### Failure mode: the container exits immediately
Meaning: the main process ended.

Check:
- did you use `sleep infinity`?
- did the container crash on startup?

### Failure mode: `docker exec` says the container is not running
Meaning: either the container never started correctly or it exited after startup.

Check:
- whether the run command succeeded,
- whether the container name is correct,
- whether the main process is still alive.

### Failure mode: `python3 test.py` fails when recording video
Meaning: the most likely missing system dependency is the video encoder toolchain.

In this assignment, the Dockerfile installs `ffmpeg` exactly to prevent that problem.

### Failure mode: the script runs but no files appear where you expect
Meaning: you may be confused about the host path versus container path.

Remember the mapping:
- host homework folder on your Mac,
- mounted into the container as `/workspace`.

If the mount is correct, outputs created in `/workspace/test_outputs` from inside the container should also appear in the mounted folder on your Mac.

## 10. What to submit

For the required parts, your submission should contain:

1. Your written explanation for the Dockerfile directives in Part B.
2. Your written explanation for the run-command pieces in Part C.
3. A screenshot of the successful `python3 test.py` terminal output.
4. One frame from the recorded FrozenLake video.

For the optional extra-credit part, also include your custom Dockerfile and any supporting explanation or figures.

## 11. What to say if you want the shortest honest answer to “what do I need to learn?”

Here is the blunt version.

For **this** assignment, from `cs175`, you mainly need to learn:
- the **agent–environment interaction loop**,
- the difference between **observation**, **action**, and **reward**,
- the idea that the agent acts at time `t` and sees the reward **after** that action,
- the idea that FrozenLake is an **RL environment**, but this homework is **not yet an RL algorithm homework**.

That means:
- **must read**: Chapter 2,
- **read selected parts of**: Chapter 4,
- **optional only**: Chapter 6,
- **skip for now**: the rest.

## 12. Final checklist

Before you submit, check each item in order.

### Setup
- Docker Desktop installed and running.
- You used the Apple silicon version.
- You removed `--gpus all`.

### Build and run
- You built the image from the correct folder.
- The image finished building without errors.
- The container started and stayed alive.
- You entered it with `docker exec -it ... bash`.

### Test
- `python3 test.py` completed successfully.
- The terminal showed the success message.
- A plot file was saved.
- A video file was recorded.

### Submission
- Part B answers written.
- Part C answers written.
- Console screenshot captured.
- One video frame captured.

If every one of those checks passes, you are done with the required assignment.
