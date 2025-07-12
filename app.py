"""Entry point for Apriscout application."""

from apriscout import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
