
## 1. Core Concepts & Utilities
* **`bash`**: The shell interpreter and engine that translates your text commands into system operations and manages environment state.
* **`cat`**: Short for "concatenate". A command-line utility used to read, display, or merge file contents directly in the terminal.
* **`grep`**: A pattern searching tool. Special regex characters like `[` and `]` must be escaped with backslashes (`\[ERROR\]`) to match literally, or run with `grep -F` for plain text mode.

---

## 2. Data Flow & Redirection
* **`|` (Pipe):** Directs the standard output (`stdout`) of one command directly into the standard input (`stdin`) of the next command (e.g., `cat log.txt | grep "ERROR"`).
* **`>` (Overwrite Redirect):** Captures command output and writes it to a file, **overwriting** any existing content.
* **`>>` (Append Redirect):** Captures command output and **appends** it to the end of an existing file without deleting what is inside.

---

## 3. Startup Configuration (`~/.bashrc`)
* **`~/.bashrc`**: A hidden startup script stored in your home directory (`~`) that runs automatically whenever a new interactive Bash session opens.
* **Purpose**: Stores persistent environment variables (`export VAR="val"`), updates system executable paths (`PATH`), sets up aliases (command shortcuts), and initializes runtime tools (like Conda).
* **Reloading**: Run `source ~/.bashrc` to apply configuration changes immediately without restarting your terminal.

---

## 4. File Generation & Heredocs (`EOF`)
* **Heredoc (`cat << 'EOF' > file.txt`)**: A terminal pattern used to create multiline files directly from the command line.
* **`EOF` (End of File)**: A standard sentinel word that tells Bash where the multiline block ends. You can use any word, but `EOF` is the universal convention.
* **Variable Expansion Rules**: 
  * **Unquoted (`cat << EOF`)**: Bash evaluates and replaces `$VARIABLES` with their stored values before writing.
  * **Quoted (`cat << 'EOF'`)**: Bash treats text literally, preserving exact characters like `$`.

---

## 5. Variables & Environment (`export`)
* **Local Shell Variables (`VAR="val"`)**: Private to the active shell session; invisible to child scripts or external programs.
* **`export VAR="val"`**: Promotes a variable to an **Environment Variable**, making it public so sub-processes (like Python or Docker) inherit it.
* **Why use Environment Variables?**: Keeps secrets, credentials, and hardware paths out of source code, making code portable across local and cloud environments.

---

## 6. Process Hierarchy
* **Process**: A running program in memory with its own isolated memory space.
* **Parent Process**: The launcher program (e.g., your interactive Bash shell prompt).
* **Sub-process (Child)**: A worker program spawned by the parent (e.g., running `python train.py` inside Bash). Crashes in child processes do not crash the parent shell.
---

## 7. The `$PATH` Variable
* **`$PATH`**: An environment variable storing a colon-separated (`:`) list of folder paths where Bash searches for executable commands (e.g., `python`, `pip`, `git`).
* **Search Order**: Scanned **left-to-right**. Bash executes the first matching binary it finds and stops searching.
* **`command not found` Error**: Occurs either because a tool isn't installed OR its executable folder path is missing from `$PATH`.
* **Inspection**: Run `echo $PATH` to see your current search path list.

---

## 8. Virtual Environment Activation & Isolation
* **How `conda activate` Works**: Prepends the active environment's binary folder (e.g., `~/anaconda3/envs/my-env/bin`) to the **very front** of your `$PATH`.
* **Isolation Mechanism**: Because the environment folder sits at the beginning of `$PATH`, Bash finds and executes that environment's `python` and packages before `base` or system binaries.
* **Environment State Variables**: Sets tracking variables like `CONDA_PREFIX` (root path of active env) and `CONDA_DEFAULT_ENV` (active env name).
