```
# GroupMe Messaging Bot Scheduler via GitHub Actions

This repository provides a robust, automated framework for sending scheduled messages to a **GroupMe group** using a bot integrated with **GitHub Actions**.

---

## How to Use This Repository: Step-by-Step Setup

The solution leverages a Python script (`send_message.py`) to interact with the GroupMe Bot API, and a GitHub Actions workflow (`.github/workflows/message_scheduler.yml`) to manage the execution and scheduling.

---

### Step 1: Create Your GroupMe Bot and Obtain the Bot ID

1. Visit the **GroupMe Developers site** and log in: `https://dev.groupme.com/bots`
2. Click **"Create Bot"**.
3. Select the desired group, name your bot (e.g., "SchedulerBot"), and click **"Submit"**.
4. **Crucially**, copy the **Bot ID** (a long alphanumeric string) displayed after creation. This ID is how GitHub Actions will authenticate and send messages.

---

### Step 2: Configure the GitHub Secret

The Bot ID must be stored securely as a repository secret on GitHub.

1. Navigate to your repository on GitHub.
2. Go to the **Settings** tab.
3. In the left sidebar, select **Secrets and variables → Actions**.
4. Click **New repository secret**.
5. Set the name of the secret to **`GROUPME_BOT_ID`** (this name must be exact).
6. Paste the **Bot ID** you copied in Step 1 into the **Value** field.
7. Click **Add secret**.

---

### Step 3: Define Your Schedule and Messages (Editing the Workflow)

All scheduling and message content is defined within the **`.github/workflows/message_scheduler.yml`** file. You must edit two primary sections: the trigger schedule and the individual message jobs.

---

#### A. Defining the Execution Schedule

In the `on: schedule:` section, use **cron syntax** to specify when the workflow should run.

* **File Location:** `.github/workflows/message_scheduler.yml`
* **Section to Edit:** `on: schedule:`

**Required Edits Example:**
```yaml
on:
  schedule:
    - cron: '00 10 * * 1-5'  # Every weekday (Mon-Fri) at 10:00 UTC
    - cron: '30 20 * * 0'    # Every Sunday at 20:30 UTC
```
Note: GitHub Actions cron schedules execute based on UTC (Coordinated Universal Time). Always convert your local desired time to UTC before setting the cron string. The format is: minute hour day-of-month month day-of-week.

---

#### B. Defining the Message Jobs

Each unique message you wish to send requires its own job block within the workflow file.

* **File Location:** `.github/workflows/message_scheduler.yml`
* **Section to Edit:** The individual job blocks (e.g., starting with `send_message_example:`).

**Edits Required per Message Job:**

- **Job Name:** Change the job name (e.g., from `send_message_example` to `send_message_sunday_reminder`).
- **if: Condition:** This condition determines when the job actually executes.
  - Scheduled Trigger: Update the cron string in `github.event.schedule == '...'` to exactly match one of the cron strings defined in your `on: schedule:` block (e.g., `'30 20 * * 0'`).
  - Manual Trigger (Optional): Update the message identifier in `github.event.inputs.message_day == '...'` (e.g., change `example` to `sunday_msg`). This lets you manually select this specific message to send via the Actions tab.
- **Message Text:** In the final `run:` step, update the text between the quotes with your desired message.

To add a new scheduled message:

1. Copy an entire existing job block.
2. Update the Job Name (line 1).
3. Update the cron string in the `if:` condition.
4. Update the message identifier in the `if:` condition (if using manual triggers).
5. Update the message text on the final `run: python send_message.py "..."` line.

---

### Manual Execution (Workflow Dispatch)

The workflow is configured with `workflow_dispatch` to allow testing or immediate message sending outside of the established schedule.

1. Go to the **Actions** tab in your repository.
2. Select the Message Scheduler workflow from the sidebar.
3. Click the **Run workflow** dropdown button.
4. If manual inputs are configured (Step 3B), enter the specific message identifier (e.g., `sunday_msg`) corresponding to the job you want to run.
5. Click **Run workflow** to execute the job immediately.

---

### File Overview

- `send_message.py`: The Python script that takes a message as a command-line argument and posts it to the GroupMe Bot API using the `GROUPME_BOT_ID` environment variable.
- `.github/workflows/message_scheduler.yml`: The GitHub Actions workflow file defining the schedule and the individual message jobs.
- `requirements.txt`: Lists the Python dependency (`requests`) needed by the script.

---
```
