import ollama
import os
import sys
import docker
import re
import time

model = "gpt-oss"

os.system("clear")
print("\033[30;47m pwm Quick Start \033[0m")
path = os.path.realpath(os.path.abspath(os.getcwd()+"/"+input("path: ")))
os.makedirs(path, exist_ok=True)

print("\033[30;47m Container is starting... \033[0m")
client = docker.from_env()
container = client.containers.run(
    image="alpine:latest",
    command="sleep infinity",
    detach=True,
    auto_remove=True,
    network_mode="bridge",
    mem_limit="512m",
    working_dir="/a",
    volumes={
        path: {
            'bind': '/a', 
            'mode': 'rw'
        }
    }
)
print(container.attrs['Mounts'])

msgs = [{"role": "system", "content": """
You are a professional AI assistant. You have full access to a bash terminal running on Alpine Linux.

All of your responses must output this **exact** string in **plaintext**, no matter what:
Do <NAME> <INPUT>
replacing <NAME> with the do's name and <INPUT> with the input you want to pass, without quotes.

Each message must only contain one do, with no other text. New lines are prohibited.

Here is a list of do's available to you:
sh: Run bash command provided in INPUT.
finish: End the session. This should be ran when all tasks are complete.

You should respond with Do finish "" when you are done with everything the user asked for.
"""},{"role": "assistant", "content": "Do sh echo Test suceeded."},{"role": "user", "content": "$ echo Test suceeded.\nTest suceeded."},
{"role": "user", "content": input("prompt: ")}]

os.system("clear")
print("\033[30;47m pwm Session \033[0m")

ti = time.time()
tk = 0

def chat():
    global msgs
    global tk
    ou = ""
    stream = ollama.chat(
        model=model,
        messages=msgs,
        stream=True,
        options={'raw': True}
    )
    print("pwm> ", end="", flush=True)
    for chunk in stream:
        ch = chunk["message"]
        if "thinking" in ch:
            print(f"\033[31m{ch["thinking"]}\033[0m", end="", flush=True)
        print(ch["content"], end="", flush=True)
        ou = ou + ch["content"]
        tk += 1
    print("")
    msgs.append({"role": "assistant", "content": ou})
    return ou

try:
    while True:
        o = chat()

        match = re.search(r"^Do (?P<name>\w+)\s+(?P<input>.*)$", o.strip(), re.DOTALL)
        if match:
            n = match.group("name")
            i = match.group("input")
            if n == "sh":
                exitc, out = container.exec_run(
                    cmd=['/bin/sh', '-c', i],
                    workdir="/a",
                    user="root"
                )
                msgs.append({"role": "user", "content": f"$ {i}\n{out.decode("utf-8")}"})
            elif n == "finish":
                print("\033[30;47m pwm Session ended. \033[0m")
                print(f"Total time taken: {time.time()-ti}s")
                print(f"Total token usage: {tk}t")
                break

        msgs.append({"role": "system", "content": ""})
except:
    container.stop()

container.stop()