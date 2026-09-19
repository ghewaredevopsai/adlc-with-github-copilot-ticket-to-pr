# Participant instructions

These steps set up your machine for the course and start the Global Bank app on your own machine.

You do most steps by giving a prompt to **GitHub Copilot in VS Code**. Each prompt is in a grey box.
Copy the whole box and paste it into the Copilot Chat window.

It takes about 20 minutes. Most of that time is the first Maven build.

## Where everything goes

You **clone** the repositories. You do not fork them. Your changes stay on branches in your own clone.

```
$HOME/
  adlc-with-github-copilot-ticket-to-pr/   the course: outline, slides, metrics board
  global-bank/                             the code you work on
    global-bank-platform/                  scripts to run the whole app, and the map of all services
    global-bank-account/
    global-bank-authentication/
    global-bank-customer/
    global-bank-transaction/
    global-bank-rules/
    global-bank-frontend/
```

`$HOME` is your home folder:

| Operating system | Home folder |
|---|---|
| Windows | `C:\Users\<you>` |
| macOS | `/Users/<you>` |
| Linux | `/home/<you>` |

## Before you start

Install these tools:

- Git
- **JDK 25** (for example Temurin 25) and Maven 3.9 or newer
- Node.js 22 or newer
- VS Code, signed in to GitHub, with GitHub Copilot working

**How to use Copilot for these steps:**

1. Open VS Code. If it asks for a folder, open your home folder.
2. Open Copilot Chat: **View > Chat**, or `Ctrl+Alt+I` (`Cmd+Ctrl+I` on macOS).
3. At the bottom of the chat box, set the mode to **Agent**.
   Agent mode can run commands in a terminal. Ask mode only answers questions.
4. Paste a prompt and press Enter.
5. Copilot asks before it runs each command. Read the command, then click **Continue** (or **Allow**).

> Copilot may choose slightly different commands each time. That is normal.
> The prompts ask it to show you the result, so you can check each step.

---

## Step 1. Check your tools

```text
Check that my machine has the tools this course needs. Run each command below in the terminal and show me the first line of each output in a table, with PASS or FAIL.
Use PowerShell on Windows. Use the normal shell on macOS or Linux.

- git --version          (PASS if 2.40 or newer)
- java -version          (PASS only if the version is 25 or newer)
- mvn -version           (PASS if Apache Maven 3.9 or newer)
- node --version         (PASS if v22 or newer)
- npm --version          (PASS if it prints a version)

Do not install or change anything. If a tool fails, tell me what to install.
```

If `java` reports a version older than 25, install JDK 25 and set `JAVA_HOME` to it. Then open a new
VS Code window and run Step 1 again.

## Step 2. Clone the course repository into your home folder

```text
Clone the course repository into my home folder. Run this one command in the terminal:

git clone https://github.com/ghewaredevopsai/adlc-with-github-copilot-ticket-to-pr.git "$HOME/adlc-with-github-copilot-ticket-to-pr"

If the folder already exists, do not clone again. Run "git pull" inside it instead.
Then list the files in that folder, so I can see the clone worked.
```

## Step 3. Clone the Global Bank repositories into `$HOME/global-bank`

```text
Clone the seven Global Bank repositories into the folder global-bank in my home folder.
Use PowerShell on Windows. Use the normal shell on macOS or Linux.

1. Create the folder "$HOME/global-bank" if it does not exist.
2. Inside it, clone each of these repositories with git clone. Keep the default folder names.
   https://github.com/brainupgrade-in/global-bank-platform.git
   https://github.com/brainupgrade-in/global-bank-account.git
   https://github.com/brainupgrade-in/global-bank-authentication.git
   https://github.com/brainupgrade-in/global-bank-customer.git
   https://github.com/brainupgrade-in/global-bank-transaction.git
   https://github.com/brainupgrade-in/global-bank-rules.git
   https://github.com/brainupgrade-in/global-bank-frontend.git
3. If a repository folder already exists, do not clone it again. Run "git pull" inside it instead.
4. Do not fork any repository.
5. At the end, show me a table of the seven folders with the current branch of each one.
```

All seven folders must sit side by side inside `global-bank`. The start script in Step 5 looks for
them there.

## Step 4. Open the code in VS Code

Do this step by hand:

1. **File > Open Folder**.
2. Choose `global-bank` in your home folder, then **Open**.
3. If VS Code asks whether you trust the authors, choose **Yes**.

The next prompts run from this window. Open Copilot Chat again and check that the mode is still **Agent**.

## Step 5. Start Global Bank on localhost

Global Bank has five Spring Boot services and one web app. They all run on your machine.
You do not need Docker or Kubernetes.

| Part | Port | Address |
|---|---|---|
| authentication | 8084 | `http://localhost:8084/auth` |
| customer | 8085 | `http://localhost:8085/customer` |
| account | 8086 | `http://localhost:8086/account` |
| transaction | 8087 | `http://localhost:8087/transaction` |
| rules | 8090 | `http://localhost:8090/rules` |
| web app | 4200 | `http://localhost:4200` |

Each service keeps its data in memory. When you stop a service, its data goes back to the starting data.

