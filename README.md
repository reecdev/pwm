## IMPORTANT: pwm is stil in a very early beta and this readme is incomplete! pwm is currently not reccomended for real use, as it is not production-ready yet.

# pwm
pwm (Parallel Worker Manager) is a program that allows you to run agents that operate autonomously and can complete tasks for you.
Note that this is not the same as OpenClaw; OpenClaw is designed to be a general assistant while pwm is designed to be a program that lets you run multiple workers in parallel to complete multiple tasks at the same time.

## Use cases
pwm can be useful if you have a ton of projects you want to publish but you're too lazy to make docs for. You can spin up 5 instances of pwm at once to write docs for every single project in parallel. (hence the name: Parallel Worker Manager)

## Safety
pwm is also designed with security in mind. When starting a worker, you will be asked to assign it a folder. Each pwm worker can only read or write the files inside of it's assigned folder. This is to prevent it from wrecking your entire system by running something like `sudo rm -rf /`. Furthermore, each worker is also inside of a temporary container that self-destructs when the worker is finished doing it's tasks, so if it runs a malicious command or accidently installs malware, it will be contained and won't compromise your main machine.

## Requirements
To run pwm, you will need to install Docker and Ollama on your computer. Currently, only Linux is officially supported.
You will then have to install an Ollama model. We reccomend `gpt-oss:20b` since it can run on most consumer machines and is fairly smart.
