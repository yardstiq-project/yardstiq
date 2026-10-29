from yardstiq.cli.main_cli import run
import typer
from typer.testing import CliRunner
from yardstiq.cli.main_cli import app  # import your Typer app

runner = CliRunner()

_RUN_PROBLEM = ["maxcut", "unsupported", None]
_RUN_DATASET = ["data_test.json", "wrong_path", None]
_RUN_QPU = ["qiskit-aer", "unsupported", None]
_RUN_CONFIG = ["max-shot", "unsupported", "compilation-parameters", None]
_RUN_CONFIG_VALUES = ["42", "A", "", "{'param1': 'value1', 'param2': 'value2'}", None]
_RUN_PIPELINE = ["qall", ""]


def _test_run_problem():
    for problem in _RUN_PROBLEM:
        try:
            runner.invoke(app, ["run", problem, "data_test.json", "qiskit-aer"])
        except Exception as e:
            if not problem == "maxcut":
                assert isinstance(e, typer.BadParameter) 
    
def _test_run_dataset():
    for dataset in _RUN_DATASET:
        try:
            runner.invoke(app, ["run", "maxcut", dataset, "qiskit-aer"])
        except Exception as e:
            if not dataset == "data_test.json":
                assert isinstance(e, FileNotFoundError)

def _test_run_qpu():
    for qpu in _RUN_QPU:
        try:
            runner.invoke(app, ["run", "maxcut", "data_test.json", qpu])
        except Exception as e:
            if not qpu == "qiskit-aer":
                assert isinstance(e, typer.BadParameter)

def _test_run_config():
    for config in _RUN_CONFIG:
        for value in _RUN_CONFIG_VALUES:
            try:
                runner.invoke(app, ["run", "maxcut", "data_test.json", "qiskit-aer", f"{config} {value}"])
            except Exception as e:
                if not (config == "max-shot" and value == "42"):
                    assert isinstance(e, typer.BadParameter)

def _test_run_pipeline():
    for pipeline in _RUN_PIPELINE:
        try:
            runner.invoke(app, ["run", "maxcut", "data_test.json", "qiskit-aer", f"--pipeline {pipeline}"])
        except Exception as e:
            if not pipeline == "qall":
                assert isinstance(e, typer.BadParameter)

def test_cli():
    _test_run_problem()
    _test_run_dataset()
    _test_run_qpu() 
    _test_run_config()
    _test_run_pipeline()

