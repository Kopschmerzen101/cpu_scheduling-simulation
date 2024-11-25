import random
import time
import threading

# Define constants for the assignment
users = ["P1", "P2", "P3", "P4", "P5"]
job_types = ["Print", "Scan"]
job_lengths = {"Short": (1, 5), "Medium": (6, 15), "Large": (16, 50)}
mutex_printer = threading.Lock()  # Mutex lock for printer
mutex_scanner = threading.Lock()  # Mutex lock for scanner
semaphore_job_queue = threading.Semaphore(1)  # Semaphore for job queue control
flag = [False, False]
turn = 0  # Used in Peterson's Solution

# Queue to store generated jobs
job_queue = []

# Function to create a job
def create_job(user):
    job_type = random.choice(job_types)
    length_category = random.choice(list(job_lengths.keys()))
    length_pages = random.randint(*job_lengths[length_category])
    arrival_time = random.randint(1, 5)

    job = {
        "User": user,
        "Job Type": job_type,
        "Length": length_pages,
        "Arrival Time": arrival_time
    }

    job_queue.append(job)
    print(f"{user}: {job_type} Job, {length_pages} pages, Arrival Time: {arrival_time} seconds.")

# Generate jobs for each user
def generate_jobs():
    for user in users:
        for _ in range(10):  # 10 jobs per user
            create_job(user)

# Without synchronization (Task 1)
def run_without_sync():
    print("\nRunning jobs without synchronization...\n")
    for job in job_queue:
        execute_job(job)

# With mutex synchronization (Task 2)
def run_with_mutex_sync():
    print("\nRunning jobs with mutex synchronization...\n")
    for job in job_queue:
        if job["Job Type"] == "Print":
            with mutex_printer:
                execute_job(job)
        elif job["Job Type"] == "Scan":
            with mutex_scanner:
                execute_job(job)

# With semaphore synchronization (Task 2)
def run_with_semaphore_sync():
    print("\nRunning jobs with semaphore synchronization...\n")
    for job in job_queue:
        semaphore_job_queue.acquire()  # Acquire access to job queue
        execute_job(job)
        semaphore_job_queue.release()  # Release access after job execution

# Peterson's Solution (Task 2)
def run_with_peterson_sync(job):
    global turn, flag
    print("\nRunning jobs with Peterson's solution for mutual exclusion on printer...\n")

    for job in job_queue:
        if job["Job Type"] == "Print":
            peterson_lock(0)
            execute_job(job)
            peterson_unlock(0)
        elif job["Job Type"] == "Scan":
            execute_job(job)  # Scanner runs without Peterson's lock in this example

# Peterson's lock
def peterson_lock(id):
    global turn, flag
    other = 1 - id
    flag[id] = True
    turn = other
    while flag[other] and turn == other:
        pass  # Busy-wait

# Peterson's unlock
def peterson_unlock(id):
    global flag
    flag[id] = False

# Execute a job with page-by-page logging
def execute_job(job):
    for page in range(1, job["Length"] + 1):
        print(f"{job['User']} - {job['Job Type']} Job: Page {page}/{job['Length']} in progress...")
        time.sleep(1)  # Simulate processing time for each page
    print(f"{job['User']} - {job['Job Type']} Job complete.\n")

# Main function to control job generation and execution style selection
def main():
    print("Generating Jobs...\n")
    generate_jobs()

    print("\nChoose execution mode:")
    print("1. Run without synchronization")
    print("2. Run with mutex synchronization")
    print("3. Run with semaphore synchronization")
    print("4. Run with Peterson's solution (for printer)")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        run_without_sync()
    elif choice == "2":
        run_with_mutex_sync()
    elif choice == "3":
        run_with_semaphore_sync()
    elif choice == "4":
        for job in job_queue:
            run_with_peterson_sync(job)
    else:
        print("Invalid choice. Please choose between 1-4.")

# Run the main function
main()
