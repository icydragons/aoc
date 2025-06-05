import os
import requests

def download_input(day):
    url = f"https://adventofcode.com/2024/day/{day}/input"
    session_cookie = "PUT_COOKIE_HERE" # Replace with your actual session cookie
    headers = {
        "Cookie": f"session={session_cookie}"  
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(f"aoc/Advent2024/{day}.txt", "w") as file:
            file.write(response.text)
        print(f"Downloaded input for day {day}")
    else:
        print(f"Failed to download input for day {day}: {response.status_code}")

def main():
    
    for day in range(1, 26):
        download_input(day)

if __name__ == "__main__":
    main()