from ui import MainApplication


def main():
    # Instantiate the UI
    app = MainApplication()

    # 💡 This is where you can easily bind commands later!
    # Example: app.sidebar.csvBtn.config(command=your_browser_function)

    # Run the Tkinter mainloop
    app.mainloop()


if __name__ == "__main__":
    main()
