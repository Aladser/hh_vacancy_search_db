import os.path
import pytest
from src import DBManager
from src.parser import ConfigParser, EmployerParser
from src.api import HHApi


@pytest.fixture
def conn_params():
    """параметры БД"""
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.dirname(config_dir) + '/env'
    return ConfigParser.parse(config_path)


@pytest.fixture
def employments():
    """путь до employers"""
    abs_path = os.path.dirname(os.path.abspath(__file__))
    employments_filename = os.path.dirname(abs_path) + '/employers'
    return EmployerParser.parse(employments_filename)


@pytest.fixture
def url_vacancies(employments):
    hh_api = HHApi()
    return hh_api.load_vacancies(employments)


@pytest.fixture
def db_manager(conn_params, employments):
    db_manager = DBManager(**conn_params)
    db_manager.recreate_tables(employments)
    return db_manager


def test_work(db_manager, url_vacancies):
    db_manager.remove_vacancies()
    db_manager.load_vacancies(url_vacancies)

    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword()
