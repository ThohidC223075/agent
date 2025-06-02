import os
import subprocess
import time

# ✅ এই ফাংশন Git কমান্ড চালায় এবং ফলাফল রিটার্ন করে
def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"❌ Error running {' '.join(command)}")
        print(result.stderr)
    else:
        print(result.stdout.strip())
    return result

# ✅ চেক করবে .git আছে কি না
def is_git_repo(path):
    return os.path.exists(os.path.join(path, '.git'))

# ✅ রিমোট রিপোজিটরি থেকে পরিবর্তন এসেছে কি না তা চেক করে এবং pull করে
def pull_if_needed():
    fetch_result = run_git_command(['git', 'fetch'])
    status_result = run_git_command(['git', 'status'])

    if "Your branch is behind" in status_result.stdout:
        print("🔄 Remote repo has updates. Pulling...")
        run_git_command(['git', 'pull', 'origin', 'main'])
    else:
        print("✅ Local repo is up to date.")

# ✅ লোকাল চেঞ্জ আছে কি না তা দেখে commit করে
def push_if_changed(commit_msg):
    status = run_git_command(['git', 'status', '--porcelain'])
    if status.stdout.strip() != "":
        print("📦 Changes found. Committing and pushing...")
        run_git_command(['git', 'add', '.'])
        run_git_command(['git', 'commit', '-m', commit_msg])
        run_git_command(['git', 'push', 'origin', 'main'])
    else:
        print("✅ No changes to commit.")

# ✅ নতুন রিপো বানানো
def initialize_and_push(path, remote_url, commit_msg):
    os.chdir(path)
    run_git_command(['git', 'init'])
    run_git_command(['git', 'add', '.'])
    run_git_command(['git', 'commit', '-m', commit_msg])
    run_git_command(['git', 'branch', '-M', 'main'])
    run_git_command(['git', 'remote', 'add', 'origin', remote_url])
    run_git_command(['git', 'push', '-u', 'origin', 'main'])

# ✅ মূল ফাংশন
def main():
    path = os.getcwd()
    os.chdir(path)

    if is_git_repo(path):
        print("📁 This is already a Git repository.")
        while True:
            pull_if_needed()  # রিমোট থেকে চেক করে দরকার হলে pull
            commit_msg = input("✍️ Enter commit message (or press enter to skip): ").strip()
            if commit_msg:
                push_if_changed(commit_msg)
            time.sleep(0)  # ১০ সেকেন্ড পরপর চেক করবে
    else:
        print("⚠️ No Git repository found.")
        remote_url = input("🔗 Enter your remote Git repository URL: ").strip()
        commit_msg = input("✍️ Enter initial commit message: ").strip()
        initialize_and_push(path, remote_url, commit_msg)
        print("✅ Repository initialized and code pushed.")

if __name__ == "__main__":
    main()
