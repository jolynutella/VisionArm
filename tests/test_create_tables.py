from visionarm import create_app
from visionarm.commands import create_tables


def test_create_tables(runner):
    app = create_app()
    with app.app_context():
        result = runner.invoke(create_tables)
        assert result.exit_code == 0
