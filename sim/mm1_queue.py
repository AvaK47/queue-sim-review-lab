import simpy
import random
import sys

def run_simulation(lambda_, mu, total_time, seed=None):
    """Run M/M/1 queue simulation and return average wait and list of waits."""
    if seed is not None:
        random.seed(seed)

    env = simpy.Environment()
    server_free_time = [0.0]          # time when server becomes free (mutable)
    wait_times = []

    def service_time():
        """Exponential service time with rate mu."""
        return random.expovariate(mu)

    def customer(env, arrival_time, wait_times, server_free_time):
        # arrival/service bookkeeping
        service_start = server_free_time[0]          # BUG: should be max(arrival_time, ...)
        wait = service_start - arrival_time          # may be negative when server idle
        wait_times.append(wait)

        service_duration = service_time()
        server_free_time[0] = service_start + service_duration
        yield env.timeout(service_duration)

    def arrival_process(env):
        count = 0
        while True:
            interarrival = random.expovariate(lambda_)
            yield env.timeout(interarrival)
            arrival_time = env.now
            count += 1
            env.process(customer(env, arrival_time, wait_times, server_free_time))

    env.process(arrival_process(env))
    env.run(until=total_time)

    if wait_times:
        avg_wait = sum(wait_times) / len(wait_times)
    else:
        avg_wait = 0.0
    return avg_wait, wait_times

if __name__ == "__main__":
    LAMBDA = 0.95      # arrival rate
    MU = 1.0           # service rate  -> rho = 0.95
    TOTAL_TIME = 100000
    avg, waits = run_simulation(LAMBDA, MU, TOTAL_TIME, seed=42)
    print(f"Average wait time: {avg:.4f}")
    print(f"Number of customers served: {len(waits)}")
    # Optional: show how many negative waits occurred (debugging)
    # print(f"Negative waits: {sum(1 for w in waits if w < 0)}")
