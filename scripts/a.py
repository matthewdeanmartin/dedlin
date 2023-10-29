import asyncio


async def fetch_google_html():
    return await asyncio.sleep(1, "2")


async def echo_text(text):
    print(f"Echoed: {text}")


async def main():
    while True:
        print("\nOptions:")
        print("1. Echo text")
        print("2. Fetch HTML from google.com")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            text = input("Enter text to echo: ")
            echo_text(text)
        elif choice == "2":
            html_content = await fetch_google_html()
            print(html_content[:500] + "...")  # Print only the first 500 characters for brevity
        elif choice == "3":
            print("Exiting...")
            break
        else:
            return "yo"


if __name__ == "__main__":
    asyncio.run(main())
