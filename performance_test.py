import subprocess
import cProfile
import pstats
import io
from app import app

def run_ab_test(url, num_requests, concurrency):
    cmd = f"ab -n {num_requests} -c {concurrency} {url}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def run_wrk_test(url, duration, threads):
    cmd = f"wrk -d {duration} -t {threads} {url}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def profile_app():
    pr = cProfile.Profile()
    pr.enable()
    
    # Simulate some requests
    client = app.test_client()
    for _ in range(1000):
        client.get('/')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    return s.getvalue()

if __name__ == "__main__":
    print("Running Apache Benchmark test:")
    print(run_ab_test("http://localhost:5000/", 1000, 10))
    
    print("\nRunning wrk test:")
    print(run_wrk_test("http://localhost:5000/", "30s", 4))
    
    print("\nRunning Python profiler:")
    print(profile_app())