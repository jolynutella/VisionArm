from visionarm import create_app
from visionarm.commands import create_tables

def test_create_tables(runner):
    """
    Test case to verify the creation of database tables.
    It creates an instance of the Flask application using `create_app()`,
    sets up an application context, and then invokes the `create_tables` command
    using the provided `runner` object. Finally, it checks if the command exits
    with an exit code of 0, indicating successful execution.
    """
    app = create_app()
    with app.app_context():
        result = runner.invoke(create_tables)
        assert result.exit_code == 0