Use the prompt for your operating system.

### macOS or Linux

```text
Start the Global Bank app on localhost. Run this command in the terminal, from the global-bank folder:

bash global-bank-platform/scripts/local.sh start

The first run builds all five services with Maven, so it can take several minutes. Wait for it to finish.
Then show me the last 15 lines of its output.
If any line starts with a cross (✗), show me the log file it names and explain the error.
Use mvn, not ./mvnw. The ./mvnw wrapper does not work in these repositories.
```

### Windows

The start script is a bash script, so on Windows Copilot starts each part with PowerShell.

```text
Start the Global Bank app on localhost. Use PowerShell. Work from the global-bank folder in my home folder.
Use mvn, not ./mvnw. The ./mvnw wrapper does not work in these repositories.

1. Create the folder "$HOME\global-bank\logs" if it does not exist.
2. Build each of these five folders with: mvn -B -q clean package -DskipTests
   global-bank-authentication, global-bank-customer, global-bank-account, global-bank-transaction, global-bank-rules
   Build them one at a time. If a build fails, stop and show me the error.
3. Start each service in the background from its own folder, with its log in the logs folder. For example:
   Start-Process java -ArgumentList '-jar','target\authentication.jar' -WorkingDirectory "$HOME\global-bank\global-bank-authentication" -RedirectStandardOutput "$HOME\global-bank\logs\auth.log" -RedirectStandardError "$HOME\global-bank\logs\auth.err.log" -WindowStyle Hidden
   Each folder has one jar in target: authentication.jar, customer.jar, account.jar, transaction.jar, rules.jar.
4. Wait until each service answers its health address with "UP". Try every 5 seconds, for up to 2 minutes:
   http://localhost:8084/auth/actuator/health
   http://localhost:8085/customer/actuator/health
   http://localhost:8086/account/actuator/health
   http://localhost:8087/transaction/actuator/health
   http://localhost:8090/rules/actuator/health
5. In global-bank-frontend, run "npm install" once. Then start the web app in the background:
   Start-Process npm.cmd -ArgumentList 'run','dev' -WorkingDirectory "$HOME\global-bank\global-bank-frontend" -RedirectStandardOutput "$HOME\global-bank\logs\frontend.log" -RedirectStandardError "$HOME\global-bank\logs\frontend.err.log" -WindowStyle Hidden
6. Wait until http://localhost:4200 answers.
7. Show me a table of the six parts with UP or DOWN. If a part is DOWN, show me the end of its log file and explain the error.
```

## Step 6. Check that it works

The web app shows demo data when a service is down. So a page that loads does **not** prove the services
work. This prompt checks the services directly.

```text
Check that Global Bank is running on localhost.
Use PowerShell on Windows. Use curl on macOS or Linux.

1. Call each health address and show me the status:
   http://localhost:8084/auth/actuator/health
   http://localhost:8085/customer/actuator/health
   http://localhost:8086/account/actuator/health
   http://localhost:8087/transaction/actuator/health
   http://localhost:8090/rules/actuator/health
2. Sign in through the web app, to test the whole path. Send a POST request to
   http://localhost:4200/auth/login with the header Content-Type: application/json and this body:
   {"userid":"john","password":"unigps"}
   Show me the userid and role from the reply. Do not show the authToken.

Tell me PASS if all five services say UP and the sign-in returns the role CUSTOMER. Otherwise tell me FAIL and why.
```

Then open **http://localhost:4200** in your browser. Sign in as `john` with the password `unigps`.
The users `admin`, `eric` and `ratan` use the same password.

## Step 7. Stop Global Bank

Stop the app at the end of the day, or before you start it again.

### macOS or Linux

```text
Stop the Global Bank app. Run this command from the global-bank folder:

bash global-bank-platform/scripts/local.sh stop

Then run "bash global-bank-platform/scripts/local.sh status" and show me the output. Every part should say down.
```

### Windows

```text
Stop the Global Bank app. Use PowerShell.
For each of the ports 8084, 8085, 8086, 8087, 8090 and 4200, find the process that is listening on it and stop that process:
Get-NetTCPConnection -LocalPort <port> -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Then check each port again and show me a table of the ports with STOPPED or STILL RUNNING.
```

---

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `release version 25 not supported` | Maven is using a JDK older than 25 | Install JDK 25. Set `JAVA_HOME` to it. Open a new VS Code window. |
| `MavenWrapperMain` not found | Something ran `./mvnw` | Use `mvn`. The wrapper files are not in these repositories. |
| A Maven download hangs or fails | Your network needs a proxy for Maven | Ask your IT team for the Maven proxy settings for `~/.m2/settings.xml`. |
| `port 8084 is in use` (or another port) | Something else uses that port, or an old copy is still running | Run Step 7, then start again. |
| `not found next to global-bank-platform` | A repository is missing or in the wrong folder | Run Step 3 again. All seven folders must be inside `global-bank`. |
| The web page loads, but Step 6 says FAIL | The web app is showing demo data | Ask Copilot to show you the log of the service that is down. |
| `Permission denied` on `local.sh` | The script is not marked as runnable | Start it with `bash` in front, as the prompt does. |
