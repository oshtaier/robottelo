from airgun.decorators import parametrize
from robottelo.datafactory import gen_string, valid_data_list


@parametrize('name', valid_data_list())
def test_positive_create(session, name):
    with session:
        session.architecture.create_architecture({'name': name})


def test_positive_create_with_os(session):
    name = gen_string('alpha')
    with session:
        session.architecture.create_architecture({
            'name': name,
            'os_dict_values': {
                'operation': 'Add', 'values': ['RedHat 59.9', 'RedHat 7.3']}
        })
