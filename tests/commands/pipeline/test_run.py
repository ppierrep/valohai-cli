from click import BadParameter
from pytest import raises

from tests.commands.run_test_utils import RunAPIMock
from tests.fixture_data import PROJECT_DATA, PIPELINE_YAML
from valohai_cli.commands.pipeline.run import run
from valohai_cli.commands.pipeline.run.utils import match_pipeline
from valohai_cli.ctx import get_project


def test_pipeline_run_success(runner, logged_in_and_linked):
    add_valid_pipeline_yaml()
    args = ['training']
    with RunAPIMock(PROJECT_DATA.get('id')) as m:
        output = runner.invoke(run, args).output
    assert 'Success' in output


def test_pipeline_run_no_name(runner, logged_in_and_linked):
    add_valid_pipeline_yaml()
    args = ['']
    with RunAPIMock(PROJECT_DATA.get('id')) as m:
        output = runner.invoke(run, args).output
    assert 'Usage: ' in output


def test_match_pipeline(runner, logged_in_and_linked):
    add_valid_pipeline_yaml()
    config = get_project().get_config()
    matches = match_pipeline(config, 'Training')
    assert matches == "Training Pipeline"


def test_match_pipeline_ambiguous(runner, logged_in_and_linked):
    add_valid_pipeline_yaml()
    config = get_project().get_config()
    with raises(BadParameter):
        match_pipeline(config, 'Train')


def add_valid_pipeline_yaml():
    with open(get_project().get_config_filename(), 'w') as yaml_fp:
        yaml_fp.write(PIPELINE_YAML)
